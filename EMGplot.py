import pdb
import sys
import matplotlib.pyplot as plt
import tkinter
from tkinter.filedialog import askopenfilename
import csv
import numpy as np
import openpyxl as excel

def EMGread():
    emg_file = askopenfilename(filetypes= [('EMG','.emg')], initialdir = "C:\\", title="Choose EMG file")
    with open(emg_file, 'r') as f:
        reader = csv.reader(f)
        csv_data = [data for data in reader]
    emg_data = np.asarray(csv_data, dtype=np.int64)

    return emg_data


def switchRead ():
    switch_file = askopenfilename(filetypes= [('Switch Output','.xls*')], initialdir = "C:\\", title="Choose Output from Switch Wizard file")
    wb = excel.load_workbook(switch_file)

    reaction_sheet=wb.get_sheet_by_name("Switch Trial Data")
    data_withtitle = np.array([[cell.value for cell in col] for col in reaction_sheet['A2':'J100']])
    reaction_data = data_withtitle[:,1:]

    return reaction_data

def main():
    reaction_data_aligned = []
    switch_timings = []

    while True:
        try:
            emg_data= EMGread()
            reaction_data = switchRead()
            first_trigger_index = np.where(emg_data==reaction_data[0,1])[0][0]
            break
        except IndexError:
            print("No switch trigger in the EMG file. Try again")

    root = tkinter.Tk()
    root.destroy()
    #WORK OUT HOW TO ITERATE THROUGH THIS...

    #reaction_data[:,1]


    for row in reaction_data:
         if row[7] is not None:
             switch_timings.append(row[7])
             #switch_timings.append(row[8])

    count=0
    for row in emg_data:
        if count<len(switch_timings):
            if row[1] == switch_timings[count]:
                reaction_data_aligned.append([row[0],1])
                count=count+1
            else:
                reaction_data_aligned.append([row[0],0])
        else:
            reaction_data_aligned.append([row[0],0])

    pdb.set_trace()

    switch_data = np.asarray(reaction_data_aligned,dtype=np.int32)

    #np.savetxt("trigger-formatted.csv", reaction_data_aligned, delimiter=",", fmt='%s')
    fig, ax = plt.subplots()

    ax.plot(emg_data[:,0],emg_data[:,2],'b')

    ax2 = ax.twinx()

    ax2.plot(switch_data[:,0], switch_data[:,1],'r')

    plt.show()


if __name__ == "__main__":
    main()
