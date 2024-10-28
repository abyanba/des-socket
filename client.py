import socket
from des import encryption  # Import fungsi enkripsi DES

# Key disepakati (hardcoded)
key = "12345678abcdefgh"

def client_program():
    host = socket.gethostname()
    port = 5000

    client_socket = socket.socket()
    client_socket.connect((host, port))

    message = input("Enter message to send: ")

    # Enkripsi pesan sebelum dikirim
    encrypted_message = encryption(message, key)
    print(f"Sending Encrypted Message: {encrypted_message}")

    client_socket.send(encrypted_message.encode())

    # Menerima pesan asli yang telah didekripsi server
    decrypted_message = client_socket.recv(1024).decode()
    print(f"Received from server: {decrypted_message}")

    client_socket.close()

if __name__ == '__main__':
    client_program()
