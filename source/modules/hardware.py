import subprocess
from re import search


class TPM:
    def __init__(self):
        self.name = "TPM"
        self.type = "Hardware"


    def validation(self):    
        command = subprocess.run(["powershell", "-Command", "get-tpm"], capture_output=True, text=True)

        tpm_present = search(r'TpmPresent\s*:\s*(\w+)', command.stdout)
        tpm_enabled = search(r'TpmEnabled\s*:\s*(\w+)', command.stdout)
        
        if tpm_present.group(1) == "True":
            if tpm_enabled.group(1) == "True":
                return True
            
        return False


class SecureBoot:
    def __init__(self):
        self.name = "Secure Boot"
        self.type = "Hardware"


    def validation(self):
        command = subprocess.run(["powershell", "-Command", "Confirm-SecureBootUEFI"], capture_output=True, text=True)
        
        if command.stdout.strip() in ("True", "Cmdlet not supported on this platform."):
            return True
        
        return False