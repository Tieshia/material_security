# Filesystem

**Filesystem Extension for PyFilesystem**

The `Filesystem` class serves as an extension of PyFilesystem's in-memory filesystem, specifically utilizing the MemoryFS module (accessible [here](https://www.pyfilesystem.org/page/memoryfs/)). This extension enhances the capabilities of PyFilesystem's in-memory filesystem by providing methods for efficient management of directories and files within the virtual filesystem. Leveraging the abstraction offered by FS objects, this extension allows developers to write code that remains agnostic to the physical location of files. For instance, a function designed to search for duplicate files in a directory will seamlessly operate on a variety of storage locations, including the local hard drive, zip files, FTP servers, or Amazon S3. This versatility demonstrates the power and flexibility of PyFilesystem's Filesystem extension in enabling consistent and adaptable file management across diverse storage environments.

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

- **Create an empty file:**

    ```python
    fs.touch("new_file.txt")
    ```

- **Append text to a file:**

    ```python
    fs.appendtext("existing_file.txt", "additional text")
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

- **List the directory tree:**

    ```python
    tree_structure = fs.tree()
    ```

- **Find files matching a pattern:**

    ```python
    matched_files = fs.find("*.txt")
    ```

- **Close the filesystem:**

    ```python
    fs.close()
    ```

## Note

- The filesystem uses a simplified path processing logic to handle operations on paths.

- Ensure to call the `close` method when done with the filesystem to clean up resources.

Feel free to explore and customize the `Filesystem` class based on your specific use case!
