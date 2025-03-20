import os
import subprocess
import serial.tools.list_ports
from pathlib import Path

#commands to make it work :
#pyinstaller --onefile --hidden-import=esptool esp_builder.py
#python -m PyInstaller --onefile --add-data "Blink.ino.bootloader.bin;." esp_builder.py

# Firmware binary file
bootloader = "Blink.ino.bootloader.bin"
partitions = "Blink.ino.partitions.bin"
boot_app0 = "C:\\Users\\Admin\\AppData\\Local\\Arduino15\\packages\\esp32\\hardware\\esp32\\3.0.7/tools/partitions/boot_app0.bin"
firmware = "Blink.ino.bin"

# Check if the firmware file exists
for file in [bootloader, partitions, boot_app0, firmware]:
    if not Path(file).exists():
        print(f"Error: Required file '{file}' not found. Please check the file name and location.")
        exit(1)

# Function to detect ESP32 serial port
def find_esp32_port():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if "USB" in port.description or "UART" in port.description or "CP210" in port.description or "CH340" in port.description:
            return port.device
    return None

# Get ESP32 port
port = find_esp32_port()

if port:
    print(f"ESP32 detected on {port}. Uploading firmware...")
    command = (
        f"python -m esptool --chip esp32 --port {port} --baud 921600 "
        "--before default_reset --after hard_reset write_flash -e -z "
        "--flash_mode keep --flash_freq keep --flash_size keep "
        f"0x1000 {bootloader} "
        f"0x8000 {partitions} "
        f"0xe000 {boot_app0} "
        f"0x10000 {firmware}"
    )
    subprocess.run(command, shell=True)
    print("Upload complete!")
else:
    print("No ESP32 detected. Please check your connection.")

