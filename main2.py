import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from acceldata import AccelData
from srs import Srs
from utilities import save_file, write2txt


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        # Widgets
        lbl_import = tk.Label(self, text="Import Oscilloscope Data:")
        lbl_import.grid(row=0, column=0, columnspan=2, padx=5, pady=2, sticky=tk.W)

        self.btn_import = tk.Button(self, command=self.import_click, text="Read", padx=5, pady=5, width=7)
        self.btn_import.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

        self.btn_connect = tk.Button(self, text="Connect", state="disabled", padx=5, pady=5, width=7)
        self.btn_connect.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

        lbl_plot = tk.Label(self, text="Time Data:")
        lbl_plot.grid(row=2, column=0, columnspan=2, padx=5, pady=2, sticky=tk.W)

        self.btn_plot = tk.Button(self, state="disabled", command=lambda: MainPlot.update_plot(self.controller.app2),
                                  text="Plot", padx=5, pady=5, width=7)
        self.btn_plot.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

        self.btn_export_time = tk.Button(self, state="disabled", command=self.export_txt_click, text="Export",
                                         padx=5, pady=5, width=7)
        self.btn_export_time.grid(row=3, column=1, padx=10, pady=5)

        lbl_srs = tk.Label(self, text="Calculate SRS (CH1):")
        lbl_srs.grid(row=4, column=0, columnspan=2, padx=5, pady=2, sticky=tk.W)

        self.btn_srs = tk.Button(self, state="normal", command=self.srs_click, text="SRS",
                                 padx=5, pady=5, width=7)
        self.btn_srs.grid(row=5, column=0, padx=10, pady=5)

        self.btn_export_srs = tk.Button(self, state="disabled", command=self.export_srs_click, text="Export",
                                        padx=5, pady=5, width=7)
        self.btn_export_srs.grid(row=5, column=1, padx=10, pady=5)

    def import_click(self):
        import_win = AccelData(self, self.controller)
        self.wait_window(import_win)

        if not self.controller.bool_imported:
            pass
        else:
            self.btn_import.config(state="disabled")
            self.btn_export_time.config(state="normal")
            self.btn_plot.config(state="normal")
            self.btn_srs.config(state="normal")
            tk.messagebox.showinfo(title="Info", message="File imported successfully!")

    def export_txt_click(self):
        file = save_file()
        write2txt(file, self.controller.channels_accel)
        tk.messagebox.showinfo(title="Info", message="Time Data vs Acceleration exported successfully!")

    def srs_click(self):
        srs_win = Srs(self, self.controller)
        self.wait_window(srs_win)
        self.btn_export_srs.config(state="normal")

    def export_srs_click(self):
        file = save_file()
        a = np.vstack((self.controller.fn, self.controller.a_abs))
        a = np.transpose(a)
        write2txt(file, a)
        tk.messagebox.showinfo(title="Info", message="SRS exported successfully!")


class MainPlot(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        self.fig, self.ax = plt.subplots()
        self.ax.set(xlabel='Time (s)', ylabel='Acceleration (gn)',
                    title='Acceleration vs Time')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.toolbar.pack(side="top", fill="both", expand=True)

    def update_plot(self):
        for i in range(1, 4):
            if self.controller.chbox_val[i-1].get() == 1:
                self.ax.plot(self.controller.channels_accel[:, 0], self.controller.channels_accel[:, i])
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

        self.app1 = MainPage(container, self)
        self.app2 = MainPlot(container, self)
        self.app1.pack(side="left", fill="y", expand=False)
        self.app2.pack(side="right", fill="both", expand=True)

        #############################
        # Variable Controller
        #############################

        # Checkbox values from AccelData()
        self.chbox_val = [tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()]
        # Sensitivity values from AccelData()
        self.sens_val = np.array((10, 10, 0, 0), dtype=float)
        # Oscilloscope file imported boolean
        self.bool_imported = False
        # time and voltage from oscilloscope
        self.channels_volt = []
        # time and channels from oscilloscope
        self.channels_accel = []
        # frequency array
        self.fn = []
        self.a_abs = []


if __name__ == "__main__":
    app = App()
    app.mainloop()
