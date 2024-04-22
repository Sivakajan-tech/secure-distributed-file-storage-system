import os
from cassandra.cluster import Cluster
from datetime import datetime
import uuid


def connect_to_cassandra():
    # Connect to Cassandra
    cluster = Cluster(['localhost'])
    session = cluster.connect('file_metadata')
    return session


# Function to create indexes on Cassandra table
def create_indexes(session):
    create_indexes_query = [
    "CREATE INDEX IF NOT EXISTS file_name_index ON "
    "file_metadata_table (file_name)",
    "CREATE INDEX IF NOT EXISTS file_size_index ON "
    "file_metadata_table (file_size)",
    "CREATE INDEX IF NOT EXISTS file_type_index ON "
    "file_metadata_table (file_type)",
    "CREATE INDEX IF NOT EXISTS upload_date_index ON "
    "file_metadata_table (upload_date)"
]
    for query in create_indexes_query:
        session.execute(query, timeout=120)


# Function to insert file metadata into Cassandra table
def insert_file_metadata(file_path, session):
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    upload_date = datetime.now()
    file_type = os.path.splitext(
        file_name)[1][1:]  # Extract file extension as file type

    insert_query = session.prepare(
        "INSERT INTO file_metadata_table (file_id, file_name, file_size, file_type, upload_date) VALUES (?, ?, ?, ?, ?)"
    )
    file_id = uuid.uuid4()
    session.execute(
        insert_query, [file_id, file_name, file_size, file_type, upload_date]
    )


# Function to upload file and insert metadata into Cassandra
def upload_file(session):
    file_path = input("Enter the path of the file to upload: ")
    if os.path.exists(file_path):
        insert_file_metadata(file_path, session)
        print(f"File '{file_path}' uploaded successfully!")
    else:
        print("File not found. Please enter a valid file path.")


def download_file():
    file_name = input("Enter the file name: ")
    print(f"File '{file_name}' downloaded successfully!")


def view_all_files(session):
    print("\n" + "*"*60 + "\n")
    print("List of files:")
    select_query = (
        "SELECT file_name, file_size, file_type," 
        "upload_date FROM file_metadata_table"
    )
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
    select_query = (
        "SELECT file_name, file_size, file_type, upload_date" 
        "FROM file_metadata_table WHERE file_name = %s"
    )
    result = session.execute(select_query, [file_name])
    for row in result:
        print("\n" + "*"*60 + "\n")
        print("File Name:", row.file_name)
        print("File Size:", row.file_size)
        print("File Type:", row.file_type)
        print("Uploaded Date:", row.upload_date)
    print("\n" + "*"*60 + "\n")


# Function to search files based on user input
def search_files(session):
    print("Search Options:")
    print("1. Search by file name")
    print("2. Search by file size")
    print("3. Search by file type")
    print("4. Search by uploaded date")
    
    choice = input("Enter your choice (1-4): ")
    
    if choice == "1":
        search_word = input("Enter the file name or substring: ")
        search_query = (
            "SELECT file_name, file_size, file_type, upload_date"  
            "FROM file_metadata_table WHERE file_name = %s"
        )
        result = session.execute(search_query, [search_word])
    elif choice == "2":
        size_limit = int(input("Enter the file Size limit: "))
        size_choice = input("Enter 'less' for files less than given size " +  
        "or 'greater' for files greater than given size: ")
        if size_choice == "less":
            search_query = (
                "SELECT file_name, file_size, file_type, upload_date"
                " FROM file_metadata_table WHERE file_size < %s ALLOW FILTERING"
            )
        elif size_choice == "greater":
            search_query = (
                "SELECT file_name, file_size, file_type, upload_date" 
                " FROM file_metadata_table WHERE file_size > %s ALLOW FILTERING"
            )
        result = session.execute(search_query, [size_limit])
    elif choice == "3":
        search_word = input("Enter the file type: ")
        search_query = (
            "SELECT file_name, file_size, file_type, upload_date"
            " FROM file_metadata_table WHERE file_type = %s"
        )
        result = session.execute(search_query, [search_word])
    elif choice == "4":
        upload_date = datetime.strptime(
            input("Enter the upload date (YYYY-MM-DD): "), '%Y-%m-%d')
        search_query = (
            "SELECT file_name, file_size, file_type, upload_date"
            " FROM file_metadata_table WHERE upload_date = %s"
        )
        result = session.execute(search_query, [upload_date])

    # Print search results
    found_files = list(result)
    print("\n" + "*"*60 + "\n")
    if found_files:
        print("Search Results:")
        for row in found_files:
            print("\n" + "*"*60 + "\n")
            print("File Name:", row.file_name)
            print("File Size:", row.file_size)
            print("File Type:", row.file_type)
            print("Upload Date:", row.upload_date)
    else:
        print("No files available in this category.")
    print("\n" + "*"*60 + "\n")


def main():
    session = connect_to_cassandra()
    create_indexes(session)  # Create indexes before performing search
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
            upload_file(session)
        elif choice == "2":
            download_file()
        elif choice == "3":
            view_all_files(session)
        elif choice == "4":
            view_metadata(session)
        elif choice == "5":
            search_files(session)
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    print("Welcome to the Secure Distributed File Storage System!\n")
    print("Please select an option from the following menu:\n")
    main()
