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

**Testing the Code:**
To run the test scripts on either client or server run ```python3 -m unittest test_server.py``` or ```python3 -m unittest test_client.py```.

**Potential Security Issues:**

In this codebase has no input validation in the serialize and deserialize methods. This could potentially allow some sort of arbitrary code execution by a malicious actor. A fix for this could be using a more secure serialization method than the current json one. There is also no authentication or authorization within this codebase, allowing any user to join. This could be mitigated with an actual authentication method and allowed users. Additionally, this code is vulnerable to DoS and DDoS attacks, as there is no limit on connections and messages sent. Preventing too many clients from joining and limiting how often messages can be received could mitigate this. Finally, there is the potential for my threading usage to cause race conditions and incorrect updating of global variables in ways that I did not foresee, potentially causing any number of issues.

**Timeline**

Sprint 0: Form teams, Setup Tools, Submit SOW [Template] (Sept 08-Sept 22)
Sprint 1: Socket Programming, TCP Client Server (Sept 22-Oct 06)
Sprint 2:  Develop Game Message Protocol, Manage Client connections (Oct 06-Oct 20)
Sprint 3:  Multi-player functionality, Synchronize state across clients. (Oct 20-Nov 03)
Sprint 4:  Game play, Game State (Nov 03-Nov 17)
Sprint 5: Implement Error Handling and Testing (Nov 17-Dec 6)

**Retrospective**

I believe that a lot went right in this project, my server and clients work together seemlessly, the game logic functions, and I learned a lot about writing networking software, especially in Python. I also learned quite a bit about threading thanks to my use of multithreading to allow the server to handle multiple clients and to allow the client to listen to the server and wait for user input concurrently. There are still elements that could be improved, I have no form of question randomization implemented and I also do not allow for multiple different correct answers (such as a singular vs plural form of a word). I also should store questions and answers in a file such as a CSV file for easy editing rather than in a python dictionary directly within the code. Finally, I initially wanted to add encryption but never got around to fully implementing it, so that feature is missing. 
