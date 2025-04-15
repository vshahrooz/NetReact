import paramiko
import time
import re


# Router 1 credentials
ROUTER1 = {
    "hostname": "192.168.1.1",
    "username": "admin",
    "password": "password"
}

# Router 2 credentials
ROUTER2 = {
    "hostname": "192.168.1.2",
    "username": "admin",
    "password": "password"
}

# Ping target and source interface
PING_TARGET = "8.8.8.8"
PING_SOURCE_INTERFACE = "GigabitEthernet0/0"

# Phase 1 settings
PHASE1_PING_COUNT = 100
PHASE1_INTERVAL_SECONDS = 10
PHASE1_TIMEOUT_THRESHOLD = 10

# Phase 2 settings
PHASE2_PING_COUNT = 1000
PHASE2_INTERVAL_SECONDS = 300  # 5 minutes
PHASE2_TIMEOUT_THRESHOLD = 5

# Commands for Phase 2 (execute and remove) on Router 2
PHASE2_COMMANDS = [
    "configure terminal",
    "interface GigabitEthernet0/1",
    "shutdown",
    "exit",
    "exit"
]

PHASE2_REMOVE_COMMANDS = [
    "configure terminal",
    "interface GigabitEthernet0/1",
    "no shutdown",
    "exit",
    "exit"
]


def ssh_run_commands(router, commands):
    """Execute commands on router via SSH"""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(router["hostname"], username=router["username"], password=router["password"])
    shell = ssh.invoke_shell()
    time.sleep(1)
    shell.send("terminal length 0\n")
    time.sleep(1)

    for cmd in commands:
        shell.send(cmd + "\n")
        time.sleep(1)

    time.sleep(2)
    output = shell.recv(10000).decode()
    ssh.close()
    return output


def get_ping_timeouts(output):
    """Count timeout occurrences in ping output"""
    return len(re.findall(r"Request timed out|100 percent packet loss", output, re.IGNORECASE))


def do_ping(router, count, source, destination):
    """Execute ping command on router"""
    command = [f"ping {destination} repeat {count} source {source}"]
    print(f"[+] Pinging {destination} {count} times from {source}")
    return ssh_run_commands(router, command)


def phase1():
    """Primary monitoring phase"""
    while True:
        output = do_ping(ROUTER1, PHASE1_PING_COUNT, PING_SOURCE_INTERFACE, PING_TARGET)
        timeouts = get_ping_timeouts(output)
        print(f"[Phase 1] Timeout count: {timeouts}")
        if timeouts >= PHASE1_TIMEOUT_THRESHOLD:
            print("[!] High timeout count detected - Entering Phase 2")
            ssh_run_commands(ROUTER2, PHASE2_COMMANDS)
            phase2()
        time.sleep(PHASE1_INTERVAL_SECONDS)


def phase2():
    """Remediation phase"""
    while True:
        output = do_ping(ROUTER1, PHASE2_PING_COUNT, PING_SOURCE_INTERFACE, PING_TARGET)
        timeouts = get_ping_timeouts(output)
        print(f"[Phase 2] Timeout count: {timeouts}")
        if timeouts < PHASE2_TIMEOUT_THRESHOLD:
            print("[+] Connectivity improved - Removing commands and returning to Phase 1")
            ssh_run_commands(ROUTER2, PHASE2_REMOVE_COMMANDS)
            break
        time.sleep(PHASE2_INTERVAL_SECONDS)

    phase1()


if __name__ == "__main__":
    print("🟢 Starting ping monitoring to", PING_TARGET)
    phase1()
