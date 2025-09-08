# Assignment says we need to use threading to run both client and server in one process
# so this combines client.py and server.py that we had before

# this is the message/connection flow: 
# [client1 --> server2 --> client2 --> server3 --> client3 --> server1 --> client1]
# clientN & serverN are two parts of the same node N (sharing the same process & uuid)
# defined in two threads, one functions as receiver, the other as sender.


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
    
# shared state class for client & server thread
# i.e. shared data like: uuid
class NodeState:
    def __init__(self):
        self.local_node_uuid = uuid.uuid4() # generate uuid for this node
        self.leader_elected = False   # flag to indicate if leader elected

        self.current_message = None 

class Message:

    # message thread is initalized with ID
    def __init__(self, received_uuid=None, flag=0):
        super().__init__()
        self.received_uuid = received_uuid or uuid.uuid4() # received from sender (client)
        self.flag = flag # flag to indicate if leader elected

    # json format
    def msg_to_json(self):
        return json.dumps({'received_uuid': str(self.received_uuid), 'flag': self.flag}) + "\n"
    
    # json -> object
    @staticmethod
    def json_to_msg(data):
        msgDict = json.loads(data)
        received_uuid = uuid.UUID(msgDict['received_uuid'])

        return Message(received_uuid, msgDict['flag'])
    

'''    def run(self):
        print(f"Message from {self.received_uuid} \n")
        time.sleep(5)'''


# function to read config.txt for server IP and PORT
def read_config_file():
    with open("config.txt", "r") as file:
        lines = file.readlines()

        # Assigned second line as server
        server_ip, server_port = lines[1].strip().split(",")

        # Client is assigned as first line
        client_ip, client_port = lines[0].strip().split(",")

        return server_ip, int(server_port), client_ip, int(client_port)
    
# the receiver
# server() takes server_port, and sharedState object (data class)
def server(server_ip, server_port, sharedState):
    print("I am the Server---------- This is my ID:")

    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', server_port))  # port server is using
    serverSocket.listen(1)                # server is listening

    print("The server is ready to receive")

    # accepting connection needs to be external to while loop -- otherwise it gets stuck after first request is served
    # "if someone connects to the port im listening on, ill accept"
    connectionSocket, addr = serverSocket.accept() 

    while True:
        # receive message from incoming connection
        sentence = connectionSocket.recv(1024).decode()
        
        # convert to message object
        message = Message.json_to_msg(data=sentence)

        print(f"Received from uuid: {message.received_uuid} with leader elected: {message.flag}")

        # server() should only be responsible for updating the shared NodeState
        #      based on what message they received.
        # case: leader already elected - would never reach us
        # case: we are the leader - UUID has returned back to us
        if message.received_uuid == sharedState.local_node_uuid:
            # print final message, and close connection
            print("Leader already elected: ", message.received_uuid)
            log_message("Received", message, "same", "1", sharedState.local_node_uuid)
            #connectionSocket.send(Message(message.received_uuid, flag=1).msg_to_json().encode())
            
            # uuid remains same
            message.flag = 1
            log_message("Sent", message, "", 1)

            # update flags - indicating leader elected
            sharedState.leader_elected = True
            sharedState.current_message = message

            # close connection with client
            connectionSocket.close()
            break
        
        # case: our node uuid < received uuid
        # just pass message along (we're not the leader)
        elif message.received_uuid > sharedState.local_node_uuid:
            print(f"Forwarding message along: {message.received_uuid}")
            
            log_message("Received", message, "greater", "0")
            #connectionSocket.send(message.msg_to_json().encode())
            # higher uuid wins, we don't modify message object
            log_message("Sent", message, "", 0)

        # case: our node uuid > received uuid
        # we are a better candidate for leader, modify message
        else: # message.received_uuid < sharedState.local_node_uuid:
            print(f"Modifying message to our uuid: {sharedState.local_node_uuid}")

            log_message("Received", message, "less", "0")
            #connectionSocket.send(Message(sharedState.local_node_uuid, flag=0).msg_to_json().encode())
            # update message object with our uuid
            message.received_uuid = sharedState.local_node_uuid
            message.flag = 0

            sharedState.current_message = message

            log_message("Sent", message, "", 0)

# functions as transmitter for the (client, server) node
# it passes along whatever the server logic decided was the msg
def client(client_ip, client_port, sharedState):

    print("I am the Client---------- This is my ID:", sharedState.local_node_uuid)

    # pull message from shared state
    message = sharedState.current_message

    # identify socket to connect to
    clientSocket = socket(AF_INET, SOCK_STREAM)

    # wait a bit for server to come online
    time.sleep(1)

    # establish connection with external server (external node)
    clientSocket.connect((client_ip, client_port))

    while True:

        log_message("Sent", message, "", message.flag)

        # client sends a message to external server
        clientSocket.send(message.msg_to_json().encode())
        print(f"Sent message with uuid: {message.received_uuid} and flag: {message.flag}")

        # client expects external server response -- asynch ring doesnt want this
        # response = clientSocket.recv(1024)

        print(f"Received message with uuid: {message.received_uuid}, flag: {message.flag}")

        # Log received message
        # now we evaluate the message we sent out (do we need to close connection?)
        # leader was elected already (told by our own local server thread)
        if message.flag == 1:
            log_message("Received", message, "same", "1", message.received_uuid)
            print(f"Leader is {message.received_uuid}")
            log_message("Leader", message, "", "", message.received_uuid)
            break  # Exit the loop when leader is elected
        #else:
        #    continue looping

    clientSocket.close()


def main():

    # server() only receives message and updates shared message state
    # client() only sends message based on shared message state
    
    server_ip, server_port, client_ip, client_port = read_config_file()
    print(f"Server IP: {server_ip}, Server Port: {server_port}") # this is us
    print(f"Client IP: {client_ip}, Client Port: {client_port}") # this is external node

    sharedState = NodeState()

    # Start server and client threads for Node 1, Node 2, and Node 3
    server_thread = threading.Thread(target=server, args=(server_ip, server_port, sharedState))
    client_thread = threading.Thread(target=client, args=(client_ip, client_port, sharedState))

    # Start the threads
    server_thread.start()
    client_thread.start()

    # Wait for all threads to finish
    server_thread.join()
    client_thread.join()


if __name__ == "__main__":
    main()