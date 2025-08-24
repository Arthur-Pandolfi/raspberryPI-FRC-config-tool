import os
import gc
import time
import argparse
import subprocess
from ._utils import config, errors

os.system("clear")
# config.reset_envs()

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
    command_outside_frc = "sudo nmcli con down FRC-Scenario / sudo nmcli con up World Wide Web Scenario"

    config.set_roboRIO_ip()
    config.set_raspberry_name()
    ip, netmask, gateway = config.get_wanted_ip()
    config.setup_network(gateway, ip, netmask)
    print(f"To use the raspberry outside of FRC scneario, use the command: {command_outside_frc}")

def _install_dependencies():
    dependencies = [
            "ufw", "git", "curl", "wget", "build-essential", "make", \
            "build-essential", "libssl-dev", "zlib1g-dev", "libffi-dev", "liblzma-dev", \
            "network-manager"
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
    print("Downloading ZSH")
    subprocess.run(
        "sudo apt install zsh -y", 
        shell=True,
        stdout=subprocess.DEVNULL
    )
    
    print("Downloading Oh My Zsh")
    subprocess.run(
        'sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"',
        input="y\n",
        shell=True,
        text=True,
        stdout=subprocess.DEVNULL
    )

    # Change the shell to ZSH
    print("Changing shell to ZSH")
    subprocess.run(
        "sudo chsh -s /bin/zsh $USER",
        shell=True,
        stdout=subprocess.DEVNULL
    )

    # Download Powerlevel10k and set for default theme
    print("Downloading pwoerlevel10k")
    subprocess.run(
        "git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ~/powerlevel10k",
        shell=True,
        stdout=subprocess.DEVNULL
    )

    print("Setting the powerlevel10k as default theme")
    subprocess.run(
        "echo 'source ~/powerlevel10k/powerlevel10k.zsh-theme' >>~/.zshrc",
        shell=True,
        stdout=subprocess.DEVNULL
    )

    # Config the plugins
    # Auto suggestions
    print("Setuping extensions...")
    subprocess.run(
        "git clone https://github.com/zsh-users/zsh-autosuggestions ~/.zsh/zsh-autosuggestions",
        shell=True,
        stdout=subprocess.DEVNULL
    )

    subprocess.run(
        "echo 'source ~/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh' >> ${ZDOTDIR:-$HOME}/.zshrc",
        shell=True,
        stdout=subprocess.DEVNULL
    )

    # Syntax Highlything
    subprocess.run(
        "git clone https://github.com/zsh-users/zsh-syntax-highlighting.git",
        shell=True,
        stdout=subprocess.DEVNULL
    )

    subprocess.run(
        "echo 'source ${(q-)PWD}/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh' >> ${ZDOTDIR:-$HOME}/.zshrc",
        shell=True,
        stdout=subprocess.DEVNULL
    )
    print("Shell setup with succes!")
    os.system("clear")

def _setup_pyenv():
    # Download pyenv
    subprocess.run(
        "curl -fsSL https://pyenv.run | bash", 
        shell=True,
        stdout=subprocess.DEVNULL
    )

    # Setup the PATH var's
    pyenv_home = "$HOME/.pyenv"
    pyenv_root = "$PYENV_ROOT/bin:$PATH"
    pyenv_eval = "$(pyenv init - zsh)"

    subprocess.run(
        f"""echo 'export PYENV_ROOT="{pyenv_home}"' >> ~/.zshrc""",
        shell=True,
        stdout=subprocess.DEVNULL
    )

    subprocess.run(
        f"""echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="{pyenv_root}"' >> ~/.zshrc""",
        shell=True,
        stdout=subprocess.DEVNULL
    )

    subprocess.run(
        f"""echo 'eval "{pyenv_eval}"' >> ~/.zshrc""",
        shell=True,
        stdout=subprocess.DEVNULL
    )


def main():
    print("Downloading requireds dependencies...")
    _install_dependencies()
    print("All dependencies downloaded!\n")
    _setup_dependencies()

    setup_shell = input("Do you want to setup the shell to ZSH with pwoerlevel10k (requires a nerd font) Y/N ")
    if setup_shell.lower().strip() == "y":
        _setup_shell()
    
    setup_pyenv = input("Do you want to setup pyenv? Y/N ")
    if setup_pyenv.lower().strip() == "y":
        _setup_pyenv()
        print("restart the terminal to all changes take effect, install python <=3.11, then, restart this script")
        exit()
    else:
        print("if you don't have a python installation, reset the script and download python 3.11")
    
    if execution_type == "total":
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
        subprocess.run("reboot", shell=True)

if __name__ == "__main__":
    main()
