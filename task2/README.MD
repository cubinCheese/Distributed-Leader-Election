# Task 2: Distributed Leader Election

## Overview

This project implements a distributed leader election algorithm for a partial double ring topology using Python and threading.

- **`myleprocess.py`**: Main implementation for Task 2.
- **Makefile**: Provides convenient commands for running and testing nodes.
- **Config files**: `config<number>.txt` (1–5) — Each node’s IP address and port configuration.
- **Log files**: `node_<number>_log.txt` (1–5) — Each node’s activity log.

---

## How to Run

### 1. Launch Nodes

Open **five terminals**, one for each node.

### 2. Start Each Node

Run the following command in each terminal, replacing `<node_type>` and `<number>` as appropriate:

```sh
python3 myleprocess.py <node_type> <number>
```

- `<node_type>`: `x`, `y`, or `n` (node type)
- `<number>`: `1`, `2`, `3`, `4`, or `5` (corresponds to config and log file)

> **Note:**  
> - `<number>` selects the config file (`config<number>.txt`) and log file (`node_<number>_log.txt`) for that node.
> - `<node_type>` must match the node type described in the config file.

### 3. Initiate Leader Election

Choose **one node** to act as the initiator.  
- On that node’s terminal, **press [Enter]** when prompted:
  ```
  Press [Enter] to initiate the election on this node, or type 'no' to skip:
  ```
- **Do not press Enter** on other nodes; just leave them running.
- **YOU MUST WAIT UNTIL YOU SEE THIS PROMPT** on all processes (terminals) before you utilizing it to start leader election in any chosen node. (this indicates that all client connections are ready to elect a leader)

> If you type anything other than Enter (e.g., `no`), the node will skip initiating the election.

---

## Example Topology

Suppose you want node 1 to be an x-type node:

```sh
python3 myleprocess.py x 1        # Node 1 (x-type, uses config1.txt)
python3 myleprocess.py n 2        # Node 2 (n-type, uses config2.txt)
python3 myleprocess.py n 3        # Node 3 (n-type, uses config3.txt)
python3 myleprocess.py n 4        # Node 4 (n-type, uses config4.txt)
python3 myleprocess.py y 5        # Node 5 (y-type, uses config5.txt)
```

---

## Using the Makefile

You can use the Makefile to run nodes more easily:

- `make run` — Runs the generic command (`python3 myleprocess.py`)

These are presets, to be run on each individual terminal.
- `make test1` — Runs node 1 as x-type
- `make test2` — Runs node 2 as n-type
- `make test3` — Runs node 3 as n-type
- `make test4` — Runs node 4 as n-type
- `make test5` — Runs node 5 as y-type

---

## Log Files

- Each run generates new log files for each node.
- Old logs are deleted before each run.
- Logs are written to `node_<number>_log.txt` in the working directory.

---

## Notes

- Ensure each node’s config file matches its intended type and number.
- Only one node should initiate the election per run.
- For troubleshooting, check the log files for each node.

---

## SAMPLE OUTPUT

- After running `python3 myleprocess.py [node_type] [number]` you will receive...
- Below are dropdown menus with sample outputs

<details>
  <summary>Node 1 (which was selected as x)</summary>

