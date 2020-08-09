import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import datetime as dt

import tkinter as tk
from tkinter import messagebox
import tkinter.simpledialog as simpledialog

MAX_SET_NUM = 10000
LIMIT_SET_NUM = MAX_SET_NUM * 0.9
UPDATE_TIME = 5

def readyCsv():
    server_path = Path(str(Path.home()) + r"\Desktop")
    date = dt.datetime.today().strftime("%Y%m%d")
    csv_list = list(server_path.glob("aaa_"+ date + ".csv"))

    df = pd.read_csv(csv_list.pop(), index_col=0)
    df = df.loc[:, ['SET']]
    df.index = pd.to_datetime(df.index, format='%Y%m%d_%H:%M:%S')
    return df

def makeFigure(df):
    fig = plt.figure(figsize=(8,6))

    ax = fig.add_subplot(111)
    ax.grid()
    ax.axhline(LIMIT_SET_NUM, ls='dashed', color = "red")
    tday = dt.date.today().strftime('%Y-%m-%d')
    sxmin = tday + ' 00:00'
    sxmax = tday + ' 23:59'
    xmin = dt.datetime.strptime(sxmin, '%Y-%m-%d %H:%M')
    xmax = dt.datetime.strptime(sxmax, '%Y-%m-%d %H:%M')
    plt.xlim([xmin,xmax])
    plt.ylim([0,MAX_SET_NUM])
    plt.xticks(rotation=45)
    plt.title("Realtime limit check SET_number")
#    plt.legend('SET',bbox_to_anchor=(1, 0), loc='lower right', borderaxespad=1, fontsize=10)

    plt.plot(df,"b")
#    plt.plot(df.index,df.loc[:,'SET'],"b", label="SET")
    
def upper_limit_check_setnum(now_set_number):
    if now_set_number > LIMIT_SET_NUM:
        root = tk.Tk()
        root.withdraw()
        res = messagebox.showwarning("alert", "SET number is over 90%")
        print("showwarning", res)
        return True
    return False

if __name__ == '__main__':
    limit_check_flg = False
    df = readyCsv()
    makeFigure(df)
    while True:
        df = readyCsv()
        if limit_check_flg == False:
            now_set_number = df.iloc[-1]['SET']
            limit_check_flg = upper_limit_check_setnum(now_set_number)
#        plt.plot(df.index,df.loc[:,'SET'],"b", label="SET")
        plt.plot(df,"b")
        plt.pause(UPDATE_TIME)