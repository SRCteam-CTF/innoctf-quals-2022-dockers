#!/usr/bin/python3
import socket
import threading
import os
import time
import random
from secrets import flag
from Crypto.Cipher import AES

KEY_LEN = 16
BLOCK_SIZE = 16

class Encryption:
    def __init__(self):
        self.pad = lambda s: s + bytes([(BLOCK_SIZE - len(s) % BLOCK_SIZE)] * (BLOCK_SIZE - len(s) % BLOCK_SIZE))
        self.unpad = lambda s: s[:-s[len(s) - 1]]
        self.key = bytes([i for i in self.__get_random_key()])
        self.checksums_storage = []

    def __srand(self, seed):
        self.s = seed

    def __rand(self):
        self.s = (0x10001 * self.s) % (2 ** 31)
        return self.s
    
    def __get_checksums(self):
        for i in self.key:
            checksum = 0
            for j in range(8):
                checksum += i & (1 << j)
            yield checksum

    def __get_random_key(self):
        for _ in range(KEY_LEN):
            yield random.randint(0, 255)

    def gen_new_key(self, seed):
        self.__srand(seed)
        iters = random.randint(0, 1000000)
        for i in range(iters):
            self.__rand()

        checksums = [i % 256 for i in self.__get_checksums()]
        r = []
        for i in range(8):
            new = (self.__rand() >> 16) & 0xffff
            r.append((new >> 8) & 0xff)
            r.append(new & 0xff)


        k_new = []
        for i in range(KEY_LEN):
            if checksums[i] % 2 == self.key[i] % 2:
                k_new.append(((checksums[i] + 1) % 256) ^ self.key[i])
            else:
                k_new.append(checksums[i] ^ self.key[i])
        for i in range(KEY_LEN):
            r_ = random.randint(0, int((time.time() % 1) * 0xffffffff) % 1337) + 2
            if ((self.key[i] % 1337) + 2) & 2 != r_ & 2:
                k_new[i] |= (((self.key[i] % 1337) + 2) & 2) | (r_ & 2)
            else:
                k_new[i] |= 2

        for i in range(KEY_LEN):
            k_new[i] |= 192

        for i in range(KEY_LEN):
            k_new[i] ^= r[i]

        self.key = bytes(r)
        return bytes(k_new)
    
    def get_unique_round_id(self):
        checksums = [i for i in self.__get_checksums()]
        id_ = 0
        for i in range(checksums):
            id_ |= checksums[i] << (i * 3)

        return id_

    def encrypt(self, message):
        cipher = AES.new(self.key, AES.MODE_CBC)
        ciphertext = cipher.encrypt(self.pad(bytes(message)))
        iv = cipher.iv
        ciphertext = iv + ciphertext
        return ciphertext

    def decrypt(self, message):
        data = bytes(message[16:])
        iv = bytes(message[:16])
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted = self.unpad(cipher.decrypt(data))
        return decrypted

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(700)
        print(f'Listening on {self.host}:{self.port}')
        while True:
            client, address = self.sock.accept()
            client.settimeout(500)
            threading.Thread(target=self.listenToClient, args=(client, address)).start()

    def listenToClient(self, client, address):
        try:
            print("%s: connected" % address[0])
            enc = Encryption()
            client.sendall("Hello, only if you have a key that I have, we could communicate. Let's try!\n".encode())
            time.sleep(0.1)
            while True:
                client.sendall("\nHere is the message for you:\n".encode())
                time.sleep(0.1)
                encrypted = enc.encrypt(flag.encode())
                client.sendall(encrypted)
                client.settimeout(2)
                data = None
                try:
                    data = client.recv(1024).decode()
                except Exception:
                    pass
    
                if data == flag:
                    time.sleep(0.1)
                    client.sendall("Right!\n".encode())
                    return
    
                seed = int(time.time())
                client.sendall("\nGenerating new key...\n".encode())
                time.sleep(0.1)
    
                # Generate a new key and send it encrypted by the previous one
                new_key = enc.gen_new_key(seed)
                client.sendall(new_key)
        except BrokenPipeError:
            print(f'{address[0]} disconnected\n')
            return

if __name__ == "__main__":
    port_num = os.getenv('PORT', 8083)
    try:
        ThreadedServer('', port_num).listen()
    except KeyboardInterrupt:
        os._exit(0)
