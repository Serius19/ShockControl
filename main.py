import tkinter as tk
import numpy as np
from import_page import ImportPage
from export_page import ExportPage


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # configure root window
        self.title("Shock Control System")
        self.resizable(False, False)

        #############################
        # Variable Controller
        #############################
        # Checkbox values from import_page()
        self.chbox_val = [tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()]
        # Sensitivity values from import_page()
        self.sens_val = np.array((10, 10, 10, 10), dtype=float)
        # time and voltage from import_page()
        self.channels_volt = []
        # time and channels from import_page()
        self.channels_accel = []
        # frequency array from srs.py
        self.fn = []
        # Acceleration array from srs.py
        self.a_abs = []
        # table info for export page
        self.table_info = {'path': str(), 'dt': float(), 'samples': int()}

        #############################
        # Frame Controller
        #############################
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.Page1 = ImportPage(parent=container, controller=self)
        self.Page2 = ExportPage(parent=container, controller=self)
        self.Page1.grid(row=0, column=0, sticky="nsew")
        self.Page2.grid(row=0, column=0, sticky="nsew")
        self.Page1.tkraise()

    @staticmethod
    def change_page(page):
        page.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()
