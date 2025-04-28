from .errors import VarNotFound
from typing import Optional, Union

def get_environment_vars() -> str:
    try:
        with open("/etc/environment", "r") as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError("Environment file not found")
    
def get_environment_var(val: str) -> Union[str, int, float, bool]:
    try:
        with open("/etc/environment", "r") as file:
            file_splited = file.read().split()
            for var in file_splited:
                if var.split("=")[0] == val:
                    return var.split("=")[1]
    except FileNotFoundError:
        raise FileNotFoundError("Environment file not found")

def add_environment_var(val: str) -> bool:
    val = f"{val}\n"
    try:
        with open("/etc/environment", "a") as file:
            file.write(val)
            return True
    except FileNotFoundError:
        raise FileNotFoundError("Environment file not found")

def update_environment_var(var: str, new_val: Union[str, int, float, bool]) -> bool:
    str_lines = ""
    new_val = f"{new_val}\n"
    try:
        with open("/etc/environment", "r+") as file:
            lines = file.readlines()
            line_index = -1
            
            for line in lines:
                line_index += 1
                if line.startswith(var + "="):
                    # Separate and update the new value to the list 
                    temp = line.split("=")
                    temp[1] = str(new_val)
                    
                    # Transform the lsit to string
                    delmiter = "="
                    final_archive = delmiter.join(temp)
                    lines[line_index] = final_archive
                    str_lines = "".join(lines)

    except FileNotFoundError:
        raise FileNotFoundError("Environment file not found")

    try:
        # Update the file
        del(file)
        with open("/etc/environment", "w") as file:
            file.write(str_lines)
    except FileNotFoundError:
        raise FileNotFoundError("Environment file not found")
