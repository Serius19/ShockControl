import tkinter as tk
import numpy as np
from scipy import signal
from tkinter import messagebox
import matplotlib.pyplot as plt


class LowpassFilt(tk.Toplevel):
    def __init__(self, parent, controller):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        self.title("Filtering")
        self.resizable(False, False)
        self.grab_set()

        self.generate_widgets()

    def generate_widgets(self):
        win = tk.Frame(self)
        win.pack(side="top", fill="both", expand=True)
        # Widgets
        # ROW 0 ________________________________________
        crow = 0
        tk.Label(win, text="DATA FILTERING, Enter Desired Parameters!").grid(column=0, row=crow, columnspan=2,
                                                                             padx=5, pady=10)
        # ROW 1 ________________________________________
        crow = 1
        tk.Label(win, text="4th order butterworth filter on enabled channels!").grid(column=0, row=crow, columnspan=2, padx=5, pady=10)
        # ROW 2 ________________________________________
        crow = 2
        tk.Label(win, text="Frequency:").grid(column=0, columnspan=2, row=crow, padx=5, pady=(5, 0))

        # ROW 3 ________________________________________
        crow = 3
        self.f = tk.StringVar()
        self.f.set("300")
        self.f_ent = tk.Entry(win, width=5, textvariable=self.f)
        self.f_ent.grid(row=crow, column=0, padx=(5, 0), pady=(2, 5), sticky=tk.E)

        tk.Label(win, text="Hz:").grid(column=1, row=crow, padx=(0, 5), pady=(5, 0), sticky=tk.W)

        # ROW 4 ________________________________________
        crow = 4
        btn_calc = tk.Button(win, text="Calculate", command=self.calculate, font="Helvetica 12")
        btn_calc.grid(row=crow, column=0, columnspan=2, padx=5, pady=(10, 10))

    def calculate(self):
        try:
            f_l = float(self.f.get())
            if f_l >= 0.5*self.controller.table_info['sr']:
                tk.messagebox.showerror(title="Error", message="Selected frequency must be lower than the Nyquist frequency")
                return

            sos = signal.butter(4, f_l, 'low', fs=self.controller.table_info['sr'], output='sos')

            self.controller.channels_filt = self.controller.channels_accel[:, 0]
            for i in range(1, len(self.controller.channels_accel[0, :])):
                filtered = signal.sosfilt(sos, self.controller.channels_accel[:, i])
                self.controller.channels_filt = np.vstack((self.controller.channels_filt, filtered))
            self.controller.channels_filt = np.transpose(self.controller.channels_filt)

            # Plot filtered Acceleration vs Time
            fig3, ax3 = plt.subplots()

            for i in range(1, len(self.controller.channels_filt[0, :])):
                ax3.plot(self.controller.channels_filt[:, 0], self.controller.channels_filt[:, i], label=f"CH{i}")

            ax3.set(xlabel='Time (s)', ylabel='Acceleration (g)',
                    title=f"low-pass filter at {f_l} Hz, filtered Acceleration (g)")
            ax3.grid()
            ax3.legend(loc="upper right")
            fig3.show()

            self.destroy()

        except Exception as e:
            tk.messagebox.showerror(title="Error", message=str(e))
            return
