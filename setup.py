import os
import gc
import time
import argparse
import subprocess
from ._utils import config, errors

os.system("clear")
config.reset_envs()

RED = '\033[91m'
RESET = '\033[0m'

# --------------------------------------------- Arguments configuration ---------------------------------------------
parser = argparse.ArgumentParser(
    description="The setup script for the NetworkTables application"
)
parser.add_argument("--type", required=True, type=str)
args = parser.parse_args()
execution_type = args.type
# --------------------------------------------- Arguments configuration ---------------------------------------------

print("Press Ctrl+C to exit\n")

def _team_number_config():
    number = config.get_team_number()
    config.set_team_number(number=number)

def _network_config():
    config.set_roboRIO_ip()
    config.set_raspberry_name()
    ip, netmask = config.get_wanted_ip()
    config.set_rasp_ip(ip, netmask)

def _install_dependencies():
    dependencies = ["openssh", "ufw", "cronie"]
    
    for dependency in dependencies:
        print()
        print(f"Downloading depndency: {dependency}")
        result = subprocess.run(f"sudo pacman -S {dependency} --noconfirm", shell=True, text=True, capture_output=True)
        if result.returncode == 0:
            print("Dependency installed successfully")
        else:
            print(RED + "failed to install the dependency: " + RESET + dependency)

    os.system("clear")

def _setup_dependencies():  
    subprocess.run("sudo systemctl enable sshd", shell=True, text=True, capture_output=True)
    subprocess.run("sudo ufw allow 22/tcp", shell=True, text=True, capture_output=True)
    subprocess.run("sudo systemctl enable cronie", shell=True, text=True, capture_output=True)
    subprocess.run("sudo systemctl start cronie", shell=True, text=True, capture_output=True)
    config.setup_crontab()

def main():
    print("Downloading requireds dependencies...")
    _install_dependencies()
    print("All dependencies downloaded!\n")
    _setup_dependencies()

    if execution_type == "total":
        _team_number_config()
        _network_config()
    elif execution_type == "network":
        _network_config()
    else:
        raise errors.InvalidArgumentError("Invalid argument, use --type")

    print("\nEnd of setup!\n")
    print("Rebooting to apply changes...")
    subprocess.run("reboot", shell=True, text=True, capture_output=True)

if __name__ == "__main__":
    main()
