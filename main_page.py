import os
import tkinter as tk
from tkinter import messagebox
from utilities import read_csv_file, read_csv_data


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=2)
        self.grid_rowconfigure(3, weight=2)

        self.initialize_widgets()

    def initialize_widgets(self):
        # ROW 0 ________________________________________
        crow = 0
        tk.Label(self, padx=5, pady=2, text="AUSTEST SHOCK PROGRAM",
                 font="Helvetica 16 bold").grid(column=0, row=crow, padx=5, pady=(5, 0), sticky=tk.S)

        # ROW 1 ________________________________________
        crow = 1
        tk.Label(self, padx=5, pady=2, text="Select type of shock to analyse",
                 font="Helvetica 10").grid(column=0, row=crow, padx=5, pady=(0, 5), sticky=tk.N)

        # ROW 2 ________________________________________
        crow = 2
        btn_file_select = tk.Button(self, padx=5, pady=5, command=self.file_select, text="SRS (csv file)",
                                    font="Helvetica 14")
        btn_file_select.grid(column=0, row=crow, padx=5, pady=5, sticky=tk.N)

        # ROW 3 ________________________________________
        crow = 3
        btn_hs_select = tk.Button(self, padx=5, pady=5, command=self.hs_select, text="Half Sine (csv file)",
                                  font="Helvetica 14")
        btn_hs_select.grid(column=0, row=crow, padx=5, pady=5, sticky=tk.N)

    def file_select(self):
        try:
            filename = read_csv_file()
            head_tail = os.path.split(filename.name)
            self.controller.table_info['path'] = head_tail[1]
            self.controller.channels_volt, self.controller.table_info['ch_num'] = read_csv_data(filename)

            # Open import page and destroy self
            self.controller.page_2_open()
            self.destroy()

        except Exception as e:
            tk.messagebox.showerror(title="Error", message=str(e))
            return

    def hs_select(self):
        pass
