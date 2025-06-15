import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, Menu
from ttkthemes import ThemedTk
import json
import os
import subprocess
import ctypes
import utils
import webbrowser

THEME = "yaru"
utils.set_per_monitor_v2_dpi_awareness()

class ResolutionScaler(ThemedTk):
    def __init__(self):
        super().__init__()
        self.ad = utils.AppData("ResolutionScaler")

        self.USER32 = ctypes.windll.user32
        self.SCREEN_SIZE = utils.get_monitor_resolutions()[0]
        self.OTD_PATH = os.path.join(self.ad.get_app_folder(), "otd_daemon.exe")
        is_otd_running = utils.is_otd_running()
        self.withdraw()

        if not os.path.exists(self.OTD_PATH) and not is_otd_running:
            if messagebox.askyesno("Error", "otd_daemon.exe not found. Download it?"):
                utils.download_otd(self.ad.get_app_folder())
                messagebox.showinfo("Download complete", "otd_daemon.exe is ready.")
                utils.run_daemon_silently(self.OTD_PATH)
            else:
                self.destroy()
                return

        self.TARGET_WIDTH, self.TARGET_HEIGHT = self.SCREEN_SIZE
        self.TARGET_POS = (self.TARGET_WIDTH // 2, self.TARGET_HEIGHT // 2)
        self.TABLET_ROTATION = 180
        self.TABLET_WIDTH_MM = 101.6
        self.TABLET_HEIGHT_MM = 76.2
        self.TABLET_NAME = "XP-Pen Star G430S"
        self.MONITOR_INDEX = 0
        self.ALIGNMENT = "TOP_LEFT"

        self.PRESET_FILE_PATH = os.path.join(self.ad.get_app_folder(), "presets.json")
        self.title("Resolution Scaler")
        self.geometry("600x900")
        self.resizable(False, False)
        self.minsize(500, 500)

        self.style = ttk.Style(self)
        self.style.theme_use(THEME)

        self.presets = []
        self.configure(bg="#f8f8f8")

        self.load_settings()
        self.setup_ui()
        self.load_presets()
        self.deiconify()

    def load_settings(self):
        data = self.ad.read_file("settings.json")
        if data:
            try:
                settings = json.loads(data)
                self.TABLET_WIDTH_MM = settings.get("t_width_mm", 101.6)
                self.TABLET_HEIGHT_MM = settings.get("t_height_mm", 76.2)
                self.TABLET_NAME = settings.get("tablet_name", self.TABLET_NAME)
                self.MONITOR_INDEX = settings.get("monitor_index", 0)
                self.TARGET_WIDTH, self.TARGET_HEIGHT = utils.get_monitor_resolutions()[self.MONITOR_INDEX]
                self.TARGET_POS = (self.TARGET_WIDTH // 2, self.TARGET_HEIGHT // 2)
            except json.JSONDecodeError:
                print("settings.json is invalid.")
        else:
            self.edit_settings()

    def setup_ui(self):
        self.create_menu()

        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        ttk.Label(main_frame, text="Resolution Scaler", font=("Segoe UI", 16, "bold")).pack(pady=10)
        ttk.Separator(main_frame).pack(fill="x", pady=10)

        input_frame = ttk.LabelFrame(main_frame, text="Scaling")
        input_frame.pack(fill="x", pady=10)

        ttk.Label(input_frame, text="Scale Factor (0.001 - 1.0):").pack(anchor="w", pady=(10, 0))
        self.scale_var = tk.StringVar(value="1")
        self.scale_entry = ttk.Entry(input_frame, textvariable=self.scale_var, width=15)
        self.scale_entry.pack(pady=5)
        self.scale_entry.bind("<KeyRelease>", lambda e: self.update_scaled())

        ttk.Label(input_frame, text="Preset Name:").pack(anchor="w", pady=(10, 0))
        self.preset_name_var = tk.StringVar()
        self.preset_name_entry = ttk.Entry(input_frame, textvariable=self.preset_name_var, width=25)
        self.preset_name_entry.pack(pady=5)

        self.result_label = ttk.Label(input_frame, text="Scaled Width: 0, Scaled Height: 0")
        self.result_label.pack(pady=10)

        ttk.Button(input_frame, text="Apply to Tablet", command=self.apply_to_tablet).pack(pady=5)

        self.settings_label = ttk.Label(main_frame, text="R: 180°, A: Top Left", font=("Segoe UI", 10, "bold"))
        self.settings_label.pack(pady=10)

        ttk.Separator(main_frame).pack(fill="x", pady=10)

        preset_frame = ttk.LabelFrame(main_frame, text="Presets")
        preset_frame.pack(fill="both", expand=True)

        self.preset_listbox = tk.Listbox(preset_frame, height=8)
        self.preset_listbox.pack(fill="both", expand=True, padx=10, pady=5)
        self.preset_listbox.bind("<<ListboxSelect>>", self.apply_selected_preset)

        btn_frame = ttk.Frame(preset_frame)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Save Preset", command=self.save_preset).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Delete Preset", command=self.delete_selected_preset).grid(row=0, column=1, padx=5)

        self.update_scaled()

    def edit_settings(self):
        settings_win = tk.Toplevel(self)
        settings_win.title("Setup")
        settings_win.geometry("400x300")
        settings_win.resizable(False, False)

        form = ttk.Frame(settings_win, padding=20)
        form.pack(expand=True, fill="both")

        def make_field(label, var, row):
            ttk.Label(form, text=label).grid(row=row, column=0, sticky="w", pady=5)
            entry = ttk.Entry(form, textvariable=var)
            entry.grid(row=row, column=1, sticky="ew", pady=5)
            form.grid_columnconfigure(1, weight=1)

        width_var = tk.StringVar(value=str(self.TABLET_WIDTH_MM))
        height_var = tk.StringVar(value=str(self.TABLET_HEIGHT_MM))
        name_var = tk.StringVar(value=self.TABLET_NAME)
        monitor_var = tk.StringVar(value=str(self.MONITOR_INDEX + 1))

        make_field("Tablet Width (mm):", width_var, 0)
        make_field("Tablet Height (mm):", height_var, 1)
        make_field("Tablet Name:", name_var, 2)
        make_field("Monitor Number:", monitor_var, 3)

        def save():
            try:
                self.TABLET_WIDTH_MM = float(width_var.get())
                self.TABLET_HEIGHT_MM = float(height_var.get())
                self.TABLET_NAME = name_var.get()
                self.MONITOR_INDEX = int(monitor_var.get()) + 1
                self.TARGET_WIDTH, self.TARGET_HEIGHT = utils.get_monitor_resolutions()[self.MONITOR_INDEX]
                self.TARGET_POS = (self.TARGET_WIDTH // 2, self.TARGET_HEIGHT // 2)

                self.ad.write_file("settings.json", json.dumps({
                    "t_width_mm": self.TABLET_WIDTH_MM,
                    "t_height_mm": self.TABLET_HEIGHT_MM,
                    "tablet_name": self.TABLET_NAME,
                    "monitor_index": self.MONITOR_INDEX
                }, indent=2))

                messagebox.showinfo("Saved", "Settings updated successfully.")
                settings_win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Could not save settings:\n{e}")

        ttk.Button(form, text="Save", command=save).grid(row=4, column=0, columnspan=2, pady=10)


    def create_menu(self):
        menubar = Menu(self)
        self.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Copy Width", command=self.copy_width)
        file_menu.add_command(label="Copy Height", command=self.copy_height)
        file_menu.add_separator()
        file_menu.add_command(label="Tablet Settings", command=self.open_tablet_settings)
        file_menu.add_command(label="Setup", command=self.edit_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Remove All App Data", command=self.remove_all_app_data)
        menubar.add_cascade(label="File", menu=file_menu)

        menubar.add_command(label="Repo", command=lambda: webbrowser.open("https://github.com/IgnacyFluder/ResolutionScaler"))

    def update_scaled(self):
        try:
            scale = float(self.scale_var.get())
            if 0.001 <= scale <= 1.0:
                width = int(self.TARGET_WIDTH * scale)
                height = int(self.TARGET_HEIGHT * scale)
                self.result_label.config(text=f"Scaled Width: {width}, Scaled Height: {height}")
            else:
                self.result_label.config(text="Scale out of range.")
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

    def save_preset(self):
        name = self.preset_name_var.get().strip()
        try:
            scale = float(self.scale_var.get())
            if not (0.001 <= scale <= 1.0): raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter a valid scale factor (0.001 - 1.0).")
            return

        if not name:
            messagebox.showerror("Error", "Enter a name for the preset.")
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

    def delete_selected_preset(self):
        selection = self.preset_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Select a preset to delete.")
            return
        index = selection[0]
        preset_name = self.presets[index]["name"]
        if messagebox.askyesno("Confirm Delete", f"Delete preset '{preset_name}'?"):
            del self.presets[index]
            self.save_presets_to_file()
            self.update_preset_listbox()
            messagebox.showinfo("Deleted", f"Preset '{preset_name}' deleted.")

    def update_preset_listbox(self):
        self.preset_listbox.delete(0, tk.END)
        for p in self.presets:
            self.preset_listbox.insert(tk.END, f"{p['name']} (Scale: {p['scale']:.3f})")

    def apply_selected_preset(self, event):
        selection = self.preset_listbox.curselection()
        if not selection:
            return
        preset = self.presets[selection[0]]
        self.scale_var.set(str(preset["scale"]))
        self.TABLET_ROTATION = preset.get("rotation", 180)
        self.ALIGNMENT = preset.get("alignment", "TOP_LEFT")
        self.update_settings_label()
        self.update_scaled()

    def update_settings_label(self):
        self.settings_label.config(text=f"R: {self.TABLET_ROTATION}°, A: {self.ALIGNMENT.replace('_', ' ').title()}")

    def remove_all_app_data(self):
        if messagebox.askyesno("Confirm", "Delete all app data? This will close the app.", icon='warning'):
            utils.kill_otd()
            self.ad.clear_app_data()
            messagebox.showinfo("Cleared", "All app data has been cleared. Restart the app.")
            self.destroy()

    def save_presets_to_file(self):
        with open(self.PRESET_FILE_PATH, "w") as f:
            json.dump(self.presets, f, indent=2)

    def load_presets(self):
        if os.path.exists(self.PRESET_FILE_PATH):
            with open(self.PRESET_FILE_PATH, "r") as f:
                try:
                    self.presets = json.load(f)
                except json.JSONDecodeError:
                    self.presets = []
        self.update_preset_listbox()

    def open_tablet_settings(self):
        TabletSettings(self)

    def get_position(self, height_mm, width_mm):
        if self.ALIGNMENT == "TOP_LEFT":
            return (self.TABLET_WIDTH_MM - width_mm/2, self.TABLET_HEIGHT_MM - height_mm/2)
        elif self.ALIGNMENT == "TOP_RIGHT":
            return (self.TABLET_WIDTH_MM - width_mm/2, height_mm/2)
        elif self.ALIGNMENT == "BOTTOM_LEFT":
            return (width_mm/2, self.TABLET_HEIGHT_MM - height_mm/2)
        elif self.ALIGNMENT == "BOTTOM_RIGHT":
            return (width_mm/2, height_mm/2)
        return (0, 0)

    def apply_to_tablet(self):
        try:
            scale = float(self.scale_var.get())
            if not (0.001 <= scale <= 1.0): raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid scale factor.")
            return

        width_mm = round(self.TABLET_WIDTH_MM * scale)
        height_mm = round(self.TABLET_HEIGHT_MM * scale)
        pos = self.get_position(height_mm, width_mm)

        try:
            subprocess.run([
                os.path.join(self.ad.get_app_folder(), 'otd.exe'),
                "setdisplayarea", self.TABLET_NAME,
                str(self.TARGET_WIDTH), str(self.TARGET_HEIGHT),
                str(self.TARGET_POS[0]), str(self.TARGET_POS[1])
            ], check=True)

            subprocess.run([
                os.path.join(self.ad.get_app_folder(), 'otd.exe'),
                "settabletarea", self.TABLET_NAME,
                str(width_mm), str(height_mm),
                str(pos[0]).replace(".", ","), str(pos[1]).replace(".", ","),
                str(self.TABLET_ROTATION)
            ], check=True)

            messagebox.showinfo("Success", f"Tablet area set to {width_mm}x{height_mm}mm.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to apply: {e}")

class TabletSettings(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.title("Tablet Settings")
        self.geometry("500x400")
        self.configure(bg="white")

        self.rotation = self.master.TABLET_ROTATION

        self.label = tk.Label(self, text=f"{self.rotation}°", font=("Segoe UI", 24), bg="white")
        self.label.pack(pady=20)

        self.button_frame = ttk.Frame(self)
        self.button_frame.pack()

        alignments = ["TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT"]
        for i, align in enumerate(alignments):
            ttk.Button(self.button_frame, text=align.replace("_", " "), command=lambda a=align: self.set_alignment(a)).grid(row=i//2, column=i%2, padx=10, pady=5)

        self.bind("<Button-1>", self.rotate)

    def rotate(self, event):
        if event.widget in self.button_frame.winfo_children():
            return
        self.rotation = (self.rotation + 90) % 360
        self.label.config(text=f"{self.rotation}°")
        self.master.TABLET_ROTATION = self.rotation
        self.master.update_settings_label()

    def set_alignment(self, alignment):
        self.master.ALIGNMENT = alignment
        self.master.update_settings_label()

if __name__ == "__main__":
    app = ResolutionScaler()
    app.mainloop()
