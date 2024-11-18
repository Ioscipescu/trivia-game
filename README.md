# Trivia Game

This is a simple game of trivia implemented using Python and sockets.

**How to play:**

1. **Start the server:** Run the `server.py` script. ```python server -p PORT``` or ```.\server -p PORT``` the server listens on 0.0.0.0 automatically.
2. **Connect clients:** Run the `client.py` script  ```python client -i SERVER_IP/DNS -p PORT``` or ```.\client -i SERVER_IP/DNS -p PORT``` on two to ten different machines or terminals.
3. **Choose username:** Every client gets to choose their own unique username
4. **Play the game:** Players all answer the question at the same time, once every player has answered the correct answer is displayed and points are allocated. After 10 questions a winner or winners are declared.

**Technologies used:**

* Python
* Sockets
* Threads

**Message Protocol:**

Each message contains a header and the content. The header contains the message's byteorder, the message type, the encoding of the message, the checksum (not implemented yet), the length of the message, and the expected response. The content of the message is the actual content getting sent by the server or client. 

The message type can be any of:
    ANSWER
    QUESTION
    RESULT
    QUIT
    ERROR
    NONE
    HELP
    STATUS
    NAME
    ACKNOWLEDGMENT
Not all message types are used yet but they are all planned to be used in the future.

**Additional resources:**

* [Link to Python documentation]
* [Link to sockets tutorial]
