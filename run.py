from Pcsx2Updater.Pcsx2Updater import Pcsx2Updater
import os
import sys
import platform

def main():

    if getattr(sys, 'frozen', False):
        ROOT_DIR = os.path.dirname(os.path.abspath(sys.executable))
    elif __file__:
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    
    os.system("clear" if platform.system() == "Linux" else "cls")
    
    Pcsx2Updater(ROOT_DIR)

if __name__ == "__main__":
    main()
