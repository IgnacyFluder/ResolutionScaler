import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import subprocess
import re
import ctypes
import utils
from tkinter import Menu
import webbrowser
from tkinter import simpledialog

utils.set_per_monitor_v2_dpi_awareness()

class ResolutionScaler(tk.Tk):
    def __init__(self):
        super().__init__()

        self.ad = utils.AppData("ResolutionScaler")

        # Constants
        self.USER32 = ctypes.windll.user32
        self.SCREEN_SIZE = utils.get_monitor_resolutions()[0][0], utils.get_monitor_resolutions()[0][1]
        self.OTD_PATH = self.ad.get_app_folder()+"\\otd.exe"
        is_otd_running = utils.is_otd_running()
        self.withdraw()
        if not os.path.exists(self.OTD_PATH) and not is_otd_running:
            if messagebox.askyesno("Error", "otd.exe not found in app folder nor is it running. Would you like to download it now?"):
                utils.download_otd(self.ad.get_app_folder())
                messagebox.showinfo("Download complete", "otd will now run in the background.")
                utils.run_daemon_silently(self.OTD_PATH)
                self.deiconify()
                
            else: 
                self.destroy()
        elif not os.path.exists(self.OTD_PATH) and is_otd_running:
            if messagebox.askyesno("Info", "otd.exe was found running in the background.\nWe recommend placing the otd.exe file in the app folder for better compatibility.\n\nYou can download it from the GitHub repository."):
                if messagebox.askokcancel("Warning", "otd.exe will be shutdown, click cancel to keep it running"):
                    utils.kill_otd()
                else:
                    self.destroy()
                utils.download_otd(self.ad.get_app_folder())
                messagebox.showinfo("Download complete", "otd will now run in the background.")
                utils.run_daemon_silently(self.OTD_PATH)
                self.deiconify()
            else:
                pass

        self.TARGET_WIDTH = self.SCREEN_SIZE[0]
        self.TARGET_HEIGHT = self.SCREEN_SIZE[1]

        self.TARGET_POS = (int(self.TARGET_WIDTH/2), int(self.TARGET_HEIGHT/2))
        self.TABLET_ROTATION = 180
        self.TABLET_WIDTH_MM = 101.6
        self.TABLET_HEIGHT_MM = 76.2
        self.TABLET_NAME = "XP-Pen Star G430S"

        self.MONITOR_INDEX = 0
        self.ALIGNMENT = "TOP_LEFT" # "TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT"
        self.PRESET_FILE_PATH = self.ad.get_app_folder()+"\\presets.json"

        

        self.title("Resolution Scaler")
        self.geometry("550x600")
        self.resizable(True, True)

        self.presets = []
        self.configure(bg="#f0f0f0")
        self.style = ttk.Style(self)
        self.style.theme_use("vista")

        ## Load settings
        self.withdraw()
        if self.ad.read_file("settings.json") is not None:
            try:
                settings = json.loads(self.ad.read_file("settings.json"))
                self.TABLET_WIDTH_MM = settings.get("t_width_mm", 101.6)
                self.TABLET_HEIGHT_MM = settings.get("t_height_mm", 76.2)
                self.TABLET_NAME = settings.get("tablet_name", "XP-Pen Star G430S")
                self.MONITOR_INDEX = settings.get("monitor_index", 0)
                self.TARGET_WIDTH = utils.get_monitor_resolutions()[self.MONITOR_INDEX][0]
                self.TARGET_HEIGHT = utils.get_monitor_resolutions()[self.MONITOR_INDEX][1]
                self.TARGET_POS = (int(self.TARGET_WIDTH/2), int(self.TARGET_HEIGHT/2))

            except json.JSONDecodeError:
                print("Error loading settings.json, using defaults.")
        else:
            self.edit_settings()

        

        self.setup_ui()
        self.load_presets()

    def edit_settings(self):
        simpledialog.messagebox.showinfo("Initial config", "Please look at the readme file to get the exact tablet name and size in mm.\nYou will be prompted to enter them in a moment.\n")
        
        TABLET_NAME = simpledialog.askstring(title="Tablet name",
                              prompt="Enter tablet name(get exact name from readme):", initialvalue=self.TABLET_NAME)
        if not TABLET_NAME:
            return
        
        TABLET_WIDTH_MM = simpledialog.askfloat(title="Tablet width (mm)",
                               prompt="Enter tablet width (mm):", initialvalue=self.TABLET_WIDTH_MM)
        if TABLET_WIDTH_MM is None:
            return
        
        TABLET_HEIGHT_MM = simpledialog.askfloat(title="Tablet height (mm)",
                                prompt="Enter tablet height (mm):", initialvalue=self.TABLET_HEIGHT_MM)
        if TABLET_HEIGHT_MM is None:
            return
        
        self.TABLET_NAME = TABLET_NAME
        self.TABLET_WIDTH_MM = TABLET_WIDTH_MM 
        self.TABLET_HEIGHT_MM = TABLET_HEIGHT_MM

        if len(utils.get_monitor_resolutions()) == 1:
            self.MONITOR_INDEX = 0
            self.TARGET_WIDTH = utils.get_monitor_resolutions()[self.MONITOR_INDEX][0]
            self.TARGET_HEIGHT = utils.get_monitor_resolutions()[self.MONITOR_INDEX][1]
            self.TARGET_POS = (int(self.TARGET_WIDTH/2), int(self.TARGET_HEIGHT/2))

        else:
            utils.get_monitor_resolutions()
            MONITOR_INDEX = utils.choose_monitor(utils.get_monitor_resolutions())
            if MONITOR_INDEX is None:
                pass
            else:
                self.MONITOR_INDEX = MONITOR_INDEX

            for i, res in enumerate(utils.get_monitor_resolutions()):
                if res == self.MONITOR_INDEX:
                    self.MONITOR_INDEX = i
                    break
            self.TARGET_WIDTH = utils.get_monitor_resolutions()[self.MONITOR_INDEX][0]
            self.TARGET_HEIGHT = utils.get_monitor_resolutions()[self.MONITOR_INDEX][1]
            self.TARGET_POS = (int(self.TARGET_WIDTH/2), int(self.TARGET_HEIGHT/2))

        self.ad.write_file("settings.json", json.dumps({
            "t_width_mm": self.TABLET_WIDTH_MM,
            "t_height_mm": self.TABLET_HEIGHT_MM,
            "tablet_name": self.TABLET_NAME,
            "monitor_index": self.MONITOR_INDEX
        }, indent=2))

    def setup_ui(self):

        self.deiconify()
        menubar = Menu(self)
        self.config(menu=menubar)
        
        file = Menu(menubar, tearoff = 0)
        menubar.add_cascade(label ='File', menu = file)
        file.add_command(label ='Copy width', command = self.copy_width)
        file.add_command(label ='Copy height', command = self.copy_height)
        file.add_separator()
        file.add_command(label="Tablet settings", command=self.open_tablet_settings)
        file.add_separator()
        file.add_command(label="Setup", command=self.edit_settings)
        file.add_command(label ='Remove all app data', command = self.remove_all_app_data)

        preset = Menu(menubar, tearoff = 0)
        menubar.add_cascade(label ='Preset', menu = preset)
        preset.add_command(label ='Save preset', command = self.save_preset)
        preset.add_command(label ='Delete preset', command = self.delete_selected_preset)


        menubar.add_command(label ='Repo', command = lambda: webbrowser.open(""))

        title_label = ttk.Label(self, text="Resolution Scaler", font=("Segoe UI", 16, "bold"))
        title_label.pack(pady=(10, 5))

        ttk.Label(self, text="Scale Factor (0.001 - 1.0):").pack(pady=(15, 5))

        self.scale_var = tk.StringVar(value="1")
        self.scale_entry = ttk.Entry(self, textvariable=self.scale_var, width=20)
        self.scale_entry.pack(pady=5)
        self.scale_entry.bind("<KeyRelease>", lambda e: self.update_scaled())

        ttk.Label(self, text="Preset Name:").pack(pady=(10, 0))
        self.preset_name_var = tk.StringVar()
        self.preset_name_entry = ttk.Entry(self, textvariable=self.preset_name_var, width=30)
        self.preset_name_entry.pack(pady=5)

        self.result_label = ttk.Label(self, text="Scaled Width: 0, Scaled Height: 0", font=("Segoe UI", 10, "bold"))
        self.result_label.pack(pady=10)

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=5)

        #ttk.Button(button_frame, text="Copy Width", command=self.copy_width).grid(row=0, column=0, padx=5)
        #ttk.Button(button_frame, text="Copy Height", command=self.copy_height).grid(row=0, column=1, padx=5)
        #ttk.Button(button_frame, text="Save Preset", command=self.save_preset).grid(row=0, column=0, padx=5)
        #ttk.Button(button_frame, text="Delete Preset", command=self.delete_selected_preset).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Apply to Tablet", command=self.apply_to_tablet).grid(row=0, column=2, padx=5)
        #ttk.Button(button_frame, text="Tablet settings", command=self.open_tablet_settings).grid(row=0, column=3, padx=5)

        self.settings_label = ttk.Label(self, text="R: "+str(self.TABLET_ROTATION)+"°, A: "+self.ALIGNMENT.replace("_", " ").title(), font=("Segoe UI", 10, "bold"))
        self.settings_label.pack(pady=(10, 0))

        ttk.Label(self, text="Saved Presets:").pack(pady=(15, 5))
        self.preset_listbox = tk.Listbox(self, height=8, width=40)
        self.preset_listbox.pack(pady=5)
        self.preset_listbox.bind("<<ListboxSelect>>", self.apply_selected_preset)

        

        self.update_scaled()

    def open_tablet_settings(self):
        TabletSettings(self)


    def update_scaled(self):
        try:
            scale = float(self.scale_var.get())
            if 0.001 <= scale <= 1.0:
                width = int(self.TARGET_WIDTH * scale)
                height = int(self.TARGET_HEIGHT * scale)
                self.result_label.config(text=f"Scaled Width: {width}, Scaled Height: {height}")
            else:
                self.result_label.config(text="Scale factor out of range.")
        except ValueError:
            self.result_label.config(text="Invalid scale factor.")

    def copy_width(self):
        try:
            scale = float(self.scale_var.get())
            width = int(self.TARGET_WIDTH * scale)
            self.clipboard_clear()
            self.clipboard_append(width)
            messagebox.showinfo("Copied", f"Scaled Width: {width} copied to clipboard!")
        except ValueError:
            messagebox.showerror("Error", "Invalid scale factor.")

    def copy_height(self):
        try:
            scale = float(self.scale_var.get())
            height = int(self.TARGET_HEIGHT * scale)
            self.clipboard_clear()
            self.clipboard_append(height)
            messagebox.showinfo("Copied", f"Scaled Height: {height} copied to clipboard!")
        except ValueError:
            messagebox.showerror("Error", "Invalid scale factor.")

    def remove_all_app_data(self):
        confirm_1 = messagebox.askyesno("Confirm", "Are you sure you want to remove all app data? This will delete all presets and settings.", icon='warning')
        confirm_2 = messagebox.askyesno("Confirm", "This will also terminate otd.exe if it is running.\nAre you sure you want to continue?", icon='warning')
        if confirm_1 and confirm_2:
            utils.kill_otd()
            self.ad.clear_app_data()
            messagebox.showinfo("Cleared", "All app data has been cleared.\nPlease restart the application.")
            self.destroy()

    def save_preset(self):
        name = self.preset_name_var.get().strip()
        try:
            scale = float(self.scale_var.get())
            if not (0.001 <= scale <= 1.0):
                raise ValueError("Scale out of range.")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid scale factor (0.001 - 1.0).")
            return

        if not name:
            messagebox.showerror("Error", "Please enter a name for the preset.")
            return

        if any(p["name"] == name for p in self.presets):
            messagebox.showinfo("Exists", "A preset with this name already exists.")
            return

        preset = {"name": name, "scale": scale, "rotation": self.TABLET_ROTATION, "alignment": self.ALIGNMENT}
        self.presets.append(preset)
        self.save_presets_to_file()
        self.update_preset_listbox()
        self.preset_name_var.set("")
        messagebox.showinfo("Saved", f"Preset '{name}' saved successfully.")

    def save_presets_to_file(self):
        with open(self.ad.get_app_folder()+"\\presets.json", "w") as f:
            json.dump(self.presets, f, indent=2)

    def load_presets(self):
        if os.path.exists(self.ad.get_app_folder()+"\\presets.json"):
            with open(self.ad.get_app_folder()+"\\presets.json", "r") as f:
                try:
                    self.presets = json.load(f)
                except json.JSONDecodeError:
                    self.presets = []
        self.update_preset_listbox()

    def update_preset_listbox(self):
        self.preset_listbox.delete(0, tk.END)
        for preset in self.presets:
            display = f"{preset['name']} (Scale: {preset['scale']:.3f})"
            self.preset_listbox.insert(tk.END, display)

    def apply_selected_preset(self, event):
        selection = self.preset_listbox.curselection()
        if selection:
            index = selection[0]
            preset = self.presets[index]
            self.scale_var.set(str(preset["scale"]))
            try:
                self.ALIGNMENT = preset["alignment"]
                self.TABLET_ROTATION = preset["rotation"]
            except KeyError:
                pass
            self.update_settings_label()
            self.update_scaled()

    def delete_selected_preset(self):
        selection = self.preset_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a preset to delete.")
            return

        index = selection[0]
        preset_name = self.presets[index]["name"]
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the preset '{preset_name}'?")
        if confirm:
            del self.presets[index]
            self.save_presets_to_file()
            self.update_preset_listbox()
            messagebox.showinfo("Deleted", f"Preset '{preset_name}' deleted successfully.")

    def get_position(self, height_mm, width_mm):
        if self.ALIGNMENT == "TOP_LEFT":
            return (self.TABLET_WIDTH_MM - width_mm/2, self.TABLET_HEIGHT_MM - height_mm/2)
        elif self.ALIGNMENT == "TOP_RIGHT":
            return (self.TABLET_WIDTH_MM - width_mm/2, height_mm/2)
        elif self.ALIGNMENT == "BOTTOM_LEFT":
            return (width_mm/2, self.TABLET_HEIGHT_MM - height_mm/2)
        elif self.ALIGNMENT == "BOTTOM_RIGHT":
            return (width_mm/2, height_mm/2)
        else:
            raise ValueError("Invalid alignment specified.")

    def update_settings_label(self):
        self.settings_label.config(
            text=f"R: {self.TABLET_ROTATION}°, A: {self.ALIGNMENT.replace('_', ' ').title()}"
        )

    def apply_to_tablet(self):
        try:
            scale = float(self.scale_var.get())
            if not (0.001 <= scale <= 1.0):
                raise ValueError("Scale out of range.")
        except ValueError:
            messagebox.showerror("Error", "Invalid scale factor.")
            return

        width_mm = round((self.TABLET_WIDTH_MM * scale))
        height_mm = round((self.TABLET_HEIGHT_MM * scale))
        print(f"Calculated Tablet Area: {width_mm}mm x {height_mm}mm")
        if not self.TABLET_NAME:
            messagebox.showerror("Error", "Failed to detect tablet name.")
            return

        try:
            # Set the display area to the chosen monitor
            result_1 = subprocess.run(
                ["otd", "setdisplayarea", self.TABLET_NAME, str(self.TARGET_WIDTH), str(self.TARGET_HEIGHT), str(self.TARGET_POS[0]), str(self.TARGET_POS[1])],
                capture_output=True, text=True
            )

            
            # Then set the tablet area with your scale-based sizes as before
            pos = self.get_position(height_mm, width_mm)
            result_2 = subprocess.run(
                ["otd",
                 "settabletarea",
                 self.TABLET_NAME,
                 str(width_mm),
                 str(height_mm),
                 str(pos[0]).replace(".", ","),
                 str(pos[1]).replace(".", ","),
                 str(self.TABLET_ROTATION)
                ],
                capture_output=True, text=True
            )

            if result_1.returncode != 0 and result_2.returncode != 0:
                raise Exception("[! 1] \n" + result_1.stderr + "\n[! 2] \n" + result_2.stderr)

            messagebox.showinfo("Success", f"Tablet area updated to {width_mm}mm x {height_mm}mm.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply to tablet:\n{e}")

