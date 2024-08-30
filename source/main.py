import subprocess
import os
import re


def clear():
    os.system("cls")


def smbv1_status():
    result = subprocess.run(["powershell", "-Command", "Get-WindowsOptionalFeature", "-Online", "-FeatureName SMB1Protocol"], capture_output=True, text=True)
    result = re.search(r'State\s*:\s*(\w+)', result.stdout).group(1)
    
    return result


def disable_smbv1():
    subprocess.run(["powershell", "-Command", "Disable-WindowsOptionalFeature", "-Online", "-FeatureName SMB1Protocol"], capture_output=True, text=True)

    if smbv1_status() == "Disabled":
        print("SMBv1 was successfully disabled")
    else:
        print("ERROR: SMBv1 wasn't disabled")


def main():
    disable_smbv1()


if __name__ == "__main__":
    main()