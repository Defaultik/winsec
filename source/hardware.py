import subprocess
from re import search


class TPM:
    def validation():    
        command = subprocess.run(["powershell", "-Command", "get-tpm"], capture_output=True, text=True)

        if search(r'TpmPresent\s*:\s*(\w+)', command.stdout).group(1) == "True":
            if search(r'TpmEnabled\s*:\s*(\w+)', command.stdout).group(1) == "True":
                return True
            
            return False


class SecureBoot:
    def validation():
        command = subprocess.run(["powershell", "-Command", "Confirm-SecureBootUEFI"], capture_output=True, text=True)
        
        if command.stdout.strip() in ("True", "Cmdlet not supported on this platform."):
            return True
        
        return False