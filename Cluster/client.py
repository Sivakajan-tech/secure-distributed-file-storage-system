import socket
from typing import List


def get_ip_port(file_name) -> List[str:str]:
    ip_map = {}
    with open(file_name, "r") as file:
        # Read lines one by one
        for line in file:
            # Split the line into IP address and port number
            ip, port = line.strip().split()
            ip_map[ip] = port
    return ip_map


def send_file(client_socket, file_path):
    with open(file_path, "rb") as file:
        data = file.read(1024)
        while data:
            client_socket.send(data)
            data = file.read(1024)


def main():
    ip_map = get_ip_port("client_map.txt")

    # Prompt the client for the file path
    file_path = input("Enter the file path: ")
    file_name = file_path.split("/")[-1]

    for ip, port in ip_map.items():
        try:
            with socket.socket(
                socket.AF_INET, socket.SOCK_STREAM
            ) as client_socket:
                client_socket.connect((ip, int(port)))

                # Listen for incoming connections
                print("Server is listening on {}:{}".format(ip, port))

                client_socket.send(file_name.encode("utf-8"))

                send_file(client_socket, file_path)
                print("File sent successfully")

                # Close the client connection
                client_socket.close()
        except Exception as e:
            print(f"Error sending chunk to {ip}:{port}: {e}")


if __name__ == "__main__":
    main()
