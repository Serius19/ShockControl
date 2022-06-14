import tkinter as tk
import numpy as np
from scipy.signal import lfilter
import matplotlib.pyplot as plt


class Srs(tk.Toplevel):
    def __init__(self, parent, controller):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        self.title("Calculate SRS")
        self.resizable(False, False)
        self.grab_set()

        self.arr = []

        self.generate_widgets()

    def generate_widgets(self):
        win = tk.Frame(self)
        win.pack(side="top", fill="both", expand=True)
        # Widgets
        # ROW 0 ________________________________________
        crow = 0
        tk.Label(win, text="Shock Response Spectrum, Enter Desired Parameters!").grid(column=0, row=crow, columnspan=2,
                                                                                      padx=5, pady=10)
        # ROW 1 ________________________________________
        crow = 1
        tk.Label(win, text="Calculating from Channel 1 of input file!").grid(column=0, row=crow, columnspan=2, padx=5,
                                                                             pady=10)
        # ROW 2 ________________________________________
        crow = 2
        tk.Label(win, text="Octave Spacing:").grid(column=0, row=crow, padx=5, pady=(5, 0))
        tk.Label(win, text="Damping (Q):").grid(column=1, row=crow, padx=5, pady=(5, 0))

        # ROW 3 ________________________________________
        crow = 3
        options = ["1/3", "1/6", "1/12", "1/24"]
        self.Octr = tk.StringVar()
        self.Octr.set("1/24")
        self.ent_oct = tk.OptionMenu(win, self.Octr, *options)
        self.ent_oct.grid(row=crow, column=0, padx=5, pady=(2, 5))

        self.Qr = tk.StringVar()
        self.Qr.set("10")
        self.Q_ent = tk.Entry(win, width=5, textvariable=self.Qr)
        self.Q_ent.grid(row=crow, column=1, padx=5, pady=(2, 5))

        # ROW 4 ________________________________________
        crow = 4
        tk.Label(win, text="Min Freq (Hz):").grid(column=0, row=crow, padx=5, pady=(5, 0))
        tk.Label(win, text="Max Freq (Hz):").grid(column=1, row=crow, padx=5, pady=(5, 0))

        # ROW 5 ________________________________________
        crow = 5
        self.f1 = tk.StringVar()
        self.f1.set("2")
        ent_f1 = tk.Entry(win, width=5, textvariable=self.f1)
        ent_f1.grid(row=crow, column=0, padx=5, pady=(2, 10))

        self.f2 = tk.StringVar()
        self.f2.set("500")
        ent_f2 = tk.Entry(win, width=5, textvariable=self.f2)
        ent_f2.grid(row=crow, column=1, padx=5, pady=(2, 10))

        # ROW 6 ________________________________________
        crow = 6
        self.cb_val = tk.IntVar()
        checkbox = tk.Checkbutton(win, text="Enable Limits",
                                  command=lambda: self.cb_check(),
                                  variable=self.cb_val)
        checkbox.grid(row=crow, column=0, columnspan=2, padx=5, pady=(5, 0))

        # ROW 7 ________________________________________
        crow = 7
        tk.Label(win, text="t1 (s):").grid(column=0, row=crow, padx=5, pady=(5, 0))
        tk.Label(win, text="t2 (s):").grid(column=1, row=crow, padx=5, pady=(5, 0))

        # ROW 8 ________________________________________
        crow = 8
        self.t1 = tk.StringVar()
        self.t1.set("0")
        self.ent_t1 = tk.Entry(win, width=7, state="disabled", textvariable=self.t1)
        self.ent_t1.grid(row=crow, column=0, padx=5, pady=(2, 10))

        self.t2 = tk.StringVar()
        self.t2.set(str(self.controller.channels_accel[-1, 0]))
        self.ent_t2 = tk.Entry(win, width=7, state="disabled", textvariable=self.t2)
        self.ent_t2.grid(row=crow, column=1, padx=5, pady=(2, 10))

        # ROW 9 ________________________________________
        crow = 9
        btn_calc = tk.Button(win, text="Calculate", command=self.calculate)
        btn_calc.grid(row=crow, column=0, columnspan=2, padx=5, pady=(10, 10))

    def calculate(self):
        # collect values from user input
        damp = 1./(2.*(float(self.Qr.get())))
        int_f1 = float(self.f1.get())
        int_f2 = float(self.f2.get())
        self.int_t1 = float(self.t1.get())
        self.int_t2 = float(self.t2.get())

        # Calculate frequency array depending on user selected octave range
        num, dem = self.Octr.get().split("/")
        octave = float(num)/float(dem)
        noct = np.log(int_f2/int_f1)/np.log(2)
        num_fn = int(np.ceil(noct*float(dem)))+1
        self.controller.fn = np.zeros(num_fn, dtype=float)
        self.controller.fn[0] = int_f1
        for i in range(1, num_fn):
            self.controller.fn[i] = self.controller.fn[i-1]*(2.**octave)

        # Calculate omega values from frequency
        omega = 2*np.pi*self.controller.fn

        # Calculate SRS array and store in the controller variable
        self.controller.a_abs = self.srs_accel(num_fn, omega, damp)

        fig, ax = plt.subplots()
        ax.plot(self.controller.fn, self.controller.a_abs)
        ax.set(xlabel='Frequency (Hz)', ylabel='Acceleration (g)',
               title='Shock Response Spectrum')
        ax.set_xscale('log')
        ax.set_xlim(int_f1, int_f2)
        ax.grid()
        fig.show()

        self.destroy()

    def srs_accel(self, num_fn, omega, damp):
        a_abs = np.zeros(num_fn, dtype=float)
        ac = np.zeros(3)
        bc = np.zeros(3)
        dt = self.controller.channels_accel[1, 0] - self.controller.channels_accel[0, 0]

        if self.cb_val.get() == 1:
            range_arr = np.where(np.logical_and(self.controller.channels_accel[:, 0] >= self.int_t1, self.controller.channels_accel[:, 0] <= self.int_t2))
            self.arr = self.controller.channels_accel[range_arr[0]:range_arr[-1], 1]
        else:
            self.arr = self.controller.channels_accel[:, 1]

        for j in range(0, int(num_fn)):
            omegad = omega[j] * np.sqrt(1. - (damp ** 2))

            e = np.exp(-damp * omega[j] * dt)
            k = omegad * dt
            c = e * np.cos(k)
            s = e * np.sin(k)
            sp = s / k

            ac[0] = 1.
            ac[1] = -2. * c
            ac[2] = +e ** 2

            bc[0] = 1. - sp
            bc[1] = 2. * (sp - c)
            bc[2] = e ** 2 - sp

            resp = lfilter(bc, ac, self.arr, axis=-1, zi=None)
            a_abs[j] = max(abs(resp))

        return a_abs

    def cb_check(self):
        if self.cb_val.get() == 1:
            self.ent_t1.config(state="normal")
            self.ent_t2.config(state="normal")
        else:
            self.ent_t1.config(state="disabled")
            self.ent_t2.config(state="disabled")
