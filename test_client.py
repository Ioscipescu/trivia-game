import unittest
from unittest.mock import patch, MagicMock
import client
from client import start_client, receive_messages
from libmessage import Message
import threading
import os


class TestClient(unittest.TestCase):

    @patch("client.socket.socket")
    def test_start_client_connection_refused(self, mock_socket):
        """Test that the client exits gracefully when the server connection is refused."""
        mock_socket.return_value.connect.side_effect = ConnectionRefusedError
        with self.assertRaises(SystemExit) as cm:
            start_client(host="127.0.0.1", port=12345)
        self.assertEqual(cm.exception.code, os.EX_NOHOST)

    @patch("client.socket.socket")
    @patch("builtins.input", side_effect=["TestUser", "ready", "exit"])
    def test_start_client_ready_message(self, mock_input, mock_socket):
        """Test sending a 'ready' message after setting the username."""
        mock_socket_instance = mock_socket.return_value

        mock_socket_instance.recv.side_effect = [
            Message(Message.MessageType.NAME, content="TestUser").serialize(),
            Message(Message.MessageType.STATUS, content="Game starting", expected_response=Message.MessageType.QUESTION).serialize(),
            b""
        ]

        with self.assertRaises(SystemExit):
            start_client(host="127.0.0.1", port=12345)

        self.assertEqual(mock_socket_instance.send.call_count, 2)

        first_call = Message.deserialize(mock_socket_instance.send.call_args_list[0][0][0])
        self.assertEqual(first_call.content, "TestUser")

        second_call = Message.deserialize(mock_socket_instance.send.call_args_list[1][0][0])
        self.assertEqual(second_call.header["type"], Message.MessageType.STATUS)
        self.assertEqual(second_call.content, "ready")
        self.assertEqual(second_call.header["expected_response"], Message.MessageType.QUESTION)


    @patch("client.socket.socket")
    @patch("client.receive_messages")
    def test_receive_messages(self, mock_receive_messages, mock_socket):
        """Test that messages received from the server are handled correctly."""
        mock_socket_instance = mock_socket.return_value
        message_ready = Message(Message.MessageType.STATUS, content="ready", expected_response=Message.MessageType.QUESTION).serialize()
        message_question = Message(Message.MessageType.QUESTION, content="What is 2 + 2?", expected_response=Message.MessageType.ANSWER).serialize()

        mock_socket_instance.recv.side_effect = [message_ready, message_question, b""]

        def mocked_receive_messages(socket_instance):
            receive_messages(socket_instance)

        with patch("client.receive_messages", side_effect=mocked_receive_messages):
            thread = threading.Thread(target=receive_messages, args=(mock_socket_instance,))
            thread.start()
            thread.join()

        self.assertEqual(mock_socket_instance.recv.call_count, 3)


if __name__ == "__main__":
    unittest.main()
