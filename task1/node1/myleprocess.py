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
'''
@param message_type: "Received" or "Sent"
@param msg: Message object
@param comparison: "greater", "less", or "" (for leader messages)
    # message.uuid was greater/less than/equal to local uuid
@param state: "Not Leader", "Leader Elected", or "" (for leader messages)
@param leader_id: UUID of the elected leader (for leader messages)
'''
def log_message(message_type, msg, comparison, state, leader_id=None):
    if message_type == "Received":
        print(f"Received: uuid={msg.received_uuid}, flag={msg.flag}, {comparison}, {state}")
        logging.info(f"Received: uuid={msg.received_uuid}, flag={msg.flag}, {comparison}, {state}")
    elif message_type == "Sent":
        print(f"Sent: uuid={msg.received_uuid}, flag={msg.flag}")
        logging.info(f"Sent: uuid={msg.received_uuid}, flag={msg.flag}")
    elif message_type == "Ignored":
        print(f"Ignored: uuid={msg.received_uuid}")
        logging.info(f"Ignored: uuid={msg.received_uuid}")
    elif message_type == "Leader":
        print(f"Leader is decided to {leader_id}")
        logging.info(f"Leader is decided to {leader_id}")
    

# message class to hold incoming message data
class Message:

    # message thread is initalized with ID
    def __init__(self, received_uuid=None, flag=0):
        super().__init__()
        self.received_uuid = received_uuid # received from sender (client)
        self.flag          = flag          # flag to indicate if leader elected

    # function that converts message object -> json string
    def msg_to_json(self):
        return json.dumps({'received_uuid': str(self.received_uuid), 'flag': self.flag}) + "\n"
    
    # function that converts json string -> message object
    @staticmethod
    def json_to_msg(data):
        msgDict = json.loads(data)
        received_uuid = uuid.UUID(msgDict['received_uuid'])

        return Message(received_uuid, msgDict['flag'])


# function to read config.txt to retrieve (server & client) IP and PORT numbers
def read_config_file():
    with open("config.txt", "r") as file:
        lines = file.readlines()

        # Assigned first line as server
        server_ip, server_port = lines[0].strip().split(",")

        # Client is assigned as second line
        client_ip, client_port = lines[1].strip().split(",")

        return server_ip, int(server_port), client_ip, int(client_port)


