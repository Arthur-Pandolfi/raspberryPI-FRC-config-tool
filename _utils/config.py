import gc
import subprocess
from typing import Union
from . import environment

#----------------------------------------------- Basic Configurations -----------------------------------------------
# Get functions
def get_team_number() -> int:
    while True:
        try:
            return int(input("Write your team number here: "))
        except Exception:
            print("\nPlease, write a valid team number\n")

def get_wanted_ip() -> list[str, str]:
    while True:
        try:
            ip = input("Write the wanted IP here: ")
            netmask = input("Write the wanted netmask here (type 0 to default -> 255.255.255.0): ")
            
            if netmask == "0":
                netmask = "255.255.255.0"
            
            return ip, netmask
        
        except Exception:
            print("\nPlease, write a ip and netmask\n")

def get_raspberry_name() -> str:
    name = input("Enter the wanted name to show in NetworkTables [0 for the user name]")

    if name == "0":
        user_name = subprocess.run(["awk -F: '{ print $1 }' /etc/passwd | grep 'frc-'"], shell=True, capture_output=True, text=True)
        return user_name
    else:
        return name

# Set functions
def set_raspberry_name():
    name = get_raspberry_name()
    environment.add_environment_var(f"RASPBERRY_NAME={name}")

def set_team_number(number: int) -> Union[None, FileNotFoundError]:
    environment.add_environment_var(f"TEAM_NUMBER={number}")
    gc.collect()

def set_roboRIO_ip() -> None:
    base_ip = "roborio-TEAM-frc.local"
    team_number = environment.get_environment_var(val="TEAM_NUMBER")
    base_ip = base_ip.split("-")
    base_ip[1] = team_number
    
    # Convert to string
    final_ip = " ".join(base_ip)
    
    # Convert to a formated string
    final_ip = final_ip.replace(" ", "-")

    environment.add_environment_var(val=f"ROBORIO_IP={final_ip}")
    gc.collect()

def set_rasp_ip(ip: str, netmask: str = "255.255.255.0") -> None:
    subprocess.run(f"ifconfig eth0 {ip} netmask {netmask}", shell=True, capture_output=True, text=True)
    gc.collect()
#----------------------------------------------- Basic Configurations -----------------------------------------------

#----------------------------------------------- Boot Configurations ------------------------------------------------
def setup_contrab():
    with open("/var/spool/cron/crontabs/root", "a") as file:
        file.write("@reboot /bin/bash -c '/home/frc_os/.pyenv/versions/3.9.13/bin/python3 /home/frc_os/startup.py >> /home/frc_os/logs/startup_output.log 2>&1'")
#----------------------------------------------- Boot Configurations ------------------------------------------------
