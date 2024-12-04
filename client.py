#!/usr/bin/env python3

import argparse
import socket
import sys
import os
import threading
from libmessage import Message

# Create a lock to manage access to shared resources
response_lock = threading.Lock()
previous_response = Message(Message.MessageType.NONE, content="", expected_response=Message.MessageType.NONE)
username = ""

def receive_messages(client_socket):
    """Thread function to receive messages from the server and update the previous_response."""
    global previous_response
    global username
    try:
        while True:
            response = client_socket.recv(1024)
            if not response:
                print("Server closed the connection.")
                break
            message = Message.deserialize(response)
            
            if message.header["type"] == Message.MessageType.NAME:
                with response_lock:
                    username = message.content
                print(f"Your name has been set to {username}, to start the game type ready")
                continue

            # Update the previous_response using a lock
            with response_lock:
                previous_response = message
            
            print(f"\nServer response: {message.content}")
            # print(message.header["expected_response"])
            # Check if the message is a "game start" message and send acknowledgment
            if message.header["expected_response"] == Message.MessageType.ACKNOWLEDGMENT:
                # print("Sending acknowledgment.")
                acknowledgment = Message(Message.MessageType.ACKNOWLEDGMENT, content="Acknowledged", expected_response=Message.MessageType.QUESTION)
                client_socket.send(acknowledgment.serialize())
            

    except Exception as e:
        print(f"Error receiving data data from the server, closing connection")
    finally:
        client_socket.close()

def start_client(host='127.0.0.1', port=12345):
    global previous_response
    global username

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
    except ConnectionRefusedError:
        print("Connection Refused by server, make sure that the IP and Port are correct and try again")
        sys.exit(os.EX_NOHOST) 

    print("Connected to the server. Please send your desired username")

    # Start a thread to listen for server messages
    receiver_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receiver_thread.daemon = True  # Daemon thread will exit when the main program exits
    receiver_thread.start()

    try:
        while True:
            # Use the lock to safely access previous_response
            with response_lock:
                expected_response = previous_response.header["expected_response"]
            
            # Check if the server expects an answer
            # if expected_response == Message.MessageType.ANSWER:
            #     message_content = input("Enter your answer: ")
            # else:
            message_content = input() #"Enter message: "

            if message_content.lower() == "exit":
                break  # Exit loop to close connection and terminate client

            if username == "":
                message = Message(Message.MessageType.NAME, content=message_content, expected_response=Message.MessageType.NAME)
            elif message_content.lower() == "ready":
                message = Message(Message.MessageType.STATUS, content="ready", expected_response=Message.MessageType.QUESTION)
            else:
                message = Message(Message.MessageType.ANSWER, content=message_content, expected_response=Message.MessageType.RESULT)
                
            client_socket.send(message.serialize())

    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        client_socket.close()
        sys.exit(0)
        print("Connection closed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start the client and connect to the server.")
    parser.add_argument("-i", "--ip", type=str, required=True, help="IP or DNS of the server")
    parser.add_argument("-p", "--port", type=int, required=True, help="Port to connect to")
    args = parser.parse_args()
    
    start_client(args.ip, args.port)
