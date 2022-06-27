import tkinter as tk
import numpy as np
from main_page import MainPage
from import_page import ImportPage
from export_page import ExportPage


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # configure root window
        self.title("Shock Control System")
        self.resizable(True, True)

        #############################
        # Variable Controller
        #############################
        # Checkbox IntVar() values from import_page()
        self.chbox_val = [tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()]
        # Checkbox Int values from import_page()
        self.chbox_int = [int(), int(), int(), int()]
        # Sensitivity values from import_page()
        self.sens_val = np.array((10, 10, 10, 10), dtype=float)
        # time and voltage from import_page()
        self.channels_volt = []
        # time and channels from import_page()
        self.channels_accel = []
        #Filter array from Lowpassfilt
        self.channels_filt = []
        # frequency array from srs.py
        self.fn = []
        # Acceleration array from srs.py
        self.a_abs = []
        # table info for export page
        self.table_info = {'path': str(), 'dt': float(), 'sr': float(), 'samples': int(), 'ch_num': int(0)}


        #############################
        # Frame Controller
        #############################
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.Page_1 = MainPage(parent=self.container, controller=self)
        self.Page_1.grid(row=0, column=0, sticky="nsew")

    def page_1_open(self):
        self.Page_1 = MainPage(parent=self.container, controller=self)
        self.Page_1.grid(row=0, column=0, sticky="nsew")

    def page_2_open(self):
        self.Page_2 = ImportPage(parent=self.container, controller=self)
        self.Page_2.grid(row=0, column=0, sticky="nsew")

    def page_3_open(self):
        self.Page_3 = ExportPage(parent=self.container, controller=self)
        self.Page_3.grid(row=0, column=0, sticky="nsew")


if __name__ == "__main__":
    app = App()
    app.mainloop()
