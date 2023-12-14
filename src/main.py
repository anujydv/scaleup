
""" import modules """
from .setup import SetupManager

# call different setup class methord in main function
if __name__ == "__main__":
    SetupManager.start_server()
