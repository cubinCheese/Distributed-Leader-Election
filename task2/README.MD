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

## Contact

For questions or issues, please contact the course staff or open an issue in your repository.