# Assignment says we need to use threading to run both client and server in one process
# so this combines client.py and server.py that we had before

import threading
import time
import uuid
from socket import *
import json
import logging

# Function to log messages received and sent
def log_message(message_type, msg, comparison, state, leader_id=None):
    if message_type == "Received":
        logging.info(f"Received: uuid={msg.received_uuid}, flag={msg.flag}, {comparison}, {state}")
    elif message_type == "Sent":
        logging.info(f"Sent: uuid={msg.received_uuid}, flag={msg.flag}")
    elif message_type == "Ignored":
        logging.info(f"Ignored: uuid={msg.received_uuid}")
    elif message_type == "Leader":
        logging.info(f"Leader is decided to {leader_id}")
    

class Message:

    # message thread is initalized with ID
    def __init__(self, received_uuid=None, flag=0):
        super().__init__()
        self.received_uuid = received_uuid or str(uuid.uuid4())# received from sender (client)
        self.flag = flag # flag to indicate if leader elected

    # json format
    def msg_to_json(self):
        return json.dumps(self.__dict__) + "\n"
    
    # json -> object
    @staticmethod
    def json_to_msg(data):
        msgDict = json.loads(data)
        return Message(msgDict['received_uuid'], msgDict['flag'])
    

    def run(self):
        print(f"Message from {self.received_uuid} \n")
        time.sleep(5)


# function to read config.txt for server IP and PORT
def read_config_file():
    with open("config.txt", "r") as file:
        lines = file.readlines()

        # Assigned second line as server
        server_ip, server_port = lines[1].strip().split(",")

        # Client is assigned as first line
        client_ip, client_port = lines[0].strip().split(",")

        return server_ip, int(server_port), client_ip, int(client_port)
    

def server():
    print("I am the Server----------")
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
        
        message = Message.json_to_msg(data=sentence)
        print(f"Received from uuid: {message.received_uuid} with leader elected: {message.flag}")

        # case: leader already elected - would never reach us

        # case: we are the leader - UUID has returned back to us
        if message.received_uuid == node_uuid:
            # print final message, and close connection
            print("Leader already elected: ", message.received_uuid)
            log_message("Received", message, "same", "1", node_uuid)
            connectionSocket.send(Message(message.received_uuid, flag=1).msg_to_json().encode())
            log_message("Sent", message, "", 1)
            connectionSocket.close()
            break
        
        # case: our server uuid < received uuid
        # just pass message along (we're not the leader)
        elif message.received_uuid > node_uuid:
            print(f"Forwarding message along: {message.received_uuid}")
            
            log_message("Received", message, "greater", "0")
            connectionSocket.send(message.msg_to_json().encode())
            log_message("Sent", message, "", 0)

        # case: our server uuid > received uuid
        # we are a better candidate for leader, modify message
        else: # message.received_uuid < node_uuid:
            print(f"Modifying message to our uuid: {node_uuid}")

            log_message("Received", message, "less", "0")
            connectionSocket.send(Message(node_uuid, flag=0).msg_to_json().encode())
            log_message("Sent", message, "", 0)

def client():
    print("I am the Client----------")
    server_ip, server_port, client_ip, client_port = read_config_file()
    print(f"Server IP: {server_ip}, Server Port: {server_port}")
    print(f"Client IP: {client_ip}, Client Port: {client_port}")

    # generate uuid
    node_uuid = uuid.uuid4().hex

    # identify socket to connect to
    clientSocket = socket(AF_INET, SOCK_STREAM)

    # wait a bit for server to come online
    time.sleep(1)

    # establish connection with server
    clientSocket.connect((server_ip, server_port))

    while True:
            
        # create message obj with our own uuid
        message = Message(received_uuid=node_uuid)

        log_message("Sent", message, "", 0)

        clientSocket.send(message.msg_to_json().encode())
        print(f"Sent message with uuid: {message.received_uuid} and flag: {message.flag}")

        # server response
        response = clientSocket.recv(1024)
        print("From Server: ", response.decode())
        if response:
            msg = Message.json_to_msg(response)
            print(f"Received message with uuid: {msg.received_uuid}, flag: {msg.flag}")

            # Log received message
            if msg.flag == 1:
                log_message("Received", msg, "same", "1", msg.received_uuid)
                print(f"Leader is {msg.received_uuid}")
                log_message("Leader", msg, "", "", msg.received_uuid)
                break  # Exit the loop when leader is elected

            # Otherwise, forward the message
            time.sleep(1)

    clientSocket.close()


def main():
    # Start server and client threads for Node 1, Node 2, and Node 3
    server_thread_1 = threading.Thread(target=server)
    client_thread_1 = threading.Thread(target=client)

    server_thread_2 = threading.Thread(target=server)
    client_thread_2 = threading.Thread(target=client)

    server_thread_3 = threading.Thread(target=server)
    client_thread_3 = threading.Thread(target=client)

    # Start the threads
    server_thread_1.start()
    client_thread_1.start()

    server_thread_2.start()
    client_thread_2.start()

    server_thread_3.start()
    client_thread_3.start()

    # Wait for all threads to finish
    server_thread_1.join()
    client_thread_1.join()

    server_thread_2.join()
    client_thread_2.join()

    server_thread_3.join()
    client_thread_3.join()


if __name__ == "__main__":
    main()