from psutil import virtual_memory, cpu_percent, disk_usage
from gpiozero import CPUTemperature
from networktables import NetworkTables
from .. import environment

async def get_ram():
    ram = virtual_memory()
    ram_total = ram.total / (1024 ** 3)
    ram_usage = ram.used / (1024 ** 3)
    ram_free = ram.free / (1024 ** 3)

    return ram_total, ram_usage, ram_free

async def get_cpu_usage():
    return cpu_percent(interval=1)

async def get_cpu_temperature():
    cpu = CPUTemperature()
    return cpu.temperature

async def get_disk_usage():
    disk = disk_usage("/")
    disk_total = disk.total / (1024 ** 3)
    disk_used = disk.used / (1024 ** 3)
    disk_free = disk.free / (1024 ** 3)

    return disk_total, disk_used, disk_free

async def update_ram():
    ram_entry = NetworkTables.getTable(environment.get_environment_var("RASPBERRY_NAME")).getSubTable("System").getSubTable("Infos").getEntry("RAM")
    while True:
        ram_total, ram_usage, ram_free = await get_ram()
        ram_entry.setStringArray([f"{ram_total:.2f}", f"{ram_usage:.2f}", f"{ram_free:.2f}"])
