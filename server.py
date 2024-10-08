import socket
import sys
import threading
from libmessage import Message

def handle_client(client_socket, address):
    print(f"Connection established with {address}")
    try:
        while True:
                # Receive data from the client
                data = client_socket.recv(1024)
                if not data:
                    break

                message = Message.deserialize(data)
                print(f"Received from {address}: {message.content}")

                if message.content.lower() == "exit":
                    print(f"Connection closed by {address}")
                    break
                elif message.content.lower() == "help":
                    response = "Available commands: 'exit', 'help'"
                    client_socket.send(Message("response", response).serialize())
                else:
                    response = f"Echo: {message.content}"
                    client_socket.send(Message("response", response).serialize())

    except Exception as e:
        print(f"Error with {address}: {e}")
    finally:
        client_socket.close()

def start_server(host='127.0.0.1', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    try:
        while True:
            client_socket, address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
            client_thread.start()
        
    except KeyboardInterrupt:
        print("caught keyboard interrupt, exiting")
    finally:
        server_socket.close()

if __name__ == "__main__":
    if len(sys.argv) == 3:
        host, port = sys.argv[1], int(sys.argv[2])
        start_server(host, port)
    elif len(sys.argv) == 0:
        start_server()
    else:
        print("usage:", sys.argv[0], "<host> <port>")
        sys.exit(1)
