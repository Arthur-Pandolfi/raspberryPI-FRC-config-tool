import gc
import psutil
import asyncio
import subprocess
from _utils import environment, logs
from _utils.networktables import update_values
from networktables import NetworkTables

LOGS_PATH = "/home/frc_os/frc_os/logs/"
LOGS_NAME = "/home/frc_os/frc_os/logs/startup.log"

def _get_ip():
    ip = subprocess.run(["ifconfig eth0 | grep inet"], shell=True,  capture_output=True, text=True)
    ip = ip.stdout.split()
    return ip[1]

# ----------------------------------------- Network Tables initialization -----------------------------------------
async def _connect_network_tables() -> bool:
    roboRIO_ip = environment.get_environment_var("ROBORIO_IP")
    NetworkTables.initialize(roboRIO_ip)

    logs.write_log(LOGS_NAME, f"Connecting to network tables // IP: {roboRIO_ip} // {logs.get_time()} \n")
    while not NetworkTables.isConnected():
        await asyncio.sleep(delay=0.5)
    logs.write_log(LOGS_NAME, f"Connected to network tables! {logs.get_time()} \n")
    
    gc.collect()
    return True

async def _create_table():
    logs.write_log(LOGS_NAME, f"Creating default table {logs.get_time()} \n")
    NetworkTables.getTable(environment.get_environment_var("RASPBERRY_NAME"))
    logs.write_log(LOGS_NAME, f"Default table created! {logs.get_time()} \n")

    gc.collect()

async def _create_subtables():
    logs.write_log(LOGS_NAME, f"Creating subtables {logs.get_time()} \n")
    system_table = NetworkTables.getTable(environment.get_environment_var("RASPBERRY_NAME")).getSubTable("System")
    system_table.getSubTable("Config")    
    logs.write_log(LOGS_NAME, f"Config subtable created {logs.get_time()} \n")
    system_table.getSubTable("Infos")
    logs.write_log(LOGS_NAME, f"Infos subtable created {logs.get_time()} \n")
    logs.write_log(LOGS_NAME, f"All subtables created! {logs.get_time()} \n")
    gc.collect()    

async def _create_system_substable_entrys():
    table = NetworkTables.getTable(environment.get_environment_var("RASPBERRY_NAME"))
    system_table = table.getSubTable("System")
    config_table = system_table.getSubTable("Config")    

    # Config subtable entrys
    config_table.getEntry("Network").setStringArray("")
    config_table.getEntry("Commands").setStringArray("")
    config_table.getEntry("Max_CPU_Usage").setString("")

async def _create_infos_subtable_entrys():
    table = NetworkTables.getTable(environment.get_environment_var("RASPBERRY_NAME"))
    system_table = table.getSubTable("System")
    infos_table = system_table.getSubTable("Infos")
      
    disk_total, disk_used, disk_free = await update_values.get_disk_usage()
    ram_total, ram_usage, ram_free = await update_values.get_ram()
    
    cpu_count = psutil.cpu_count()
    cpu_temp = 50 
    cpu_usage = await update_values.get_cpu_usage()
    # Im dont using this function bacause im emualting the ubuntu in WSL 2.0, and don't have sesnors to get CPU temp 
    # await update_values.get_cpu_temperature()
    

    infos_table.getEntry("CPU_Info").setStringArray([cpu_count, cpu_usage, f"{cpu_temp}Cº"])
    infos_table.getEntry("Disk_info").setStringArray([f"{disk_total:.2f} GB", f"{disk_used:.2f} GB", f"{disk_free:.2f} GB"])
    infos_table.getEntry("Coral_is_available").setBoolean(False)
    infos_table.getEntry("IP").setString(_get_ip())
    infos_table.getEntry("RAM").setStringArray([f"{ram_total:.2f}", f"{ram_usage:.2f}",f"{ram_free:.2f}"])
    infos_table.getEntry("Hearthbeat").setBoolean(True)
    infos_table.getEntry("Status").setString("Starting vision script")
    infos_table.getEntry("Error").setStringArray([""])

    gc.collect()

async def _create_entrys():
    logs.write_log(LOGS_NAME, f"Creating entrys {logs.get_time()} \n")
    
    await _create_system_substable_entrys()
    await _create_infos_subtable_entrys()

    logs.write_log(LOGS_NAME, f"All entrys created! {logs.get_time()} \n")
    NetworkTables.flush()
    gc.collect()
# ----------------------------------------- Network Tables initialization -----------------------------------------

# Main functions
async def _network_tables():
    await _connect_network_tables()
    await _create_table()
    await _create_subtables()
    await _create_entrys()


async def main():
     logs.create_log(LOGS_PATH, LOGS_NAME)
     await _network_tables()


if __name__ == "__main__":
    asyncio.run(main())
