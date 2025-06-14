import ctypes
from ctypes import wintypes
import os
import tkinter as tk
import requests
import zipfile
import shutil
import os
import tempfile
import subprocess
from tkinter import messagebox

def download_otd(destination_folder: str):
    """
    Downloads OpenTabletDriver's latest Windows release,
    renames the daemon to otd.exe, and places it in the destination folder.
    """
    # Ensure destination folder exists
    os.makedirs(destination_folder, exist_ok=True)

    # GitHub API for latest release
    url = "https://api.github.com/repos/OpenTabletDriver/OpenTabletDriver/releases/latest"
    headers = {"Accept": "application/vnd.github.v3+json"}

    try:
        print("Fetching latest release info...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Find the Windows zip asset
        asset = next((a for a in data['assets'] if a['name'].endswith("win-x64.zip")), None)
        if not asset:
            raise Exception("Windows release asset not found.")

        print(f"Downloading: {asset['name']}")
        zip_url = asset['browser_download_url']
        zip_response = requests.get(zip_url, stream=True)
        zip_response.raise_for_status()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp_zip:
            for chunk in zip_response.iter_content(chunk_size=8192):
                tmp_zip.write(chunk)
            tmp_zip_path = tmp_zip.name

        print("Extracting files...")
        with zipfile.ZipFile(tmp_zip_path, 'r') as zip_ref:
            extract_dir = tempfile.mkdtemp()
            zip_ref.extractall(extract_dir)

        # Look for the daemon and rename it
        daemon_path = None
        for root, _, files in os.walk(extract_dir):
            for file in files:
                if file.lower() == "opentabletdriver.daemon.exe":
                    daemon_path = os.path.join(root, file)
                    break

        if not daemon_path:
            raise Exception("Daemon executable not found in extracted files.")

        # Destination path for renamed file
        dest_path = os.path.join(destination_folder, "otd.exe")
        shutil.move(daemon_path, dest_path)

        print(f"OpenTabletDriver daemon saved to: {dest_path}")

    except Exception as e:
        print(f"Error: {e}")

def is_otd_running(process_name="otd.exe"):
    try:
        output = subprocess.check_output('tasklist', text=True)
        return process_name.lower() in output.lower()
    except subprocess.CalledProcessError:
        return False

import subprocess

def kill_otd():
    try:
        subprocess.run(["taskkill", "/f", "/im", "otd.exe"], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to terminate otd.exe: {e.stderr.decode()}")



def run_daemon_silently(exe_path):
    CREATE_NO_WINDOW = 0x08000000
    subprocess.Popen([exe_path],
                     creationflags=CREATE_NO_WINDOW,
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL)


def choose_monitor(monitor_resolutions):
    selection = {'index': None}

    def on_select(index):
        selection['index'] = index
        win.destroy()

    win = tk.Toplevel()
    win.title("Select Monitor")
    win.geometry("300x200")
    win.grab_set()  # Make the dialog modal

    tk.Label(win, text="Select the monitor you want to use:").pack(pady=10)

    for i, res in enumerate(monitor_resolutions):
        btn_text = f"Monitor {i + 1}: {res[0]}x{res[1]}"
        tk.Button(win, text=btn_text, command=lambda i=i: on_select(i)).pack(pady=5, fill="x", padx=20)

    win.wait_window()  # Pause execution until window is closed
    return selection['index']


class AppData:
    def __init__(self, app_name):
        self.app_name = app_name
        self.appdata_path = os.getenv('APPDATA')
        self.app_folder = os.path.join(self.appdata_path, self.app_name)
        os.makedirs(self.app_folder, exist_ok=True)

    def get_appdata_path(self):
        return self.appdata_path

    def get_app_folder(self):
        return self.app_folder
    
    def write_file(self, filename, content):
        file_path = os.path.join(self.app_folder, filename)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return file_path
    
    def read_file(self, filename):
        file_path = os.path.join(self.app_folder, filename)
        if not os.path.exists(file_path):
            return None
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    def clear_app_data(self):
        if not os.path.exists(self.app_folder):
            messagebox.showinfo("Info", "No app data to clear.")
            return

        # Create a temporary batch file to delete app data
        with tempfile.NamedTemporaryFile(delete=False, suffix=".bat", mode="w", encoding="utf-8") as bat_file:
            # Write deletion commands to the batch file
            for item in os.listdir(self.app_folder):
                item_path = os.path.join(self.app_folder, item)
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    bat_file.write(f'del /f /q "{item_path}"\n')
                elif os.path.isdir(item_path):
                    bat_file.write(f'rmdir /s /q "{item_path}"\n')

            # Close the batch file so we can execute it
            bat_path = bat_file.name

        # Run the batch file with elevation (admin rights)
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", bat_path, None, None, 1
        )

        print("App data deletion initiated with elevated permissions.")


    



USER32 = ctypes.windll.user32

def set_per_monitor_v2_dpi_awareness():
    SetProcessDpiAwarenessContext = USER32.SetProcessDpiAwarenessContext
    SetProcessDpiAwarenessContext.restype = wintypes.BOOL
    SetProcessDpiAwarenessContext.argtypes = [ctypes.c_void_p]
    SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))

# Structures
class RECT(ctypes.Structure):
    _fields_ = [
        ('left', ctypes.c_long),
        ('top', ctypes.c_long),
        ('right', ctypes.c_long),
        ('bottom', ctypes.c_long)
    ]

class MONITORINFO(ctypes.Structure):
    _fields_ = [
        ('cbSize', wintypes.DWORD),
        ('rcMonitor', RECT),
        ('rcWork', RECT),
        ('dwFlags', wintypes.DWORD)
    ]

def get_monitor_resolutions():
    monitors = []

    def monitor_enum_proc(hMonitor, hdcMonitor, lprcMonitor, dwData):
        info = MONITORINFO()
        info.cbSize = ctypes.sizeof(MONITORINFO)
        USER32.GetMonitorInfoW(hMonitor, ctypes.byref(info))

        width = info.rcMonitor.right - info.rcMonitor.left
        height = info.rcMonitor.bottom - info.rcMonitor.top
        monitors.append((width, height))
        return 1

    MONITORENUMPROC = ctypes.WINFUNCTYPE(
        ctypes.c_int,
        wintypes.HMONITOR,
        wintypes.HDC,
        ctypes.POINTER(RECT),
        wintypes.LPARAM
    )

    USER32.EnumDisplayMonitors(None, None, MONITORENUMPROC(monitor_enum_proc), None)

    return monitors
