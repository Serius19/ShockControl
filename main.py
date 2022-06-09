import tkinter as tk
import numpy as np
from import_page import ImportPage
from srs_page import SRSPage


class App(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        # stack frames on top of each other, then the one we want visible

        # create main frame to hold all other frames
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # create frames

        self.app1 = ImportPage(container, self)
        self.app2 = SRSPage(container, self)

        self.frames = {ImportPage.__name__, SRSPage.__name__}

        self.app1.grid(row=0, column=0, sticky="nsew")
        self.app2.grid(row=0, column=0, sticky="nsew")

        self.show_frame("ImportPage")

        #############################
        # Variable Controller
        #############################

        # Checkbox values from AccelData()
        self.chbox_val = [tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()]
        # Sensitivity values from AccelData()
        self.sens_val = np.array((10, 10, 0, 0), dtype=float)
        # Oscilloscope file imported boolean from AccelData()
        self.bool_imported = False
        # time and voltage from oscilloscope from AccelData()
        self.channels_volt = []
        # time and channels from oscilloscope from AccelData()
        self.channels_accel = []

    def show_frame(self, page_name):
        # Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()
