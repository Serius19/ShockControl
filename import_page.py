import tkinter as tk
from tkinter import messagebox
import numpy as np


class ImportPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        self.entries = [tk.Entry(), tk.Entry(), tk.Entry(), tk.Entry()]
        self.checkboxes = [tk.Checkbutton(), tk.Checkbutton(), tk.Checkbutton(), tk.Checkbutton()]
        self.channels = []

        self.initialize_widgets()

    def initialize_widgets(self):
        # ROW 0 ________________________________________
        message = (f"File: {self.controller.table_info['path']} | "
                   f"Channels detected: {self.controller.table_info['ch_num']}")

        crow = 0
        tk.Label(self, padx=5, pady=5, text=message, font="Helvetica 14").grid(column=0, columnspan=5, row=crow, padx=5, pady=5)

        # ROW MID ______________________________________
        for i in range(0, self.controller.table_info['ch_num']):
            lbl_ch = tk.Label(self, text="CH" + str(i + 1) + ":")
            lbl_ch.grid(column=0, row=i + 1, padx=5, pady=5)
            self.entries[i] = tk.Entry(self, width=10)
            self.entries[i].grid(column=3, row=i + 1, padx=5, pady=5)
            self.entries[i].insert(-1, str(self.controller.sens_val[i]))
            self.entries[i].config(state="disabled")
            tk.Label(self, text="Sensitivity:").grid(column=2, row=i + 1, padx=5, pady=5)
            tk.Label(self, text="mV/g").grid(column=4, row=i + 1, padx=5, pady=5)
            self.checkboxes[i] = tk.Checkbutton(self, fg="red", text="Disabled",
                                                command=self.cb_check, state="normal",
                                                variable=self.controller.chbox_val[i])
            self.checkboxes[i].grid(column=1, row=i + 1, padx=5, pady=5)

        self.checkboxes[0].select()
        self.cb_check()

        # ROW END ________________________________________
        crow = i+2
        btn_import = tk.Button(self, width=10, command=self.import_file, text="Import", padx=5, pady=5)
        btn_import.grid(column=1, row=crow, padx=5, pady=5)

        btn_quit = tk.Button(self, width=10, command=self.exit_page, text="Quit", padx=5, pady=5)
        btn_quit.grid(column=3, row=crow, padx=5, pady=5)

    def cb_check(self):
        for i in range(0, self.controller.table_info['ch_num']):
            if self.controller.chbox_val[i].get() == 1:
                self.checkboxes[i].config(fg="green", text="Enabled")
                self.entries[i].config(state="normal")
            else:
                self.checkboxes[i].config(fg="red", text="Disabled")
                self.entries[i].config(state="disabled")

    def import_file(self):
        # Iterate over checkbox intVar() to int()
        self.controller.chbox_int = [e.get() for e in self.controller.chbox_val]
        if all(a == 0 for a in self.controller.chbox_int):
            tk.messagebox.showerror(title="Error", message="At least 1 Channel must be enabled")
            return

        try:
            for i in range(0, self.controller.table_info['ch_num']):
                if self.controller.chbox_val[i].get() == 1:
                    if float(self.entries[i].get()) != 0:
                        self.controller.sens_val[i] = float(self.entries[i].get())
                    else:
                        tk.messagebox.showerror(title="Error", message="Sensitivity cannot be zero")
                        return
                else:
                    self.controller.sens_val[i] = 1

            # Calculate enabled channels from user inputted sensitivity
            self.controller.channels_accel = self.controller.channels_volt[:, 0]
            for j in range(0, self.controller.table_info['ch_num']):
                if self.controller.chbox_val[j].get() == 1:
                    temp = self.controller.channels_volt[:, j+1] * 1000 / self.controller.sens_val[j]
                    self.controller.channels_accel = np.vstack((self.controller.channels_accel, temp))
            self.controller.channels_accel = np.transpose(self.controller.channels_accel)

            self.controller.table_info['dt'] = self.controller.channels_accel[1, 0] - self.controller.channels_accel[0, 0]
            self.controller.table_info['sr'] = 1 / self.controller.table_info['dt']
            self.controller.table_info['samples'] = len(self.controller.channels_accel[:, 0])

        except Exception as e:
            tk.messagebox.showerror(title="Error", message=str(e))
            return

        # Open export page and destroy self
        self.controller.page_3_open()
        self.destroy()

    def exit_page(self):
        self.controller.destroy()
