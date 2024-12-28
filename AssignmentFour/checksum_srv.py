import socket
import sys
import threading
import time

class ChecksumServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.checksums = {}
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

    def clean_expired_checksums(self):
        current_time = time.time()
        expired_keys = [k for k, v in self.checksums.items() if v['expiration'] < current_time]
        for key in expired_keys:
            del self.checksums[key]

    def handle_client(self, client_socket):
        try:
            data = client_socket.recv(1024).decode('utf-8')
            
            if data.startswith('BE|'):
                _, file_id, validity, checksum_len, checksum = data.split('|')
                file_id = int(file_id)
                validity = int(validity)
                
                self.checksums[file_id] = {
                    'checksum': checksum,
                    'expiration': time.time() + validity
                }
                
                client_socket.send('OK'.encode('utf-8'))
            
            elif data.startswith('KI|'):
                _, file_id = data.split('|')
                file_id = int(file_id)
                
                self.clean_expired_checksums()
                
                if file_id in self.checksums:
                    checksum = self.checksums[file_id]['checksum']
                    response = f"{len(checksum)}|{checksum}"
                else:
                    response = "0|"
                
                client_socket.send(response.encode('utf-8'))
        
        except Exception as e:
            print(f"Error handling client: {e}")
        
        finally:
            client_socket.close()

    def run(self):
        print(f"Checksum server running on {self.host}:{self.port}")
        while True:
            client_socket, addr = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 checksum_srv.py <ip> <port>")
        sys.exit(1)
    
    host = sys.argv[1]
    port = int(sys.argv[2])
    
    server = ChecksumServer(host, port)
    server.run()

if __name__ == "__main__":
    main()