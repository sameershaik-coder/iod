import os
import shutil
from pathlib import Path
from dotenv import load_dotenv

PROJECT_DIR = "iod-web"
load_dotenv()
def get_root_directory():
    current_directory = os.getcwd() 
    return current_directory

def get_shared_media_docker_base_directory():
    return "/app/media"