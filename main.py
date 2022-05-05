import tkinter as tk


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        # Widgets
        lbl_import = tk.Label(self, text="Import Oscilloscope File:")
        btn_import = tk.Button(self, command=self.import_click, text="Read Data", padx=5, pady=5)

        # Packing
        lbl_import.grid(row=0, column=0, padx=5, pady=2)
        btn_import.grid(row=1, column=0, padx=5, pady=5)

    def import_click(self):
        AccelData(self, self.controller)


class AccelData(tk.Toplevel):
    def __init__(self, parent, controller):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        self.title("Import Accelerometer Data")
        self.resizable(False, False)

        win = tk.Frame(self)
        win.pack(side="top", fill="both", expand=True)

        # Widgets
        # ROW 0 ________________________________________
        crow = 0
        self.lblImport = tk.Label(win, text="Accelerometer parameters:")
        self.lblImport.grid(column=0, columnspan=5, row=crow, padx=5, pady=2)

        # ROW 1-4 ______________________________________

        self.entCh = []*4
        for i in range(0, 4):
            self.lblCh = tk.Label(win, text="CH" + str(i+1) + ":")
            self.lblCh.grid(column=0, row=i+1, padx=5, pady=5)
            tk.Label(win, text="Sensitivity:").grid(column=2, row=i+1, padx=5, pady=5)
            self.ent = tk.Entry(win, width=10)
            self.ent.grid(column=3, row=i+1, padx=5, pady=5)
            self.entCh.append(self.ent)
            tk.Label(win, text="mV/g").grid(column=4, row=i+1, padx=5, pady=5)

        self.chkCh1 = tk.Checkbutton(win, fg="green", text="Enabled",
                                     command=lambda: self.cb_check(self.chkCh1, self.controller.chbox_val[0]),
                                     variable=self.controller.chbox_val[0])
        self.chkCh1.grid(column=1, row=1, padx=5, pady=5)
        self.chkCh1.select()
        self.chkCh2 = tk.Checkbutton(win, fg="green", text="Enabled",
                                     command=lambda: self.cb_check(self.chkCh2, self.controller.chbox_val[1]),
                                     variable=self.controller.chbox_val[1])
        self.chkCh2.grid(column=1, row=2, padx=5, pady=5)
        self.chkCh2.select()
        self.chkCh3 = tk.Checkbutton(win, fg="red", text="Disabled",
                                     command=lambda: self.cb_check(self.chkCh3, self.controller.chbox_val[2]),
                                     variable=self.controller.chbox_val[2])
        self.chkCh3.grid(column=1, row=3, padx=5, pady=5)
        self.chkCh4 = tk.Checkbutton(win, fg="red", text="Disabled",
                                     command=lambda: self.cb_check(self.chkCh4, self.controller.chbox_val[3]),
                                     variable=self.controller.chbox_val[3])
        self.chkCh4.grid(column=1, row=4, padx=5, pady=5)

        # ROW 5 ________________________________________
        crow = 5
        self.btn_fileSel = tk.Button(win, text="File Select", padx=5, pady=5)
        self.btn_fileSel.grid(column=1, columnspan=3, row=crow, padx=5, pady=5)

    @staticmethod
    def cb_check(obj, var):
        if var.get() == 1:
            obj.config(fg="green", text="Enabled")
        else:
            obj.config(fg="red", text="Disabled")


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
        # Entry values from AccelData()

        #self.chbox_int = [self.chbox_val[0].get(), self.chbox_val[1].get(), self.chbox_val[2].get(), self.chbox_val[3].get()]


if __name__ == "__main__":
    app = App()
    app.mainloop()
