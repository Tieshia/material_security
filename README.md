# Filesystem

## Table of Contents

- [Getting Started](#getting-started)
- [Filesystem Operations](#filesystem-operations)
- [Additional Operations](#additional-operations)
- [Note](#note)

## Getting Started

To use the `Filesystem` class, follow these steps:

1. Clone and open the repo.
2. Run `pip3 install -r requirements.txt`
3. Open the python interpreter by running `python3`
2. **Import the `Filesystem` class:**

    ```python
    from filesystem import Filesystem
    ```

3. **Create an instance of the `Filesystem` class:**

    ```python
    fs = Filesystem()
    ```

    This initializes the filesystem with a root directory (`/`) and sets the current working directory (`pwd`) to the root.
4. Run tests on the `Filesystem` class by calling `python3 -m unittest test_filesystem.py`

## Filesystem Operations

### Working with Directories

- **List the contents of the current directory:**
  
    ```python
    contents = fs.listdir()
    ```

- **Make a new directory:**

    ```python
    fs.makedir("new_directory")
    ```

- **Change the current working directory:**

    ```python
    fs.changedir("path/to/directory")
    ```

- **Remove a directory:**

    ```python
    fs.removedir("directory_to_remove")
    ```

- **Move a directory:**

    ```python
    fs.movedir("source_directory", "destination_directory")
    ```

### Working with Files

- **Create an file or append text to an existing file:**

    ```python
    fs.touch("new_filename.txt", content="")
    ```

- **Read the content of a file:**

    ```python
    content = fs.readtext("existing_file.txt")
    ```

- **Move a file:**

    ```python
    fs.movefile("source_file.txt", "destination_directory/new_file.txt")
    ```

- **Remove a file:**

    ```python
    fs.removefile("file_to_remove.txt")
    ```

- **Copy a file:**

    ```python
    fs.copyfile("source_file.txt", "destination_directory/new_file.txt")
    ```

### Additional Operations

- **Get the current working directory:**

    ```python
    current_directory = fs.pwd()
    ```

- **Find files matching a pattern:**

    ```python
    matched_files = fs.find("*.txt")
    ```

## Note

- The filesystem uses a simplified path processing logic to handle operations on paths.

Feel free to explore and customize the `Filesystem` class based on your specific use case!
