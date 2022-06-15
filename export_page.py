import tkinter as tk
from tkinter import messagebox
import numpy as np
from utilities import save_file, write2txt
from srs import Srs


class ExportPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        self.initialize_widgets()

    def initialize_widgets(self):
        # ROW 0 ________________________________________
        crow = 0
        btn_import_nf = tk.Button(self, state="normal", command=self.import_nf_click, text="Import New File",
                                  padx=5, pady=5, width=8)
        btn_import_nf.grid(row=crow, column=0, padx=10, pady=5)

        # ROW 1 ________________________________________
        crow = 1
        btn_view_volt = tk.Button(self, state="normal", command=self.view_volt_click, text="Plot Voltage",
                                  padx=5, pady=5, width=8)
        btn_view_volt.grid(row=crow, column=0, padx=10, pady=5)

        # ROW 2______________________________________
        crow = 2
        btn_view_g = tk.Button(self, state="normal", command=self.view_volt_click, text="Plot Acceleration",
                               padx=5, pady=5, width=8)
        btn_view_g.grid(row=crow, column=0, padx=10, pady=5)

        # ROW 3______________________________________
        crow = 3
        self.btn_export_time = tk.Button(self, state="normal", command=self.export_txt_click, text="Export",
                                         padx=5, pady=5, width=7)
        self.btn_export_time.grid(row=crow, column=0, columnspan=2, padx=10, pady=5)

        # ROW 3______________________________________
        crow = 3
        lbl_srs = tk.Label(self, text="Calculate SRS (CH1):")
        lbl_srs.grid(row=crow, column=0, columnspan=2, padx=5, pady=2, sticky=tk.W)

        # ROW 4______________________________________
        crow = 4
        self.btn_srs = tk.Button(self, state="normal", command=self.srs_click, text="SRS",
                                 padx=5, pady=5, width=7)
        self.btn_srs.grid(row=crow, column=0, padx=10, pady=5)

        self.btn_export_srs = tk.Button(self, state="disabled", command=self.export_srs_click, text="Export",
                                        padx=5, pady=5, width=7)
        self.btn_export_srs.grid(row=crow, column=1, padx=10, pady=5)

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
        srs_final = np.vstack((self.controller.fn, self.controller.a_abs))
        write2txt(file, np.transpose(srs_final))
        tk.messagebox.showinfo(title="Info", message="SRS exported successfully!")

    def import_nf_click(self):
        pass

    def view_volt_click(self):
        pass

    def view_g_click(self):
        pass
