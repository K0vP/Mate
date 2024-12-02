import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.menu import menu_app

if __name__ == "__main__":
    menu_app()