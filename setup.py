import os
import argparse
import subprocess
from time import sleep
from ._utils import config, errors

os.system("clear")
config.reset_envs()

RED = '\033[91m'
GREEN = '\033[32m'
RESET = '\033[0m'

# --------------------------------------------- Arguments configuration ---------------------------------------------
parser = argparse.ArgumentParser(
    description="A script taht help configures a RaspberryPI for FRC"
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
    command_in_frc = "sudo nmcli con up FRC-Scenario"
    command_outside_frc = "sudo nmcli con down FRC-Scenario / sudo nmcli con up World-Wide-Web-Scenario"

    config.set_roboRIO_ip()
    config.set_raspberry_name()
    ip, netmask, gateway = config.get_wanted_ip()
    config.setup_network(gateway, ip, netmask)
    print(GREEN + f"\nTo use the raspberry outside of FRC scneario, use the command: {command_outside_frc}\n" + RESET)
    print(GREEN + f"\nTo use the raspberry inside of FRC scneario, use the command: {command_in_frc}\n" + RESET)

def _install_dependencies():
    dependencies = [
            "ufw", "git", "curl", "wget", "build-essential", "make", \
            "build-essential", "libssl-dev", "zlib1g-dev", "libffi-dev", "liblzma-dev", \
            "numactl", "network-manager", "btop", "htop"
        ]
    
    for dependency in dependencies:
        print()
        print(f"Downloading depndency: {dependency}")
        result = subprocess.run(f"sudo apt install {dependency} -y", shell=True)
        if result.returncode == 0:
            print("Dependency installed successfully")
        else:
            print(RED + "failed to install the dependency: " + RESET + dependency)

    os.system("clear")

def _setup_dependencies():  
    subprocess.run("sudo ufw allow 22/tcp", shell=True, stdout=subprocess.DEVNULL)
    subprocess.run("sudo systemctl enable NetworkManager", shell=True, stdout=subprocess.DEVNULL)

def _setup_shell():
    # Download ZSH and Oh My Zsh
    user = os.environ.get("SUDO_USER", os.environ["USER"])   
    print("Downloading ZSH")
    subprocess.run(
        "sudo apt install zsh -y", 
        shell=True,
        stdout=subprocess.DEVNULL
    )
    
    print("Downloading Oh My Zsh")
    subprocess.run(
        f'sudo HOME=/home/{user} sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"',
        input="y\n",
        shell=True,
        text=True,
        stdout=subprocess.DEVNULL
    )

    # Change the shell to ZSH
    print("Changing shell to ZSH")

    subprocess.run(
        f"sudo chsh -s /bin/zsh {user}",
        shell=True,
        stdout=subprocess.DEVNULL
    )

    # Download Powerlevel10k and set for default theme
    print("Downloading pwoerlevel10k")
    subprocess.run(
        f"git clone --depth=1 https://github.com/romkatv/powerlevel10k.git /home/{user}/powerlevel10k",
        shell=True,
        stdout=subprocess.DEVNULL
    )

    print("Setting the powerlevel10k as default theme")
    subprocess.run(
        f"echo 'source /home/{user}/powerlevel10k/powerlevel10k.zsh-theme' >>/home/{user}/.zshrc",
        shell=True,
        stdout=subprocess.DEVNULL
    )

    # Config the plugins
    # Auto suggestions
    print("Setuping extensions...")
    subprocess.run(
        f"git clone https://github.com/zsh-users/zsh-autosuggestions /home/{user}/.zsh/zsh-autosuggestions",
        shell=True,
        stdout=subprocess.DEVNULL
    )

    subprocess.run(
        f"echo 'source /home/{user}/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh' >> ${{ZDOTDIR:-/home/user{user}/.zshrc}}",
        shell=True,
        stdout=subprocess.DEVNULL
    )

    # Syntax Highlything
    subprocess.run(
        f"git clone https://github.com/zsh-users/zsh-syntax-highlighting.git /home/{user}/.zsh/zsh-syntax-highlighting",
        shell=True,
        stdout=subprocess.DEVNULL
    )

    subprocess.run(
        f"echo 'source /home/{user}/.zsh/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh' >> ${{ZDOTDIR:-/home/{user}/.zshrc}}",
        shell=True,
        stdout=subprocess.DEVNULL
    )

    # Add the backward-word and forward-word using Ctrl + Arrow and pyenv auto eval venvs
    with open(f"/home/{user}/.zshrc", "a") as file:
        if file.writable():
            lines = [
                '\nbindkey "^[[1;5C" forward-word\n',
                'bindkey "^[[1;5D" backward-word\n',
                'export PYENV_ROOT="$HOME/.pyenv"\n',
                '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"\n',
                'eval "$(pyenv init - zsh)"\n',
                'eval "$(pyenv virtualenv-init -)"\n'
            ]
            
            file.writelines(lines)

    print(f"Removing the only root permission on home directory... {user}")
    subprocess.run(
        f"sudo chown -R {user}:{user} /home/{user}/",
        shell=True,
        stdout=subprocess.DEVNULL
    )

    print("Shell setup with succes!")
    sleep(2)
    os.system("clear")

def main():
    print("Downloading requireds dependencies...")
    _install_dependencies()
    print("All dependencies downloaded!\n")
    _setup_dependencies()

    print("This script requires python <=3.11")
    setup_shell = input("Do you want to setup the shell to ZSH with pwoerlevel10k (requires a nerd font) Y/N ")
    if setup_shell.lower().strip() == "y":
        _setup_shell()
    
    if execution_type == "total":   
        python_path = input("Please, put the full path for your python 3.11 binary directory (ex: /python3.11/bin/): ").strip()
        config.create_service()
        config.setup_autorun_scripts(python_path)
        _team_number_config()
        _network_config()
    elif execution_type == "network":
        _network_config()
    else:
        raise errors.InvalidArgumentError("Invalid argument, use --type to run the configuration mode "
        "('total' for configure everything or 'network' to configure only the network)")

    print("\nEnd of setup!\n")
    if input("Do you want to reboot now [Y/N]: ").strip().lower() == "y":
        print("Rebooting to apply changes...")
        subprocess.run("sudo reboot", shell=True)

if __name__ == "__main__":
    main()
