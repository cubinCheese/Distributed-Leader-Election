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
