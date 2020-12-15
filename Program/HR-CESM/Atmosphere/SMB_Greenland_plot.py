#Program plots the SMB Greenland

from pylab import *
import numpy
import datetime
import time
import glob, os
import math
import netCDF4 as netcdf
import matplotlib.colors as colors

#Making pathway to folder with all data
directory  = '../../../Data/HR-CESM/'

#-----------------------------------------------------------------------------------------
#--------------------------------MAIN SCRIPT STARTS HERE----------------------------------
#-----------------------------------------------------------------------------------------	


TEMP_data = netcdf.Dataset(directory+'Ocean/SMB_Greenland.nc', 'r')

#Writing data to correct variable	
time_year	= TEMP_data.variables['time'][:]     	
SLR_all_per	= TEMP_data.variables['SLR_Greenland'][:]

TEMP_data.close()

#-----------------------------------------------------------------------------------------

fig, ax	= subplots()

ax.fill_between(time_year, SLR_all_per[4],  SLR_all_per[10], color = 'k', alpha = 0.25)
ax.fill_between(time_year, SLR_all_per[6],  SLR_all_per[8], color = 'k', alpha = 0.25)

RCP_graph	= ax.plot_date(time_year,  SLR_all_per[7], '-k', linewidth = 2.0, label = 'HR-CESM')


ax.set_xlabel('Model year')
ax.set_ylabel('Global mean sea-level rise (cm)')
ax.set_ylim(-0.5, 5)
ax.grid()

ax.set_xticks([	datetime.datetime(2000, 1, 1).toordinal(),
		datetime.datetime(2010, 1, 1).toordinal(),
		datetime.datetime(2020, 1, 1).toordinal(),
		datetime.datetime(2030, 1, 1).toordinal(), 
		datetime.datetime(2040, 1, 1).toordinal(),
		datetime.datetime(2050, 1, 1).toordinal(), 
		datetime.datetime(2060, 1, 1).toordinal(),
		datetime.datetime(2070, 1, 1).toordinal(),
		datetime.datetime(2080, 1, 1).toordinal(),
		datetime.datetime(2090, 1, 1).toordinal(),
		datetime.datetime(2100, 1, 1).toordinal()])


ax.set_title('c) HR-CESM')

ax2 = fig.add_axes([0.15, 0.68, 0.2, 0.2])

ax2.set_ylim(-0.1, 1.1)
ax2.set_xlim(0, 2.6)
ax2.axis('off')

x_legend	= np.arange(0, 1.51, 0.1)
ax2.fill_between(x_legend, 0.05, 0.95, color = 'k', alpha = 0.25)
ax2.fill_between(x_legend, 0.25, 0.75, color = 'k', alpha = 0.25)
ax2.plot(x_legend, 0.5 + np.zeros(len(x_legend)), linestyle = '-', color = 'k', linewidth = 3.0)

ax2.text(2.35, 0.05,'5$\%$', color ='k',fontsize=15,ha='left',va='center')
ax2.plot([1.5, 2.32], [0.05, 0.05], '--k', linewidth = 0.5)

ax2.text(2.05, 0.25,'25$\%$', color ='k',fontsize=15,ha='left',va='center')
ax2.plot([1.5, 2.02], [0.25, 0.25], '--k', linewidth = 0.5)

ax2.text(1.85, 0.5,'50$\%$', color ='k',fontsize=15,ha='left',va='center')
ax2.plot([1.5, 1.82], [0.5, 0.5], '--k', linewidth = 0.5)

ax2.text(2.05, 0.75,'75$\%$', color ='k',fontsize=15,ha='left',va='center')
ax2.plot([1.5, 2.02], [0.75, 0.75], '--k', linewidth = 0.5)

ax2.text(2.35, 0.95,'95$\%$', color ='k',fontsize=15,ha='left',va='center')
ax2.plot([1.5, 2.32], [0.95, 0.95], '--k', linewidth = 0.5)

show()