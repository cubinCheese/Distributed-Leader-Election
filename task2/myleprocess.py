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
import os
import argparse


# This function sets up the log file for a particular node
def setup_log_for_node(node_number):
    log_filename = f'node_{node_number}_log.txt'

    # Delete the log file if it exists (clears the file)
    if os.path.isfile(log_filename):
        os.remove(log_filename)

    logging.basicConfig(filename=log_filename, level=logging.INFO, filemode='w')
    

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
# first line - my self (listening on port), second / third line - peers to connect to
def read_config_file(node_number):
    filename = f"config{node_number}.txt"
    with open(filename, "r") as file:
        lines = file.readlines()

        # Assigned first line as server
        server_ip, server_port = lines[0].strip().split(",")

        # Client is assigned as second line
        client_ip, client_port = lines[1].strip().split(",")

        # If there's a third line, it's an additional peer (for 'x' node)
        if len(lines) > 2:
            peer_client_ip, peer_client_port = lines[2].strip().split(",")
            return server_ip, int(server_port), client_ip, int(client_port), peer_client_ip, int(peer_client_port)
        
        # otherwise, we just return the standard two lines (for 'n' and 'y' nodes)
        return server_ip, int(server_port), client_ip, int(client_port)
def old_read_config_file():
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

        self.seen_own_uuid_count = 0        # number of times we've seen our own UUID
        # this is important because in a double ring, the outer ring's UUID will return to itself
        # before the inner ring can send its own UUID up to the outer ring node. (hence a lower UUID can beat a higher UUID due to delay)

        # this here is deprecated -- we now support multiple connections
        # client needs to make first connection
        # server needs to send subsequent messages to that socket
        #self.clientSocket = None  # client socket needs to be accessible to both functions since
        self.clientSockets = []


        # add list of peer nodes - for client connection
        self.peers = [] # list of (ip, port) tuples for peer nodes
        self.lock = threading.Lock()  # Add this line

    # function to add peer nodes to the list (that client needs to connect to)
    def add_peer(self, ip, port):
        self.peers.append((ip, port))

    # modified - now supports one or multiple connections
    # the receiver
    # server() takes server_port, and sharedState object (data class)
    def server(self, server_ip, server_port):
        print("I am the Server---------- This is my ID:", self.local_node_uuid)

        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.bind((server_ip, server_port))  # port server is using
        serverSocket.listen(5)                       # server is listening

        print("The server is ready to receive")
            
        # function to handle each client connection in a separate thread
        # separated out our original server logic to handle each connection
        def handle_client_connection(connectionSocket): # reads in current connection socket
            while True:
                print("Waiting to receive data...")
                # receive message from incoming connection
                sentence = connectionSocket.recv(1024).decode()
                print(f"Raw received: {sentence}")
                if not sentence:
                    break  # no empty strings
                # convert to message object - split by newline to handle stream of messages
                for msg_str in sentence.strip().split('\n'):
                    if msg_str:
                        message = Message.json_to_msg(data=msg_str)
                        print(f"[Node {self.local_node_uuid}] Received message: uuid={message.received_uuid}, flag={message.flag}")
                        self.leader_election_logic(message) # call leader election process

                        # If leader is elected, close connection and break
                        if self.leader_flag:
                            connectionSocket.close()
                            return
            connectionSocket.close()

        while True:
            # accept connection until leader is elected
            connectionSocket, addr = serverSocket.accept() 

            # spawn a new thread to handle each client connection
            threading.Thread(target=handle_client_connection, args=(connectionSocket,), daemon=True).start()

    # function that handles the leader election logic
    # based on the message received, it decides whether to forward, modify, or stop forwarding
    def leader_election_logic(self, message: Message=None):
        if self.leader_flag:
            log_message("Ignored", message, "", "")
            return  # if leader already elected, ignore further messages
        
        outgoing_socket = self.clientSockets[0] 

        if outgoing_socket is None:
            print("Error: destination_clientSocket is None in leader_election_logic")
            return
        
        # prevent race condition - due to multiple server() threads
        with self.lock:
            # case: we are the leader - UUID has returned back to us
            if message.flag == 0:
                if message.received_uuid == self.local_node_uuid: # leader election only happens if this occurs twice.
                    self.seen_own_uuid_count += 1
                    if self.seen_own_uuid_count == 2:
                        # None -> leader uuid initalized
                        print("Second time seeing own UUID. Declaring self as leader:", self.local_node_uuid)
                        log_message("Leader", message, "equal", "", self.local_node_uuid)
                        self.leader_uuid = self.local_node_uuid # we are the leader
                        self.leader_flag = True
                        self.send_node_message(Message(self.local_node_uuid, flag=1), outgoing_socket)     # send updated message
                    elif self.seen_own_uuid_count < 2:
                        # we've seen our own UUID once already, but we can drop it
                        log_message("Incoming UUID == Local UUID: Seen Once Before.Dropping Message", message, "", "")
                        return

                # case: our node uuid < received uuid
                # just pass message along (we're not the leader)
                elif self.local_node_uuid < message.received_uuid:
                    #print(f"(unmodified) Forwarding message along: {message.received_uuid}, with leader: {message.flag}")
                    log_message("Received", message, "greater", "Not Leader")
                    self.send_node_message(message, outgoing_socket)     # send unmodified message

                # case: our node uuid > received uuid
                # we are a better candidate for leader, modify message
                else: # message.received_uuid < self.local_node_uuid:
                    #print(f"Modifying message to our uuid: {self.local_node_uuid}, with leader: 0")
                    log_message("Received", message, "less", "Not Leader")
                    self.leader_flag = False
                    self.send_node_message(Message(received_uuid=self.local_node_uuid, flag=0), outgoing_socket)     # send updated message

            # we just received the final Leader Message that was broadcasted
            elif message.flag == 1:
                if message.received_uuid == self.local_node_uuid:
                    self.leader_flag = True
                    self.leader_uuid = message.received_uuid
                    #print("Leader elected:", self.leader_uuid, "flag: ", message.flag)
                    log_message("Leader", message, "", "", self.leader_uuid)
                    return  # election complete, stop forwarding
                else:
                    log_message("Received", message, "", "Leader Elected")
                    self.leader_uuid = message.received_uuid
                    self.leader_flag = True
                    self.send_node_message(message, outgoing_socket)
                    # After forwarding, stop processing further messages
                    return

    

    # MODIFIED FOR TASK2 - Accomdating multiple connections
    # functions as transmitter for the (client, server) node
    # it passes along whatever the server logic decided was the msg
    def client(self, is_x_node=False):

        # UNMODIFIED original client() implementation from task1
        # function that handles one client connection
        def core_client_logic(ip, port):
            curr_clientSocket = socket(AF_INET, SOCK_STREAM)
            time.sleep(5)
            connectionEstablished = False
            while not connectionEstablished:
                try:
                    curr_clientSocket.connect((ip, port))
                    connectionEstablished = True
                except ConnectionRefusedError:
                    print(f"Connection refused, retrying... {ip}:{port}")
                    time.sleep(1)

            # store outgoing socket for forwarding
            self.clientSockets.append(curr_clientSocket)

            # After successfully connecting to a peer, send message
            if is_x_node:
                message = Message(received_uuid=self.local_node_uuid, flag=0)
                self.send_node_message(message, curr_clientSocket)
                log_message("Sent", message, "", "")

            # Persistent loop for 'x' node to connect to both peers
            while True:
                data = curr_clientSocket.recv(1024).decode()
                if not data:
                    break
                for msg_str in data.strip().split('\n'):
                    if msg_str:
                        message = Message.json_to_msg(msg_str)
                        print(f"[Client Node {self.local_node_uuid}] Received message: uuid={message.received_uuid}, flag={message.flag}")
                        self.leader_election_logic(message)
                        # If leader is elected, close connection and break
                        if self.leader_flag:
                            curr_clientSocket.close()
                            return
            curr_clientSocket.close()


        # 'x' node has two connections to make - spawns two threads to handle
        if is_x_node:
            print(self.peers, "this is peers list")
            threads = []
            for (ip, port) in self.peers:
                print(f"I am the Client---------- This is my ID: {self.local_node_uuid}")
                print(f"Node {self.local_node_uuid} is the Client. Connecting to {ip}:{port}")
                t = threading.Thread(target=core_client_logic, args=(ip, port)) # or i can do one after the after.
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
        # otherwise we just stick to original client logic - single connection
        else:
            client_ip, client_port = self.peers[0]
            core_client_logic(client_ip, client_port)

    # will not modify -- because we'd have to call close() which erases persistent
    # Helper function to send messages
    # Initalize first message in chain of election process (start of node chain)
    # Send subsequent messages in chain of election process
    def send_node_message(self, message: Message, current_Socket=None):
        try:
            current_Socket.sendall(message.msg_to_json().encode()) # sendall is more reliable
        except Exception as e:
            log_message("ClientSocket send error:", message, "", "", e)
    # server() also needs access to clientSocket to send messages


