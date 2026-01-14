import os
import sys
import psutil
import tkinter as tk
from tkinter import messagebox

def kill_executables(folder):
    killed = []
    not_found = []

    exe_paths = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith(".exe")
    ]

    for exe in exe_paths:
        exe = os.path.abspath(exe)
        found = False

        for proc in psutil.process_iter(["pid", "exe", "name"]):
            try:
                if proc.info["exe"] and os.path.abspath(proc.info["exe"]) == exe:
                    found = True
                    proc.terminate()
                    try:
                        proc.wait(timeout=2)
                    except psutil.TimeoutExpired:
                        proc.kill()
                    killed.append(f"{proc.info['name']} (PID {proc.pid})")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        if not found:
            not_found.append(os.path.basename(exe))

    return killed, not_found


def popup_result(killed, not_found):
    root = tk.Tk()
    root.withdraw()

    msg = ""

    if killed:
        msg += "Processus arrêtés :\n"
        msg += "\n".join(killed) + "\n\n"

    if not_found:
        msg += "Aucun processus actif pour :\n"
        msg += "\n".join(not_found)

    if not msg:
        msg = "Aucun exécutable trouvé."

    messagebox.showinfo("Résultat", msg)
    root.destroy()


def main():
    if len(sys.argv) < 2:
        sys.exit(1)

    folder = sys.argv[1]

    if not os.path.isdir(folder):
        sys.exit(1)

    killed, not_found = kill_executables(folder)
    popup_result(killed, not_found)


if __name__ == "__main__":
    main()
