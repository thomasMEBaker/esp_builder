

#commands to make it work :
#python -m PyInstaller --onefile --clean --add-binary "python39.dll;." --add-binary "MotusVR_Explore_NimBLE.ino.bootloader.bin;." --add-binary "MotusVR_Explore_NimBLE.ino.partitions.bin;." --add-binary "MotusVR_Explore_NimBLE.ino.bin;." --add-binary "boot_app0.bin;." --add-binary "CP210xVCPInstaller_x64.exe;." --add-binary "CP210xVCPInstaller_x86.exe;." --add-data "slabvcp.inf;." esp_builder.py
#python -m PyInstaller --clean --console --collect-binaries python --add-binary "MotusVR_Explore_NimBLE.ino.bootloader.bin;." --add-binary "MotusVR_Explore_NimBLE.ino.partitions.bin;." --add-binary "MotusVR_Explore_NimBLE.ino.bin;." --add-binary "boot_app0.bin;." esp_builder.py
#https://pyinstaller.org/en/stable/usage.html

#python -m PyInstaller --onefile --clean --console --collect-binaries python esp_builder.py


print("Python availble")





