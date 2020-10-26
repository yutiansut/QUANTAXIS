import socket
import sys
import time


def fetchCodeZjlx(code = None):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 10000)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)

    try:

        # Send data
        # message = b'This is the message.  It will be repeated.'
        strMsg = 'read:%s'%code
        message = strMsg.encode()
        sock.sendall(message)
        print('sending {!r}'.format(message))

        while True:
            data = sock.recv(512)
            if len(data) == 0:
                time.sleep(1)
                continue

            # print('received {!r}'.format(data))

            cmdString = data.decode();
            cmdArry = cmdString.split('@')

            print(cmdArry[0])
            cmd = cmdArry[0].strip('0')
            print(cmd)

            if (cmd == 'progress'):
                print('progress')
                print(cmdArry[1])
                continue

            if (cmd == 'logging'):
                print('logging')
                print(cmdArry[1])
                continue

            if (cmd == 'data'):
                print("data is ")
                print(cmdArry[1].encode('utf-8'))

            if (cmd == 'finished'):
                print('finish')
                print(cmdArry[1].encode('utf-8'))
                break;

    finally:
        print('closing socket')
        sock.close()


if __name__ == '__main__':
    fetchCodeZjlx(code = '000232')

    fetchCodeZjlx(code = '002424')

    fetchCodeZjlx(code = '300439')
