import os

def combine_chunks(directory, output_file):
    with open(output_file, 'wb') as outfile:
        for index,filename in enumerate(os.listdir(directory)):
            if filename.endswith('.chunk'):
                chunk_file = os.path.join(directory, f"chunk{index+1}.chunk")
                with open(chunk_file, 'rb') as infile:
                    outfile.write(infile.read())


directory = 'chunks'
output_file = 'try.txt'
combine_chunks(directory, output_file)