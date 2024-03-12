import os

def make_chunks(file_path, chunk_size):
    with open(file_path, 'rb') as file:
        file_size = os.path.getsize(file_path)
        num_chunks = file_size // chunk_size + 1

        os.makedirs('chunks', exist_ok=True)

        # Read and write the file in chunks
        for i in range(num_chunks):
            data = file.read(chunk_size)
            chunk_file_path = f'chunks/chunk{i+1}.chunk'
            with open(chunk_file_path, 'wb') as chunk_file:
                chunk_file.write(data)

    print(f'{num_chunks} chunks created successfully.')

file_path = 'MakeChunks/try.txt'
chunk_size = 1024
make_chunks(file_path, chunk_size)