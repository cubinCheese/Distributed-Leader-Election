
# Project Overview 🧐

This repository contains an implementation of the **Leader Election Problem** in distributed systems. The project demonstrates how multiple processes (nodes) can coordinate to elect a single leader in both simple and more complex network topologies, using **Python**, **sockets**, and **multithreading**.

## What is the Leader Election Problem?

In distributed computing, **leader election** is the process of designating a single process as the organizer of a task distributed among several computers (nodes). A valid leader election algorithm must satisfy the following conditions:

1. **Termination**: The algorithm should finish within a finite time once the leader is selected.  
2. **Uniqueness**: Exactly one process considers itself as leader.  
3. **Agreement**: All other processes know who the leader is.  

# Usage Instructions
## Task 1: Single Ring Leader Election

**Instructions:**  
1. Open three separate terminals.
2. In each terminal, navigate to the corresponding node directory:
    - `cd task1/node1`
    - `cd task1/node2`
    - `cd task1/node3`
3. Run the node process in each terminal:
    ```sh
    python3 myleprocess.py
    ```
4. On **one node only**, press `[Enter]` when prompted to initiate the leader election.

For more details, see the README in `task1/`.

---

## Task 2: Partial Double Ring Leader Election

**Instructions:**  
1. Open five separate terminals.
2. In each terminal, navigate to the `task2` directory:
    - `cd task2`
3. Run each node with its type and number:
    ```sh
    python3 myleprocess.py <node_type> <number>
    ```
    - `<node_type>`: `x`, `y`, or `n`
    - `<number>`: `1`, `2`, `3`, `4`, or `5`
4. On **one node only**, press `[Enter]` when prompted to initiate the leader election.

For more details, see the README in `task2/`.

---

# More Implementation Details 🥳

## Generating Unique IDs

Each process is assigned a **Universally Unique Identifier (UUID)** using Python's `uuid.uuid4()` method. UUIDs are 128-bit labels that are practically guaranteed to be unique, allowing processes to compare identifiers to determine the leader.

## Node Configuration

- Assumes an **asynchronous non-anonymous ring**.  
- Each node has exactly two neighbors.  
- Each node acts as both **server** (accepting connections) and **client** (initiating connections).  
- Connection information is stored in a `config.txt` file with the format:  
- Nodes maintain persistent socket connections for communication.  

## Multithreading

- The server process runs in a separate thread to allow simultaneous client connections.  
- After establishing connections, single-threaded or shared-memory multi-threaded execution handles the election process.  

## Leader Election Algorithm

- Each node executes the **O(n² asynchronous ring algorithm)**.  
- Messages are sent from client to server, containing a `uuid` and `flag` to indicate election status:  
`{
  "uuid": "123e4567-e89b-42d3-a456-556642440000",
  "flag": 0 }

`
## Challenges and Considerations

- **Multiple Initiators**: If multiple nodes start the election simultaneously, messages propagate around the ring with their UUIDs. The algorithm ensures that the node with the highest UUID eventually becomes the leader, while lower UUIDs are ignored.

- **Asynchronous Communication**: Nodes may receive messages in any order. Using persistent connections, multithreading, and message logging ensures correct processing and avoids lost or duplicated messages.

- **Dynamic Topologies**: The partially double ring introduces additional connections, requiring nodes to handle multiple incoming connections and maintain consistent state across the extended network.

- **Termination Detection**: Each node must determine locally when the election has finished, ensuring all nodes have the same `leader_id` despite asynchronous delays.


[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/kd2D9bOv)

    
