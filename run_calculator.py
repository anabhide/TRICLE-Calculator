import sys
import os

# handle relative path
FOLDER_DIR = os.getcwd()
sys.path.append(FOLDER_DIR)

from triangle import views

# run the calculator view
if __name__ == "__main__":
    views.main()
