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

    # Menerima kunci dari klien
    key = conn.recv(1024).decode('utf-8')
    print(f"Received DES Key from client: {key}")

    while True:
        # Terima pesan terenkripsi dari klien
        encrypted_data = conn.recv(1024).decode('utf-8')
        if not encrypted_data:
            break

        # Dekripsi pesan yang diterima
        decrypted_data = des.decrypt(encrypted_data, key=key)
        print(f"Received Encrypted Message: {encrypted_data}")
        print(f"Decrypted Message: {decrypted_data}")

        # Ambil input respons dari server, enkripsi, dan kirim kembali ke klien
        response = input("Enter response to send: ")
        encrypted_response = des.encrypt(response, key=key)
        print(f"Encrypted Response: {encrypted_response}")
        conn.send(encrypted_response.encode('utf-8'))

    conn.close()

if __name__ == '__main__':
    server_program()
