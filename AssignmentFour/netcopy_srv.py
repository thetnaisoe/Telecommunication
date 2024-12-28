import socket
import sys
import hashlib

def calculate_checksum(filename):
    md5_hash = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()

def get_checksum_from_server(checksum_host, checksum_port, file_id):
    """Retrieve checksum from the checksum server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((checksum_host, checksum_port))
        message = f"KI|{file_id}"
        sock.send(message.encode('utf-8'))
        response = sock.recv(1024).decode('utf-8')
        
        if response == "0|":
            return None
        
        checksum_len, checksum = response.split('|')
        return checksum

def main():
    if len(sys.argv) != 7:
        print("Usage: python3 netcopy_srv.py <srv_ip> <srv_port> <chsum_srv_ip> <chsum_srv_port> <file_id> <filename>")
        sys.exit(1)

    # Parse command line arguments
    srv_ip, srv_port = sys.argv[1], int(sys.argv[2])
    chsum_srv_ip, chsum_srv_port = sys.argv[3], int(sys.argv[4])
    file_id = int(sys.argv[5])
    filename = sys.argv[6]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((srv_ip, srv_port))
        server_socket.listen(1)
        print(f"Server listening on {srv_ip}:{srv_port}")

        client_socket, addr = server_socket.accept()
        
        with open(filename, 'wb') as file:
            while True:
                chunk = client_socket.recv(4096)
                if not chunk:
                    break
                file.write(chunk)

    local_checksum = calculate_checksum(filename)

    server_checksum = get_checksum_from_server(chsum_srv_ip, chsum_srv_port, file_id)

    if server_checksum and local_checksum == server_checksum:
        print("CSUM OK")
    else:
        print("CSUM CORRUPTED")

if __name__ == "__main__":
    main()