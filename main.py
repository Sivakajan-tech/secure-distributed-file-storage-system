import os
from cassandra.cluster import Cluster


def connect_to_cassandra():
    # Connect to Cassandra
    cluster = Cluster(['localhost'])
    session = cluster.connect('file_metadata')
    return session

def create_index(session):
    # Create index on file_name column
    create_index_query = "CREATE INDEX IF NOT EXISTS file_name_index ON file_metadata_table (file_name)"
    session.execute(create_index_query)

def upload_file():
    file_name = input("Enter the file name: ")
    print(f"File '{file_name}' uploaded successfully!")


def download_file():
    file_name = input("Enter the file name: ")
    print(f"File '{file_name}' downloaded successfully!")

def view_all_files(session, search_query=None):
    print("List of files:")
    if search_query:
        # need to be implemented
        print("Need to be implemented")
        result = []
    else:
        select_query = "SELECT file_name, file_size, file_type, upload_date FROM file_metadata_table"
        result = session.execute(select_query)
    for row in result:
        print("\n" + "*"*60 + "\n")
        print("File Name:", row.file_name)
        print("File Size:", row.file_size)
        print("File Type:", row.file_type)
        print("Upload Date:", row.upload_date)
    print("\n" + "*"*60 + "\n")


def view_metadata(session):
    file_name = input("Enter the specific file name: ")
    select_query = "SELECT file_name, file_size, file_type, upload_date FROM file_metadata_table WHERE file_name = %s"
    result = session.execute(select_query, [file_name])
    for row in result:
        print("\n" + "*"*60 + "\n")
        print("File Name:", row.file_name)
        print("File Size:", row.file_size)
        print("File Type:", row.file_type)
        print("Uploaded Date:", row.upload_date)
    print("\n" + "*"*60 + "\n")


def main():
    session = connect_to_cassandra()
    create_index(session)
    while True:
        print("Options:")
        print("1. Upload a file")
        print("2. Download a file")
        print("3. View all files")
        print("4. View metadata for a specific file")
        print("5. Search files")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            upload_file()
        elif choice == "2":
            download_file()
        elif choice == "3":
            view_all_files(session)
        elif choice == "4":
            view_metadata(session)
        elif choice == "5":
            search_query = input("Enter search query: ")
            view_all_files(session, search_query)
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    print("Welcome to the Secure Distributed File Storage System!\n")
    print("Please select an option from the following menu:\n")
    main()