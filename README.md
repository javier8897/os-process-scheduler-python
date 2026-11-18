# Python University Projects: From Fundamentals to OS Process Scheduling

This repository showcases my progression in Python throughout my university Algorithms and Data Structures coursework—moving from foundational procedural programming in the first half of the year to a full Object-Oriented Operating System simulator for my final capstone project.

---

## 1. OS Process Scheduler Simulator (`process_simulator.py`) — Final Capstone Project
*(Main Portfolio Project — Adapted from Spanish to English)*

A command-line Operating System Process Scheduler developed as my final integrative project (selected among three options) to apply all concepts covered during the academic year.

### Key Technical Highlights
* **Object-Oriented Architecture:** Modular design structured around `Process` and `Simulator` classes.
* **Round-Robin & Queue Management:** Uses `collections.deque` for efficient $O(1)$ FIFO operations across Ready and Blocked queues.
* **Anti-Starvation Mechanism:** Dynamic priority-aging system that automatically boosts the priority of processes waiting beyond a configurable cycle threshold.
* **Data Structures & Algorithms:** Implements recursive subtask call stacks and a custom Insertion Sort algorithm to reorder the ready queue by priority on demand.
* **File I/O & Persistence:** Automatically reads/generates external `.txt` configuration files (`quantum` and process count) and exports detailed execution logs.

### How to Run
```bash
python process_simulator.py
