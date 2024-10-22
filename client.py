import socket
import sys
from libmessage import Message

def start_client(host='127.0.0.1', port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    print("Connected to the server. Type 'help' for available commands.")
    try:
        while True:
                message_content = input("Enter message: ")
                message = Message("command",content=message_content)
                client_socket.send(message.serialize())

                if message_content.lower() == "exit":
                    break

                # Receive response from the server
                response = client_socket.recv(1024)
                message = Message.deserialize(response)
                print(f"Server response: {message.content}")
    except KeyboardInterrupt:
        print("caught keyboard interrupt, exiting")
    finally:
        client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) == 3:
        host, port = sys.argv[1], int(sys.argv[2])
        start_client(host, port)
    elif len(sys.argv) == 0:
        start_client()
    else:
        print("usage:", sys.argv[0], "<host> <port>")
        sys.exit(1)
