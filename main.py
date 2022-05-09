import tkinter as tk
from tkinter import messagebox
import numpy as np

from acceldata import AccelData
from utilities import save_file, write2txt


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        # Widgets
        lbl_import = tk.Label(self, text="Import Oscilloscope File:")
        lbl_import.grid(row=0, column=0, padx=5, pady=2, sticky="W")

        self.btn_import = tk.Button(self, command=self.import_click, text="Read Data", padx=5, pady=5)
        self.btn_import.grid(row=1, column=0, padx=5, pady=5)

        lbl_export = tk.Label(self, text="Export time vs acceleration data:")
        lbl_export.grid(row=2, column=0, padx=5, pady=2, sticky="W")

        self.btn_export_txt = tk.Button(self, state="disabled", command=self.export_txt_click,  text="Export Data", padx=5, pady=5)
        self.btn_export_txt.grid(row=3, column=0, padx=5, pady=5)

    def import_click(self):
        import_win = AccelData(self, self.controller)
        self.wait_window(import_win)

        if not self.controller.bool_imported:
            pass
        else:
            self.btn_import.config(state="disabled")
            self.btn_export_txt.config(state="normal")
            tk.messagebox.showinfo(title="Info", message="File imported successfully!")

    def export_txt_click(self):
        file = save_file()
        write2txt(file, self.controller.channels_accel)
        file.close()
        tk.messagebox.showinfo(title="Info", message="File exported successfully!")


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # configure root window
        self.title("Shock Control System")
        self.geometry("300x250")
        self.resizable(False, False)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {"MainFrame": MainPage(container, self)}
        self.frames["MainFrame"].pack(side="top", fill="both", expand=True)

        #############################
        # Variable Controller
        #############################

        # Checkbox values from AccelData()
        self.chbox_val = [tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()]
        # Sensitivity values from AccelData()
        self.sens_val = np.array((10, 10, 0, 0), dtype=float)
        # File imported boolean
        self.bool_imported = False

        # time and voltage from oscilloscope
        self.channels_volt = []
        # time and channels from oscilloscope
        self.channels_accel = []


if __name__ == "__main__":
    app = App()
    app.mainloop()
