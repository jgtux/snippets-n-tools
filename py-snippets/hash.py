import hashlib

# Hash snippets

"""
  Compute the MD5 hash of a file.

  Args:
      path (str): Path to the file.

  Returns:
       str: MD5 hash of the file contents.
"""
def file_hash(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

# Example usage:
# file_hash = file_hash("example.csv")
# print(file_hash)
