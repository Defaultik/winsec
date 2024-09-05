import subprocess
from re import search


# TODO: WPAD, TLS, DNS
class SMBv1:
    def __init__(self):
        self.name = "SMBv1"
        self.type = "Network"


    def validation(self):
        result = subprocess.run(["powershell", "-Command", "Get-WindowsOptionalFeature -Online -FeatureName SMB1Protocol"], capture_output=True, text=True)

        if search(r'State\s*:\s*(\w+)', result.stdout).group(1) == "Disabled":
            return True
        
        return False


    def disable():
        subprocess.run(["powershell", "-Command", "Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol"], capture_output=True, text=True)
    

class LLMNR:
    def __init__(self):
        self.name = "LLMNR"
        self.type = "Network"


    def validation(self):
        result = subprocess.run(["powershell", "-Command", "Get-ItemProperty", "-Path 'HKLM:\\Software\\Policies\\Microsoft\\Windows NT\\DNSClient' -name EnableMulticast"], capture_output=True, text=True)

        if result.stdout:
            return True

        return False


    def disable():
        subprocess.run(["powershell", "-Command", "New-Item", "-Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows NT' -Name DNSClient"], capture_output=True, text=True)
        subprocess.run(["powershell", "-Command", "New-ItemProperty", "-Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows NT\\DNSClient' -Name EnableMultiCast -Value 0 -PropertyType DWORD"], capture_output=True, text=True)


class NetBIOS:
    def __init__(self):
        self.name = "NetBIOS"
        self.type = "Network"


    def validation(self):
        result = subprocess.run(["powershell", "-Command", "Get-ItemPropertyValue", "-Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Services\\NetBT\\Parameters\\Interfaces\\tcpip*' -Name NetbiosOptions"], capture_output=True, text=True)
        if all(num == "2" for num in result.stdout.split()):
            return True

        return False
    

    def disable():
        subprocess.run(["powershell", "-Command", "Set-ItemProperty", "-Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Services\\NetBT\\Parameters\\Interfaces\\tcpip*' -Name NetbiosOptions -Value 2"])