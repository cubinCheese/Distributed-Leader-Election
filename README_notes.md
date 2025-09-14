TODO: Setup a node that acts as server/client

# using localhost for now (127.0.0.1) will need to replace that line when testing in class.
# or 172.17.164.20\20 ? via "ip a" under eth0

for now placed 
"172.17.164.20,5001
172.17.164.20,5002" as client and server ip with separate ports

# utilized example from class on client/server py
# adjusted both to read IP/PORT number from config.txt

# server and client will have access to eachother's identifiers immediately 
#    server won't have to wait for client to connect before saving their ip/port


Currently
(to quit) client will type "quit" 
    - triggers client to close connection
    - sends to server, triggering server to close connection too


Server1 talks to Client1, client1 transmits to clientN...
#
# server runs (process 1) --> server runs (process 2 on other terminal) --> input() on first terminal --> input on second terminal 

# recall: server thread is supposed to handle logic for leader election.