import subprocess
import re


def smbv1_status():
    result = subprocess.run(["powershell", "-Command", "Get-WindowsOptionalFeature -Online -FeatureName SMB1Protocol"], capture_output=True, text=True)
    if re.search(r'State\s*:\s*(\w+)', result.stdout).group(1) == "Disabled":
        return True
    
    return False


def smbv1_disable():
    subprocess.run(["powershell", "-Command", "Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol"], capture_output=True, text=True)
    

def llmnr_status():
    result = subprocess.run(["powershell", "-Command", "Get-ItemProperty", "-Path 'HKLM:\\Software\\Policies\\Microsoft\\Windows NT\\DNSClient' -name EnableMulticast"], capture_output=True, text=True)
    if result.stdout:
        return True

    return False


def llmnr_disable():
    subprocess.run(["powershell", "-Command", "New-Item", "-Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows NT' -Name DNSClient"], capture_output=True, text=True)
    subprocess.run(["powershell", "-Command", "New-ItemProperty", "-Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows NT\\DNSClient' -Name EnableMultiCast -Value 0 -PropertyType DWORD"], capture_output=True, text=True)
    

"""
def netbios_status():
    ...


def disable_netbios():
    ...


def wpad_status():
    ...
    
    
def disable_wpad():
    ...

    
def tls_outdated_status():
    ...
    

def diable_tls_outdated():
    ...
"""


def tpm_validate():    
    command = subprocess.run(["powershell", "-Command", "get-tpm"], capture_output=True, text=True)
    if re.search(r'TpmPresent\s*:\s*(\w+)', command.stdout).group(1) == "True":
        if re.search(r'TpmEnabled\s*:\s*(\w+)', command.stdout).group(1) == "True":
            return True
        
        return False

    
def secureboot_validate():
    command = subprocess.run(["powershell", "-Command", "Confirm-SecureBootUEFI"], capture_output=True, text=True)
    if command.stdout.strip() in ("True", "Cmdlet not supported on this platform."):
        return True
    
    return False


def main():
    print("INFO: Validating TPM...")
    if tpm_validate():
        print("INFO: TPM successfully validated\n")
    else:
        print("WARNING: TPM is Disabled, but your computer supports it\nStrongly recommended to turn it on in BIOS/UEFI\n")

    print("INFO: Validating Secure Boot...")
    if secureboot_validate():
        print("INFO: Secure Boot successfully validated\n")
    else:
        print("WARNING: Secure Boot is Disabled, but your computer supports it\nStrongly recommended to turn it on in BIOS/UEFI\n")

    print("INFO: Trying to disable SMBv1...")
    smbv1_disable()
    if smbv1_status():
        print("INFO: SMBv1 successfully disabled\n")
    else:
        print("WARNING: Failed to disable SMBv1\n")

    print("INFO: Trying to disable LLMNR...")
    llmnr_disable()
    if llmnr_status():
        print("INFO: LLMNR successfully disabled")
    else:
        print("WARNING: Failed to disable LLMNR")


if __name__ == "__main__":
    main()