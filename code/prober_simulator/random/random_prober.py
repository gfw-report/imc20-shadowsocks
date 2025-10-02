#!/usr/bin/env python3

import socket
import time
import sys
import os
import binascii
import threading

HOST = '127.0.0.1'    # The remote host
PORT = 50800              # The same port as used by the server
TIMEOUT = 10

def send_payload(payload_hex, note):
    if not note:
        note = []
    payload_bytes = bytearray.fromhex(payload_hex)

    connection_success = False
    errno = 'No Error'
    err_message = 'No Error'
    message = ''
    print("Trying to connect to SS server port...")
    timestamp = time.time()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.settimeout(TIMEOUT)
            src_ip, src_port = s.getsockname()
            connection_success = True

            time.sleep(0.1)

            s.sendall(payload_bytes)
            print("Payload sent, waiting for server's response...")
            data = s.recv(1024)
        print('Received', repr(data))
        message = data
    except socket.error as E:
        errno = E.errno
        err_message = str(E)
    endtime = time.time()

    print("Testing finished...")

    result = (timestamp, *note, src_ip, src_port, HOST, PORT, endtime - timestamp,  payload_hex, len(payload_hex) / 2, connection_success, errno, err_message, message)
    print(';'.join(str(x) for x in result))
    with lock:
        with open(output_file, 'a+') as f:
            f.write(';'.join(str(x) for x in result))
            f.write("\n")

legit_payload_hex = \
    "80af2e609d2b9fece1a1d62d5ad54206c5c4352a8ffece88c101086e197e799a07dc883f638f4463fed7850bddeb0c710dd3d869496533aace1c440881abc730df9a78e2bd2a180b0ff3ecdf37cc3e52cfb27e54b58c9b906786e075ad6b67b2139df6f6d7a354888715417971382789af7b162926c08f41066d072863219696187c5e95afc4067b276cc17d8cbbb7af3ed5e7137b6d010478d1c9450434c1b900a1b203b63b5965dcb429aceda6fa17e071dfa40e360487faea888590d23913b4cd81625d4a4afb9b0c1a28065b2fa8eb1925bd96c3fa9680495a2b395fdb393d0e0072f2aec7e5df701a919fd7fe77465ce49225bfd3980b59332c3c300690f62fe9be94610320a4b2b35574bfbf53ceaaad38ba36ea5a8abfa564f3475eb0d7c30f324e0227cb501cccaeeffd8bac480f97e442eba6474dd2bd9390f9fd4d708e71d3b83fe0f439abb33c2a57b34e291a9c01e3c0d9abe90fcd0ea88c18dd018e87f51c173fc5483b33086efaa05a33a14272003397438d39b3104e5c350a5b5f2d3bd4531bbd06dd02d18601f3b080e286b9125a77cbab25332a51cceb620cefb4a41f41c3b2196588e6559b37b3d34f9249278b0d90d52553772e051aadc36e08b5e4b30e8a2a79f9692b1e4fe287365c2c7304ef0adf40d6d516e45c12e569ff719882841cd575e8e9b6a5d61fc03983aeed5b7e480d5b30acaa503bd4467af61d3477c71112395936a48e51f0ba3f2d868e74cc69c8753803e2205a4729aa"

def generate_replay_type1_payload_hex(legit_payload_hex):
    return legit_payload_hex

def generate_replay_type2_payload_hex(legit_payload_hex):
    first_byte = legit_payload_hex[:2]
    new_first_byte = binascii.b2a_hex(os.urandom(1)).decode("utf-8")
    while new_first_byte == first_byte:
        new_first_byte = binascii.b2a_hex(os.urandom(1)).decode("utf-8")
    return new_first_byte + legit_payload_hex[2:]

def generate_replay_type3_payload_hex(legit_payload_hex):
    first_eight_byte = legit_payload_hex[:16]
    new_first_eight_byte = binascii.b2a_hex(os.urandom(8)).decode("utf-8")
    while new_first_eight_byte == first_eight_byte:
        new_first_eight_byte = binascii.b2a_hex(os.urandom(1)).decode("utf-8")

    middle_byte = legit_payload_hex[62:64]
    new_middle_byte = binascii.b2a_hex(os.urandom(1)).decode("utf-8")
    while new_middle_byte == middle_byte:
        new_middle_byte = binascii.b2a_hex(os.urandom(1)).decode("utf-8")

    return new_first_eight_byte + legit_payload_hex[16:62] + \
         new_middle_byte  + legit_payload_hex[64:]

def generate_len_non_replay_payload_hex(length):
    return binascii.b2a_hex(os.urandom(length)).decode("utf-8")

payload_file = sys.argv[1]
output_file = sys.argv[2]
method = sys.argv[3]

if __name__ == "__main__":
    lock = threading.Lock()

    MAX_THREAD = 1
    threads = []
    f = open(output_file, 'a+')

    for index in range(1, 100):
        print("Sending non-replay payload {}...".format(index))
        for _ in range(150):
            t = threading.Thread(
                target=send_payload,
                args=(generate_len_non_replay_payload_hex(index),
                      [method, 'non_replay']))
            threads.append(t)
            t.start()

        if index % MAX_THREAD == 0:
            for t in threads:
                t.join()

    for t in threads:
        t.join()

    f.close()
