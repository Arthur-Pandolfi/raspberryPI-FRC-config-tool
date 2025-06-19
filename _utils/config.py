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
    name = input("Enter the wanted name to show in NetworkTables [0 for the user name]: ")

    if name == "0":
        user_name = subprocess.run("whoami", shell=True, capture_output=True, text=True)
        name = f"raspberry-{user_name.stdout}"
        return name
    else:
        return name

# Set functions
def reset_envs():
    with open("/etc/environment", "w+"):
        pass

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
    netmask_to_cidr = {
    "255.0.0.0":        "/8",
    "255.255.0.0":      "/16",
    "255.255.255.0":    "/24",
    "255.255.255.128":  "/25",
    "255.255.255.192":  "/26",
    "255.255.255.224":  "/27",
    "255.255.255.240":  "/28",
    "255.255.255.248":  "/29",
    "255.255.255.252":  "/30",
    "255.255.255.255":  "/32"
    }

    ip_config_file = f"""
    interface eth0
    static ip_address={ip}{netmask_to_cidr[netmask]}
    static routers={ip}
    static domain_name_servers=8.8.8.8 1.1.1.1
    """

    with open("/etc/dhcpcd.conf", "a") as file:
        file.write("\n" + ip_config_file)

#----------------------------------------------- Basic Configurations -----------------------------------------------

#----------------------------------------------- Boot Configurations ------------------------------------------------
def setup_crontab():
    cron_job = "@reboot /home/frc_os/frc_os/.venv/bin/python /home/frc_os/startup.py >> /home/frc_os/logs/startup.log 2>&1\n"

    result = subprocess.run("crontab -l", shell=True, capture_output=True, text=True)
    current_crontab = result.stdout if result.returncode == 0 else ""

    if cron_job in current_crontab:
        print("The crontab is already configured")
        return

    updated_crontab = current_crontab + cron_job
    result = subprocess.run("crontab -", shell=True, input=updated_crontab, text=True)

#----------------------------------------------- Boot Configurations ------------------------------------------------
