#Program plots the CORR and RMS between the HR-CESM/LR-CESM and Mercator

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
directory_cesm_control      = '../../../Data/HR-CESM_Control/'
directory_cesm_low_control  = '../../../Data/LR-CESM_Control/'

#-----------------------------------------------------------------------------------------
#--------------------------------MAIN SCRIPT STARTS HERE----------------------------------
#-----------------------------------------------------------------------------------------

TEMP_data = netcdf.Dataset(directory_cesm_control+'/Ocean/TEMP_Southern_Ocean_Mercator_CORR_RMS.nc', 'r')

#Writing data to correct variable	
time_cesm	= TEMP_data.variables['time'][:]     	
corr_cesm	= TEMP_data.variables['CORR'][:] 
rms_cesm	= TEMP_data.variables['RMS'][:] 		

TEMP_data.close()
#-----------------------------------------------------------------------------------------

TEMP_data = netcdf.Dataset(directory_cesm_low_control+'/Ocean/TEMP_Southern_Ocean_Mercator_CORR_RMS.nc', 'r')

#Writing data to correct variable	
time_cesm_low	= TEMP_data.variables['time'][:]     	
corr_cesm_low	= TEMP_data.variables['CORR'][:] 
rms_cesm_low	= TEMP_data.variables['RMS'][:] 

TEMP_data.close()

#-----------------------------------------------------------------------------------------

for year_i in range(len(time_cesm)):	
	time_cesm[year_i] 	= datetime.datetime(2000 + year_i, 1, 1).toordinal()

#-----------------------------------------------------------------------------------------

fig, ax1	= subplots()

CESM_graph	= ax1.plot_date(time_cesm, corr_cesm, '-k', linewidth = 2.0, label = 'HR-CESM Control')
CESM_low_graph	= ax1.plot_date(time_cesm, corr_cesm_low, '--k', linewidth = 2.0, label = 'LR-CESM Control')	

ax1.set_xlabel('Model year')
ax1.set_ylabel("Correlation coefficient")
ax1.set_ylim(0.75, 1)
ax1.grid()

ax2 = ax1.twinx()

ax2.plot_date(time_cesm, rms_cesm, '-r', linewidth = 2.0)
ax2.plot_date(time_cesm, rms_cesm_low, '--r', linewidth = 2.0)	
ax2.set_ylabel("Root-mean-square deviation ($^{\circ}$C)", color = 'r')
ax2.tick_params(axis='y', colors='red')	
ax2.set_ylim(0.5, 1.3)

graphs	      = CESM_graph + CESM_low_graph

legend_labels = [l.get_label() for l in graphs]
ax1.legend(graphs, legend_labels, loc='upper left',
 		  ncol=1, fancybox=True, shadow=False, numpoints = 1)

ax1.set_xticks([datetime.datetime(2000, 1, 1).toordinal(),
		datetime.datetime(2010, 1, 1).toordinal(),
		datetime.datetime(2020, 1, 1).toordinal(),
		datetime.datetime(2030, 1, 1).toordinal(), 
		datetime.datetime(2040, 1, 1).toordinal(),
		datetime.datetime(2050, 1, 1).toordinal(), 
		datetime.datetime(2060, 1, 1).toordinal(),
		datetime.datetime(2070, 1, 1).toordinal()])


ax1.set_title('b) Correlation coefficient and root-mean-square deviation')
show()