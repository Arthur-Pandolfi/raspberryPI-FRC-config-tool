import gc
import asyncio
from _utils import environment, logs
from networktables import NetworkTables

LOGS_PATH = "./logs/startup.log"
logs.create_log(LOGS_PATH)

async def _connect_network_tables() -> bool:
    roboRIO_ip = environment.get_environment_var("ROBORIO_IP")
    NetworkTables.initialize(roboRIO_ip)

    logs.write_log(LOGS_PATH, f"Connecting to network tables {logs.get_time()} \n")
    while not NetworkTables.isConnected():
        await asyncio.sleep(delay=0.5)
    logs.write_log(LOGS_PATH, f"Connected to network tables! {logs.get_time()} \n")
    
    gc.collect()
    return True

async def _create_table():
    logs.write_log(LOGS_PATH, f"Creating default table {logs.get_time()} \n")
    NetworkTables.getTable(environment.get_environment_var("RASPBERRY_NAME"))
    logs.write_log(LOGS_PATH, f"Default table created! {logs.get_time()} \n")

    gc.collect()

async def _create_subtables():
    logs.write_log(LOGS_PATH, f"Creating subtables {logs.get_time()} \n")
    system_table = NetworkTables.getTable(environment.get_environment_var("RASPBERRY_NAME")).getSubTable("System")
    system_table.getSubTable("Config")    
    logs.write_log(LOGS_PATH, f"Config subtable created {logs.get_time()} \n")
    system_table.getSubTable("Infos")
    logs.write_log(LOGS_PATH, f"Infos subtable created {logs.get_time()} \n")
    logs.write_log(LOGS_PATH, f"All subtables created! {logs.get_time()} \n")
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
    infos_table = table.getSubTable("Infos")  
    
    infos_table.getEntry("Hardware_Usage").setStringArray([""])
    infos_table.getEntry("CPU_Count").setNumber(0)
    infos_table.getEntry("Memory_Info").getDoubleArray(0.0)
    infos_table.getEntry("Coral_is_available").setBoolean(False)
    infos_table.getEntry("IP").setString("")
    infos_table.getEntry("RAM").setDoubleArray([0.0])
    infos_table.getEntry("Hearthbeat").setBoolean(False)
    infos_table.getEntry("Status").setString("")
    infos_table.getEntry("Error").setStringArray([""])

async def _create_entrys():
    logs.write_log(LOGS_PATH, f"Creating entrys {logs.get_time()} \n")
    
    await _create_system_substable_entrys()
    await _create_infos_subtable_entrys()

    logs.write_log(LOGS_PATH, f"All entrys created! {logs.get_time()} \n")
    NetworkTables.flush()
    gc.collect()

# -------------------------------------------- Network Initialization -----------------------------------------------

async def _network_tables():
    await _connect_network_tables()
    await _create_table()
    await _create_subtables()
    await _create_entrys()

# -------------------------------------------- Network Initialization -----------------------------------------------

async def main():
    routine1 = asyncio.create_task(_network_tables())

    await asyncio.gather(
        routine1
    )

if __name__ == "__main__":
    asyncio.run(main())
