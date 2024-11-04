import argparse
import random
import socket
import struct
import sys
import time

RANGE_LIMITS = (1, 100)

def pack_guess(operation, number):
    return struct.pack('ci', operation, number)

def unpack_response(response_data):
    return struct.unpack('ci', response_data)

def receive_full(sock, length):
    return sock.recv(length, socket.MSG_WAITALL)

def calculate_guesses(range_bounds):
    if range_bounds[1] - range_bounds[0] == 1:
        return [pack_guess(b'=', range_bounds[0]), pack_guess(b'=', range_bounds[1])]
    else:
        current_guess = (range_bounds[0] + range_bounds[1]) // 2
        return [pack_guess(b'<', current_guess)]

def adjust_range(response_code, range_bounds, guessed_number):
    if response_code == 'I':
        range_bounds[1] = guessed_number
    elif response_code == 'N':
        range_bounds[0] = guessed_number
    else:
        raise ValueError('Unexpected response received.')

def check_end_game(response_code):
    return response_code in ('K', 'Y', 'V')

def initiate_game(params, show_logs=False):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        client_socket.connect((params.address, params.port))

        range_bounds = list(RANGE_LIMITS)

        game_active = True
        while game_active:
            guess_packets = calculate_guesses(range_bounds)
            
            for guess_packet in guess_packets:
                time.sleep(random.randint(1, 5))  # Simulate thinking time
                client_socket.sendall(guess_packet)

                response = receive_full(client_socket, 8)
                response_code = unpack_response(response)[0].decode()

                guess = unpack_response(guess_packet)
                guessed_number = int(guess[1])

                if show_logs:
                    print(f">>> {guess[0].decode()} {guess[1]}")
                    print(f"<<< {response_code}")

                if check_end_game(response_code):
                    return

                adjust_range(response_code, range_bounds, guessed_number)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('address', type=str)
    parser.add_argument('port', type=int)
    params = parser.parse_args(sys.argv[1:])
    initiate_game(params, show_logs=True)

if __name__ == "__main__":
    main()