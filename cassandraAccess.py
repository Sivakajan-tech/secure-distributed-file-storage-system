from cassandra.cluster import Cluster
import uuid
from datetime import datetime

# Connect to Cassandra
cluster = Cluster(['localhost'])
session = cluster.connect('file_metadata')

# Insert data
for i in range(3):  # Inserting 3 different files
    # Generate a UUID for file_id
    file_id = uuid.uuid4()

    # Convert string date to datetime object
    upload_date = datetime.strptime('2024-04-20', '%Y-%m-%d')

    # Prepare insert query
    insert_query = session.prepare(
        "INSERT INTO file_metadata_table (" + 
        "file_id, file_name, file_size, file_type, upload_date" +
        ") VALUES (?, ?, ?, ?, ?)"
    )

    # Execute insert query
    session.execute(
        insert_query,
        [file_id, f'test{i+1}', 10 * (i+1), 'pdf', upload_date]
    )

# Query data
select_query = "SELECT file_id, file_name, file_size, " + 
"file_type, upload_date FROM file_metadata_table"
result = session.execute(select_query)
for row in result:
    file_id = row.file_id
    file_name = row.file_name
    file_size = row.file_size
    file_type = row.file_type
    upload_date = row.upload_date.date()  # Extracting date part

    print("File ID:", file_id)
    print("File Name:", file_name)
    print("File Size:", file_size)
    print("File Type:", file_type)
    print("Upload Date:", upload_date)

# Close connection
session.shutdown()
cluster.shutdown()
