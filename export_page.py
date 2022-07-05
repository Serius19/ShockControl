import tkinter as tk
from tkinter import messagebox
import numpy as np
from matplotlib import pyplot as plt
from utilities import save_file, write2txt, fft
from srs import Srs
from filtering import LowpassFilt


class ExportPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        self.initialize_widgets()
        self.update_table()

    def initialize_widgets(self):
        # ROW 0 ________________________________________
        crow = 0
        btn_import_nf = tk.Button(self, state="normal", command=self.import_nf_click, text="Import New File",
                                  padx=5, pady=5, width=12)
        btn_import_nf.grid(row=crow, column=0, padx=10, pady=5)

        self.txt_info = tk.Text(self, state="normal", height=7, width=30, padx=5, pady=5)
        self.txt_info.grid(row=crow, rowspan=3, column=1, columnspan=2, padx=(10, 2), pady=5)

        # ROW 1 ________________________________________
        crow = 1
        btn_view_volt = tk.Button(self, state="normal", command=self.view_volt_click, text="Plot Voltage",
                                  padx=5, pady=5, width=12)
        btn_view_volt.grid(row=crow, column=0, padx=10, pady=5)

        # ROW 2______________________________________
        crow = 2
        btn_view_g = tk.Button(self, state="normal", command=self.view_g_click, text="Plot Acceleration",
                               padx=5, pady=5, width=12)
        btn_view_g.grid(row=crow, column=0, padx=10, pady=5)

        # ROW 3______________________________________
        crow = 3
        self.btn_filter = tk.Button(self, state="normal", command=self.filter_click, text="Filter Data",
                                    padx=5, pady=5, width=12)
        self.btn_filter.grid(row=crow, column=0, padx=10, pady=5)

        self.btn_fft = tk.Button(self, state="disabled", command=self.fft_click, text="FFT",
                                 padx=5, pady=5, width=12)
        self.btn_fft.grid(row=crow, column=1, padx=10, pady=5, sticky=tk.W)

        # ROW 4______________________________________
        crow = 4
        self.btn_export_time = tk.Button(self, state="normal", command=self.export_txt_click, text="Export Time",
                                         padx=5, pady=5, width=12)
        self.btn_export_time.grid(row=crow, column=0, padx=10, pady=5)

        # ROW 5______________________________________
        crow = 5
        btn_srs = tk.Button(self, state="normal", command=self.srs_click, text="SRS Calculate",
                            padx=5, pady=5, width=12)
        btn_srs.grid(row=crow, column=0, padx=10, pady=5)

        self.btn_export_srs = tk.Button(self, state="disabled", command=self.export_srs_click, text="Export SRS",
                                        padx=5, pady=5, width=12)
        self.btn_export_srs.grid(row=crow, column=1, padx=10, pady=5, sticky=tk.W)

        btn_quit = tk.Button(self, state="normal", command=self.exit_page, text="Quit",
                             padx=5, pady=5, width=8)
        btn_quit.grid(row=crow, column=2, padx=5, pady=5, sticky=tk.E)

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
        self.controller.page_1_open()
        self.destroy()

    def view_volt_click(self):
        # Plot Voltage vs Time Graph
        fig1, ax1 = plt.subplots()

        for i in range(1, len(self.controller.channels_volt[0, :])):
            ax1.plot(self.controller.channels_volt[:, 0], self.controller.channels_volt[:, i]*1000, label=f"CH{i}")

        ax1.set(xlabel='Time (s)', ylabel='Voltage (mV)',
                title='Voltage vs Time')
        ax1.legend(loc="upper right")
        ax1.grid()
        fig1.show()

    def view_g_click(self):
        # Plot Acceleration vs Time
        fig2, ax2 = plt.subplots()

        for i in range(1, len(self.controller.channels_accel[0, :])):
            ax2.plot(self.controller.channels_accel[:, 0], self.controller.channels_accel[:, i], label=f"CH{i}")

        ax2.set(xlabel='Time (s)', ylabel='Acceleration (g)',
                title='Acceleration vs Time')
        ax2.legend(loc="upper right")
        ax2.grid()
        fig2.show()

    def filter_click(self):
        filt_win = LowpassFilt(self, self.controller)
        self.wait_window(filt_win)
        self.btn_fft.config(state="normal")

    def fft_click(self):
        n = self.controller.table_info['samples']
        t = self.controller.table_info['dt']
        fourier, fft_freq = fft(self.controller.channels_filt[:, 1], n, t)
        fig4, ax4 = plt.subplots()
        ax4.plot(fft_freq, abs(fourier) / n)
        ax4.set_xlim(0, 1000)
        fig4.show()

    def update_table(self):
        self.txt_info.delete('1.0', tk.END)
        message = (
            f"Imported file: {self.controller.table_info['path']} \n"
            f"Time increment: {self.controller.table_info['dt']} seconds\n"
            f"Sample rate: {self.controller.table_info['sr']} Hz\n"
            f"Number of samples: {self.controller.table_info['samples']}\n"
                   )
        self.txt_info.insert('end', message)

    def exit_page(self):
        self.controller.destroy()
