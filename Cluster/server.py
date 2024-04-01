import os
import socket
from typing import List
import unicodedata


def get_file_name(file_name_bytes) -> str:
    """
    This code attempts to decode the received byte stream using UTF-8 and,
    if it fails, it falls back to decoding using `latin-1` encoding
    and removes control characters (which may cause issues during decoding).
    """
    # Decode using UTF-8 and handle errors
    try:
        return file_name_bytes.decode("utf-8")
    except UnicodeDecodeError:
        # Replace non-UTF-8 characters with a placeholder or remove them
        sanitized_file_name = "".join(
            c
            for c in file_name_bytes.decode("latin-1")
            if unicodedata.category(c)[0] != "C"
        )
        return sanitized_file_name


def get_ip_port(file_name) -> List[str:str]:
    ip_map = {}
    with open(file_name, "r") as file:
        # Read lines one by one
        for line in file:
            # Split the line into IP address and port number
            ip, port = line.strip().split()
            ip_map[ip] = port
    return ip_map


def start_server(server_address):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen(1)
    print(f"Server listening on {server_address[0]}:{server_address[1]}")

    while True:
        print("Waiting for a connection...")
        client_socket, client_address = server_socket.accept()
        print(
            f"Connection established from {client_address[0]}:{client_address[1]}"  # noqa E501
        )

        # Receive the file name
        file_name = get_file_name(client_socket.recv(1024))
        if file_name:
            file_loc = f"./collection/{file_name}"
            os.makedirs(os.path.dirname(file_loc), exist_ok=True)

            # Receive the file data and save it
            with open(file_loc, "wb") as file:
                data = client_socket.recv(1024)
                while data:
                    file.write(data)
                    data = client_socket.recv(1024)

        print(f"File {file_name} received and saved successfully\n")
        client_socket.close()


if __name__ == "__main__":
    ip_map = get_ip_port("client_map.txt")

    # Define the server address and port
    server_address = (
        list(ip_map.keys())[0],
        int(ip_map[list(ip_map.keys())[0]]),
    )
    print("Server started successfully!\n")

    start_server(server_address)
