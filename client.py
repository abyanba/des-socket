import socket
from des_cli import DES

def client_program():
    des = DES()
    host = socket.gethostname()
    port = 5000

    client_socket = socket.socket()
    client_socket.connect((host, port))

    key = des.generate_des_key()
    print(f"Generated DES Key: {key}")

    message = input(" -> ")

    while message.lower().strip() != 'bye':
        encrypted_message = des.encrypt(message, key)
        client_socket.send(encrypted_message.encode('utf-8'))

        data = client_socket.recv(1024).decode('utf-8')
        decrypted_message = des.decrypt(data, key)

        print('Received from server: ' + decrypted_message)
        message = input(" -> ")

    client_socket.close()

if __name__ == '__main__':
    client_program()