```
python3 myleprocess.py x 1
Node 1 (x) Configuration:
  Server IP: 127.0.0.1, Server Port: 5001
  Client IP: 127.0.0.1, Client Port: 5002
  Additional Peer IP: 127.0.0.1, Port: 5003
I am the Server---------- This is my ID: 6dd5026c-2c96-43bf-bb22-b86d552f6f39
The server is ready to receive
current x node ip/port: 127.0.0.1 5002
current x node ip/port: 127.0.0.1 5003
Press [Enter] to initiate the election on this node, or type 'no' to skip: Waiting to receive data...

Sent: uuid=6dd5026c-2c96-43bf-bb22-b86d552f6f39, flag=0
Sent: uuid=6dd5026c-2c96-43bf-bb22-b86d552f6f39, flag=0
Sent: uuid=6dd5026c-2c96-43bf-bb22-b86d552f6f39, flag=0
Sent: uuid=6dd5026c-2c96-43bf-bb22-b86d552f6f39, flag=0
Raw received: {"received_uuid": "6dd5026c-2c96-43bf-bb22-b86d552f6f39", "flag": 0}

[Node 6dd5026c-2c96-43bf-bb22-b86d552f6f39] Received message: uuid=6dd5026c-2c96-43bf-bb22-b86d552f6f39, flag=0
Waiting to receive data...
Raw received: {"received_uuid": "d1bdafd6-b54c-4606-8317-deaccc97a211", "flag": 0}

[Node 6dd5026c-2c96-43bf-bb22-b86d552f6f39] Received message: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0
Received: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0, greater, Not Leader
Sent: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0
Sent: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0
Waiting to receive data...
Raw received: {"received_uuid": "d1bdafd6-b54c-4606-8317-deaccc97a211", "flag": 0}

[Node 6dd5026c-2c96-43bf-bb22-b86d552f6f39] Received message: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0
Received: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0, greater, Not Leader
Sent: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0
Sent: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0
Waiting to receive data...
Raw received: {"received_uuid": "d1bdafd6-b54c-4606-8317-deaccc97a211", "flag": 0}

[Node 6dd5026c-2c96-43bf-bb22-b86d552f6f39] Received message: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0
Received: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0, greater, Not Leader
Sent: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0
Sent: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0
Waiting to receive data...
Raw received: {"received_uuid": "d1bdafd6-b54c-4606-8317-deaccc97a211", "flag": 1}

[Node 6dd5026c-2c96-43bf-bb22-b86d552f6f39] Received message: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=1
Received: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=1, , Leader Elected
Sent: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=1
Sent: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=1

```

</details>

<details>
  <summary>Node 2 (which was selected as n)</summary>

```
python3 myleprocess.py n 2
Node 2 (n) Configuration:
  Server IP: 127.0.0.1, Server Port: 5002
  Client IP: 127.0.0.1, Client Port: 5004
I am the Server---------- This is my ID: d1bdafd6-b54c-4606-8317-deaccc97a211
The server is ready to receive
Waiting to receive data...
Press [Enter] to initiate the election on this node, or type 'no' to skip: Raw received: {"received_uuid": "6dd5026c-2c96-43bf-bb22-b86d552f6f39", "flag": 0}

[Node d1bdafd6-b54c-4606-8317-deaccc97a211] Received message: uuid=6dd5026c-2c96-43bf-bb22-b86d552f6f39, flag=0
Received: uuid=6dd5026c-2c96-43bf-bb22-b86d552f6f39, flag=0, less, Not Leader
Sent: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0
Waiting to receive data...
Raw received: {"received_uuid": "d1bdafd6-b54c-4606-8317-deaccc97a211", "flag": 0}

[Node d1bdafd6-b54c-4606-8317-deaccc97a211] Received message: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0
Waiting to receive data...
Raw received: {"received_uuid": "d1bdafd6-b54c-4606-8317-deaccc97a211", "flag": 0}

[Node d1bdafd6-b54c-4606-8317-deaccc97a211] Received message: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0
Second time seeing own UUID. Declaring self as leader: d1bdafd6-b54c-4606-8317-deaccc97a211
Leader is decided to d1bdafd6-b54c-4606-8317-deaccc97a211
Sent: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=1
```
</details>

<details>
  <summary>Node 3 (which was selected as n)</summary>

  ```
  python3 myleprocess.py n 3
Node 3 (n) Configuration:
  Server IP: 127.0.0.1, Server Port: 5003
  Client IP: 127.0.0.1, Client Port: 5005
I am the Server---------- This is my ID: 0bbf5eec-ef64-4fcf-b5a1-6b8590283046
The server is ready to receive
Waiting to receive data...
Press [Enter] to initiate the election on this node, or type 'no' to skip: Raw received: {"received_uuid": "6dd5026c-2c96-43bf-bb22-b86d552f6f39", "flag": 0}

[Node 0bbf5eec-ef64-4fcf-b5a1-6b8590283046] Received message: uuid=6dd5026c-2c96-43bf-bb22-b86d552f6f39, flag=0
Received: uuid=6dd5026c-2c96-43bf-bb22-b86d552f6f39, flag=0, greater, Not Leader
Sent: uuid=6dd5026c-2c96-43bf-bb22-b86d552f6f39, flag=0
Waiting to receive data...
Raw received: {"received_uuid": "d1bdafd6-b54c-4606-8317-deaccc97a211", "flag": 0}

[Node 0bbf5eec-ef64-4fcf-b5a1-6b8590283046] Received message: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0
Received: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0, greater, Not Leader
Sent: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0
Waiting to receive data...
Raw received: {"received_uuid": "d1bdafd6-b54c-4606-8317-deaccc97a211", "flag": 0}

[Node 0bbf5eec-ef64-4fcf-b5a1-6b8590283046] Received message: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0
Received: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0, greater, Not Leader
Sent: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0
Waiting to receive data...
Raw received: {"received_uuid": "d1bdafd6-b54c-4606-8317-deaccc97a211", "flag": 0}

[Node 0bbf5eec-ef64-4fcf-b5a1-6b8590283046] Received message: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0
Received: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0, greater, Not Leader
Sent: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0
Waiting to receive data...
Raw received: {"received_uuid": "d1bdafd6-b54c-4606-8317-deaccc97a211", "flag": 1}

[Node 0bbf5eec-ef64-4fcf-b5a1-6b8590283046] Received message: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=1
Received: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=1, , Leader Elected
Sent: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=1
  ```
