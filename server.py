from socket import *

# function to read config.txt for server IP and PORT
def read_config_file():
    with open("config.txt", "r") as file:
        lines = file.readlines()

        # Assigned second line as server
        server_ip, server_port = lines[1].strip().split(",")

        # Client is assigned as first line
        client_ip, client_port = lines[0].strip().split(",")

        return server_ip, int(server_port), client_ip, int(client_port)
    
def main():
    server_ip, serverPort, client_ip, client_port = read_config_file()
    print(f"Server IP: {server_ip}, Server Port: {serverPort}")
    print(f"Client IP: {client_ip}, Client Port: {client_port}")


    #serverPort = 5002
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)
    print("The server is ready to receive")

    while True:
        connectionSocket, addr = serverSocket.accept()

        sentence = connectionSocket.recv(1024).decode()
        capSentence = sentence.upper() + " -signed by server"
        connectionSocket.send(capSentence.encode())

        # terminate connection from server side -- based on client input
        if sentence == "quit":
            print("terminating server connection...")
            connectionSocket.close()
            break

main()