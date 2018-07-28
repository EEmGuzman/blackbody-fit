#!/usr/bin/env python3

# This program reads a csv file of mjd,B,Be,V,Ve,I,Ie, values and fits
# a black body to the data to find the temperature at a given epoch.
# Usage is ./multiblbf inputcsvfilename scaleguess tempguess outfilename

import sys
import csv
from math import pi
from scipy.optimize import curve_fit
from scipy.constants import h,k,c
import numpy as np


def planck_dist(lam, a, T):
    lam = 1e-10 * lam
    return a*4*pi*2*h*(c**2) / ((lam**5) * (np.exp(h*c / (lam*k*T)) - 1))

def plfit(funcfit, xvalues, yvalues, p0, errs):
    """
    Fit the planck distribution to a set of wavelength and flux values.
    Returns a best fit temperature and its associated error.
    """
    temps = []
    temperrs = []
    popt, pconv = curve_fit(funcfit, xvalues, yvalues, p0=p0, sigma=errs)
    perrors = np.sqrt(np.diag(pconv))
    print('The temp. is approx. {} K +- {}'.format(int(popt[1]),int(perrors[1])))
    temps.append(int(popt[1]))
    temperrs.append(int(perrors[1]))
    return (temps, temperrs)

def vegamag2flux(x,option):
    """
    Convert magnitude (Johnson Band) to flux (W/m^3).
    """
    zptB = -20.498
    zptV = -21.100
    zptI = -22.371
    if option.lower() == 'b':
        zpt = zptB
    elif option.lower() == 'v':
        zpt = zptV
    elif option.lower() == 'i':
        zpt = zptI
    return 10000000 * 10**((zpt - (x))*0.4)

# Reading data in from CSV
mjd = []
Bmag = []
Berr = []
Vmag = []
Verr = []
Imag = []
Ierr = []
with open(str(sys.argv[1]), 'r') as infile:
    magdata = csv.reader(infile)
    for row in magdata:
        mjd.append(row[0])
        Bmag.append(float(row[1]))
        Berr.append(float(row[2]))
        Vmag.append(float(row[3]))
        Verr.append(float(row[4]))
        Imag.append(float(row[5]))
        Ierr.append(float(row[6]))

Bflux = vegamag2flux(np.array(Bmag), 'b')
Bfluxerr = vegamag2flux(np.array(Berr), 'b')
Vflux = vegamag2flux(np.array(Vmag), 'v')
Vfluxerr = vegamag2flux(np.array(Verr), 'v')
Iflux = vegamag2flux(np.array(Imag), 'i')
Ifluxerr = vegamag2flux(np.array(Ierr), 'i')

# effective Wavelengths of B, V, I Johnson bands.
ewl = [4380, 5450, 7980]

# Finding triplets of B,V,I
nepochs = len(Bflux)
fluxvals = np.zeros((nepochs,3))
fluxerrs = np.zeros((nepochs,3))
for counter in range(nepochs):
    fluxvals[counter] = [Bflux[counter], Vflux[counter], Iflux[counter]]
    fluxerrs[counter] = [Bfluxerr[counter], Vfluxerr[counter], Ifluxerr[counter]]

# Finding the temperature values
for value in range(nepochs):
    temps, temperrs = plfit(planck_dist, ewl, fluxvals[value], [float(sys.argv[2]), int(sys.argv[3])], fluxerrs[value])

# Writing mjd,temp,err data to a file for plotting later.
rdata = zip(mjd, temps, temperrs)
with open(str(sys.argv[4]), 'w') as outfile:
    odata = csv.writer(outfile)
    for row in rdata:
        odata.writerow(row)
