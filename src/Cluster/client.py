import socket
import string
import random
from typing import List

from src.MakeChunks.fileBreak import make_chunks
from src.MakeChunks.fileMake import combine_chunks


def generate_random_folder_name(length=8):
    return "".join(
        random.choices(string.ascii_letters + string.digits, k=length)
    )


def get_ip_port(file_name) -> List[str:str]:
    ip_map = {}
    with open(file_name, "r") as file:
        # Read lines one by one
        for line in file:
            # Split the line into IP address and port number
            ip, port = line.strip().split()
            ip_map[ip] = port
    return ip_map


def send_chunks_to_ip(chunk, chunk_id, folder_name, ip, port):
    chunk_name = f"{folder_name}/Chunk_{chunk_id}"
    try:
        with socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        ) as client_socket:
            client_socket.connect((ip, int(port)))

            # Listen for incoming connections
            print("Server is listening on {}:{}".format(ip, port))

            # Send chunk name length and chunk name
            chunk_name_encoded = chunk_name.encode("utf-8")
            client_socket.sendall(
                len(chunk_name_encoded).to_bytes(4, byteorder="big")
            )
            client_socket.sendall(chunk_name_encoded)

            client_socket.sendall(chunk)  # Send chunk data
            print(f"Chunk_{chunk_id} sent to {ip}:{port}")

            # Close the client connection
            client_socket.close()
    except Exception as e:
        print(f"Error sending chunk to {ip}:{port}: {e}")


def send_chunks(folder_name, num_chunks, ip, port):
    for i in range(1, num_chunks + 1):
        chunk_file_path = f"{folder_name}/chunk{i}.chunk"
        with open(chunk_file_path, "rb") as chunk_file:
            chunk = chunk_file.read()
            send_chunks_to_ip(chunk, i, folder_name, ip, port)


if __name__ == "__main__":
    ip_map = get_ip_port("client_map.txt")
    CHUNK_SIZE = 1024  # Size of each chunk in bytes
    folder_name = generate_random_folder_name()

    # Prompt the client for the file path
    file_path = input("Enter the file path: ")
    file_name = file_path.split("/")[-1]

    # todo: Need to add workflow to select random IP using load balancing
    ip, port = list(ip_map.items())[0]

    # Step 1: Create chunks and save them in the local
    num_chunks = make_chunks(file_path, CHUNK_SIZE, folder_name)

    # Step 2: Send the chunks to different IPs
    send_chunks(folder_name, num_chunks, ip, port)

    # Step 3: Combine chunks back into a single file
    OUTPUT_FILE = "/Users/sivakajan/Semester 8/CS4262 - Distributed Systems/secure-distributed-file-storage-system/try_combined.txt"  # noqa E501
    combine_chunks(folder_name, OUTPUT_FILE)
