import os
import socket
import subprocess
import sys
import shutil

def get_free_port(start=5500, max_tries=50):
    port = start
    while port < start + max_tries:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('0.0.0.0', port))
                return port
            except OSError:
                port += 1
    raise OSError("No free ports found.")

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
    except Exception:
        ip = "localhost"
    return ip

def is_python_installed():
    return shutil.which("python") or shutil.which("python3")

def offer_install_python_linux():
    print("Python not found. Attempting installation (Linux only)...")
    confirm = input("Install Python via apt? [Y/n]: ").strip().lower()
    if confirm in ("y", ""):
        subprocess.call(["sudo", "apt", "update"])
        subprocess.call(["sudo", "apt", "install", "-y", "python3"])
    else:
        print("Python is required. Exiting.")
        sys.exit(1)

def launch_server_in_terminal(port):
    script = f"""
import http.server
import socketserver
PORT = {port}
Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(('0.0.0.0', PORT), Handler) as httpd:
    print('Serving at: http://localhost:' + str(PORT))
    print('Serving on LAN: http://{get_local_ip()}:' + str(PORT))
    httpd.serve_forever()
"""

    filename = "temp_server.py"
    with open(filename, "w") as f:
        f.write(script)

    if os.name == "nt":  # Windows
        terminal = "powershell" if shutil.which("powershell") else "cmd"
        subprocess.Popen([terminal, "/c", f"python {filename}"], creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:  # Linux
        terminals = ["gnome-terminal", "x-terminal-emulator", "konsole", "xterm"]
        for term in terminals:
            if shutil.which(term):
                subprocess.Popen([term, "-e", f"python3 {filename}"])
                break
        else:
            print("No compatible Linux terminal found. Run the server manually: python3 temp_server.py")

if __name__ == "__main__":
    if not is_python_installed():
        if os.name == "nt":
            print("Python is not installed. Please install Python from https://python.org before running this script.")
            sys.exit(1)
        else:
            offer_install_python_linux()

    port = get_free_port()
    print(f"Launching server on port {port}...")
    launch_server_in_terminal(port)