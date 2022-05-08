import tkinter as tk
import numpy as np
from utilities import read_csv_data, read_csv_file


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        # Widgets
        lbl_import = tk.Label(self, text="Import Oscilloscope File:")
        self.btn_import = tk.Button(self, command=self.import_click, text="Read Data", padx=5, pady=5)

        # Packing
        lbl_import.grid(row=0, column=0, padx=5, pady=2)
        self.btn_import.grid(row=1, column=0, padx=5, pady=5)

    def import_click(self):
        import_win = AccelData(self, self.controller)
        self.wait_window(import_win)
        print("Window destroyed")

        if not self.controller.bool_imported:
            pass
        else:
            self.btn_import.config(state="disabled")


class AccelData(tk.Toplevel):
    def __init__(self, parent, controller):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        self.title("Import Accelerometer Data")
        self.resizable(False, False)
        self.grab_set()

        win = tk.Frame(self)
        win.pack(side="top", fill="both", expand=True)

        # Widgets
        # ROW 0 ________________________________________
        crow = 0
        self.lblImport = tk.Label(win, text="Accelerometer parameters:")
        self.lblImport.grid(column=0, columnspan=5, row=crow, padx=5, pady=2)

        # ROW 1-4 ______________________________________
        for i in range(0, 4):
            self.lblCh = tk.Label(win, text="CH" + str(i + 1) + ":")
            self.lblCh.grid(column=0, row=i + 1, padx=5, pady=5)
            tk.Label(win, text="Sensitivity:").grid(column=2, row=i + 1, padx=5, pady=5)
            tk.Label(win, text="mV/g").grid(column=4, row=i + 1, padx=5, pady=5)

        self.chkCh1 = tk.Checkbutton(win, fg="green", text="Enabled",
                                     command=lambda: self.cb_check(self.chkCh1, self.controller.chbox_val[0],
                                                                   self.entCh1),
                                     variable=self.controller.chbox_val[0])
        self.chkCh1.grid(column=1, row=1, padx=5, pady=5)
        self.chkCh1.select()
        self.chkCh2 = tk.Checkbutton(win, fg="green", text="Enabled",
                                     command=lambda: self.cb_check(self.chkCh2, self.controller.chbox_val[1],
                                                                   self.entCh2),
                                     variable=self.controller.chbox_val[1])
        self.chkCh2.grid(column=1, row=2, padx=5, pady=5)
        self.chkCh2.select()
        self.chkCh3 = tk.Checkbutton(win, fg="red", text="Disabled",
                                     command=lambda: self.cb_check(self.chkCh3, self.controller.chbox_val[2],
                                                                   self.entCh3),
                                     variable=self.controller.chbox_val[2])
        self.chkCh3.grid(column=1, row=3, padx=5, pady=5)
        self.chkCh4 = tk.Checkbutton(win, fg="red", text="Disabled",
                                     command=lambda: self.cb_check(self.chkCh4, self.controller.chbox_val[3],
                                                                   self.entCh4),
                                     variable=self.controller.chbox_val[3])
        self.chkCh4.grid(column=1, row=4, padx=5, pady=5)

        self.entCh1 = tk.Entry(win, width=10)
        self.entCh1.grid(column=3, row=1, padx=5, pady=5)
        self.entCh2 = tk.Entry(win, width=10)
        self.entCh2.grid(column=3, row=2, padx=5, pady=5)
        self.entCh3 = tk.Entry(win, width=10, state="disabled")
        self.entCh3.grid(column=3, row=3, padx=5, pady=5)
        self.entCh4 = tk.Entry(win, width=10, state="disabled")
        self.entCh4.grid(column=3, row=4, padx=5, pady=5)

        # ROW 5 ________________________________________
        crow = 5
        self.btn_fileSel = tk.Button(win, command=self.file_select, text="File Select", padx=5, pady=5)
        self.btn_fileSel.grid(column=1, columnspan=3, row=crow, padx=5, pady=5)

    @staticmethod
    def cb_check(obj, var, obj1):
        if var.get() == 1:
            obj.config(fg="green", text="Enabled")
            obj1.config(state="normal")
        else:
            obj.config(fg="red", text="Disabled")
            obj1.config(state="disabled")

    def file_select(self):
        try:
            if self.controller.chbox_val[0].get() == 1:
                self.controller.sens_val[0] = float(self.entCh1.get())

            if self.controller.chbox_val[1].get() == 1:
                self.controller.sens_val[1] = float(self.entCh2.get())

            if self.controller.chbox_val[2].get() == 1:
                self.controller.sens_val[2] = float(self.entCh3.get())

            if self.controller.chbox_val[3].get() == 1:
                self.controller.sens_val[3] = float(self.entCh4.get())

            filename = read_csv_file()

            t, ch1_volt, ch2_volt, ch3_volt, ch4_volt = read_csv_data(filename)

            self.controller.time = t
            self.controller.ch1 = ch1_volt/self.controller.sens_val[0] ^ -2
            self.controller.ch2 = ch2_volt / self.controller.sens_val[1] ^ -2
            self.controller.ch3 = ch3_volt / self.controller.sens_val[2] ^ -2
            self.controller.ch4 = ch4_volt / self.controller.sens_val[3] ^ -2

            print(self.controller.time)
            print(self.controller.ch1)
            print(self.controller.ch2)
            self.controller.bool_imported = True
            self.destroy()

        except Exception as e:
            print(e)
            pass


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # configure root window
        self.title("Shock Control System")
        self.geometry("300x250")
        self.resizable(False, False)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {"MainFrame": MainPage(container, self)}
        self.frames["MainFrame"].pack(side="top", fill="both", expand=True)

        #############################
        # Variable Controller
        #############################

        # Checkbox values from AccelData()
        self.chbox_val = [tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()]
        # Sensitivity values from AccelData()
        self.sens_val = np.zeros(4, dtype=float)
        # File imported boolean
        self.bool_imported = False

        # Time domain
        self.time = []
        self.ch1 = []
        self.ch2 = []
        self.ch3 = []
        self.ch4 = []


if __name__ == "__main__":
    app = App()
    app.mainloop()
