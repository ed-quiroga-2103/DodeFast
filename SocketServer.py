import socket

HOST = '172.20.10.7'  # Standard loopback interface address (localhost)
PORT = 65000        # Port to listen on (non-privileged ports are > 1023)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    while True:
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if data == b"True":
                    print(data)
                if not data:
                    break
                conn.sendall(data)
