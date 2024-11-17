import os 
from dotenv import load_dotenv
import os
import shutil


load_dotenv()

ROOT_DIR = os.getenv('ROOT_DIR')

def delete_files_in_folder(folder_path):
    try:
        # Check if the folder exists
        if not os.path.exists(folder_path):
            print(f"The folder '{folder_path}' does not exist.")
            return

        # Iterate over all items in the folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

        print(f"All files in '{folder_path}' have been deleted.")
    except Exception as e:
        print(f"An error occurred: {e}")


def delete_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File '{file_path}' has been deleted successfully.")
        else:
            print(f"The file '{file_path}' does not exist.")
    except PermissionError:
        print(f"Permission denied: Unable to delete '{file_path}'.")
    except Exception as e:
        print(f"An error occurred while trying to delete '{file_path}': {str(e)}")

def create_directory_if_not_exists(directory_path):
    # Check if the directory exists
    if not os.path.exists(directory_path):
        try:
            # Create the directory
            os.makedirs(directory_path)
            print(f"Directory created: {directory_path}")
        except OSError as e:
            print(f"Error creating directory {directory_path}: {e}")
    else:
        print(f"Directory already exists: {directory_path}")

def copy_file(source_path, destination_path):
    try:
        shutil.copy2(source_path, destination_path)
        print(f"File copied successfully from {source_path} to {destination_path}")
    except IOError as e:
        print(f"Unable to copy file. {e}")
    except:
        print("Unexpected error occurred while copying file.")

def append_text_to_file(file_path, text):
    try:
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(text)
            print(f"Text successfully appended to {file_path}")
    except IOError:
        print(f"Error: An I/O error occurred while writing to the file at {file_path}.")


def read_text_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except IOError:
        print(f"Error: An I/O error occurred while reading the file at {file_path}.")

def write_to_file(filename, text, mode='w', encoding='utf-8'):
    try:
        with open(filename, mode, encoding=encoding) as file:
            file.write(text)
        print(f"Text successfully written to {filename}")
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")
    except UnicodeEncodeError as e:
        print(f"A Unicode encoding error occurred: {e}")
        print("Try using a different encoding, such as 'utf-8' or 'utf-16'")