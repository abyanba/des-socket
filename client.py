import socket
from des_cli import DES

def client_program():
    des = DES()
    host = socket.gethostname()
    port = 5000

    client_socket = socket.socket()
    client_socket.connect((host, port))

    # Hasilkan dan kirim kunci ke server
    key = des.generate_des_key()
    print(f"Generated DES Key: {key}")
    client_socket.send(key.encode('utf-8'))

    while True:
        message = input("Enter message to send (type 'bye' to exit): ")
        if message.lower().strip() == 'bye':
            break

        # Enkripsi pesan sebelum dikirim
        encrypted_message = des.encrypt(message, key=key)
        print(f"Original Message: {message}")
        print(f"Encrypted Message: {encrypted_message}")

        # Kirim pesan terenkripsi ke server
        client_socket.send(encrypted_message.encode('utf-8'))

        # Terima respons dari server dan dekripsi
        data = client_socket.recv(1024).decode('utf-8')
        decrypted_message = des.decrypt(data, key=key)
        print(f"Received Encrypted Response: {data}")
        print(f"Decrypted Response: {decrypted_message}")

    client_socket.close()

if __name__ == '__main__':
    client_program()
