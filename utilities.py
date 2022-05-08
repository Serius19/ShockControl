from tkinter import filedialog as fd
import numpy as np
import pandas as pd


def read_csv_file():
    filetypes = (
        ('CSV files', '*.csv'),
        ('All files', '*.*')
    )

    filename = fd.askopenfile(
        title='Select CSV file',
        filetypes=filetypes
    )
    return filename


def read_csv_data(filename):
    df = pd.read_csv(filename, skiprows=[0])
    header = df.columns

    t_step = float(header[-1])
    seq = df.Sequence.to_numpy()
    t = seq*t_step

    ch1_volt = df.Volt.to_numpy()
    ch2_volt = 0
    ch3_volt = 0
    ch4_volt = 0

    if len(df.columns) == 5:
        df.columns = ["Sequence", "Volt", "Volt2", "NAN", "NAN"]
        ch2_volt = df.Volt2.to_numpy()

    elif len(df.columns) == 6:
        df.columns = ["Sequence", "Volt", "Volt2", "Volt3", "NAN", "NAN"]
        ch2_volt = df.Volt2.to_numpy()
        ch3_volt = df.Volt3.to_numpy()

    elif len(df.columns) == 7:
        df.columns = ["Sequence", "Volt", "Volt2", "Volt3", "Volt4", "NAN", "NAN"]
        ch2_volt = df.Volt2.to_numpy()
        ch3_volt = df.Volt3.to_numpy()
        ch4_volt = df.Volt4.to_numpy()

    print(ch1_volt)
    print(ch2_volt)
    print(ch3_volt)
    print(ch4_volt)

    return t, ch1_volt, ch2_volt, ch3_volt, ch4_volt
