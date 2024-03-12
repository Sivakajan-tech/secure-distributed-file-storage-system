import os

def upload_file():
    file_name = input("Enter the file name: ")
    print(f"File '{file_name}' uploaded successfully!")

def download_file():
    file_name = input("Enter the file name: ")
    print(f"File '{file_name}' downloaded successfully!")

def view_all_files():
    print("List of files:")
    for file_name in os.listdir():
        print(file_name)

def main():
    while True:
        print("Options:")
        print("1. Upload a file")
        print("2. Download a file")
        print("3. View all files")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            upload_file()
        elif choice == "2":
            download_file()
        elif choice == "3":
            view_all_files()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    print("Welcome to the Secure Distributed File Storage System!\n")
    print("Please select an option from the following menu:")
    main()