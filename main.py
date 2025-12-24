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
    pyautogui_error = False
    if lib_notinstalled == "None":
        not_installed = 'pyautogui'
    else:
        not_installed += ', pyautogui'
    
    if not_installed == False:
        not_installed = True

import time
import threading as th
import os

if lib_notinstalled == True:
    print(f"Oh, you have not installed neded libs! Neded not install libs: {not_installed}")
    if discordrpc_error == True:
        os.system("pip install discord-rpc")
    if pyautogui_error == True:
        os.system("pip install pyautogui")

import discordrpc
import pyautogui

rpc = discordrpc.RPC(app_id=1453309601914294352)

def find_fl_studio_window():
    """Find and return the FL Studio window if it exists"""
    windows = pyautogui.getAllWindows()
    for window in windows:
        if window.title and "FL Studio" in window.title:
            return window
    return None

def extract_project_name(title):
    parts = title.split(" - FL Studio")
    if parts and parts[0]:
        filename = parts[0].strip()
        if filename.endswith('.flp'):
            return filename[:-4]
        return filename
    return title

# Continuous monitoring
while True:
    fl_window = find_fl_studio_window()
    
    if fl_window:
        project_name = extract_project_name(fl_window.title)

        if rpc_set == False or in_project == False:
            if project_name == "Welcome to FL Studio":
                rpc.set_activity(
                    details="Working in FL Studio",
                    large_image="icon_fl_studio",
                    state=f"Not in project"
                )

                rpc_set = True
            else:
                rpc.set_activity(
                    details="Working in FL Studio",
                    large_image="icon_fl_studio",
                    state=f"Project: {project_name}"
                )

                in_project = True

            start_rpc = th.Thread(target=rpc.run())
            start_rpc.start()
    else:
        if rpc_set == True:
            # Clear activity when FL Studio is not found
            rpc.disconnect()

            rpc_set = False
            in_project = False
    
    time.sleep(5)  # Check every 5 seconds