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
    for module in (TPM(), SecureBoot(), SMBv1(), LLMNR(), NetBIOS()):
        print("INFO: Validating " + module.name)

        if module.validation():
            print(f"INFO: {module.name} successfully validated\n")
        else:
            if module.type == "Hardware":
                print(f"WARNING: {module.name} is Disabled, but your computer supports it\nStrongly recommended to turn it on in BIOS/UEFI\n")
            elif module.type == "Network":
                module.disable()
                
                if module.validation():
                    print(f"INFO: {module.name} successfully disabled\n")
                else:
                    print(f"WARNING: Failed to disable {module.name}\n")


if __name__ == "__main__":
    init()