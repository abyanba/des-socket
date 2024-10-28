import socket
from des import decryption  # Import fungsi dekripsi DES

# Key disepakati (hardcoded)
key = "12345678abcdefgh"  

def server_program():
    host = socket.gethostname()
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)
    conn, address = server_socket.accept()
    print("Connection from:", address)

    while True:
        encrypted_message = conn.recv(1024).decode()
        if not encrypted_message:
            break
        
        print(f"Received Encrypted Message: {encrypted_message}")
        # Dekripsi pesan yang diterima
        decrypted_message = decryption(encrypted_message, key)
        print(f"Decrypted Message: {decrypted_message}")

        # Kirim pesan asli kembali ke client
        conn.send(decrypted_message.encode())

    conn.close()

if __name__ == '__main__':
    server_program()
