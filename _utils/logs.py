import os
from datetime import datetime

def get_time():
    return datetime.now()

def create_log(log_path: str):
    if not os.path.exists(log_path):
        with open(log_path, "w"):
            pass

def write_log(log_path: str, content: str):
    with open(log_path, "a") as file:
        file.write(content)