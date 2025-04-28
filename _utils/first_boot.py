import gc
import subprocess
from . import environment

def set_team_number() -> None | FileNotFoundError:
    temp = subprocess.run(["awk -F: '{ print $1 }' /etc/passwd"], shell=True, capture_output=True, text=True)
    users = temp.stdout.split()
    frc_team_number = users[len(users) - 1]
    team_number = frc_team_number.split("-")[1]

    environment.add_environment_var(val=f"TEAM_NUMBER={team_number}")
    gc.collect()


def set_roboRIO_ip() -> None:
    base_ip = "roborio-TEAM-frc.local"
    team_number = environment.get_environment_var(val="TEAM_NUMBER")
    base_ip = base_ip.split("-")
    base_ip[1] = team_number
    
    # Convert to string
    delimiter = " "
    final_ip = delimiter.join(base_ip)
    
    # Convert to a formated string
    final_ip = final_ip.replace(" ", "-")

    environment.add_environment_var(val=f"ROBORIO_IP={final_ip}")
    gc.collect()
