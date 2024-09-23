# Project Title:
Trivia game

# Team:
Ben Blount

# Project Objectives:
To develop a python-based simple multiplayer online game using a client-server architecture, teaching fundamental concepts of networking and socket programming in a hands-on manner. 

This project will be a trivia game that will support between 2 and 10 players at once. The project will involve a client-server architecture, where the server will listen for incoming connections and respond to clients.

# Scope:
Inclusions:
Server-Client Architecture: The game must implement a clear server-client architecture, with the server handling game state and communication between clients.
Game Logic: The game must accurately implement the rules of the game (as defined in your SOW):
    Determining the winner.
    Handling draw conditions.
Multiplayer Capability: The game should allow multiple clients to connect and play simultaneously.
Error Handling: The game should gracefully handle common errors, such as network failures, invalid input, or unexpected game states.
Encryption: Communication between the client and server should be encrypted with an encryption scheme like RSA.
Readability: The code should be well-formatted, use meaningful variable names, and include comments to explain complex logic.
Modularity: The code should be organized into well-defined functions and modules to improve maintainability.
Efficiency: The game should avoid unnecessary computations, resource-intensive operations, or unnecessary network round trips.
Error Handling: The code should include basic error handling for connections, and gameplay

Exclusions:
There will be no need to alternate turns between players because all players play at once.
There will be no webui for this project, all of the UI will be throught the terminal.

# Deliverables:
The project should have working client and server Python scripts along with full detailed documentation so players can play the game. 

# Timeline:
Key Milestones:
This project will involve 6 (0-5) sprints.

Each sprint will be two weeks long (#5 will be three weeks due to fall break)

    Sprint 0: Form teams, Setup Tools, Submit SOW [Template] (Sept 08-Sept 22)
    Sprint 1: Socket Programming, TCP Client Server (Sept 22-Oct 06)
    Sprint 2:  Develop Game Message Protocol, Manage Client connections (Oct 06-Oct 20)
    Sprint 3:  Multi-player functionality, Synchronize state across clients. (Oct 20-Nov 03)
    Sprint 4:  Game play, Game State (Nov 03-Nov 17)
    Sprint 5: Implement Error Handling and Testing (Nov 17-Dec 6)

Task Breakdown:
Sprint 0: The Readme should take about 5 minutes to setup and the SOW required for Sprint 0 should take about 30. All required software was already installed and set up so no time needs to be dedicated tot that.

Technical Requirements:
Hardware:
There must be at least one machine capable of running the server and another 2-10 capable of running the client code. All machines will need to be linux based.
Software:
mplement client-server architecture capable of at least two simultaneous clients
Client must take the following arguments

    -h (help show the player how to connect, and play)
    -i ip address of the server (required argument)
    -p listening port of the server
    -n DNS name of the server

Server must take the following arguments

    -h (help show the user how to run the server)
    -i host-ip
    -p port

# Assumptions:
All users must be connected to the same local network, such as the csu-net network.

# Roles and Responsibilities:
As a single person team Ben will be responsible for all tasks, including managing, developing, and testing the program.

# Communication Plan:
As a single person team there will be no need for communication between people.

# Additional Notes:
Nothing to note.

