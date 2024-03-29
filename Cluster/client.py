import socket


def send_file(client_socket, file_path):
    with open(file_path, "rb") as file:
        data = file.read(1024)
        while data:
            client_socket.send(data)
            data = file.read(1024)


def main():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define the server address and port
    client_address = ("localhost", 65432)

    # Bind the socket to the server address and port
    client_socket.connect(client_address)

    # Listen for incoming connections
    print("Server is listening on {}:{}".format(*client_address))

    # # Prompt the client for the file path
    # file_path = input('Enter the file path: ')

    # file_name = file_path.split('/')[-1]
    client_socket.send("file_name".encode("utf-8"))

    # # Send the file to the client
    # send_file(client_socket, file_path)
    print("File sent successfully")

    # Close the client connection
    client_socket.close()


if __name__ == "__main__":
    main()
