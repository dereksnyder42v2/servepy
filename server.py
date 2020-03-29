#!/usr/bin/env python3

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

def toBytes(myStr):
    return bytes(myStr, "utf-8")

# thread to handle new clients. once handled, starts thread for each new client.
def handleNewClient():
    print("handleNewClient() called")
    newClientSock, newClientAddress = SERVER.accept()
    clientD[newClientSock.getpeername()] = newClientSock
    #starts thread to manage client
    Thread(target = handleClient, args = (newClientSock,)).start() 

def handleClient(client):
    print("handleClient() called")
    while True:
        msg = client.recv(BUFSZ).decode("utf-8")
        print("msg received")
        if msg != '~':
            print("Someone sent a message: %s" % (msg))
            broadcast(msg)
        else:
            client.close()
            break

#sends message to all clients
def broadcast(msg):
    print("broadcast() called")
    for clientName in clientD.keys():
        clientD[clientName].send(toBytes("%s\n" % msg)) #inner object is a socket we are sending to
        
if __name__ == "__main__":
    
    HOST = ""
    PORT = 8080
    BUFSZ = 1024
    ADDR = (HOST, PORT)
    SERVER = socket(AF_INET, SOCK_STREAM)
    SERVER.bind(ADDR)
    clientD = dict() # key: client name, value: socket object
    print("Server started...")

    SERVER.listen(5) # mandatory; optional for python >=3.5

    while True:
        try:
            acceptThread = Thread(target=handleNewClient)
            acceptThread.start()
            acceptThread.join()
            #SERVER.close()
        except:
            print("Something went wrong. Closing server...")
            SERVER.close()
            print("Server connection closed, port released. Exiting")
            quit(1)
    
