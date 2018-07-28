#!/usr/bin/env python3

# This program reads in a csv file of temp data and creates a plot.
# ./plottempdata.py kanktempdata kaittempdata valentitempdata outfilename

import sys
import csv
import numpy as np
import matplotlib.pyplot as plt

def gettempdata(filename):
    mjd = []
    temp = []
    temperr = []
    with open(str(filename), 'r') as infile:
        datain = csv.reader(infile)
        for row in datain:
            mjd.append(float(row[0]))
            temp.append(float(row[1]))
            temperr.append(float(row[2]))
    return (mjd, temp, temperr)

mjd, temp, temperr = gettempdata(sys.argv[1])
mjd2, temp2, temperr2 = gettempdata(sys.argv[2])
mjd3, temp3, temperr3 = gettempdata(sys.argv[3])

# Plotting
plt.figure()
plt.errorbar(np.array(mjd2) - 56496.9, np.array(temp2)/1000, yerr=np.array(temperr2)/1000, label='KAIT', fmt='o', capsize=2, c='lawngreen')
plt.errorbar(np.array(mjd) - 56496.9, np.array(temp)/1000, yerr=np.array(temperr)/1000, label='Konkoly', fmt='o', capsize=2, c='blue')
plt.errorbar(np.array(mjd3) - 56496.9, np.array(temp3)/1000, yerr=np.array(temperr3)/1000, label='Valenti et. al., (2014)', fmt='o', capsize=2, c='red')
plt.xlabel("MJD-56496.9")
plt.ylabel("Temperature ($10^{3}$ K)")
plt.title("SN2013ej Temperature")
plt.legend()
plt.ylim(2,16)
plt.xlim(0,110)
plt.savefig(str(sys.argv[4]))
plt.close()
