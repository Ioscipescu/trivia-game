# Trivia Game

This is a simple game of trivia implemented using Python and sockets.

**How to play:**

1. **Start the server:** Run the `server.py` script. ```python game-server.py "<host> <port>"```
2. **Connect clients:** Run the `client.py` script  ```python game-client.py "<host> <port>"``` on two to ten different machines or terminals.
3. **Choose username:** Every client gets to choose their own unique username
4. **Play the game:** Players take turns entering their moves. The player to have the most points at the end of the game wins!

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
