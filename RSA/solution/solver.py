from base64 import b64encode, b64decode
from gmpy2 import gmpy2


def bytes_to_n(b):
    n, p = 0, 1
    for byte in b:
        n += byte * p
        p *= 256
    return n


def n_to_bytes(n):
    b = []
    while n:
        b.append(n % 256)
        n //= 256
    return bytes(b)


N = int(input("N: "))
e = 257
# need to iterate over all phrases. Done here manually
while True:
    # https://crypto.stackexchange.com/questions/2323/how-does-a-chosen-plaintext-attack-on-rsa-work
    encrypted = bytes_to_n(b64decode(input("encrypted phrase: ")))
    twopow = gmpy2.powmod(2, e, N)
    need_decrypt = twopow * encrypted
    print(b64encode(n_to_bytes(need_decrypt)).decode())
    twom = bytes_to_n(b64decode(input("decrypted: ")))
    print(n_to_bytes(twom // 2))
