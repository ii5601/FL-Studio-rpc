not_installed = "None"
lib_notinstalled = False

discordrpc_error = False
pyautogui_error = False

rpc_set = False
in_project = False

try:
    import discordrpc
except ModuleNotFoundError:
    not_installed = 'discord-rpc'
    discordrpc_error = True
    lib_notinstalled = True

try:
    import pyautogui
except ModuleNotFoundError:
    pyautogui_error = True  # Исправлено: должно быть True
    if lib_notinstalled == "None":
        not_installed = 'pyautogui'
    else:
        not_installed += ', pyautogui'

    if not not_installed:
        not_installed = True

import time
import threading as th
import os
import sys

if lib_notinstalled:
    print(f"Oh, you have not installed needed libs! Needed not install libs: {not_installed}")
    if discordrpc_error:
        os.system("pip install discord-rpc")
    if pyautogui_error:
        os.system("pip install pyautogui")

    # Перезапуск после установки
    print("Libraries installed. Restarting...")
    os.execv(sys.executable, ['python'] + sys.argv)

rpc = discordrpc.RPC(app_id=1453309601914294352)

def find_fl_studio_window():
    """Find and return the FL Studio window if it exists"""
    windows = pyautogui.getAllWindows()
    for window in windows:
        title = window.title
        if title and "FL Studio" in title:
            return window
    return None


def extract_project_name(title):
    """Extract project name from FL Studio window title"""
    if not title:
        return "Unknown"

    parts = title.split(" - FL Studio")
    if parts and parts[0]:
        filename = parts[0].strip()
        if filename.endswith('.flp'):
            return filename[:-4]  # Remove .flp extension
        return filename
    return title


# Continuous monitoring
def run_rpc():
    """Main RPC monitoring function"""
    global rpc_set, in_project

    try:
        while True:
            fl_window = find_fl_studio_window()

            if fl_window:
                project_name = extract_project_name(fl_window.title)

                if project_name == "Welcome to FL Studio" or "Untitled" in project_name:
                    if not rpc_set or in_project:
                        rpc.set_activity(
                            details="Working in FL Studio",
                            large_image="icon_fl_studio",
                            state="No active project"
                        )
                        rpc_set = True
                        in_project = False
                else:
                    if not rpc_set or not in_project or rpc_set == False:
                        rpc.set_activity(
                            details="Working in FL Studio",
                            large_image="icon_fl_studio",
                            state=f"Project: {project_name}"
                        )
                        rpc_set = True
                        in_project = True
            else:
                if rpc_set:
                    # Clear activity when FL Studio is not found
                    rpc.disconnect()
                    rpc_set = False
                    in_project = False

            time.sleep(5)  # Check every 5 seconds

    except KeyboardInterrupt:
        print("\nRPC stopped by user")
        if rpc_set:
            rpc.disconnect()
    except Exception as e:
        print(f"Error: {e}")
        if rpc_set:
            rpc.disconnect()


if __name__ == "__main__":
    print("FL Studio Discord RPC starting...")
    print("Press Ctrl+C to stop")

    try:
        # Start RPC in a separate thread
        rpc_thread = th.Thread(target=run_rpc)
        rpc_thread.daemon = True
        rpc_thread.start()

        # Keep main thread alive
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nExiting...")
        if rpc_set:
            rpc.disconnect()