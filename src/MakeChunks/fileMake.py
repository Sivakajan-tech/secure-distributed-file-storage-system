import os


def combine_chunks(directory, output_file):
    with open(output_file, "wb") as outfile:
        for index in range(len(os.listdir(directory))):
            chunk_file = os.path.join(directory, f"chunk{index+1}.chunk")
            with open(chunk_file, "rb") as infile:
                outfile.write(infile.read())

    print(f"Chunks combined into {output_file} successfully.")
