#!/usr/bin/env python3
import base64
import random
import gmpy2

import loader

welcome_text = """
██████   █████  ██    ██ ██ ███████ ██   ██ ██ ███    ██  ██████
██   ██ ██   ██ ██    ██ ██ ██      ██   ██ ██ ████   ██ ██
██████  ███████ ██    ██ ██ ███████ ███████ ██ ██ ██  ██ ██   ███
██   ██ ██   ██  ██  ██  ██      ██ ██   ██ ██ ██  ██ ██ ██    ██
██   ██ ██   ██   ████   ██ ███████ ██   ██ ██ ██   ████  ██████

███████ ███████  ██████ ██████  ███████ ████████ ███████
██      ██      ██      ██   ██ ██         ██    ██
███████ █████   ██      ██████  █████      ██    ███████
     ██ ██      ██      ██   ██ ██         ██         ██
███████ ███████  ██████ ██   ██ ███████    ██    ███████  of

 █████  ██████   █████  ██████   █████  ████████
██   ██ ██   ██ ██   ██ ██   ██ ██   ██    ██
███████ ██████  ███████ ██████  ███████    ██
██   ██ ██   ██ ██   ██ ██   ██ ██   ██    ██
██   ██ ██   ██ ██   ██ ██   ██ ██   ██    ██
                     
ls  - list encrypted phrases
pub - show public key
enc - encrypt phrase
dec - decrypt phrase
"""


def b2n(b):
    n, p = 0, 1
    for byte in b:
        n += byte * p
        p *= 256
    return n


def n2b(n):
    b = []
    while n:
        b.append(n % 256)
        n //= 256
    return bytes(b)


class RSA:
    def __init__(self):
        self.e = 257
        self.key_bits = 1024
        self.q = gmpy2.next_prime(random.getrandbits(self.key_bits // 2))
        self.p = gmpy2.next_prime(random.getrandbits(self.key_bits // 2))
        self.n = self.p * self.q
        phi = (self.p - 1) * (self.q - 1)
        self.d = gmpy2.invert(self.e, phi)

    def encrypt(self, m):
        return base64.b64encode(n2b(gmpy2.powmod(b2n(m), self.e, self.n))).decode()

    def decrypt(self, c):
        return n2b(gmpy2.powmod(b2n(base64.b64decode(c)), self.d, self.n))


def main():
    print(welcome_text)
    rsa = RSA()
    phrases = loader.load_data(rsa)
    while True:
        try:
            cmd = input(">>> ")
            if cmd == "ls":
                print("List of encrypted phrases:")
                for name in phrases:
                    print(f"{name}: {phrases[name]}")
            elif cmd == "pub":
                print(rsa.n)
            elif cmd == "enc":
                phrase = input("Your phrase: ").strip()
                if len(phrase) < 10 or not phrase.isprintable():
                    print("Error: can not encrypt this phrase")
                    continue
                print("Encrypted: " + rsa.encrypt(bytes(phrase.encode())))
            elif cmd == "dec":
                enc = input("Encrypted phrase: ")
                if enc in phrases.values():
                    print("Error: this phrase is in public list")
                    continue
                print("Decrypted: " + base64.b64encode(rsa.decrypt(enc)).decode())
            else:
                print("Unknown command")
        except Exception as e:
            print(e)


main()
