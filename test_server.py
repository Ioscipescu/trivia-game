import unittest
from unittest.mock import patch, MagicMock
from libmessage import Message
import server
from server import (
    broadcast_message,
    start_game_if_ready,
    handle_question,
    end_game,
)

class TestTriviaServer(unittest.TestCase):
    def setUp(self):
        global connected_clients, client_states, client_names, client_answers, client_points, current_game_state
        server.connected_clients = []
        server.client_states = {}
        server.client_names = {}
        server.client_answers = {}
        server.client_points = {}
        server.current_game_state = server.GameState.WAITING

    @patch("server.broadcast_message")
    def test_start_game_if_ready(self, mock_broadcast_message):
        with server.client_lock:
            server.connected_clients.append(("socket1", "addr1"))
            server.connected_clients.append(("socket2", "addr2"))
            server.client_states["addr1"] = "ready"
            server.client_states["addr2"] = "ready"

        start_game_if_ready()
        mock_broadcast_message.assert_called_once()
        self.assertEqual(server.current_game_state, server.GameState.ASKING)

    @patch("server.broadcast_message")
    def test_handle_question(self, mock_broadcast_message):
        global question_sent, question_number, current_game_state
        server.question_sent = True
        server.question_number = 1
        server.current_game_state = server.GameState.ASKING

        with server.client_lock:
            server.connected_clients.append("addr1")
            server.connected_clients.append("addr2")
            server.client_names["addr1"] = "Player1"
            server.client_names["addr2"] = "Player2"
            server.client_answers["addr1"] = server.Answers.Q1.value
            server.client_answers["addr2"] = "Wrong Answer"
            server.client_points["addr1"] = 0
            server.client_points["addr2"] = 0

        handle_question()

        self.assertEqual(server.client_points["addr1"], 1)
        self.assertEqual(server.client_points["addr2"], 0)
        self.assertEqual(server.question_number, 2)
        mock_broadcast_message.assert_called()


    @patch("server.broadcast_message")
    def test_end_game(self, mock_broadcast_message):
        # Set up game results
        with server.client_lock:
            server.client_names["addr1"] = "Player1"
            server.client_names["addr2"] = "Player2"
            server.client_points["addr1"] = 5
            server.client_points["addr2"] = 3

        end_game()
        mock_broadcast_message.assert_called_once()
        self.assertEqual(server.current_game_state, server.GameState.WAITING)
        self.assertEqual(server.question_number, 1)

    @patch("server.broadcast_message")
    def test_broadcast_message(self, _):
        mock_socket1 = MagicMock()
        mock_socket2 = MagicMock()
        with server.client_lock:
            server.connected_clients.append((mock_socket1, "addr1"))
            server.connected_clients.append((mock_socket2, "addr2"))

        msg = Message(Message.MessageType.STATUS, "Test broadcast")
        broadcast_message(msg)

        mock_socket1.send.assert_called_once_with(msg.serialize())
        mock_socket2.send.assert_called_once_with(msg.serialize())

    def test_names_to_sentence(self):
        from server import names_to_sentence

        self.assertEqual(names_to_sentence([]), "")
        self.assertEqual(names_to_sentence(["Alice"]), "Alice")
        self.assertEqual(names_to_sentence(["Alice", "Bob"]), "Alice and Bob both")
        self.assertEqual(
            names_to_sentence(["Alice", "Bob", "Charlie"]),
            "Alice, Bob, and Charlie all",
        )


if __name__ == "__main__":
    unittest.main()
