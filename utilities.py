from tkinter import filedialog as fd
from tkinter import messagebox
import scipy.fft
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

    if len(df.columns) == 4:
        ch1_volt = df.Volt.to_numpy()
        arr = np.stack((t, ch1_volt), axis=1)
        ch_num = 1
        return arr, ch_num

    elif len(df.columns) == 5:
        df.columns = ["Sequence", "Volt", "Volt2", "NAN", "NAN"]
        ch1_volt = df.Volt.to_numpy()
        ch2_volt = df.Volt2.to_numpy(dtype=float)
        arr = np.stack((t, ch1_volt, ch2_volt), axis=1)
        ch_num = 2
        return arr, ch_num

    elif len(df.columns) == 6:
        df.columns = ["Sequence", "Volt", "Volt2", "Volt3", "NAN", "NAN"]
        ch1_volt = df.Volt.to_numpy()
        ch2_volt = df.Volt2.to_numpy(dtype=float)
        ch3_volt = df.Volt3.to_numpy(dtype=float)
        arr = np.stack((t, ch1_volt, ch2_volt, ch3_volt), axis=1)
        ch_num = 3
        return arr, ch_num

    elif len(df.columns) == 7:
        df.columns = ["Sequence", "Volt", "Volt2", "Volt3", "Volt4", "NAN", "NAN"]
        ch1_volt = df.Volt.to_numpy()
        ch2_volt = df.Volt2.to_numpy(dtype=float)
        ch3_volt = df.Volt3.to_numpy(dtype=float)
        ch4_volt = df.Volt4.to_numpy(dtype=float)
        arr = np.stack((t, ch1_volt, ch2_volt, ch3_volt, ch4_volt), axis=1)
        ch_num = 4
        return arr, ch_num


def save_file():
    filetypes = (
        ('Text Document', '*.txt'),
        ('All files', '*.*')
    )
    file = fd.asksaveasfile(title="Choose file location and name:", filetypes=filetypes)

    return file


def write2txt(file, a):
    try:
        np.savetxt(file, a, delimiter="\t", fmt="%5.10f")
        file.close()
    except Exception as e:
        messagebox.showerror(title="Error", message=str(e))
        return


def fft(data, n, t):
    fourier = scipy.fft.rfft(data)
    fft_freq = scipy.fft.rfftfreq(n, d=t)
    return fourier, fft_freq
