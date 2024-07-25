import os
import socket

curr_node = 1


def get_ip_port():
    ip_list = []
    with open("../../client_map.txt", "r") as file:
        # Read lines one by one
        for line in file:
            # Split the line into IP address and port number
            ip, port = line.strip().split()
            ip_list.append((ip, port))
    return ip_list


def receive_file(client_socket):
    try:
        # Receive the length of the chunk name
        chunk_name_len = (int.from_bytes
                          (client_socket.recv(4), byteorder="big"))

        # Receive the chunk name based on the received length
        chunk_name = client_socket.recv(chunk_name_len).decode("utf-8")

        if chunk_name:
            file_loc = (f"../../server_files/server-"
                        f"{curr_node}_files/{chunk_name}")
            os.makedirs(os.path.dirname(file_loc), exist_ok=True)

            # Receive the file data and save it
            with open(file_loc, "wb") as file:
                chunk = client_socket.recv(1024)
                if not chunk:
                    raise Exception("Not a chunk file")
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


# Function to send file to client
def send_file(client_socket, client_address):
    # Receive the length of the folder name
    folder_name_len = (int.from_bytes
                       (client_socket.recv(4), byteorder="big"))

    # Receive the folder name based on the received length
    folder_name = client_socket.recv(folder_name_len).decode("utf-8")

    print(folder_name)

    chunk_files_path = (f"../../server_files/server-"
                        f"{curr_node}_files/{folder_name}")
    for chunk_name in os.listdir(chunk_files_path):
        if(chunk_name=='Chunk_65'): continue
        chunk_name_encoded = chunk_name.encode("utf-8")
        client_socket.sendall(len(chunk_name_encoded)
                              .to_bytes(4, byteorder="big"))
        client_socket.sendall(chunk_name_encoded)
        full_path = os.path.join(chunk_files_path, chunk_name)
        # Open and read the file
        with open(full_path, 'rb') as chunk_file:
            chunk = chunk_file.read()
            client_socket.sendall(chunk)  # Send chunk data
            print(
                f"IP - {client_address[0]} Port {client_address[1]} "
                f"{chunk_name} Sent to client. "
            )

    finish_msg_encoded = "exit".encode("utf-8")
    client_socket.sendall(len(finish_msg_encoded)
                              .to_bytes(4, byteorder="big"))
    client_socket.sendall(finish_msg_encoded)




def start_server(server_address):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen(5)
    print("Server started successfully!\n")
    print(f"Server listening on {server_address[0]}:{server_address[1]}")

    while True:
        print("Waiting for a connection...")
        client_socket, client_address = server_socket.accept()
        print(
            f"Connection established from {client_address[0]}:{client_address[1]}"  # noqa E501
        )
        # Receive the length of the command name
        command_name_len = (int.from_bytes
                            (client_socket.recv(4), byteorder="big"))

        # Receive the chunk name based on the received length
        command = client_socket.recv(command_name_len).decode("utf-8")

        if command == 'put':
            receive_file(client_socket)
        elif command == 'get':
            send_file(client_socket, client_address)
        else:
            print("Invalid command received." + command)


if __name__ == "__main__":
    ip_list = get_ip_port()
    # Define the server address and port
    server_address = (ip_list[curr_node][0], int(ip_list[curr_node][1]))

    start_server(server_address)
