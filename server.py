from socket import *
import uuid

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

    # generate uuid for this server node
    node_uuid = uuid.uuid4().hex

    #serverPort = 5002
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)
    print("The server is ready to receive")

    # accepting connection needs to be external to while loop -- otherwise it gets stuck after first request is served
    connectionSocket, addr = serverSocket.accept()

    while True:
        sentence = connectionSocket.recv(1024).decode()
        capSentence = sentence.upper() + " -signed by server"
        connectionSocket.send(capSentence.encode())

        # accept client connection + client uuid
        # check if uuid is larger than our (own node uuid): 
        # note.. check what to reply with in (wiki) of algorithm
        
        '''
        if sentence == node_uuid: # if same uuid has returned via message, leader elected
            print("Leader Elected: ", sentence) # change "sentence" to uuid in message
            connectionSocket.close()
            break
        elif sentence > node_uuid:
            # we need to pass message along - to next node
            connectionSocket.send(sentence.encode())
            # seems like we need 2 threads -- one to maintain connection to left node, one to right node.
            # should outline design again before continuing implementation

        '''
        # terminate connection from server side -- based on client input
        if sentence == "quit":
            print("terminating server connection...")
            connectionSocket.close()
            break

main()