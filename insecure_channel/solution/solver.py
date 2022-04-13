import time
import re
import socket
from Crypto.Cipher import AES

seed = 0

IP = '127.0.0.1'
PORT = 8083

def srand(s):
    global seed
    seed = s % (2 ** 31)

def rand():
    global seed
    seed = (0x10001 * seed) % (2 ** 31)
    return seed

def create_random_table(s):
    srand(s)
    table = []
    first = rand()
    second = rand()
    iters = 0
    table.append(first)
    table.append(second)
    while True:
        r1 = rand()
        r2 = rand()
        iters += 2
        if first == r1 and second == r2:
            break
        table.append(r1)
        table.append(r2)
    print(f'Random table created in {iters} iterations')

    table_ = []
    for t in table:
        n = (t >> 16) & 0xffff
        table_.append((n >> 8) & 0xff)
        table_.append(n & 0xff)

    return table_


def solve(data, s):
    print('Seed:', s)
    table = create_random_table(s)
    
    table_str = ''
    for i in table:
        table_str += bin(i)[2:].zfill(8) + ','
    table_str = table_str[:-1]
    
    data_xored = [i ^ 0b11000011 for i in data] #0b11????11
    data_xored_str = ''
    for i in data_xored:
        d = bin(i)[2:].zfill(8)
        d = d[:2] + '.'*4 + d[6:]
        data_xored_str += d + ','
    
    data_xored_str = data_xored_str[:-1]
    print(data_xored_str)

    found = []
    for m in re.finditer(data_xored_str, table_str):
        found.append(m.start())

    print(table_str[found[0]:found[0]+len(data)*8 + len(data)-1])
    
    if len(found) > 1:
        print('warning: multiple variants')

    positions = [len(table_str[:i].split(','))-1 for i in found]
    keys = []
    for pos in positions:
        key = table[pos:pos + len(data)]
        keys.append(key)
    return keys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP, PORT))
print(sock.recv(1024))
print(sock.recv(1024))
print(sock.recv(1024))
print(sock.recv(1024))
seed = int(time.time())
data = sock.recv(1024)
if b'Here is the' in data:
    data = data[:data.index(b'\nHere is the')]
print(seed, list(data))
keys = solve(data, seed)
print(keys)
data = sock.recv(1024)

print('Data:', list(data))
iv = data[:16]
text = data[16:]

unpad = lambda s: s[:-s[len(s) - 1]]

for key in keys:
    cipher = AES.new(bytes(key), AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(text))
    print(decrypted)
