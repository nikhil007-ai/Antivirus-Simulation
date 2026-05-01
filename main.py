import subprocess
import sys


# AUTO INSTALL FUNCTION

def install(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except Exception as e:
        print(f"[ERROR] Failed to install {package}: {e}")



# CHECK MODULES

def check_and_install():
    required_packages = []  # currently none (your project uses stdlib)

    for pkg in required_packages:
        try:
            __import__(pkg)
        except ImportError:
            print(f"[INFO] Installing missing package: {pkg}")
            install(pkg)



# CHECK TKINTER 

def check_tkinter():
    try:
        import tkinter
    except ImportError:
        print("\n[ERROR] Tkinter is not installed!\n")

        if sys.platform.startswith("linux"):
            print("Run this command:")
            print("sudo apt install python3-tk")
        elif sys.platform == "win32":
            print("Reinstall Python with 'Tkinter' enabled.")
        elif sys.platform == "darwin":
            print("Install Tkinter via Homebrew or Python installer.")

        sys.exit(1)



# MAIN APP

def main():
    check_and_install()
    check_tkinter()

    import tkinter as tk
    from gui import AntivirusUI

    root = tk.Tk()
    app = AntivirusUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
