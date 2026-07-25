import socket
import json

# Integration point for acting as the default model provider
HOST = '127.0.0.1'
PORT = 65432

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Actor Model Socket listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(1024)
                if not data:
                    break
                
                # Process request
                request = json.loads(data.decode())
                print(f"Received request: {request}")
                
                # Mock response
                response = {"status": "success", "message": "Processed by Actor Model"}
                conn.sendall(json.dumps(response).encode())

if __name__ == '__main__':
    start_server()
