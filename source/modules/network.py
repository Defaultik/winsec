import subprocess
from re import search


class Network:
    def __init__(self, name):
        self.name = name
        self.type = "Network"


# TODO: WPAD, TLS, DNS
class SMBv1(Network):
    def __init__(self):
        super().__init__("SMBv1")


    def validation(self):
        result = subprocess.run(["powershell", "-Command", "Get-WindowsOptionalFeature -Online -FeatureName SMB1Protocol"], capture_output=True, text=True)

        if search(r'State\s*:\s*(\w+)', result.stdout).group(1) == "Disabled":
            return True
        
        return False


    def disable():
        subprocess.run(["powershell", "-Command", "Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol"], capture_output=True, text=True)
    

class LLMNR(Network):
    def __init__(self):
        super().__init__("LLMNR")


    def validation(self):
        result = subprocess.run(["powershell", "-Command", "Get-ItemProperty", "-Path 'HKLM:\\Software\\Policies\\Microsoft\\Windows NT\\DNSClient' -name EnableMulticast"], capture_output=True, text=True)

        if result.stdout:
            return True

        return False


    def disable():
        subprocess.run(["powershell", "-Command", "New-Item", "-Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows NT' -Name DNSClient"], capture_output=True, text=True)
        subprocess.run(["powershell", "-Command", "New-ItemProperty", "-Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows NT\\DNSClient' -Name EnableMultiCast -Value 0 -PropertyType DWORD"], capture_output=True, text=True)


class NetBIOS(Network):
    def __init__(self):
        super().__init__("NetBIOS")


    def validation(self):
        result = subprocess.run(["powershell", "-Command", "Get-ItemPropertyValue", "-Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Services\\NetBT\\Parameters\\Interfaces\\tcpip*' -Name NetbiosOptions"], capture_output=True, text=True)
        if all(num == "2" for num in result.stdout.split()):
            return True

        return False
    

    def disable():
        subprocess.run(["powershell", "-Command", "Set-ItemProperty", "-Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Services\\NetBT\\Parameters\\Interfaces\\tcpip*' -Name NetbiosOptions -Value 2"])