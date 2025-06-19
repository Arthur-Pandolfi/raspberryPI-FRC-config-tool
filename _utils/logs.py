import os
from datetime import datetime

def get_time():
    return datetime.now()

def create_log(logs_path: str, log_name: str):
    if not os.path.exists(logs_path):
        os.mkdir(logs_path)

    if not os.path.exists(log_name):
        with open(log_name, "w+"):
            pass

def write_log(log_path: str, content: str):
    with open(log_path, "a") as file:
        file.write(content)