</details>

<details>
  <summary>Node 4 (which was selected as n)</summary>

  ```
  python3 myleprocess.py n 4
Node 4 (n) Configuration:
  Server IP: 127.0.0.1, Server Port: 5004
  Client IP: 127.0.0.1, Client Port: 5005
I am the Server---------- This is my ID: 799960bf-dab7-4455-b58f-416bc121554b
The server is ready to receive
Waiting to receive data...
Press [Enter] to initiate the election on this node, or type 'no' to skip: Raw received: {"received_uuid": "d1bdafd6-b54c-4606-8317-deaccc97a211", "flag": 0}

[Node 799960bf-dab7-4455-b58f-416bc121554b] Received message: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0
Received: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0, greater, Not Leader
Sent: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0
Waiting to receive data...
Raw received: {"received_uuid": "d1bdafd6-b54c-4606-8317-deaccc97a211", "flag": 1}

[Node 799960bf-dab7-4455-b58f-416bc121554b] Received message: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=1
Received: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=1, , Leader Elected
Sent: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=1

  ```
</details>

<details>
  <summary>Node 5 (which was selected as y)</summary>

  ```
  python3 myleprocess.py y 5
Node 5 (y) Configuration:
  Server IP: 127.0.0.1, Server Port: 5005
  Client IP: 127.0.0.1, Client Port: 5001
I am the Server---------- This is my ID: 56c8f5fa-7fcc-48be-af29-36f4afd08e95
The server is ready to receive
Waiting to receive data...
Waiting to receive data...
Press [Enter] to initiate the election on this node, or type 'no' to skip: Raw received: {"received_uuid": "6dd5026c-2c96-43bf-bb22-b86d552f6f39", "flag": 0}

[Node 56c8f5fa-7fcc-48be-af29-36f4afd08e95] Received message: uuid=6dd5026c-2c96-43bf-bb22-b86d552f6f39, flag=0
Received: uuid=6dd5026c-2c96-43bf-bb22-b86d552f6f39, flag=0, greater, Not Leader
Raw received: {"received_uuid": "d1bdafd6-b54c-4606-8317-deaccc97a211", "flag": 0}

[Node 56c8f5fa-7fcc-48be-af29-36f4afd08e95] Received message: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0
Sent: uuid=6dd5026c-2c96-43bf-bb22-b86d552f6f39, flag=0
Waiting to receive data...
Received: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0, greater, Not Leader
Sent: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0
Waiting to receive data...
Raw received: {"received_uuid": "d1bdafd6-b54c-4606-8317-deaccc97a211", "flag": 0}

[Node 56c8f5fa-7fcc-48be-af29-36f4afd08e95] Received message: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0
Received: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0, greater, Not Leader
Sent: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0
Waiting to receive data...
Raw received: {"received_uuid": "d1bdafd6-b54c-4606-8317-deaccc97a211", "flag": 0}

[Node 56c8f5fa-7fcc-48be-af29-36f4afd08e95] Received message: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0
Received: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0, greater, Not Leader
Sent: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0
Raw received: {"received_uuid": "d1bdafd6-b54c-4606-8317-deaccc97a211", "flag": 1}

[Node 56c8f5fa-7fcc-48be-af29-36f4afd08e95] Received message: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=1
Waiting to receive data...
Received: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=1, , Leader Elected
Sent: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=1
Raw received: {"received_uuid": "d1bdafd6-b54c-4606-8317-deaccc97a211", "flag": 0}

[Node 56c8f5fa-7fcc-48be-af29-36f4afd08e95] Received message: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211, flag=0
Ignored: uuid=d1bdafd6-b54c-4606-8317-deaccc97a211

  ```
</details>