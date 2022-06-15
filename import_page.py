import tkinter as tk
from tkinter import messagebox
import numpy as np
from matplotlib import pyplot as plt
from utilities import read_csv_file, read_csv_data


class ImportPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        self.initialize_widgets()

    def initialize_widgets(self):
        # ROW 0 ________________________________________
        crow = 0
        self.lblImport = tk.Label(self, text="Accelerometer parameters:")
        self.lblImport.grid(column=0, columnspan=5, row=crow, padx=5, pady=2)

        # ROW 1-4 ______________________________________
        self.entries = [tk.Entry(), tk.Entry(), tk.Entry(), tk.Entry()]
        self.checkboxes = [tk.Checkbutton(), tk.Checkbutton(), tk.Checkbutton(), tk.Checkbutton()]

        for i in range(0, 4):
            lbl_ch = tk.Label(self, text="CH" + str(i + 1) + ":")
            lbl_ch.grid(column=0, row=i + 1, padx=5, pady=5)
            self.entries[i] = tk.Entry(self, width=10)
            self.entries[i].grid(column=3, row=i + 1, padx=5, pady=5)
            self.entries[i].insert(-1, str(self.controller.sens_val[i]))
            tk.Label(self, text="Sensitivity:").grid(column=2, row=i + 1, padx=5, pady=5)
            tk.Label(self, text="mV/g").grid(column=4, row=i + 1, padx=5, pady=5)
            self.checkboxes[i] = tk.Checkbutton(self, fg="green", text="Enabled",
                                                command=self.cb_check,
                                                variable=self.controller.chbox_val[i])
            self.checkboxes[i].grid(column=1, row=i + 1, padx=5, pady=5)

        self.checkboxes[0].select()
        self.cb_check()

        # ROW 5 ________________________________________
        crow = 5
        self.btn_fileSel = tk.Button(self, command=self.file_select, text="File Select", padx=5, pady=5)
        self.btn_fileSel.grid(column=1, columnspan=2, row=crow, padx=5, pady=5)

        self.btn_quit = tk.Button(self, command=self.exit_page, text="Quit", padx=5, pady=5)
        self.btn_quit.grid(column=3, columnspan=2, row=crow, padx=5, pady=5)

    def cb_check(self):
        for i in range(0, 4):
            if self.controller.chbox_val[i].get() == 1:
                self.checkboxes[i].config(fg="green", text="Enabled")
                self.entries[i].config(state="normal")
            else:
                self.checkboxes[i].config(fg="red", text="Disabled")
                self.entries[i].config(state="disabled")

    def file_select(self):
        try:
            for i in range(0, 4):
                if self.controller.chbox_val[i].get() == 1:
                    if float(self.entries[i].get()) != 0:
                        self.controller.sens_val[i] = float(self.entries[i].get())
                    else:
                        tk.messagebox.showerror(title="Error", message="Sensitivity cannot be zero")
                        return
                else:
                    self.controller.sens_val[i] = 1
        except Exception as e:
            tk.messagebox.showerror(title="Error", message=str(e))
            return

        try:
            filename = read_csv_file()

            channels = read_csv_data(filename)
            self.controller.channels_volt = channels

            # Calculate enabled channels from user inputted sensitivity
            self.controller.channels_accel = channels[:, 0]
            for j in range(1, len(channels[0])):
                if self.controller.chbox_val[j - 1].get() == 1:
                    temp = channels[:, j] / np.power(self.controller.sens_val[j - 1], -2)
                    self.controller.channels_accel = np.vstack((self.controller.channels_accel, temp))
            self.controller.channels_accel = np.transpose(self.controller.channels_accel)

        except Exception as e:
            tk.messagebox.showerror(title="Error", message=str(e))
            return

        # Plot Voltage vs Time Graph
        fig1, ax1 = plt.subplots()
        ax1.plot(self.controller.channels_volt[:, 0], self.controller.channels_volt[:, 1::])
        ax1.set(xlabel='Time (ms)', ylabel='Voltage (mV)',
                title='Voltage vs Time')
        ax1.grid()
        fig1.show()

        # Plot Acceleration vs Time
        fig1, ax1 = plt.subplots()
        ax1.plot(self.controller.channels_accel[:, 0], self.controller.channels_accel[:, 1::])
        ax1.set(xlabel='Time (ms)', ylabel='Acceleration (g)',
                title='Acceleration vs Time')
        ax1.grid()
        fig1.show()

        self.controller.change_page(self.controller.Page2)

    def exit_page(self):
        self.controller.destroy()
