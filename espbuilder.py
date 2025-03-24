import os
import subprocess
import serial.tools.list_ports
from pathlib import Path
import sys
import winreg
import serial.tools.list_ports
import ctypes

#commands to make it work :
#python -m PyInstaller --onefile --clean --add-binary "python39.dll;." --add-binary "MotusVR_Explore_NimBLE.ino.bootloader.bin;." --add-binary "MotusVR_Explore_NimBLE.ino.partitions.bin;." --add-binary "MotusVR_Explore_NimBLE.ino.bin;." --add-binary "boot_app0.bin;." --add-binary "CP210xVCPInstaller_x64.exe;." --add-binary "CP210xVCPInstaller_x86.exe;." --add-data "slabvcp.inf;." esp_builder.py
#python -m PyInstaller --onefile --clean --console --hidden-import=esptool --collect-binaries python --add-binary "esptool.exe;." --add-binary "MotusVR_Explore_NimBLE.ino.bootloader.bin;." --add-binary "MotusVR_Explore_NimBLE.ino.partitions.bin;." --add-binary "MotusVR_Explore_NimBLE.ino.bin;." --add-binary "boot_app0.bin;." esp_builder.py
#https://pyinstaller.org/en/stable/usage.html

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def is_cp210x_installed():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "CP210" in port.description:  # Check if CP210x is detected
            return True
    return False

def install_cp210x_driver():
        installer_path = resource_path("CP210xVCPInstaller_x64.exe") if sys.maxsize > 2**32 else resource_path("CP210xVCPInstaller_x86.exe")
        inf_file_path = resource_path("slabvcp.inf")  # Get the path for slabvcp.inf

        try:
                # Run installer as Administrator
                subprocess.run([installer_path, "/q"], check=True)
                print("CP210x driver installation started using EXE installer.")

                command = f'pnputil /add-driver "{inf_file_path}" /install'
                subprocess.run(["powershell", "Start-Process", "cmd.exe", "/c", command, "-Verb", "RunAs"], check=True)
                print("Driver installed using INF file.")
                
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
    print("Python okay")
    print("CP210x driver is already installed.")
    port = find_esp32_port()
    if port:
        print(f"ESP32 detected on {port}. Uploading firmware...")
        esptool_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'esptool.exe')
        command = [
            esptool_path,  # Use the esptool.exe from the current directory
            "--chip", "esp32", "--port", port, "--baud", "921600",
            "--before", "default_reset", "--after", "hard_reset", "write_flash", "-e", "-z",
            "--flash_mode", "keep", "--flash_freq", "keep", "--flash_size", "keep",
            "0x1000", bootloader,  # Separate address and filename
            "0x8000", partitions,  # Separate address and filename
            "0xe000", boot_app0,  # Separate address and filename
            "0x10000", firmware  # Separate address and filename
        ]
        
        try:
            subprocess.run(command, check=True)
            print("Upload complete!")
        except subprocess.CalledProcessError as e:
            print(f"Error uploading firmware: {e}")
    else:
        print("No ESP32 detected. Please check your connection.")
#else:
  #  print("CP210x driver not found, installing now...")
   # install_cp210x_driver()  # Call the installer function





