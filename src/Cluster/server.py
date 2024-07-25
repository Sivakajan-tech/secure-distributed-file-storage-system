import os
import socket


def start_server(server_address):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen(1)
    print("Server started successfully!\n")
    print(f"Server listening on {server_address[0]}:{server_address[1]}")

    while True:
        print("Waiting for a connection...")
        client_socket, client_address = server_socket.accept()
        print(
            f"Connection established from {client_address[0]}:{client_address[1]}"  # noqa E501
        )

        try:
            # Receive the length of the chunk name
            chunk_name_len = int.from_bytes(
                client_socket.recv(4), byteorder="big"
            )

            # Receive the chunk name based on the received length
            chunk_name = client_socket.recv(chunk_name_len).decode("utf-8")

            if chunk_name:
                file_loc = f"./collection/{chunk_name}"
                print(file_loc)
                os.makedirs(os.path.dirname(file_loc), exist_ok=True)

                # Receive the file data and save it
                with open(file_loc, "wb") as file:
                    chunk = client_socket.recv(1024)
                    if not chunk:
                        break
                    while chunk:
                        file.write(chunk)
                        chunk = client_socket.recv(1024)

                print(
                    f"File {chunk_name.split('/')[-1]} received and saved successfully\n"  # noqa E501
                )
        except Exception as e:
            print(f"Error receiving file: {e}")

        finally:
            client_socket.close()


if __name__ == "__main__":
    # Define the server address and port
    server_address = ("0.0.0.0", 65432)

    start_server(server_address)
