Analysis consists of using two programs: multiblbf.py and plottempdata.py
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------

multiblbf.py information
----------------------------
This program performs a black body fit to each epoch provided in a csv file and outputs the best fit temperature and associated errors.

Usage:

	./multiblbf inputcsvfilename scaleguess tempguess reddening outfilename

Inputs:  
-inputcsvfilename  
This program reads a csv file of mjd,B,Be,V,Ve,I,Ie, values. Values MUST be in that order, and be a csv file. Where 'Be', 'Ve', and 'Ie' are the associated errors of the magnitudes. Do not include a header.  

-scaleguess  
The blackbody fit requires a scale factor in front of the planck distribution to account for distance. Enter an initial value < 1. Value will be used for each epoch.  

-tempguess  
Initial temperature guess. Value will be used for each epoch.  

-reddening  
E(B-V) value to be used for correction of magnitudes. Relationships between reddening and extinction from Schlegel et al. (1998) are used.

-outputfilename  
Naming convention is a choice. Must end with '.csv'  

Outputs:
A csv file with mjd, temp, temperror data from black body fits.  

Example:

	./multiblbf 100daykaitsn2013ejobs.csv 0.001 20000 0.061 kaitempdata.csv


plottempdata.py information
----------------------------
This program takes two sets of temperature data and provides a plot with errorbars. Use output csv files from multiblbf.py. Currently this program is written around KAIT and Konkoly data. Names in legend can be changed manually to accommodate other pairs of data sets.  

Usage:  

	./plottempdata.py kaittempdata konktempdata outfilename

Example:  

	./plottempdata.py kaittemps.csv konktemps.csv csn2013ejtemptime.eps
