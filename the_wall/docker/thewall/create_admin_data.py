import os
from base64 import b64encode, b64decode
from db import DB
from Crypto.Cipher import AES

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)

MONGODB_STRING = os.getenv('MONGODB_STRING', '')
ADMIN_SECRET_KEY = 'tJV8ITMpqajX+jI8EKrjPf9fhkCbPJn+AOct0O6kPj8='
FLAG = 'Ararat{w4Lk_Up_And_D0wn_ou7s1d3_th3_w4ll}'
database = DB(MONGODB_STRING)

if database.get_user_id("admin"):
    print('admin exsists already')
    exit(0)

id_ = database.add_data('admin', 'iNXxuaemVySEqESu3EfSnmUop6Ty1x6sSfYWl9d/emY=')
print('admin created')

with open(f'secrets/{id_}', 'w') as f:
    f.write(ADMIN_SECRET_KEY)

print('admin secret created')

ADMIN_SECRET_KEY = b64decode(ADMIN_SECRET_KEY)

for i in FLAG:
    cipher = AES.new(ADMIN_SECRET_KEY, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(i).encode())
    iv = cipher.iv
    ciphertext = iv + ciphertext

    database.createBrick('admin', ciphertext)

print('admin data created')
