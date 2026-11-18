import os
import random
from collections import deque

CONFIG_FILE = "config_processes.txt"
LOG_FILE = "execution_log.txt"
MAX_CYCLES = 20
MAX_WAIT = 3


class Process:
    def __init__(self, pid, time, priority):
        self.pid = pid
        self.remaining = time
        self.priority = priority
        self.wait = 0
        self.total_run = 0
        self.stack = []

    def call(self, level):
        if level > 0:
            self.stack.append(f"subtask_{len(self.stack) + 1}")
            self.call(level - 1)

    def clear_stack(self):
        if self.stack:
            self.stack.pop()
            self.clear_stack()

    def run(self, quantum):
        used = min(quantum, self.remaining)
        self.remaining -= used
        self.total_run += used
        self.wait = 0
        self.call(used)
        if self.remaining == 0:
            self.clear_stack()

    def __str__(self):
        return (f"P{self.pid} | remaining: {self.remaining} | "
                f"priority: {self.priority} | stack: {len(self.stack)}")


class Simulator:
    def __init__(self):
        self.quantum, count = self.load_config()
        self.ready = deque()
        self.blocked = deque()
        self.log = []
        self.cycle = 0
        self.next_id = 1
        for _ in range(count):
            self.add(random.randint(1, 10), random.randint(1, 5))

    @staticmethod
    def load_config():
        config = {"quantum": 3, "num_processes": 8}
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE) as f:
                for line in f:
                    key, _, value = line.strip().partition("=")
                    if key in config and value.isdigit() and int(value) > 0:
                        config[key] = int(value)
        else:
            with open(CONFIG_FILE, "w") as f:
                f.write("quantum=3\nnum_processes=8\n")
        return config["quantum"], config["num_processes"]

    def add(self, time, priority):
        p = Process(self.next_id, time, priority)
        self.ready.append(p)
        self.next_id += 1
        return p

    def status(self):
        for name, queue in (("Ready", self.ready), ("Blocked", self.blocked)):
            print(f"--- {name} ---")
            print("\n".join(map(str, queue)) or "(empty)")

    def avoid_starvation(self):
        for p in self.ready:
            p.wait += 1
            if p.wait >= MAX_WAIT and p.priority > 1:
                p.priority -= 1
                p.wait = 0
                print(f"  (P{p.pid} waited too long: priority raised to {p.priority})")

    def run_cycle(self):
        p = self.ready.popleft()
        self.cycle += 1
        p.run(self.quantum)
        line = f"Process {p.pid} executed, remaining time {p.remaining}"
        self.log.append(line)
        print(f"Cycle {self.cycle}: {line}")
        if p.remaining > 0:
            self.ready.append(p)
        else:
            print(f"  -> P{p.pid} finished")
        self.avoid_starvation()

    def simulate(self, cycles=MAX_CYCLES):
        if not self.ready:
            return print("No ready processes left.")
        if cycles == 0:
            return print(f"Reached the limit of {MAX_CYCLES} cycles.")
        self.run_cycle()
        self.simulate(cycles - 1)

    def interrupt(self):
        pid = ask_number("ID to interrupt: ")
        for p in self.ready:
            if p.pid == pid:
                self.ready.remove(p)
                self.blocked.append(p)
                return print(f"P{pid} blocked.")
        print("That process is not in the ready queue.")

    def unblock(self):
        self.ready.extend(self.blocked)
        self.blocked.clear()
        print("Blocked processes moved back to the ready queue.")

    def sort(self):
        items = list(self.ready)
        for i in range(1, len(items)):
            current, j = items[i], i - 1
            while j >= 0 and items[j].priority > current.priority:
                items[j + 1] = items[j]
                j -= 1
            items[j + 1] = current
        self.ready = deque(items)
        print("Queue sorted by priority.")

    def new_process(self):
        t, pr = ask_number("Time (1-10): "), ask_number("Priority (1-5): ")
        if 1 <= t <= 10 and 1 <= pr <= 5:
            print(f"Process created: {self.add(t, pr)}")
            self.status()
        else:
            print("Values out of range.")

    def save_log(self):
        with open(LOG_FILE, "w") as f:
            f.write("\n".join(self.log) + "\n")
        print("Log saved to", LOG_FILE)


def ask_number(prompt):
    value = input(prompt)
    return int(value) if value.isdigit() else -1


def main():
    sim = Simulator()
    menu = {
        "1": ("Show status", sim.status),
        "2": ("Add process", sim.new_process),
        "3": ("Simulate (max 20 cycles)", sim.simulate),
        "4": ("Interrupt process", sim.interrupt),
        "5": ("Unblock all", sim.unblock),
        "6": ("Sort by priority", sim.sort),
        "0": ("Exit and save log", None),
    }
    print(f"Quantum: {sim.quantum}")
    sim.status()
    while True:
        print("\n" + "\n".join(f"{k}) {d}" for k, (d, _) in menu.items()))
        option = input("Option: ")
        if option == "0":
            return sim.save_log()
        action = menu.get(option)
        if action:
            action[1]()
        else:
            print("Invalid option.")


main()
