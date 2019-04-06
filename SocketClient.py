import socket
import websocket

def sendData(data, HOST, PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(data)
        #data = s.recv(1024)

def sendData2(DATA):
    # Connect to WebSocket server
    ws = websocket.WebSocket()
    ws.connect("ws://192.168.43.192:65000")
    print("Connected to WebSocket server")

    # Ask the user for some input and transmit it
    ws.send(DATA)

    # Wait for server to respond and print i
    # Gracefully close WebSocket connection
    ws.close()
