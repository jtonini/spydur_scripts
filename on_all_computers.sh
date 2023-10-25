#!/bin/bash

# Define an array with hostnames and their connection details
declare -A my_computers=(
	["host1"]="root@host1.example.com"
	["host2"]="root@host2.example.com"
	["host3"]="root@host3.example.com"
	)

# Log file for recording the results
log_file="execution.log"

on_all_computers() {
	if [ -z "$1" ]; then
		echo 'Usage: on_all_computers "command"'
		return
	fi

	for host in "${!my_computers[@]}"; do
		if [ "$host" != "($hostname -s)" ]; then
			echo " "
			echo "-------------------------"
			echo "*****	$host"

			# Run the command on the remote host via SSH
			ssh_output=$(ssh ${my_computers["$host"]} "source ~wstools.bash && $1")

			# Log results to a file
			echo "Command on $host:" >> "$log_file"
			echo "$ssh_output" >> "$log_file"

			# Check the exit status of the SSH command
			if [ $? -eq 0 ]; then
				echo "Command on $host: Success"
			else
				echo "Command on $host: Falied"
			fi
		fi
	done

	echo "Done."
}

# Example of usage:
# on_all_computers "command_to_execute"
