import random

#flag = "Ararat{L00k_At_tH3_V3ry_Imp0rtant_C0ntr4ct}"
flag = "some random test string nobody knows"

random.seed(1232367823872)
k = random.randint(0, 2 ** 256 - 1)
print('uint256 key:', '0x' + hex(k)[2:].zfill(64))

def encrypt_part(data, key, prev):
    data = data & (2 ** 256-1)
    key = key & (2 ** 256-1)
    prev = prev & (2 ** 256-1)

    a = 0x13371337133713371337133713371337
    b = 0x37133713371337133713371337133713

    x1 = (data & 0xffffffffffffffffffffffffffffffff00000000000000000000000000000000) >> 128
    x2 = data & 0xffffffffffffffffffffffffffffffff
    x1 ^= a
    x2 ^= b

    result = (x2 << 128) | x1

    k1 = (key & 0xffffffffffffffffffffffffffffffff00000000000000000000000000000000) >> 128
    k2 = key & 0xffffffffffffffffffffffffffffffff

    y1 = (result & 0xffffffffffffffffffffffffffffffff00000000000000000000000000000000) >> 128
    y2 = result & 0xffffffffffffffffffffffffffffffff
    y1 ^= k1
    y2 ^= k2

    result = (y2 << 128) | y1

    p1 = (prev & 0xffffffffffffffffffffffffffffffff00000000000000000000000000000000) >> 128
    p2 = prev & 0xffffffffffffffffffffffffffffffff
    
    z1 = (result & 0xffffffffffffffffffffffffffffffff00000000000000000000000000000000) >> 128
    z2 = result & 0xffffffffffffffffffffffffffffffff
    z1 ^= p1
    z2 ^= p2

    result = (z2 << 128) | z1
    
    return result
    

def decrypt_part(data, key, prev):
    data = data & (2 ** 256-1)
    key = key & (2 ** 256-1)
    prev = prev & (2 ** 256-1)

    p1 = (prev & 0xffffffffffffffffffffffffffffffff00000000000000000000000000000000) >> 128
    p2 = prev & 0xffffffffffffffffffffffffffffffff

    z1 = data & 0xffffffffffffffffffffffffffffffff
    z2 = (data & 0xffffffffffffffffffffffffffffffff00000000000000000000000000000000) >> 128
    z1 ^= p1
    z2 ^= p2

    k1 = (key & 0xffffffffffffffffffffffffffffffff00000000000000000000000000000000) >> 128
    k2 = key & 0xffffffffffffffffffffffffffffffff
    y1 = z2 ^ k1
    y2 = z1 ^ k2

    a = 0x13371337133713371337133713371337
    b = 0x37133713371337133713371337133713

    x1 = y2 ^ a
    x2 = y1 ^ b

    result = (x1 << 128) | x2

    return result

d = []

for i in range(0, 32 * (int(len(flag) / 32) + 1), 32):
    t = '0x'
    for j in range(i, i+32):
        if j >= len(flag):
            t += '00'
        else:
            t += hex(ord(flag[j]))[2:].zfill(2)
    d.append(int(t, 16))

print('uint256[] data:', list(map(hex, d)))

d_enc = []

iv = 2 ** 256 - 1
for i in d:
    enc = encrypt_part(i, k, iv)
    iv = enc
    d_enc.append(enc)

print('uint256[] encrypted data:', list(map(hex, d_enc)))

d_dec = []
iv = 2 ** 256 - 1
for i in d_enc:
    dec = decrypt_part(i, k, iv)
    iv = i
    d_dec.append(dec)

print('uint256[] decrypted data:', list(map(hex, d_dec)))
