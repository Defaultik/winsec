import os
from ctypes import windll
from sys import platform
from modules.network import *
from modules.hardware import *


def clear():
    # Clear the terminal on Unix and Windows systems
    if (platform == "win32"):
        os.system("cls")
    else:
        os.system("clear")


def print_options(*args):
    for i, name in enumerate(args):
        print(f"[{i + 1}]", name)


def init():
    if os.name == "nt":
        if windll.shell32.IsUserAnAdmin():
            menu()
        else:
            print("ERROR: Program launched without admin rights\nPlease run CMD/Terminal as an administrator")
    else:
        print("ERROR: This script supports only Windows systems")


def menu():
    clear()

    print("\nWelcome to the WinSec!")
    print("WinSec is made to fix the most popular vulnerabilities in Windows 10/11")
    print("\nby github.com/Defaultik\n")

    print_options("System Check", "Exit")
    selected_tab = input("Enter your task: ")
    print()
    match selected_tab:
        case "1":
            system_check()
        case "2":
            exit()
        case _:
            print("ERROR: Invalid input, try again")


def system_check():
    for module in (TPM(), SecureBoot(), SMBv1(), LLMNR(), NetBIOS()):
        print(f"[INFO] Validating {module.name}")

        if module.validation():
            print(f"[INFO] {module.name} successfully validated\n")
        else:
            if module.type == "Hardware":
                print(f"[{module.danger} RISK] {module.name} is Disabled, but your computer supports it\nStrongly recommended to turn it on\n")
            elif module.type == "Network":
                module.disable()
                
                if module.validation():
                    print(f"[{module.danger} RISK] {module.name} successfully disabled\n")
                else:
                    print(f"[WARNING] Failed to disable {module.name}\n")


if __name__ == "__main__":
    init()