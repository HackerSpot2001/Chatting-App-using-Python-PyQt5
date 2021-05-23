#!/usr/bin/python3
import socket
import threading

def broadcastMSG(msg):
    for client in clients:
        client.send(msg.encode("utf-8"))

def handle_client(client):
    while True:
        try:
            data = client.recv(1024).decode('utf-8')
            message = f"{nicknames[clients.index(client)]}: {data}"
            broadcastMSG(message)

        except:
            index = clients.index(client)
            clients.remove(index)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)



if __name__ == '__main__':
    host = '127.0.0.1'
    port = 9090
    maxConn = 99
    clients = []
    nicknames = []

    try:
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind((host,port))
        print(f"[+] Server is running on {host}:{port}")
        server.listen(maxConn)
        while True:
            client,addr = server.accept()
            print(f"{addr} connected with server")
            client.send("NAME".encode("utf-8"))
            nickname = client.recv(1024).decode("utf-8")
            print(f"Nick-Name of the client {nickname}")
            broadcastMSG(f"{nickname} Connected with the server")
            clients.append(client)
            nicknames.append(nickname)
            thread = threading.Thread(target=handle_client,args=(client,))
            thread.start()
            

    except Exception as e:
        print("Error: ",e)