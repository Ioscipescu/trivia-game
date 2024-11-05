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

connected_clients = []
client_states = {}
client_names = {}
client_answers = {}
client_points = {}
client_lock = threading.Lock()
current_game_state = GameState.WAITING
question_sent = False
question_number = 1

def log_connected_clients():
    with client_lock:
        print(f"Connected clients: {connected_clients}")
        print(f"Client states: {client_states}")

def broadcast_message(msg, exclude_address=None, locked=False):
    if not locked:
        with client_lock:
            for client_socket, addr in connected_clients:
                if addr != exclude_address:
                    try:
                        client_socket.send(msg.serialize())
                    except Exception as e:
                        print(f"Error sending message to {addr}: {e}")
    else: 
        for client_socket, addr in connected_clients:
                if addr != exclude_address:
                    try:
                        client_socket.send(msg.serialize())
                    except Exception as e:
                        print(f"Error sending message to {addr}: {e}")

def start_game_if_ready():
    global current_game_state
    with client_lock:
        ready_clients = [client for client, state in client_states.items() if state == "ready"]
        if len(connected_clients) >= 2 and len(ready_clients) == len(connected_clients):
            broadcast_message(Message(Message.MessageType.STATUS, "Game start", expected_response=Message.MessageType.ACKNOWLEDGMENT), locked=True)
            current_game_state = GameState.ASKING
            print("Game state updated to ASKING")

def handle_question():
    global question_sent, question_number, current_game_state
    with client_lock:
        if  question_number > 3:
            end_game()
        elif current_game_state == GameState.ASKING and not question_sent:
            question = Questions[f"Q{question_number}"]
            broadcast_message(
                Message(
                    Message.MessageType.QUESTION,
                    f"Question {question_number}: {question}",
                    expected_response=Message.MessageType.ANSWER
                ), 
                locked=True
            )
            question_sent = True
            print(f"Sent Question {question_number}")

        elif len(client_answers) == len(connected_clients):  # All clients have answered
            response = "Everyone has answered. "
            correct_answer = Answers[f"Q{question_number}"]

            # Award points for correct answers
            for addr, answer in client_answers.items():
                if answer == correct_answer:
                    client_points[addr] += 1
            response += f"The correct answer was {correct_answer}. Scores: \n"
            response += "\n".join([f"{client_names[addr]}: {points}" for addr, points in client_points.items()])

            # Send the results to all clients
            broadcast_message(
                Message(
                    Message.MessageType.RESULT,
                    response,
                    expected_response=Message.MessageType.ACKNOWLEDGMENT
                ),
                locked=True
            )

            # Clear answers and prepare for the next question
            client_answers.clear()
            question_sent = False
            question_number += 1

            if question_number > 3:  # Check if all questions have been asked
                print(f"Preparing to end game")  # End the game if no more questions are left
            else:
                print(f"Preparing to send Question {question_number}...")
                # Immediately send the next question

def end_game():
    global current_game_state, question_number
    current_game_state = GameState.WAITING
    question_number = 1
    for addr in client_states:
        client_states[addr] = "not_ready"
    broadcast_message(Message(Message.MessageType.STATUS, "Game over. Type 'ready' to start another game."), locked=True)

def handle_client(client_socket, address):
    with client_lock:
        connected_clients.append((client_socket, address))
        client_states[address] = "not_ready"
        client_points[address] = 0
    log_connected_clients()

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
                    name = message.content
                    if name in client_names.values():
                        name += f" ({len([n for n in client_names.values() if n == name])})"
                    client_names[address] = name
                broadcast_message(Message(Message.MessageType.STATUS, f"{address} has set their username to {name}"), exclude_address=address)
                client_socket.send(Message(Message.MessageType.NAME, name).serialize())

            elif message.header["type"].upper() == Message.MessageType.HELP:
                response = "Available commands: 'exit', 'help', 'ready'"
                client_socket.send(Message("response", response).serialize())

            elif message.header["type"].upper() == Message.MessageType.STATUS and message.content.lower() == "ready":
                with client_lock:
                    client_states[address] = "ready"
                start_game_if_ready()

            elif message.header["type"].upper() == Message.MessageType.ANSWER:
                with client_lock:
                    client_answers[address] = message.content
                handle_question()
            elif message.header["expected_response"].upper() == Message.MessageType.QUESTION:
                handle_question()


    except Exception as e:
        print(f"Error with {address}: {e}")

    finally:
        with client_lock:
            connected_clients.remove((client_socket, address))
            del client_states[address]
            del client_points[address]
            if address in client_names:
                del client_names[address]
            broadcast_message(Message(Message.MessageType.STATUS, f"Client {address} has left the game"), exclude_address=address, locked=True)
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
            threading.Thread(target=handle_client, args=(client_socket, address)).start()

    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    if len(sys.argv) == 3:
        start_server(sys.argv[1], int(sys.argv[2]))
    else:
        start_server()
