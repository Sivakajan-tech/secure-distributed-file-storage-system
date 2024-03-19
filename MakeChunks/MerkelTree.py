import hashlib


class MerkleTree:
    def __init__(self, file_path, chunk_size=1024):
        self.file_path = file_path
        self.chunk_size = chunk_size
        self.chunks = self.chunk_file()
        self.tree = self.build_tree()

    def chunk_file(self):
        with open(self.file_path, "rb") as file:
            while True:
                chunk = file.read(self.chunk_size)
                if not chunk:
                    break
                yield chunk

    def build_tree(self):
        tree = []
        # Generate leaf nodes by hashing each chunk
        for chunk in self.chunks:
            hash_value = hashlib.sha256(chunk).hexdigest()
            tree.append(hash_value)

        # Build the tree from the bottom up
        level = tree[:]
        while len(level) > 1:
            new_level = []
            # Pair adjacent nodes and hash them together
            for i in range(0, len(level), 2):
                if i + 1 < len(level):
                    combined_hash = hashlib.sha256(
                        (level[i] + level[i + 1]).encode()
                    ).hexdigest()
                    new_level.append(combined_hash)
                else:
                    # If there's an odd number of nodes, duplicate the last one
                    new_level.append(level[i])
            level = new_level
            tree.extend(new_level)

        return tree

    def root_hash(self):
        return self.tree[0]


# Example usage
if __name__ == "__main__":
    file_path = "03 - Communication in Distributed Systems.pdf"
    merkle_tree = MerkleTree(file_path)
    print("Merkle Root Hash:", merkle_tree.root_hash())
