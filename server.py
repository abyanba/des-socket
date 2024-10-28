import socket 
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 8080))
s.listen(5)

clients = []
aliases = []

def broadcast(message):
    for client in clients: 
        client.send(message)

def handle_client(client):
    while True:
        try: 
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast('{} has left chat room'.format(alias).encode('utf-8'))
            aliases.remove(alias)
            break 

# Main function to receive client connection 
def receive():
    while True:
        print('Server is running and listening...')
        client, address = s.accept()
        print('connection is established with {0}'.format(str(address)))
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)
        print('The alias of this client is {0}'.format(alias).encode('utf-8'))
        broadcast('{} has connected to the chatroom'.format(alias).encode('utf-8'))
        client.send('you are now connected!'.encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == '__main__':
    receive()