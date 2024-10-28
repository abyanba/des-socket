import socket
from des_cli import encryption_large_text, decryption_large_text, generate_random_key

def client_program():
    host = socket.gethostname()
    port = 5000
    client_socket = socket.socket()
    client_socket.connect((host, port))

    # Generate dan kirimkan key ke server
    key = generate_random_key()
    client_socket.send(key.encode())
    print("Generated Key sent to Server:", key)

    while True:
        # Ambil input dari user
        message = input("Client Message: ")
        if message.lower() == "bye":
            encrypted_message = encryption_large_text(message, key)
            client_socket.send(encrypted_message.encode())
            print("Encrypted Message:", encrypted_message)
            break

        # Enkripsi pesan sebelum dikirim
        encrypted_message = encryption_large_text(message, key)
        client_socket.send(encrypted_message.encode())
        print("Message:", message)
        print("Encrypted Message:", encrypted_message)

        # Terima respons terenkripsi dari server
        encrypted_response = client_socket.recv(1024).decode()
        if encrypted_response.lower() == "bye":
            print("Server ended the chat. Closing connection.")
            break

        decrypted_response = decryption_large_text(encrypted_response, key)
        print("Received Encrypted Response:", encrypted_response)
        print("Decrypted Response:", decrypted_response)

    client_socket.close()

if __name__ == '__main__':
    client_program()