def main():

    parser = argparse.ArgumentParser(description='Start the node process')
    parser.add_argument('node_type', choices=['x', 'y', 'n'], help='Node type: x, y, or n')
    parser.add_argument('node_number', type=int, choices=range(1, 6), help='Node number (1 to 5)')
    args = parser.parse_args()

    # Setup log file for the specific node
    setup_log_for_node(args.node_number)

    # Read configuration from the respective config file
    config_values = read_config_file(args.node_number)

    # Unpack config values
    if len(config_values) == 4:
        server_ip, server_port, client_ip, client_port = config_values
        additional_client_ip, additional_client_port = None, None
    elif len(config_values) == 6:
        server_ip, server_port, client_ip, client_port, additional_client_ip, additional_client_port = config_values

    print(f"Node {args.node_number} ({args.node_type}) Configuration:")
    print(f"  Server IP: {server_ip}, Server Port: {server_port}")
    print(f"  Client IP: {client_ip}, Client Port: {client_port}")
    if additional_client_ip:
        print(f"  Additional Peer IP: {additional_client_ip}, Port: {additional_client_port}")

    # Create shared state for this node
    sharedState = NodeState()

    # Add outgoing peers to the client peer list
    sharedState.add_peer(client_ip, client_port)
    if additional_client_ip:
        sharedState.add_peer(additional_client_ip, additional_client_port)

    # Start the server thread (always runs)
    server_thread = threading.Thread(target=sharedState.server, args=(server_ip, server_port))
    server_thread.start()

    # In main(), after starting server_thread:

    time.sleep(20)
    
    
    # All nodes initiate the election (send their own UUID)
    #input("\n[Press Enter to start the leader election on this node...]\n")
    if args.node_type == 'x':
        # marked as initiator node (only if it is the x node)
        client_thread = threading.Thread(target=sharedState.client, args=(True,))
    else:
        client_thread = threading.Thread(target=sharedState.client, args=(False,))
    client_thread.start()
    client_thread.join()
    
    '''
    # Only certain node types initiate the client (to start the election)
    if args.node_type in ['x', 'n', 'y']:
        #input("\n[Press Enter to start the leader election on this node...]\n")
        time.sleep(30)  # Give server a moment to start
        client_thread = threading.Thread(target=sharedState.client, args=(args.node_type == 'x',))
        client_thread.start()
        client_thread.join()  # Wait for the client to finish sendin
    '''

    # Wait for server thread (keeps running)
    server_thread.join()

if __name__ == "__main__":
    main()