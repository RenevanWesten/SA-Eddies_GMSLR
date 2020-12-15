#Program plots the DWeddell Gyre volume transport

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
directory_cesm		    = '../../../Data/HR-CESM/'
directory_cesm_control	    = '../../../Data/HR-CESM_Control/'
directory_cesm_low	    = '../../../Data/LR-CESM/'
directory_cesm_low_control  = '../../../Data/LR-CESM_Control/'

def ReadinData(filename):
	"""Reads-in the data"""
	HEAT_data 		= netcdf.Dataset(filename, 'r')

	time			= HEAT_data.variables['time'][:] 
	transport		= HEAT_data.variables['Transport'][:] 
	HEAT_data.close()

	return time, transport

def YearlyConverter(time, data, month_start = 1, month_end = 12):
	"""Determines yearly averaged, over different months of choice,
	default is set to January - December"""

	#Take twice the amount of years for the month day
	month_days	= np.asarray([31., 28., 31., 30., 31., 30., 31., 31., 30., 31., 30., 31., 31., 28., 31., 30., 31., 30., 31., 31., 30., 31., 30., 31.])
	month_days	= month_days[month_start - 1:month_end]
	month_days	= month_days / np.sum(month_days)
	
	if month_end <= 12:
		#Normal average over a single year, for example, February 100 - December 100
		time_year		= np.zeros(len(time) / 12)

	else:
		#If you take the average, for example, over November 100 - May 101
		#Take year 101 as the average over this period
		#There is one year less compared to the period analysed
		time_year		= np.zeros(len(time) / 12 - 1)

	#-----------------------------------------------------------------------------------------
	data_year	= ma.masked_all(len(time_year))

	for year_i in range(len(time_year)):
		#Determine the SSH over the selected months

		#The year is defined as the current year
		year			= int(str(datetime.date.fromordinal(int(time[year_i * 12])))[0:4])

		if month_end	>= 13:
			#If average is taken over, for example, November 100 - May 101, the year is defined as 101
			year = year + 1

		time_year[year_i] 	= datetime.datetime(year, 1, 1).toordinal()

		#Determine the time mean over the months of choice
		data_year[year_i]		= np.sum(data[year_i * 12 + month_start - 1: year_i * 12 + month_end] * month_days, axis = 0)

	return time_year, data_year

#-----------------------------------------------------------------------------------------
#--------------------------------MAIN SCRIPT STARTS HERE----------------------------------
#-----------------------------------------------------------------------------------------

lon_Weddell	= 320

depth_min 	= 0 
depth_max	= 6000

month_start	= 1 	#1 = January, 2 = February, 3 = March, ..., 13 = January (+ 1), ...
month_end	= 12	#12 = December, 13 = January (+ 1), 14 = February (+ 1), ...

#-----------------------------------------------------------------------------------------

time, transport_cesm		= ReadinData(directory_cesm+'/Ocean/Weddell_Gyre_transport_depth_'+str(depth_min)+'-'+str(depth_max)+'_m_lon_'+str(lon_Weddell)+'E.nc')
time_year, transport_cesm_year	= YearlyConverter(time, transport_cesm, month_start, month_end)
 
#-----------------------------------------------------------------------------------------

time, transport_cesm_control	                = ReadinData(directory_cesm_control+'/Ocean/Weddell_Gyre_transport_depth_'+str(depth_min)+'-'+str(depth_max)+'_m_lon_'+str(lon_Weddell)+'E.nc')
time_control_year, transport_cesm_control_year	= YearlyConverter(time, transport_cesm_control, month_start, month_end)

print 'HR-CESM Control', np.mean(transport_cesm_control_year), transport_cesm_control_year.min(), transport_cesm_control_year.max()

#-----------------------------------------------------------------------------------------

time, transport_cesm_low		= ReadinData(directory_cesm_low+'/Ocean/Weddell_Gyre_transport_depth_'+str(depth_min)+'-'+str(depth_max)+'_m_lon_'+str(lon_Weddell)+'E.nc')
time_year, transport_cesm_low_year	= YearlyConverter(time, transport_cesm_low, month_start, month_end)

#-----------------------------------------------------------------------------------------

time, transport_cesm_low_control	            = ReadinData(directory_cesm_low_control+'/Ocean/Weddell_Gyre_transport_depth_'+str(depth_min)+'-'+str(depth_max)+'_m_lon_'+str(lon_Weddell)+'E.nc')
time_control_year, transport_cesm_low_control_year  = YearlyConverter(time, transport_cesm_low_control, month_start, month_end)

print 'LR-CESM Control', np.mean(transport_cesm_low_control_year), transport_cesm_low_control_year.min(), transport_cesm_low_control_year.max()

#-----------------------------------------------------------------------------------------

fig, ax	= subplots()

HR_CESM_control_graph	= ax.plot_date(time_year, transport_cesm_control_year, '-k', linewidth = 2.0, label = 'HR-CESM Control')
HR_CESM_graph	        = ax.plot_date(time_year, transport_cesm_year, '-r', linewidth = 2.0, label = 'HR-CESM')


ax.set_xlabel('Model year')
ax.set_ylabel('Transport (Sv)')
ax.set_ylim(-70, -30)
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

graphs	      = HR_CESM_graph + HR_CESM_control_graph

legend_labels = [l.get_label() for l in graphs]
ax.legend(graphs, legend_labels, loc='lower left',
 		  ncol=1, fancybox=True, shadow=False, numpoints = 1)

ax.set_title('e) HR-CESM')
#-----------------------------------------------------------------------------------------
fig, ax	= subplots()

LR_CESM_control_graph	= ax.plot_date(time_year, transport_cesm_low_control_year, '-k', linewidth = 2.0, label = 'LR-CESM Control')
LR_CESM_graph	        = ax.plot_date(time_year, transport_cesm_low_year, '-r', linewidth = 2.0, label = 'LR-CESM')

ax.set_xlabel('Model year')
ax.set_ylabel('Transport (Sv)')
ax.set_ylim(-70, -30)
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

graphs	      = LR_CESM_graph + LR_CESM_control_graph

legend_labels = [l.get_label() for l in graphs]
ax.legend(graphs, legend_labels, loc='lower left',
 		  ncol=1, fancybox=True, shadow=False, numpoints = 1)

ax.set_title('f) LR-CESM')
show()
