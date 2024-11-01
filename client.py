import socket
from des_cli import encryption_large_text, decryption_large_text, generate_random_key

def client_program():
    host = socket.gethostname()
    port = 5000
    client_socket = socket.socket()
    client_socket.connect((host, port))
    encryption = encryption_large_text
    decryption = decryption_large_text
    randomkey = generate_random_key

    while True:
        # Generate dan kirimkan key ke server
        key = randomkey()
        client_socket.send(key.encode())
        print("Generated Key sent to Server:", key)
        
        # Ambil input dari user
        message = input("Client Message: ")
        if message.lower().strip() == "bye":
            break

        # Enkripsi pesan sebelum dikirim
        encrypted_message = encryption(message, key)
        client_socket.send(encrypted_message.encode())
        print("Message:", message)
        print("Encrypted Message:", encrypted_message)

        # Terima respons terenkripsi dari server
        encrypted_response = client_socket.recv(1024).decode()
        if not encrypted_response:
            break

        decrypted_response = decryption(encrypted_response, key)
        print("Received Encrypted Response:", encrypted_response)
        print("Decrypted Response:", decrypted_response)

    client_socket.close()

if __name__ == '__main__':
    client_program()
