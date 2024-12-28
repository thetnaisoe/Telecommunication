import socket
import sys
import hashlib

def calculate_checksum(filename):
    md5_hash = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()

def send_checksum_to_server(checksum_host, checksum_port, file_id, checksum):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((checksum_host, checksum_port))
        message = f"BE|{file_id}|60|{len(checksum)}|{checksum}"
        sock.send(message.encode('utf-8'))
        response = sock.recv(1024).decode('utf-8')
        return response == 'OK'

def main():
    if len(sys.argv) != 7:
        print("Usage: python3 netcopy_cli.py <srv_ip> <srv_port> <chsum_srv_ip> <chsum_srv_port> <file_id> <filename>")
        sys.exit(1)

    # Parse command line arguments
    srv_ip, srv_port = sys.argv[1], int(sys.argv[2])
    chsum_srv_ip, chsum_srv_port = sys.argv[3], int(sys.argv[4])
    file_id = int(sys.argv[5])
    filename = sys.argv[6]

    # Calculate checksum
    checksum = calculate_checksum(filename)

    # Transfer file to server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((srv_ip, srv_port))
        
        # Send file contents
        with open(filename, 'rb') as file:
            for chunk in iter(lambda: file.read(4096), b""):
                sock.send(chunk)

    # Send checksum to checksum server
    success = send_checksum_to_server(chsum_srv_ip, chsum_srv_port, file_id, checksum)
    if not success:
        print("Failed to send checksum to server")

if __name__ == "__main__":
    main()