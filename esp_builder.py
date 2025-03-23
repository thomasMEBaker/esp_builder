import os
import subprocess
import serial.tools.list_ports
from pathlib import Path
import sys
import winreg

#commands to make it work :
#python -m PyInstaller --onefile --add-binary "MotusVR_Explore_NimBLE.ino.bootloader.bin;." --add-binary "MotusVR_Explore_NimBLE.ino.partitions.bin;." --add-binary "MotusVR_Explore_NimBLE.ino.bin;." --add-binary "boot_app0.bin;." --add-binary "CP210xVCPInstaller_x64.exe;." --add-binary "CP210xVCPInstaller_x86.exe;." esp_builder.py
#https://pyinstaller.org/en/stable/usage.html

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def is_cp210x_installed():
    try:
        reg_path = r"SYSTEM\CurrentControlSet\Enum\USB\VID_10C4&PID_EA60"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
            return True  # Found in registry, meaning it's installed
    except FileNotFoundError:
        return False  # Not found, driver not installed

def install_cp210x_driver():
    installer_name = resource_path("CP210xVCPInstaller_x64.exe") if sys.maxsize > 2**32 else resource_path("CP210xVCPInstaller_x86.exe")
    installer_path = os.path.join(os.path.dirname(sys.executable), installer_name)

    try:
        subprocess.run([installer_path, "/silent"], check=True)
        print("CP210x driver installation started.")
    except Exception as e:
        print(f"Error running CP210x installer: {e}")


# Firmware binary file
bootloader = resource_path("MotusVR_Explore_NimBLE.ino.bootloader.bin")
partitions = resource_path("MotusVR_Explore_NimBLE.ino.partitions.bin")
boot_app0 = resource_path("boot_app0.bin")
firmware = resource_path("MotusVR_Explore_NimBLE.ino.bin")

# Check if the firmware file exists
for file in [bootloader, partitions, boot_app0, firmware]:
    if not Path(file).exists():
        print(f"Error: Required file '{file}' not found. Please check the file name and location.")
        sys.exit()

# Function to detect ESP32 serial port
def find_esp32_port():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if "USB" in port.description or "UART" in port.description or "CP210" in port.description or "CH340" in port.description:
            return port.device
    return None


if is_cp210x_installed():
    print("CP210x driver is already installed.")
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
else:
    print("CP210x driver not found, installing now...")
    install_cp210x_driver()  # Call the installer function





