import tkinter as tk
from tkinter import messagebox

import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

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
            MainPlot(self, self.controller).update_plot()

    def export_txt_click(self):
        file = save_file()
        write2txt(file, self.controller.channels_accel)
        file.close()
        tk.messagebox.showinfo(title="Info", message="File exported successfully!")


class MainPlot(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        self.fig, self.ax = plt.subplots()
        self.ax.set(xlabel='time (ms)', ylabel='Acceleration (gn)',
                    title='Acceleration vs Time')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

    def update_plot(self):
        for i in range(0, len(self.controller.channels_accel)):
            self.ax.plot(self.controller.channels_accel[0], self.controller.channels_accel[i])
        self.canvas.draw()


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # configure root window
        self.title("Shock Control System")
        # self.geometry("300x250")
        # self.resizable(False, False)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {"MainFrame": MainPage(container, self), "MainPlot": MainPlot(container, self)}
        self.frames["MainFrame"].grid(column=0, row=0, padx=5, pady=5)
        self.frames["MainPlot"].grid(column=1, row=0, padx=5, pady=5)

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
