# Distributed File Storage System

This project is an implementation of a secure and trusted distributed file storage system, developed as a part of the CS4262 Distributed Systems module



## Introduction

The goal of this project is to develop a distributed file storage system that securely segments a given file into equal-sized chunks and distributes them among a cluster of nodes. 
The system should ensure randomness in the distribution process for security reasons and provide mechanisms to validate and verify the integrity of the stored file chunks. 
Additionally, it should offer a user-friendly interface for users to interact with the system, including functionalities for file listing, searching, metadata viewing, 
integrity verification, and file downloading/uploading.



## Features

1. **Random File Chunk Distribution**: The system distributes file chunks among cluster nodes in a random order to enhance security.

2. **Merkle Tree for Data Integrity**: A Merkle Tree is used to ensure data integrity and verify that file chunks have not been tampered with or replaced.

3. **User Interface**: The system provides a simple user interface for users to perform various operations including:
   - Listing and searching for files stored in the system.
   - Viewing metadata such as file name, size, date of storage, and type.
   - Verifying whether a file has been tampered with or not.
   - Downloading files from the distributed storage system.
   - Uploading new files to the system.



## Installation

1. Clone the repository to your local machine:  
       `git clone https://github.com/Sivakajan-tech/secure-distributed-file-storage-system.git`    

2. Install the required dependencies:  
        `cd secure-distributed-file-storage-system`    
        `pip install -r requirements.txt`   

3. Run the system:  



## Usage

Once the system is running, you can interact with it through the provided user interface. Here are some common operations:

- To list all files stored in the system, use the `list_files` command.
- To search for a specific file, use the `search_file <filename>` command.
- To view metadata for a file, use the `view_metadata <filename>` command.
- To verify the integrity of a file, use the `verify_file <filename>` command.
- To download a file from the system, use the `download_file <filename>` command.
- To upload a new file to the system, use the `upload_file <filepath>` command.



## Assumptions

- The cluster consists of a fixed number of nodes (N>2).
- The file segmentation process divides files into equal-sized chunks (C) regardless of the file type or size.
- Security measures such as authentication and access control are assumed to be handled separately outside the scope of this project.

## Contribute

### Lint Checker
This repository enforces consistent code formatting and style using the `black` and `flake8` tools. To ensure your pull requests meet these standards, all formatting and style checks must pass before merging.


## Contributors


- [Shanmugavadivel Gopinath](https://github.com/shangopi) <br>
- [Tharsha Sivapalarajah](https://github.com/Tharsha-Sivapalarajah) <br>
- [Sivakajan Sivaparan](https://github.com/sivakajan-tech) <br>
