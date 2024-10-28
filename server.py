import socket
from des_cli import DES

def server_program():
    des = DES()
    host = socket.gethostname()
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)
    conn, address = server_socket.accept()
    print("Connection from: " + str(address))

    key = des.generate_des_key()
    print(f"Generated DES Key: {key}")

    while True:
        encrypted_data = conn.recv(1024).decode('utf-8')
        if not encrypted_data:
            break

        decrypted_data = des.decrypt(encrypted_data, key)
        print("from connected user: " + str(decrypted_data))

        response = input(' -> ')
        encrypted_response = des.encrypt(response, key)
        conn.send(encrypted_response.encode('utf-8'))

    conn.close()

if __name__ == '__main__':
    server_program()
