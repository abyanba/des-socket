import socket
from des_cli import encryption_large_text, decryption_large_text

def server_program():
    host = socket.gethostname()
    port = 5000
    encryption = encryption_large_text
    decryption = decryption_large_text

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)
    conn, address = server_socket.accept()
    print("Connection from:", address)

    while True:
        # Receive and store the key sent from the client
        key = conn.recv(1024).decode()
        print("Received Key from Client:", key)
        
        # Terima pesan terenkripsi dari klien
        encrypted_data = conn.recv(1024).decode()
        if not encrypted_data:
            break

        # Deskripsi pesan
        decrypted_data = decryption(encrypted_data, key)
        print("Received Encrypted Message:", encrypted_data)
        print("Decrypted Message:", decrypted_data)

        # Kirim pesan balik
        response = input("Server Response: ")
        if response.lower().strip() == "bye":
            break
        encrypted_response = encryption(response, key)
        conn.send(encrypted_response.encode())
        print("Encrypted Response:", encrypted_response)

    conn.close()

if __name__ == '__main__':
    server_program()
