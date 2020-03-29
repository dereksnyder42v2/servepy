#!/usr/bin/env python3

"""
command line argument #1 ("sys.argv[0]") is hostname to connect to.
./client.py localhost   # connects to chat server on local
./client.py 192.168.1.1 # connects to server on other machine in the network
"""

def toBytes(myStr):
    return bytes(myStr, "utf-8")

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

def receive():
    print("receive() called")
    while True:
        try:
            msg = clientSocket.recv(BUFSZ).decode("utf-8")
            print(msg)
        except Exception as e: # client left chat?
            print(e)
            break

def send(msg):
    print("send() called")
    clientSocket.send(toBytes(msg))
    """
    if msg == QUITMSG:
        clientSocket.close()
    """
    return

if __name__ == "__main__":
    import sys # for using command line arguent as hostname to connect to

    #...Open connection to server
    BUFSZ = 1024
    HOST = sys.argv[1]
    PORT = 8080
    ADDR = (HOST, PORT)
    clientSocket = socket(AF_INET, SOCK_STREAM)
    try:
        clientSocket.connect(ADDR)
    except:
        # connection failed
        print("The server is not available.")
        quit(1)
    print("Connected to server.")

    # "user clicked, asking for help.\n in CPSC4550, no one can hear you scream"
    
    receiveThread = Thread(target = receive)
    receiveThread.start()
    # REPL
    while True:
        msg = input(" > ")
        print("Sending %s..." % (msg))
        try:
            send(msg)
        except Exception as e:
            print("Something went wrong:", e)
            quit(1)
