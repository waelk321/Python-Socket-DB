# Python-Socket-DB

This project implements a simple TCP client/server in Python. Coded this for my class "Comp 348: Principles of Programming Languages".
The server loads customer records from a text file into memory and the client provides a menu
to perform database operations (find/add/delete/update/print report). 

# How to run 
The server expects a file named data.txt in the same folder as server.py.
Each record is one line with fields separated by |. 
example: John|43|123 Apple street|514-3452
Open **two terminals** in the project folder.

## Files
- server.py - Loads the database and handles client requests over TCP
- client.py - User interface that sends requests and displays server responses


