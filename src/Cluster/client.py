import os
import random
import socket
import string
import traceback

from src.MakeChunks.fileBreak import make_chunks
from src.MakeChunks.fileMake import combine_chunks


def generate_random_folder_name(length=8):
    return "".join(random.choices
                   (string.ascii_letters + string.digits, k=length))


def get_ip_port():
    ip_list = []
    with open("client_map.txt", "r") as file:
        # Read lines one by one
        for line in file:
            # Split the line into IP address and port number
            ip, port = line.strip().split()
            ip_list.append((ip, port))
    return ip_list


def send_chunks_to_ip(chunk, chunk_id, folder_name, ip, port):
    chunk_name = f"{folder_name}/Chunk_{chunk_id}"
    try:
        with (socket.socket(socket.AF_INET, socket.SOCK_STREAM)
              as client_socket):
            client_socket.connect((ip, int(port)))
            # Send command name length and command name
            command_name_encoded = "put".encode("utf-8")
            client_socket.sendall(
                len(command_name_encoded).to_bytes(4, byteorder="big")
            )
            client_socket.sendall(command_name_encoded)
            # Send chunk name length and chunk name
            chunk_name_encoded = chunk_name.encode("utf-8")
            client_socket.sendall(len(chunk_name_encoded)
                                  .to_bytes(4, byteorder="big"))
            client_socket.sendall(chunk_name_encoded)

            client_socket.sendall(chunk)  # Send chunk data
            print(f"Chunk_{chunk_id} sent to {ip}:{port}")

            # Close the client connection
            client_socket.close()
    except Exception as e:
        print(f"Error sending chunk to {ip}:{port}: {e}")


def send_chunks(
    folder_name, ip_list, chunk_allocation_plan, primary_nodes, backup_nodes
):
    for i in range(len(chunk_allocation_plan)):
        for j in chunk_allocation_plan[i]:
            chunk_file_path = f"./client_files/"\
                              f"{folder_name}/chunk{j}.chunk"
            with open(chunk_file_path, "rb") as chunk_file:
                chunk = chunk_file.read()
                print(
                    f"Sending Chunk {j} to primary node {primary_nodes[i]} "
                    f"with IP {ip_list[primary_nodes[i]][0]} "
                    f"port {ip_list[primary_nodes[i]][1]}"
                )
                send_chunks_to_ip(
                    chunk,
                    j,
                    folder_name,
                    ip_list[primary_nodes[i]][0],
                    ip_list[primary_nodes[i]][1],
                )
                print(
                    f"Sending Chunk {j} to secondary node {backup_nodes[i]} "
                    f"with IP {ip_list[backup_nodes[i]][0]} "
                    f"port {ip_list[backup_nodes[i]][1]}"
                )
                send_chunks_to_ip(
                    chunk,
                    j,
                    folder_name,
                    ip_list[backup_nodes[i]][0],
                    ip_list[backup_nodes[i]][1],
                )


def choose_nodes(load_details):
    min_load = min(load_details)
    max_load = max(load_details)
    min_max_val = max_load - min_load
    selection_dict = {}
    for i in range(len(load_details)):
        # scaling the load factor
        load_factor = (load_details[i] - min_load) / min_max_val
        random_factor = random.random()
        selection_dict[i] = load_factor + random_factor

    # Get the keys sorted by values (descending order)
    sorted_keys = sorted(selection_dict, key=selection_dict.get, reverse=True)
    primary_nodes = sorted_keys[:3]
    backup_nodes = sorted_keys[3:6]
    return primary_nodes, backup_nodes


def create_chunk_allocation_plan(num_chunks):
    numbers = list(range(1, num_chunks + 1))

    # Initialize 3 empty lists
    list1 = []
    list2 = []
    list3 = []

    # Shuffle the numbers randomly
    random.shuffle(numbers)

    # Distribute numbers evenly among the 3 lists
    for number in numbers:
        # Append to the list with the smallest length
        if len(list1) < len(numbers) // 3:
            list1.append(number)
        elif len(list2) < len(numbers) // 3:
            list2.append(number)
        else:
            list3.append(number)
    return [list1, list2, list3]


def upload_files(file_path, load_details):
    ip_list = get_ip_port()
    CHUNK_SIZE = 1024  # Size of each chunk in bytes
    folder_name = generate_random_folder_name()
    primary_nodes, backup_nodes = choose_nodes(load_details)

    # Step 1: Create chunks and save them in the local
    num_chunks = make_chunks(file_path, CHUNK_SIZE, folder_name)

    chunk_allocation_plan = create_chunk_allocation_plan(num_chunks)

    # Step 2: Send the chunks to different IPs
    send_chunks(
        folder_name,
        ip_list,
        chunk_allocation_plan,
        primary_nodes,
        backup_nodes,
    )


def download_files(folder_name, file_name, nodes):
    try:

        ip_list = get_ip_port()

        for i in nodes:
            with (socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                  as client_socket):
                ip, port = ip_list[i][0], ip_list[i][1]

                client_socket.connect((ip, int(port)))
                # Send command name length and command name
                command_name_encoded = "get".encode("utf-8")
                client_socket.sendall(
                    len(command_name_encoded).to_bytes(4, byteorder="big")
                )
                client_socket.sendall(command_name_encoded)
                # Send chunk name length and chunk name
                folder_name_encoded = folder_name.encode("utf-8")
                client_socket.sendall(
                    len(folder_name_encoded).to_bytes(4, byteorder="big")
                )
                client_socket.sendall(folder_name_encoded)

                while True:
                    # Receive the length of the chunk name
                    chunk_name_len = int.from_bytes(
                        client_socket.recv(4), byteorder="big"
                    )
                    if not chunk_name_len:
                        client_socket.close()
                        break

                    # Receive the chunk name based on the received length
                    chunk_name = client_socket.recv(chunk_name_len).decode("utf-8")
                    if chunk_name == "exit":
                        client_socket.close()
                        break

                    if chunk_name:
                        file_loc = (f"./downloaded_files/{folder_name}/"
                                    f"{chunk_name}")
                        os.makedirs(os.path.dirname(file_loc), exist_ok=True)
                        # Receive the file data and save it
                        with open(file_loc, "wb") as file:
                            chunk = client_socket.recv(1024)
                            if not chunk:
                                print("fsf")
                            file.write(chunk)

            if client_socket:
                client_socket.close()
        combine_chunks(f"./downloaded_files/{folder_name}", "./downloaded.txt")
        print(f"Retrieved chunks for {file_name} from {ip}:{port}")

    except Exception as e:
        print(f"Error receiving chunk to "
              f"{ip}:{port}: {e} {traceback.format_exc()}")

    finally:
        if client_socket:
            client_socket.close()
