import os
from ctypes import windll
from network import *
from hardware import *


def init():
    if os.name == "nt":
        if windll.shell32.IsUserAnAdmin():
            main()
        else:
            print("ERROR: Program launched without admin rights\nPlease run CMD/Terminal as an administrator")
    else:
        print("ERROR: This script supports only Windows systems")


def main():
    for i in (TPM(), SecureBoot()):
        print("INFO: Validating " + i.name)

        if i.validation():
            print(f"INFO: {i.name} successfully validated\n")
        else:
            print(f"WARNING: {i.name} is Disabled, but your computer supports it\nStrongly recommended to turn it on in BIOS/UEFI\n")

    for i in (SMBv1(), LLMNR(), NetBIOS()):
        print(f"INFO: Trying to disable {i.name}...")
        if i.status():
            print(f"INFO: {i.name} already disabled\n")
        else:
            i.disable()
            if i.status():
                print(f"INFO: {i.name} successfully disabled\n")
            else:
                print(f"WARNING: Failed to disable {i.name}\n")


if __name__ == "__main__":
    init()