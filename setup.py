from os import system

_DEPENDENCIES = {"requests"}

def install_dependencies():
    if "y" == input(f"Are you sure you want to download all {len(_DEPENDENCIES)}? (y/n) "):
        for dependency in _DEPENDENCIES:
            input(f"Now installing {dependency}, continue...")
            system(f"pip install {dependency}")
    else:
        print("Install aborted")

if __name__ == "__main__":
    install_dependencies()