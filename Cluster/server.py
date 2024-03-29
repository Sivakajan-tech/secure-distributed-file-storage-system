import os
import logging
import socket


def save_file(filename, data):
    with open(filename, "wb") as file:
        file.write(data)


def start_server(server_address):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen(1)
    print(f"Server listening on {server_address[0]}:{server_address[1]}")

    while True:
        print("Waiting for a connection...")
        client_socket, client_address = server_socket.accept()
        print(f"Connection established from {client_address[0]}:{client_address[1]}")  # noqa E501

        # Receive the file name
        file_name = client_socket.recv(1024).decode("utf-8")
        # if file_name:
        #     file_loc = f'./collection/{file_name}'
        #     os.makedirs(os.path.dirname(file_loc), exist_ok=True)

        #     # Receive the file data and save it
        #     with open(file_loc, "wb") as file:
        #         data = client_socket.recv(1024)
        #         while data:
        #             file.write(data)
        #             data = client_socket.recv(1024)

        print(f"File {file_name} received and saved successfully\n")
        client_socket.close()


if __name__ == "__main__":
    # Define the server address and port
    server_address = ("0.0.0.0", 65432)
    print("Server started successfully!\n")
    logging.info("Server started successfully!")

    start_server(server_address)