class TabletSettings(tk.Toplevel):
    def __init__(self, master=None, change_string=None):
        super().__init__(master)
        self.master = master
        self.rotation = self.master.TABLET_ROTATION  # Current rotation angle (0, 90, 180, 270)
        self.geometry("400x400")
        self.configure(bg="white")
        self.title("Tablet config")
        self.change_string = change_string

        # Display rotation text
        self.rotation_label = tk.Label(self, text=str(self.rotation)+"°", font=("Arial", 24), fg="gold", bg="white")
        self.rotation_label.place(relx=0.5, rely=0.5, anchor="center")

        # Create 4 corner buttons
        self.corners = []
        self.create_corner_buttons()

        # Bind click event to the whole window
        self.bind("<Button-1>", self.handle_click)

    def create_corner_buttons(self):
        button_style = {"bg": "gold", "width": 4, "height": 2}
        positions = [
            (0, 0, "nw", "TOP_LEFT"),
            (1, 0, "ne", "TOP_RIGHT"),
            (0, 1, "sw", "BOTTOM_LEFT"),
            (1, 1, "se", "BOTTOM_RIGHT"),
        ]
        for relx, rely, anchor, alignment in positions:
            btn = tk.Button(self, **button_style,
                            command=lambda a=alignment: self.update_alignment(a))
            btn.place(relx=relx, rely=rely, anchor=anchor)
            self.corners.append(btn)

    def handle_click(self, event):
        # If the clicked widget is one of the corner buttons, do nothing
        if event.widget in self.corners:
            return

        # Rotate by 90°
        self.rotation = (self.rotation + 90) % 360
        self.rotation_label.config(text=f"{self.rotation}°")

        # Update global rotation
        self.master.TABLET_ROTATION = self.rotation
        self.master.update_settings_label()

        self.change_string = ttk.Label(self, text="R: "+str(self.master.TABLET_ROTATION)+"°, A: "+self.master.ALIGNMENT.replace("_", " ").title(), font=("Segoe UI", 10, "bold"))

    def update_alignment(self, alignment):
        self.master.ALIGNMENT = alignment
        self.master.update_settings_label()

        print(f"Alignment set to: {self.master.ALIGNMENT}")

        
if __name__ == "__main__":
    app = ResolutionScaler()
    app.mainloop()