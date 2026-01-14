# installer.py
import yolezz
import os
import sys
import shutil
import ctypes
import winreg

# ================= CONFIG =================

INSTALL_DIR = r"C:\Tools"
TARGET_EXE = "executable_killer.exe"
MENU_KEY = r"Directory\shell\KillExeInFolder"
MENU_NAME = "Forcer arrêt des exécutables"

# =========================================


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def relaunch_as_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, __file__, None, 1
    )
    sys.exit(0)


# ----------- FIND EXE -----------

def find_exe():
    """
    Méthode STANDARD (sans ta lib).
    Si tu veux utiliser yolezz.find,
    donne-moi sa signature exacte.
    """
    path = yolezz.find(TARGET_EXE, debug=True)
    return path


# ----------- REGISTRY -----------

def add_context_menu(exe_path):
    with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, MENU_KEY) as key:
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, MENU_NAME)
        winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, exe_path)

    with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, MENU_KEY + r"\command") as cmd:
        winreg.SetValueEx(cmd, "", 0, winreg.REG_SZ, f"\"{exe_path}\" \"%1\"")


def remove_context_menu():
    try:
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, MENU_KEY + r"\command")
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, MENU_KEY)
    except FileNotFoundError:
        pass


# ----------- INSTALL -----------

def install():
    os.makedirs(INSTALL_DIR, exist_ok=True)

    # Si déjà copié, on prend directement ce chemin
    dst = os.path.join(INSTALL_DIR, TARGET_EXE)
    if os.path.exists(dst):
        exe_path = dst
    else:
        exe_path = find_exe()
        if not exe_path:
            ctypes.windll.user32.MessageBoxW(
                None,
                f"{TARGET_EXE} introuvable.",
                "Erreur",
                0x10
            )
            return
        shutil.copy2(exe_path, dst)

    add_context_menu(dst)

    ctypes.windll.user32.MessageBoxW(
        None,
        "Installation terminée ✔",
        "Succès",
        0x40
    )


# ----------- UNINSTALL -----------

def uninstall():
    remove_context_menu()

    exe_path = os.path.join(INSTALL_DIR, TARGET_EXE)
    if os.path.exists(exe_path):
        try:
            os.remove(exe_path)
        except Exception:
            pass

    ctypes.windll.user32.MessageBoxW(
        None,
        "Désinstallation terminée ✔",
        "Info",
        0x40
    )


# ----------- MENU -----------

def menu():
    print("\n1. Installer")
    print("2. Désinstaller")
    print("3. Quitter")

    choice = input("\nChoix : ").strip()

    if choice == "1":
        install()
    elif choice == "2":
        uninstall()
    else:
        sys.exit(0)


# ----------- MAIN -----------

def main():
    if not is_admin():
        relaunch_as_admin()

    while True:
        menu()


if __name__ == "__main__":
    main()
