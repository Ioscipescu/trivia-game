from enum import Enum
import socket
import sys
import threading
from libmessage import Message

class GameState(str, Enum):
    WAITING = "WAITING"
    ASKING = "ASKING"
    ANSWERING = "ANSWERING"

class Questions(str, Enum):
    Q1 = "Example question"
    Q2 = "Example question"
    Q3 = "Example question"

class Answers(str, Enum):
    Q1 = "Example answer"
    Q2 = "Example answer"
    Q3 = "Example answer"

# Global variables to track connected clients and their states
connected_clients = []
client_states = {}
client_names = {}
client_answers = {}
client_points = {}
client_lock = threading.Lock()
current_game_state = GameState.WAITING
questionSent = False
question_number = 1

def log_connected_clients():
    with client_lock:
        print(f"Connected clients: {connected_clients}")
        print(f"Client states: {client_states}")

def check_and_start_game():
    global current_game_state
    with client_lock:
        ready_clients = [client for client, state in client_states.items() if state == "ready"]
        if len(connected_clients) >= 2 and len(ready_clients) == len(connected_clients):
            # Broadcast "game start" to all connected clients
            print("Two or more clients are ready. Sending 'game start' to all clients.")
            for client_socket, _ in connected_clients:
                try:
                    client_socket.send(Message(Message.MessageType.STATUS, "Game start", expected_response=Message.MessageType.ACKNOWLEDGMENT).serialize())
                except Exception as e:
                    print(f"Error sending 'game start' to client: {e}")
            
            # Only set to ASKING when the game starts
            current_game_state = GameState.ASKING
            print(f"Game state updated to {current_game_state}")

def handle_question():
    global current_game_state
    global client_answers
    global questionSent
    global question_number
    with client_lock:
        print(f"Game state: {current_game_state}")
        print(f"Answers received: {len(client_answers)}")
        print(f"Question sent: {questionSent}")

        # Send the question only if we're in ASKING state and the question hasn't been sent yet
        if current_game_state == GameState.ASKING and not questionSent:
            print("Sending question to clients")
            for client_socket, _ in connected_clients:
                try:
                    question = Questions.Q1 if question_number == 1 else Questions.Q2 if question_number == 2 else Questions.Q3
                    client_socket.send(Message(Message.MessageType.QUESTION, f"Question {question_number}: {question}", expected_response=Message.MessageType.ANSWER).serialize())
                    questionSent = True
                except Exception as e:
                    print(f"Error sending 'question' to client: {e}")
        
        # Check if all clients have answered
        elif current_game_state == GameState.ASKING and len(client_answers) == len(connected_clients):
            print("All clients have answered")
            
            for client_socket, _ in connected_clients:
                try:
                    response = "Everyone has answered."
                    for address, answer in client_answers.items():
                        if answer == Answers.Q1:  # Compare the answer with the correct one
                            client_points[address] += 1
                        print(f"Client {address} answered correctly and has {client_points[address]} points.")
                        response += f"Client {address} "
                    if (response == "Everyone has answered."):
                        response += "No one answered correctly."
                    response += "have answered correctly. "
                    response += f"The correct answer was {Answers.Q1} "
                    response += f"The scores now are: \n"
                    for address, points in client_points:
                        response += f"Client {address} has {points} points.\n"
                    client_socket.send(Message(Message.MessageType.RESULT, response, expected_response=Message.MessageType.ACKNOWLEDGMENT).serialize())
                    questionSent = True
                except Exception as e:
                    print(f"Error sending 'question' to client: {e}")
            # Reset for next question or round
            client_answers = {}  # Reset client answers for the next question
            questionSent = False  # Reset the flag to allow sending the next question
            question_number += 1

            if question_number > 3:
                print("All questions have been asked. Ending the game.")
                current_game_state = GameState.WAITING  # Reset the game state to WAITING
                for address, _ in client_states:
                    client_states[address] = "not_ready"
                for client_socket, _ in connected_clients:
                    try:
                        client_socket.send(Message(Message.MessageType.STATUS, "To start another game type ready", expected_response=Message.MessageType.STATUS).serialize())
                    except Exception as e:
                        print(f"Error sending 'game start' to client: {e}")
            
            else:
                print(f"Ready for the next question {question_number}")

def handle_client(client_socket, address):
    with client_lock:
        connected_clients.append((client_socket, address))
        client_states[address] = "not_ready"
        client_points[address] = 0
        for client_socket, addr in connected_clients:
            if addr != address:
                try:
                    client_socket.send(Message(Message.MessageType.STATUS, f"Client {address} just joined the game",expected_response=Message.MessageType.NONE).serialize())
                except Exception as e:
                    print(f"Error sending 'game start' to client: {e}")
    log_connected_clients()

    print(f"Connection established with {address}")
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            
            message = Message.deserialize(data)
            print(f"Received from {address}: {message.content}")

            if message.header["type"].upper() == Message.MessageType.QUIT:
                print(f"Connection closed by {address}")
                break
            elif message.header["type"].upper() == Message.MessageType.NAME:
                with client_lock:
                    client_names[address] = message.content
                    print(f"Client {address} set name {client_names[address]}")
            elif message.header["type"].upper() == Message.MessageType.HELP:
                response = "Available commands: 'exit', 'help', 'ready'"
                client_socket.send(Message("response", response).serialize())
            elif message.header["type"].upper() == Message.MessageType.STATUS and message.content.lower() == "ready":
                with client_lock:
                    client_states[address] = "ready"
                print(f"{address} is now ready.")
                check_and_start_game()
            elif message.header["type"].upper() == Message.MessageType.ANSWER:
                with client_lock:
                    client_answers[address] = message.content
                handle_question()
            elif message.header["type"].upper() == Message.MessageType.ACKNOWLEDGMENT:
                handle_question()
            else:
                response = f"Echo: {message.header['type'].upper()} {message.content}"
                client_socket.send(Message("response", response).serialize())

    except Exception as e:
        print(f"Error with {address}: {e}")
    finally:
        with client_lock:
            connected_clients.remove((client_socket, address))
            del client_states[address]
            for client_socket, addr in connected_clients:
                if addr != address:
                    try:
                        client_socket.send(Message(Message.MessageType.STATUS, f"Client {address} just left the game", expected_response=Message.MessageType.NONE).serialize())
                    except Exception as e:
                        print(f"Error sending 'client left' to other clients: {e}")
        log_connected_clients()
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
        print("Caught keyboard interrupt, exiting")
    finally:
        server_socket.close()

if __name__ == "__main__":
    if len(sys.argv) == 3:
        host, port = sys.argv[1], int(sys.argv[2])
        start_server(host, port)
    else:
        start_server()
