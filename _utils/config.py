import os
import gc
import shutil
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
            gateway = input("Write the gateway here: (the dafult gateway is 10.TE.AM.1): ")
            
            if netmask == "0":
                netmask = "255.255.255.0"
            
            return ip, netmask, gateway
        
        except Exception:
            print("\nPlease, write a ip, gateway and netmask\n")

def get_raspberry_name() -> str:
    name = input("Enter the wanted name to show in NetworkTables [0 for the user name]: ")

    if name == "0":
        user = os.environ.get("SUDO_USER", os.environ["USER"])   
        name = f"raspberry-{user}"
        return name
    else:
        return name

# Set functions
def reset_envs():
    ALL_ENVS = [
        "ROBORIO_IP",
        "TEAM_NUMBER",
        "RASPBERRY_NAME"
    ]

    with open("/etc/environment", "r") as f:
        content = f.readlines()

    new_content = []
    for line in content:
        if not any(line.strip().startswith(env + "=") for env in ALL_ENVS):
            new_content.append(line)

    with open("/etc/environment", "w") as f:
        f.writelines(new_content)

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

def setup_network(gateway: str, ip: str, netmask: str = "255.255.255.0") -> None:
    netmask_to_cidr = {
    "255.0.0.0":        "8",
    "255.255.0.0":      "16",
    "255.255.255.0":    "24",
    "255.255.255.128":  "25",
    "255.255.255.192":  "26",
    "255.255.255.224":  "27",
    "255.255.255.240":  "28",
    "255.255.255.248":  "29",
    "255.255.255.252":  "30",
    "255.255.255.255":  "32"
    }
    
    frc_connection_profile_name = "FRC-scenario"
    www_cnnection_profile_name = "World-Wide-Web-Scenario"

    commands_frc_connection = [
        f'sudo nmcli c add type ethernet ifname eth0 con-name {frc_connection_profile_name}',
        f'sudo nmcli c mod "{frc_connection_profile_name}" ipv4.addres {ip}/{netmask_to_cidr[netmask]}',
        f'sudo nmcli c mod "{frc_connection_profile_name}" ipv4.gateway {gateway}',
        f'sudo nmcli c mod "{frc_connection_profile_name}" ipv4.method manual',
        f'sudo nmcli c mod "{frc_connection_profile_name}" ipv4.dns ""',
    ]

    for command in commands_frc_connection:
        subprocess.run(
            command,
            shell=True,
            stdout=subprocess.DEVNULL
        )

    commands_www_connection = [
        f'sudo nmcli c add type ethernet ifname eth0 con-name "{www_cnnection_profile_name}"',
        f'sudo nmcli c mod "{www_cnnection_profile_name}" ipv4.method auto'
    ]

    for command in commands_www_connection:
        subprocess.run(
            command,
            shell=True,
            stdout=subprocess.DEVNULL
        )

#----------------------------------------------- Basic Configurations -----------------------------------------------

#----------------------------------------------- Boot Configurations ------------------------------------------------
def setup_autorun_scripts(python_binary_path: str) -> None:
    user = os.environ.get("SUDO_USER", os.environ["USER"])   
    os.chdir(f"/home/{user}/raspberryPI-FRC-config-tool/")

    # Create the .sh for start python script
    with open("./scripts/start.sh", "w+") as file:
        lines = [
            "#!/bin/bash\n",
            "cd /opt\n",
            f"{python_binary_path}/python -m InitScripts.startup >> /var/log/startup_script.log\n"
        ]

        for line in lines:
            file.write(line)
    
    subprocess.run(
        "sudo chmod +x ./scripts/start.sh",
        shell=True,
        stdout=subprocess.DEVNULL
    )

    if not os.path.exists("/opt/InitScripts"):
        os.mkdir("/opt/InitScripts") 

    # Move the scripts to the path
    for archive in os.listdir("./scripts"):
        shutil.move(f"./scripts/{archive}", "/opt/InitScripts")

    # Create the .venv and download the required libs
    subprocess.run(
        f"{python_binary_path}/pip install pynetworktables psutil gpiozero",
        shell=True,
        stdout=subprocess.DEVNULL
    )

    # Move the service and start
    shutil.move("startup_service.service", "/etc/systemd/system")
    subprocess.run("sudo systemctl enable startup_service", shell=True, stdout=subprocess.DEVNULL)
#----------------------------------------------- Boot Configurations ------------------------------------------------
