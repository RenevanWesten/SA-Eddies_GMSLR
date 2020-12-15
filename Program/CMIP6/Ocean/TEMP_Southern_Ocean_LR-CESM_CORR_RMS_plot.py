#Program plots the spatial correlation and RMS

from pylab import *
import numpy
import datetime
import time
import glob, os
import math
import netCDF4 as netcdf
import matplotlib.colors as colors
from scipy import stats

#Making pathway to folder with all data
directory	= '../../../Data/CMIP6/'
directory_cesm 	= '../../../Data/LR-CESM/'

#-----------------------------------------------------------------------------------------
#--------------------------------MAIN SCRIPT STARTS HERE----------------------------------
#-----------------------------------------------------------------------------------------
	
#Get the model names and path
models = glob.glob(directory+'*')
models.sort()

for model_i in range(len(models)):
	#Only retain the model names
	models[model_i]	= models[model_i][len(directory):]

	print model_i, models[model_i]
#-----------------------------------------------------------------------------------------

TEMP_data = netcdf.Dataset(directory_cesm+'Ocean/TEMP_Southern_Ocean_LR-CESM_to_CMIP6.nc', 'r')

#Writing data to correct variable	
corr	= TEMP_data.variables['CORR'][:]
rms	= TEMP_data.variables['RMS'][:] 		

TEMP_data.close()

TEMP_data = netcdf.Dataset(directory_cesm+'Ocean/TEMP_Southern_Ocean_LR-CESM_to_HR-CESM.nc', 'r')

#Writing data to correct variable	
corr_HR	= TEMP_data.variables['CORR'][0]
rms_HR	= TEMP_data.variables['RMS'][0] 		

TEMP_data.close()

#-----------------------------------------------------------------------------------------

fig, ax	= subplots()

#HR-CESM
graph_HR_CESM	= ax.scatter(corr_HR, rms_HR, marker = 'o', color = 'red', s = 75, label = 'HR-CESM (10 km)')
graph_LR_CESM	= ax.scatter(1, 0, marker = 'o', color = 'blue', s = 75, label = 'LR-CESM (100 km)')

#HR-CMIP6 models
graph_2		= ax.scatter(corr[2], rms[2], marker = 'p', color = 'darkorange', s = 75)
graph_11	= ax.scatter(corr[11], rms[11], marker = 's', color = 'darkorange', s = 75)
graph_16	= ax.scatter(corr[16], rms[16], marker = 'D', color = 'darkorange', s = 75)
graph_17	= ax.scatter(corr[17], rms[17], marker = 'x', color = 'darkorange', s = 75)
graph_24	= ax.scatter(corr[24], rms[24], marker = '<', color = 'darkorange', s = 75)

#CMIP6 CESM related models
graph_6		= ax.scatter(corr[6], rms[6], marker = 'p', color = 'deepskyblue', s = 75)
graph_7		= ax.scatter(corr[7], rms[7], marker = 's', color = 'deepskyblue', s = 75)
graph_8		= ax.scatter(corr[8], rms[8], marker = 'D', color = 'deepskyblue', s = 75)

#CMIP6 models
graph_0		= ax.scatter(corr[0], rms[0], marker = 'p', color = 'k', s = 75)
graph_1		= ax.scatter(corr[1], rms[1], marker = 's', color = 'k', s = 75)
graph_3		= ax.scatter(corr[3], rms[3], marker = 'D', color = 'k', s = 75)
graph_4		= ax.scatter(corr[4], rms[4], marker = 'x', color = 'k', s = 75)
graph_5		= ax.scatter(corr[5], rms[5], marker = '<', color = 'k', s = 75)
graph_9		= ax.scatter(corr[9], rms[9], marker = '*', color = 'k', s = 75)
graph_10	= ax.scatter(corr[10], rms[10], marker = '>', color = 'k', s = 75)
graph_12	= ax.scatter(corr[12], rms[12], marker = 'h', color = 'k', s = 75)
graph_13	= ax.scatter(corr[13], rms[13], marker = 'v', color = 'k', s = 75)
graph_14	= ax.scatter(corr[14], rms[14], marker = 'd', color = 'k', s = 75)
graph_15	= ax.scatter(corr[15], rms[15], marker = '+', color = 'k', s = 75)
graph_19	= ax.scatter(corr[19], rms[19], marker = '1', color = 'k', s = 75)
graph_20	= ax.scatter(corr[20], rms[20], marker = '2', color = 'k', s = 75)
graph_21	= ax.scatter(corr[21], rms[21], marker = '3', color = 'k', s = 75)
graph_22	= ax.scatter(corr[22], rms[22], marker = '4', color = 'k', s = 75)
graph_26	= ax.scatter(corr[26], rms[26], marker = 'H', color = 'k', s = 75)
graph_27	= ax.scatter(corr[27], rms[27], marker = '8', color = 'k', s = 75)
graph_28	= ax.scatter(corr[28], rms[28], marker = '^', color = 'k', s = 75)
graph_29	= ax.scatter(corr[29], rms[29], marker = '|', color = 'k', s = 75)
graph_30	= ax.scatter(corr[30], rms[30], marker = '_', color = 'k', s = 75)

#Coarse CMIP6 models
graph_18	= ax.scatter(corr[18], rms[18], marker = 'p', color = 'saddlebrown', s = 75)
graph_23	= ax.scatter(corr[23], rms[23], marker = 's', color = 'saddlebrown', s = 75)
graph_25	= ax.scatter(corr[25], rms[25], marker = 'D', color = 'saddlebrown', s = 75)

ax.set_xlabel('Correlation coefficient')
ax.set_ylabel('Root-mean-square deviation ($^{\circ}$C)')
ax.grid()

ax.set_ylim(-0.05, 1)
ax.set_xlim(1.05, -0.4)

#Graphs for legend
graph_CMIP6		= ax.scatter(-100, -100, marker = 'o', color = 'k', s = 75, label = 'CMIP6 (100 km)')
graph_CMIP6_HR		= ax.scatter(-100, -100, marker = 'o', color = 'darkorange', s = 75, label = 'HR-CMIP6 ($<$ 100 km)')
graph_CMIP6_CR		= ax.scatter(-100, -100, marker = 'o', color = 'saddlebrown', s = 75, label = 'CR-CMIP6 (250 km)')
graph_CMIP6_CESM	= ax.scatter(-100, -100, marker = 'o', color = 'deepskyblue', s = 75, label = 'CMIP6 CESM (100 km)')

ax.legend(loc='upper left', fancybox=True, shadow=False, scatterpoints=1, ncol = 1, frameon = False, prop={'size': 12})

ax.set_title('a) HR-CESM')
show()