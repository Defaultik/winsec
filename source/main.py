from network import *
from hardware import *


def main():
    print("INFO: Validating TPM...")
    if TPM.validation():
        print("INFO: TPM successfully validated\n")
    else:
        print("WARNING: TPM is Disabled, but your computer supports it\nStrongly recommended to turn it on in BIOS/UEFI\n")

    print("INFO: Validating Secure Boot...")
    if SecureBoot.validation():
        print("INFO: Secure Boot successfully validated\n")
    else:
        print("WARNING: Secure Boot is Disabled, but your computer supports it\nStrongly recommended to turn it on in BIOS/UEFI\n")

    print("INFO: Trying to disable SMBv1...")
    if SMBv1.status():
        print("INFO: SMBv1 already disabled\n")
    else:
        SMBv1.disable()
        if SMBv1.status():
            print("INFO: SMBv1 successfully disabled\n")
        else:
            print("WARNING: Failed to disable SMBv1\n")

    print("INFO: Trying to disable LLMNR...")
    if LLMNR.status():
        print("INFO: LLMNR already disabled")
    else:
        LLMNR.disable()
        if LLMNR.status():
            print("INFO: LLMNR successfully disabled")
        else:
            print("WARNING: Failed to disable LLMNR")
    
    print("INFO: Trying to disable NetBIOS...")
    if NetBIOS.status():
        print("INFO: NetBIOS already disabled")
    else:
        NetBIOS.disable()
        if NetBIOS.status():
            print("INFO: NetBIOS successfully disabled")
        else:
            print("WARNING: Failed to disable NetBIOS")


if __name__ == "__main__":
    main()