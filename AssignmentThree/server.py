import argparse
import random
import select
import socket
import struct
import sys

RANGE_LIMITS = (1, 100)

def pack_response(status, value):
    return struct.pack('ci', status, value)

def unpack_guess(data):
    return struct.unpack('ci', data)

def receive_exact(sock, length):
    return sock.recv(length, socket.MSG_WAITALL)

def manage_game(params, show_logs=False):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setblocking(False)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((params.address, params.port))
        server_socket.listen()

        active_sockets = [server_socket]
        timeout = 1

        while True:
            guessed = False
            target_number = random.randint(*RANGE_LIMITS)

            if show_logs:
                print('New target number:', target_number)

            while not guessed:
                ready_to_read, _, _ = select.select(active_sockets, [], active_sockets, timeout)

                for sock in ready_to_read:
                    if sock is server_socket:
                        client_conn, client_addr = sock.accept()
                        if show_logs:
                            print('Client connected:', client_addr)
                        active_sockets.append(client_conn)
                    else:
                        data = receive_exact(sock, 8)
                        if not data:
                            if show_logs:
                                print('Client disconnected')
                            active_sockets.remove(sock)
                            sock.close()
                        else:
                            comparison, guessed_num = unpack_guess(data)
                            comparison = comparison.decode()

                            if show_logs:
                                print('Received:', comparison, guessed_num, sock.getpeername())

                            if comparison == '=':
                                if target_number == guessed_num:
                                    guessed = True
                                    status = 'Y'
                                    if show_logs:
                                        print('Correct guess from:', sock.getpeername())
                                else:
                                    status = 'K'
                                response = pack_response(status.encode(), 0)
                                sock.sendall(response)
                                active_sockets.remove(sock)
                                sock.close()
                            else:
                                if comparison == '<':
                                    status = 'I' if target_number < guessed_num else 'N'
                                else:
                                    status = 'I' if target_number > guessed_num else 'N'
                                response = pack_response(status.encode(), 0)
                                sock.sendall(response)

            active_sockets.remove(server_socket)
            for sock in active_sockets:
                response = pack_response(b'V', 0)
                sock.sendall(response)
                sock.close()

            active_sockets = [server_socket]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('address', type=str)
    parser.add_argument('port', type=int)
    args = parser.parse_args(sys.argv[1:])
    manage_game(args, show_logs=True)

if __name__ == "__main__":
    main()