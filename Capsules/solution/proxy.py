#!/usr/bin/python3
import socket
from select import select
from _thread import *
from base64 import b64encode, b64decode
import argparse
from time import sleep

# python3 proxy.py --up_ip 51.250.81.57 --up_port 40002 --low_port 1338
# ssh -p 1338 user@127.0.0.1
"""
CLIENT1 <-> lower_socket <->       <-> upper_socket <->
CLIENT2 <-> lower_socket <-> PROXY <-> upper_socket <-> SERVER
CLIENT3 <-> lower_socket <->       <-> upper_socket <->

Clients are connected to current proxy using lower sockets.
Upper sockets are used to interact with some external server (should support multiple connections).
Proxy can work in encapsulator mode - encapsulate from lower to upper sockets and decapsulate back
    or in decapsulator mode in reverse direction
"""

parser = argparse.ArgumentParser()
parser.add_argument('--up_ip', type=str, help='upper server ip', required=True)
parser.add_argument('--up_port', type=int, help='upper server port', required=True)
parser.add_argument('--low_port', type=int, help='lower listener port', required=True)
parser.add_argument('--decapsulator', default=False, action="store_true", help='proxy should decapsulate')
args = parser.parse_args()

UPPER_SERVER = (args.up_ip, args.up_port)
LOWER_LISTENER = ('0.0.0.0', args.low_port)
encapsulator = not args.decapsulator  # should current proxy encapsulate or decapsulate data from lower sockets


def encapsulate(data):
    data = b64encode(data).decode()
    line1 = "POST / HTTP/1.1" if encapsulator else "HTTP/1.1 200 OK"
    line2 = "Host: capsule" if encapsulator else "Server: Apache"
    return f"{line1}\n" \
           f"{line2}\n" \
           f"Content-Type: application/octet-stream\n" \
           f"Content-Length: {len(data) + 1}\n\n" \
           f"{data}\n".encode()


def decapsulate(data):
    lines = data.split(b'\n')
    # print("decapsulate:", lines)
    try:
        return b64decode(lines[5])
    except Exception as e:
        return None


def multi_threaded_client(lower_sock):
    buffer = b''
    upper_sock = socket.socket()
    upper_sock.connect(UPPER_SERVER)
    while True:
        try:
            inputs = [lower_sock, upper_sock]
            input_ready, _, except_ready = select(inputs, [], inputs)
            if len(except_ready) > 0:
                raise Exception
            for s in input_ready:
                if s is lower_sock:
                    data = lower_sock.recv(2**20)
                    if not data:
                        raise Exception
                    if not encapsulator:
                        buffer += data
                        if buffer[-1] != ord('\n'):
                            continue
                        # print(f"> {buffer}")
                        data = decapsulate(buffer)
                        print(f"> {data}")
                        upper_sock.sendall(data)
                        buffer = b''
                    else:
                        print(f"> {data}")
                        data = encapsulate(data)
                        # print(f"> {data}")
                        upper_sock.sendall(data)
                elif s is upper_sock:
                    data = upper_sock.recv(2 ** 20)
                    if not data:
                        raise Exception
                    if not encapsulator:
                        print(f"< {data}")
                        data = encapsulate(data)
                        # print(f"< {data}")
                        lower_sock.sendall(data)
                    else:
                        buffer += data
                        if buffer[-1] != ord('\n'):
                            continue
                        # print(f"< {buffer}")
                        data = decapsulate(buffer)
                        print(f"< {data}")
                        lower_sock.sendall(data)
                        buffer = b''
                sleep(0.1)
        except Exception as e:
            lower_sock.sendall(b"Socket error\n")
            upper_sock.sendall(b"Socket error\n")
            lower_sock.close()
            upper_sock.close()
            print(e)
            break


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(LOWER_LISTENER)
    server.listen()
    print("Listening for connections...")
    while True:
        client, address = server.accept()
        print(f'New connection: {address[0]}')
        start_new_thread(multi_threaded_client, (client,))
