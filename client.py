from socket import *
from time import sleep

# function to read config.txt for server IP and PORT
# same function from server.py
def read_config_file():
    with open("config.txt", "r") as file:
        lines = file.readlines()

        # Assigned second line as server
        server_ip, server_port = lines[1].strip().split(",")

        # Client is assigned as first line
        client_ip, client_port = lines[0].strip().split(",")

        return server_ip, int(server_port), client_ip, int(client_port)
    

def main():
    server_ip, server_port, client_ip, client_port = read_config_file()
    print(f"Server IP: {server_ip}, Server Port: {server_port}")
    print(f"Client IP: {client_ip}, Client Port: {client_port}")

    # identify socket to connect to
    clientSocket = socket(AF_INET, SOCK_STREAM)

    # wait a bit for server to come online
    sleep(1)

    # establish connection with server
    clientSocket.connect((server_ip, server_port))

    while True:
        
        

        # send something
        #sentence = "this message was encoded" 
        sentence = input("Input lowercase Sentence as message (use): ")
        
        clientSocket.send(sentence.encode())

        modifiedSentence = clientSocket.recv(1024)
        print("From Server: ", modifiedSentence.decode())

        # terminate connection from client side
        # if we type quit, we shouldn't send anything to server -- this is why we placed this here
        # for now, we actually want client to send 'quit' to server to let it know to terminate connection
        if sentence == "quit":
            print("terminating client connection...")
            clientSocket.close()
            break

main()