import socket
from des_cli import encryption_large_text, decryption_large_text, generate_random_key

def server_program():
    host = socket.gethostname()
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)
    conn, address = server_socket.accept()
    print("Connection from:", address)

    # Receive and store the key sent from the client
    key = conn.recv(1024).decode()
    print("Received Key from Client:", key)

    while True:
        # Terima pesan terenkripsi dari klien
        encrypted_data = conn.recv(1024).decode()
        if encrypted_data.lower() == "bye":
            print("Client ended the chat. Closing connection.")
            conn.send("bye".encode())  # Notify client to close
            break

        # Deskripsi pesan
        decrypted_data = decryption_large_text(encrypted_data, key)
        print("Received Encrypted Message:", encrypted_data)
        print("Decrypted Message:", decrypted_data)

        # Kirim pesan balik
        response = input("Server Response: ")
        if response.lower() == "bye":
            encrypted_response = encryption_large_text(response, key)
            conn.send(encrypted_response.encode())
            print("Encrypted Response:", encrypted_response)
            break

        encrypted_response = encryption_large_text(response, key)
        conn.send(encrypted_response.encode())
        print("Encrypted Response:", encrypted_response)

    conn.close()

if __name__ == '__main__':
    server_program()
