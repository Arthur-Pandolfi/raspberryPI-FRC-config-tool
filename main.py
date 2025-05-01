from ._utils import (
    config,
    errors
)
import gc
import argparse

# --------------------------------------------- Arguments configuration ---------------------------------------------
parser = argparse.ArgumentParser(
    description="The setup script for the system"
)
parser.add_argument("--type", required=True, type=str)
args = parser.parse_args()
execution_type = args.type
# --------------------------------------------- Arguments configuration ---------------------------------------------

print("Type press Ctrl+C to exit\n")

def _team_number_config():
        number = config.get_team_number()
        config.set_team_number(number=number)


def _network_config():
        config.set_roboRIO_ip()
        ip, netmask = config.get_wanted_ip()
        config.set_rasp_ip(ip, netmask)

if execution_type == "total":
    _team_number_config()
    _network_config()

elif execution_type == "network":
       _network_config()
else:
       raise errors.InvalidArgumentError("Invalid argument, use --type")

gc.collect()