# Shared state class for client & server thread
# Note. client is the initiator of the election process (first transmission) (transmitter)
#       server is the receiver of the election process (first reception) (receiver & subseq comms transmitter)
#       
class NodeState:
    def __init__(self):
        self.local_node_uuid = uuid.uuid4() # generate uuid for current process node
        self.leader_uuid = None             # elected leader uuid
        self.leader_flag = False            # election flag

        # client needs to make first connection
        # server needs to send subsequent messages to that socket
        self.clientSocket = None  # client socket needs to be accessible to both functions since

        #self.current_message = None  # initalize message variable to hold message object (of Message class)

    # the receiver
    # server() takes server_port, and sharedState object (data class)
    def server(self, server_ip, server_port):
        print("I am the Server---------- This is my ID:", self.local_node_uuid)

        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.bind((server_ip, server_port))  # port server is using
        serverSocket.listen(1)                       # server is listening

        print("The server is ready to receive")

        while True:
            # accept connection until leader is elected
            connectionSocket, addr = serverSocket.accept() 
            #print("I just connected to: ", addr, connectionSocket)

            while True:
                # receive message from incoming connection
                sentence = connectionSocket.recv(1024).decode()
                if not sentence:
                    break  # no empty strings

                # convert to message object - split by newline to handle stream of messages
                for msg_str in sentence.strip().split('\n'):
                    if msg_str:
                        message = Message.json_to_msg(data=msg_str)
                        
                        '''
                        print("Received:", message.received_uuid, type(message.received_uuid))
                        print("Local:", self.local_node_uuid, type(self.local_node_uuid))
                        print("Equal?", message.received_uuid == self.local_node_uuid)
                        print("Flag:", message.flag, type(message.flag))
                        '''

                        self.leader_election_logic(message) # call leader election process
            connectionSocket.close()

    # function that handles the leader election logic
    # based on the message received, it decides whether to forward, modify, or stop forwarding
    def leader_election_logic(self, message: Message):

        # case: we are the leader - UUID has returned back to us
        if message.flag == 0:
            if message.received_uuid == self.local_node_uuid:
                # None -> leader uuid initalized
                log_message("Leader", message, "equal", "", self.local_node_uuid)
                self.leader_uuid = self.local_node_uuid # we are the leader
                self.leader_flag = True
                self.send_node_message(Message(message.received_uuid, flag=1))     # send updated message

            # case: our node uuid < received uuid
            # just pass message along (we're not the leader)
            elif self.local_node_uuid < message.received_uuid:
                #print(f"(unmodified) Forwarding message along: {message.received_uuid}, with leader: {message.flag}")
                log_message("Received", message, "greater", "Not Leader")
                self.send_node_message(message)     # send unmodified message

            # case: our node uuid > received uuid
            # we are a better candidate for leader, modify message
            else: # message.received_uuid < self.local_node_uuid:
                #print(f"Modifying message to our uuid: {self.local_node_uuid}, with leader: 0")
                log_message("Received", message, "less", "Not Leader")
                self.leader_flag = False
                self.send_node_message(Message(received_uuid=self.local_node_uuid, flag=0))     # send updated message

        # we just received the final Leader Message that was broadcasted
        elif message.flag == 1:
            if message.received_uuid == self.local_node_uuid:
                self.leader_flag = True
                self.leader_uuid = message.received_uuid
                #print("Leader elected:", self.leader_uuid, "flag: ", message.flag)
                log_message("Leader", message, "", "", self.leader_uuid)
                return  # election complete, stop forwarding
            else:
                #print(f"Forwarding leader message along: {message.received_uuid}, with leader: {message.flag}")
                log_message("Received", message, "", "Leader Elected")
                self.send_node_message(message)     # send unmodified message
    


    # functions as transmitter for the (client, server) node
    # it passes along whatever the server logic decided was the msg
    def client(self, client_ip, client_port):

        print("I am the Client---------- This is my ID:", self.local_node_uuid)

        # identify socket to connect to
        self.clientSocket = socket(AF_INET, SOCK_STREAM)

        # wait a bit for server to come online
        time.sleep(5)

        # establish connection with external server (external node)
        # keep trying until successful
        connectionEstablished = False
        while not connectionEstablished:
            try:
                self.clientSocket.connect((client_ip, client_port))
                connectionEstablished = True
            except ConnectionRefusedError:
                print("Connection refused, retrying...")
                time.sleep(1)  # Wait before retrying
        # process blocked until connection made...

        # Initalize first message in chain of election process (start of node chain)
        message = Message(received_uuid=self.local_node_uuid, flag=0)

        # call helper function to send message
        self.send_node_message(message)

        # log first message sent
        log_message("Sent", message, "", "")

    # Helper function to send messages
    # Initalize first message in chain of election process (start of node chain)
    # Send subsequent messages in chain of election process
    def send_node_message(self, message: Message):
        try:
            self.clientSocket.sendall(message.msg_to_json().encode()) # sendall is more reliable
        except Exception as e:
            log_message("ClientSocket send error:", message, "", "", e)
    
    # server() also needs access to clientSocket to send messages


def main():

    # rewrite new log.txt file on each process run
    logging.basicConfig(filename='log.txt', level=logging.INFO, filemode='w')

    # server() only receives message and updates shared message state (but now also sends followup leader related messages)
    # client() only sends initial message to initaite leader election, and establishes first connection
    
    server_ip, server_port, client_ip, client_port = read_config_file()
    print(f"Server IP: {server_ip}, Server Port: {server_port}") # this is us
    print(f"Client IP: {client_ip}, Client Port: {client_port}") # this is external node

    sharedState = NodeState()

    # Start server and client threads for Node 1, Node 2, and Node 3
    server_thread = threading.Thread(target=sharedState.server, args=(server_ip, server_port))
    client_thread = threading.Thread(target=sharedState.client, args=(client_ip, client_port))

    # Start the threads
    server_thread.start()
    input()
    client_thread.start()

    # Wait for all threads to finish
    server_thread.join()
    client_thread.join()


if __name__ == "__main__":
    main()