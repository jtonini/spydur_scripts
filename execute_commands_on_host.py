# -*- coding: utf-8 -*-
"""
This file contains conveniences for our slurm development efforts.
"""

import typing
from   typing import *

min_py = (3, 8)

###
# Standard imports.
###

import enum
import os
import sys
if sys.version_info < min_py:
    print(f"This program requires Python {min_py[0]}.{min_py[1]}, or higher.")
    sys.exit(os.EX_SOFTWARE)

import math
import shlex
import subprocess

from   urdecorators import trap

# Credits
__author__ = 'João Tonini'
__copyright__ = 'Copyright 2023'
__credits__ = None
__version__ = str(math.pi**2)[:5]
__maintainer__ = 'João Tonini'
__email__ = ['jtonini@richmond.edu']
__status__ = 'Teaching example'
__license__ = 'MIT'

import paramiko

# Define a list of hostnames and their connection information
host_info = [
    {"hostname": "host1.example.com", "username": "username1", "password": "password1"},
    {"hostname": "host2.example.com", "username": "username2", "password": "password2"},
    # Add more hosts as needed
]

# Define the commands you want to execute
commands = [
    "command1",
    "command2",
    # Add more commands as needed
]

def execute_commands_on_host(hostname, username, password, commands):
    try:
        # Create an SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the remote host
        ssh.connect(hostname, username=username, password=password)

        results = []
        for command in commands:
            # Execute the command
            stdin, stdout, stderr = ssh.exec_command(command)

            # Get the command result and status
            result = stdout.read().decode('utf-8')
            status = stdout.channel.recv_exit_status()

            results.append({"command": command, "result": result, "status": status})

        # Close the SSH connection
        ssh.close()

        return results
    except Exception as e:
        return [{"command": "Error", "result": str(e), "status": 1}]

for host in host_info:
    hostname = host["hostname"]
    username = host["username"]
    password = host["password"]
    
    print(f"Executing commands on {hostname}")
    results = execute_commands_on_host(hostname, username, password, commands)

    for result in results:
        print(f"Command: {result['command']}")
        print(f"Result:\n{result['result']}")
        if result["status"] == 0:
            print("Status: Success")
        else:
            print("Status: Failure")

    print("\n")

print("Done.")

