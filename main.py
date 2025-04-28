from ._utils import (
    environment,
    first_boot
)

if (environment.get_environment_var("IS_FIRST_BOOT")):
    first_boot.set_team_number()
    first_boot.set_roboRIO_ip()
    environment.update_environment_var("IS_FIRST_BOOT", False)
    