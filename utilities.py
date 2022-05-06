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
    print(df)
    header = df.columns
    print(header)
    t_step = float(header[-1])
    print(t_step)

    seq = df.Sequence.to_numpy()
    t = seq*t_step
    print(seq)

    ch1_volt = df.Volt.to_numpy()
    print(ch1_volt)

    if len(df.columns) == 5:
        df.columns = ["Sequence", "Volt", "Volt2", "NAN", "NAN"]
        ch2_volt = df.Volt2.to_numpy()
        print(ch2_volt)
    elif len(df.columns) == 6:
        df.columns = ["Sequence", "Volt", "Volt2", "Volt3", "NAN", "NAN"]
        ch2_volt = df.Volt2.to_numpy()
        print(ch2_volt)
        ch3_volt = df.Volt3.to_numpy()
        print(ch3_volt)
    elif len(df.columns) == 7:
        df.columns = ["Sequence", "Volt", "Volt2", "Volt3", "Volt4", "NAN", "NAN"]
        ch2_volt = df.Volt2.to_numpy()
        print(ch2_volt)
        ch3_volt = df.Volt3.to_numpy()
        print(ch3_volt)
        ch4_volt = df.Volt4.to_numpy()
        print(ch4_volt)

