import json
import os
import datetime
import glob
import csv
import tkinter as tk
from tkinter import Tk
from tkinter.filedialog import askdirectory

## Define file name with timestamp
ddt = str(datetime.datetime.now().strftime("%d-%m-%y--%H-%M-%M"))
currentMonth = str(datetime.datetime.now().strftime('%B-%Y'))
output_files = "Extract_Data"+'-'+'IB'+'-'+'CPU'+'-'+'_'+'Timestamp-'+ddt+'.csv'
name = str(output_files)
print("Extracted File Name : ", name)
print("Month : ", currentMonth)

## Define & Check File Path to Source File
path = os.getcwd()
print ("File Path : ",path)

back = tk.Tk()
back.withdraw()

ask_dir = askdirectory(title='Select Folder')
print(ask_dir)

## Open Multiple File
# Change the source file pattern to match file name pattern
source_file = glob.glob(os.path.join(ask_dir,"*cpu*.json"))
# This will print the files that will be read.
# Comment this line if not use
print ("Source File Name : ",source_file)

# Create header before write to file
convert = csv.writer(open(name, 'a'))
convert.writerow(["node", "idleMax", "kernelMax", "userMax"])

# Do Loop to get the desire data
for file in source_file:
    with open(file) as files:
        parse_json = json.load(files)
        node = parse_json["imdata"][0]["procSysCPUHist5min"]["attributes"]["dn"]
        cpu_idle = parse_json["imdata"][0]["procSysCPUHist5min"]["attributes"]["idleMax"]
        cpu_kernel = parse_json["imdata"][0]["procSysCPUHist5min"]["attributes"]["kernelMax"]
        cpu_user = parse_json["imdata"][0]["procSysCPUHist5min"]["attributes"]["userMax"]
        files.close()
        convert.writerow([node, cpu_idle, cpu_kernel, cpu_user])
