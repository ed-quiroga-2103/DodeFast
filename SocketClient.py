import socket

def sendData(data, HOST, PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(data)
        data = s.recv(1024)

    print('Received', repr(data))
mes = "hola!"
#sendData(mes.encode(), "127.0.0.1",65000)