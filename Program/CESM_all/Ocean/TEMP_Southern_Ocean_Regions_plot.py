#Program plots the temperature of the five Southern Ocean regions

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
directory_mercator	    = '../../../Data/Mercator/'

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
		data_year[year_i]	= np.sum(data[year_i * 12 + month_start - 1: year_i * 12 + month_end] * month_days, axis = 0)

	return time_year, data_year

#-----------------------------------------------------------------------------------------
#--------------------------------MAIN SCRIPT STARTS HERE----------------------------------
#-----------------------------------------------------------------------------------------

TEMP_data = netcdf.Dataset(directory_cesm_control+'Ocean/TEMP_Southern_Ocean_Regions.nc', 'r')

temp_cesm_control	= TEMP_data.variables['TEMP'][:] 	

TEMP_data.close()

TEMP_data = netcdf.Dataset(directory_cesm+'Ocean/TEMP_Southern_Ocean_Regions.nc', 'r')

time_cesm	        = TEMP_data.variables['time'][:]     	
temp_cesm	        = TEMP_data.variables['TEMP'][:] 	

TEMP_data.close()

#-----------------------------------------------------------------------------------------

TEMP_data = netcdf.Dataset(directory_cesm_low_control+'Ocean/TEMP_Southern_Ocean_Regions.nc', 'r')

temp_cesm_low_control	= TEMP_data.variables['TEMP'][:] 	

TEMP_data.close()

TEMP_data = netcdf.Dataset(directory_cesm_low+'Ocean/TEMP_Southern_Ocean_Regions.nc', 'r')

temp_cesm_low	        = TEMP_data.variables['TEMP'][:] 	

TEMP_data.close()

#-----------------------------------------------------------------------------------------

TEMP_data = netcdf.Dataset(directory_mercator+'Ocean/TEMP_Southern_Ocean_Regions.nc', 'r')

time_mer	= TEMP_data.variables['time'][:]     	
temp_mer	= TEMP_data.variables['TEMP'][:] 	

TEMP_data.close()

#-----------------------------------------------------------------------------------------

#Take yearly averages
time_year, temp_cesm_control_1	= YearlyConverter(time_cesm, temp_cesm_control[:, 0])
time_year, temp_cesm_control_2	= YearlyConverter(time_cesm, temp_cesm_control[:, 1])
time_year, temp_cesm_control_3	= YearlyConverter(time_cesm, temp_cesm_control[:, 2])
time_year, temp_cesm_control_4	= YearlyConverter(time_cesm, temp_cesm_control[:, 3])
time_year, temp_cesm_control_5	= YearlyConverter(time_cesm, temp_cesm_control[:, 4])

#Take yearly averages
time_year, temp_cesm_1	= YearlyConverter(time_cesm, temp_cesm[:, 0])
time_year, temp_cesm_2	= YearlyConverter(time_cesm, temp_cesm[:, 1])
time_year, temp_cesm_3	= YearlyConverter(time_cesm, temp_cesm[:, 2])
time_year, temp_cesm_4	= YearlyConverter(time_cesm, temp_cesm[:, 3])
time_year, temp_cesm_5	= YearlyConverter(time_cesm, temp_cesm[:, 4])

#Take yearly averages
time_year, temp_cesm_low_control_1	= YearlyConverter(time_cesm, temp_cesm_low_control[:, 0])
time_year, temp_cesm_low_control_2	= YearlyConverter(time_cesm, temp_cesm_low_control[:, 1])
time_year, temp_cesm_low_control_3	= YearlyConverter(time_cesm, temp_cesm_low_control[:, 2])
time_year, temp_cesm_low_control_4	= YearlyConverter(time_cesm, temp_cesm_low_control[:, 3])
time_year, temp_cesm_low_control_5	= YearlyConverter(time_cesm, temp_cesm_low_control[:, 4])

#Take yearly averages
time_year, temp_cesm_low_1	= YearlyConverter(time_cesm, temp_cesm_low[:, 0])
time_year, temp_cesm_low_2	= YearlyConverter(time_cesm, temp_cesm_low[:, 1])
time_year, temp_cesm_low_3	= YearlyConverter(time_cesm, temp_cesm_low[:, 2])
time_year, temp_cesm_low_4	= YearlyConverter(time_cesm, temp_cesm_low[:, 3])
time_year, temp_cesm_low_5	= YearlyConverter(time_cesm, temp_cesm_low[:, 4])


#Take yearly averages
time_year_mer, temp_mer_1	= YearlyConverter(time_mer, temp_mer[:, 0])
time_year_mer, temp_mer_2	= YearlyConverter(time_mer, temp_mer[:, 1])
time_year_mer, temp_mer_3	= YearlyConverter(time_mer, temp_mer[:, 2])
time_year_mer, temp_mer_4	= YearlyConverter(time_mer, temp_mer[:, 3])
time_year_mer, temp_mer_5	= YearlyConverter(time_mer, temp_mer[:, 4])

#-----------------------------------------------------------------------------------------

fig, ax1	= subplots()

graph_Mercator		= ax1.plot_date(time_year, np.zeros(len(time_year)) + np.mean(temp_mer_1), '-b', linewidth = 2.0, label = 'Mercator')
ax1.fill_between(time_year, temp_mer_1.min(), temp_mer_1.max(), alpha=0.2, edgecolor='b', facecolor='b')

graph_HR_CESM_Control	= ax1.plot_date(time_year, temp_cesm_control_1, '-k', linewidth = 2.0, label = 'HR-CESM Control')
graph_HR_CESM		= ax1.plot_date(time_year, temp_cesm_1, '-r', linewidth = 2.0, label = 'HR-CESM')
graph_LR_CESM_Control	= ax1.plot_date(time_year, temp_cesm_low_control_1, '--k', linewidth = 2.0, label = 'LR-CESM Control')
graph_LR_CESM		= ax1.plot_date(time_year, temp_cesm_low_1, '--r', linewidth = 2.0, label = 'LR-CESM')	

ax1.set_xlabel('Model year')
ax1.set_ylabel('Temperature ($^{\circ}$C)')
ax1.set_ylim(-2, 3.5)
ax1.grid()

ax1.set_xticks([datetime.datetime(2000, 1, 1).toordinal(),
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

graphs	      = graph_HR_CESM + graph_HR_CESM_Control + graph_LR_CESM + graph_LR_CESM_Control + graph_Mercator

legend_labels = [l.get_label() for l in graphs]
ax1.legend(graphs, legend_labels, loc='lower left',
 		  ncol=1, fancybox=True, shadow=False, numpoints = 1)

ax1.set_title('b) East Antarctica')

#-----------------------------------------------------------------------------------------

fig, ax1	= subplots()

graph_Mercator		= ax1.plot_date(time_year, np.zeros(len(time_year)) + np.mean(temp_mer_2), '-b', linewidth = 2.0, label = 'Mercator')
ax1.fill_between(time_year, temp_mer_2.min(), temp_mer_2.max(), alpha=0.2, edgecolor='b', facecolor='b')

graph_HR_CESM_Control	= ax1.plot_date(time_year, temp_cesm_control_2, '-k', linewidth = 2.0, label = 'HR-CESM Control')
graph_HR_CESM		= ax1.plot_date(time_year, temp_cesm_2, '-r', linewidth = 2.0, label = 'HR-CESM')
graph_LR_CESM_Control	= ax1.plot_date(time_year, temp_cesm_low_control_2, '--k', linewidth = 2.0, label = 'LR-CESM Control')
graph_LR_CESM		= ax1.plot_date(time_year, temp_cesm_low_2, '--r', linewidth = 2.0, label = 'LR-CESM')	

ax1.set_xlabel('Model year')
ax1.set_ylabel('Temperature ($^{\circ}$C)')
ax1.set_ylim(-2, 3.5)
ax1.grid()

ax1.set_xticks([datetime.datetime(2000, 1, 1).toordinal(),
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

graphs	      = graph_HR_CESM + graph_HR_CESM_Control + graph_LR_CESM + graph_LR_CESM_Control + graph_Mercator

legend_labels = [l.get_label() for l in graphs]
ax1.legend(graphs, legend_labels, loc='upper left',
 		  ncol=1, fancybox=True, shadow=False, numpoints = 1)

ax1.set_title('c) Ross Region')

#-----------------------------------------------------------------------------------------

fig, ax1	= subplots()

graph_Mercator		= ax1.plot_date(time_year, np.zeros(len(time_year)) + np.mean(temp_mer_3), '-b', linewidth = 2.0, label = 'Mercator')
ax1.fill_between(time_year, temp_mer_3.min(), temp_mer_3.max(), alpha=0.2, edgecolor='b', facecolor='b')

graph_HR_CESM_Control	= ax1.plot_date(time_year, temp_cesm_control_3, '-k', linewidth = 2.0, label = 'HR-CESM Control')
graph_HR_CESM		= ax1.plot_date(time_year, temp_cesm_3, '-r', linewidth = 2.0, label = 'HR-CESM')
graph_LR_CESM_Control	= ax1.plot_date(time_year, temp_cesm_low_control_3, '--k', linewidth = 2.0, label = 'LR-CESM Control')
graph_LR_CESM		= ax1.plot_date(time_year, temp_cesm_low_3, '--r', linewidth = 2.0, label = 'LR-CESM')	

ax1.set_xlabel('Model year')
ax1.set_ylabel('Temperature ($^{\circ}$C)')
ax1.set_ylim(-2, 3.5)
ax1.grid()

ax1.set_xticks([datetime.datetime(2000, 1, 1).toordinal(),
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

graphs	      = graph_HR_CESM + graph_HR_CESM_Control + graph_LR_CESM + graph_LR_CESM_Control + graph_Mercator

legend_labels = [l.get_label() for l in graphs]
ax1.legend(graphs, legend_labels, loc='lower left',
 		  ncol=1, fancybox=True, shadow=False, numpoints = 1)

ax1.set_title('d) Amundsen Region')

#-----------------------------------------------------------------------------------------

fig, ax1	= subplots()

graph_Mercator		= ax1.plot_date(time_year, np.zeros(len(time_year)) + np.mean(temp_mer_4), '-b', linewidth = 2.0, label = 'Mercator')
ax1.fill_between(time_year, temp_mer_4.min(), temp_mer_4.max(), alpha=0.2, edgecolor='b', facecolor='b')

graph_HR_CESM_Control	= ax1.plot_date(time_year, temp_cesm_control_4, '-k', linewidth = 2.0, label = 'HR-CESM Control')
graph_HR_CESM		= ax1.plot_date(time_year, temp_cesm_4, '-r', linewidth = 2.0, label = 'HR-CESM')
graph_LR_CESM_Control	= ax1.plot_date(time_year, temp_cesm_low_control_4, '--k', linewidth = 2.0, label = 'LR-CESM Control')
graph_LR_CESM		= ax1.plot_date(time_year, temp_cesm_low_4, '--r', linewidth = 2.0, label = 'LR-CESM')	

ax1.set_xlabel('Model year')
ax1.set_ylabel('Temperature ($^{\circ}$C)')
ax1.set_ylim(-2, 3.5)
ax1.grid()

ax1.set_xticks([datetime.datetime(2000, 1, 1).toordinal(),
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

graphs	      = graph_HR_CESM + graph_HR_CESM_Control + graph_LR_CESM + graph_LR_CESM_Control + graph_Mercator

legend_labels = [l.get_label() for l in graphs]
ax1.legend(graphs, legend_labels, loc='upper left',
 		  ncol=1, fancybox=True, shadow=False, numpoints = 1)

ax1.set_title('e) Weddell Region')

#-----------------------------------------------------------------------------------------

fig, ax1	= subplots()

graph_Mercator		= ax1.plot_date(time_year, np.zeros(len(time_year)) + np.mean(temp_mer_5), '-b', linewidth = 2.0, label = 'Mercator')
ax1.fill_between(time_year, temp_mer_5.min(), temp_mer_5.max(), alpha=0.2, edgecolor='b', facecolor='b')

graph_HR_CESM_Control	= ax1.plot_date(time_year, temp_cesm_control_5, '-k', linewidth = 2.0, label = 'HR-CESM Control')
graph_HR_CESM		= ax1.plot_date(time_year, temp_cesm_5, '-r', linewidth = 2.0, label = 'HR-CESM')
graph_LR_CESM_Control	= ax1.plot_date(time_year, temp_cesm_low_control_5, '--k', linewidth = 2.0, label = 'LR-CESM Control')
graph_LR_CESM		= ax1.plot_date(time_year, temp_cesm_low_5, '--r', linewidth = 2.0, label = 'LR-CESM')	

ax1.set_xlabel('Model year')
ax1.set_ylabel('Temperature ($^{\circ}$C)')
ax1.set_ylim(-2, 3.5)
ax1.grid()

ax1.set_xticks([datetime.datetime(2000, 1, 1).toordinal(),
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

graphs	      = graph_HR_CESM + graph_HR_CESM_Control + graph_LR_CESM + graph_LR_CESM_Control + graph_Mercator

legend_labels = [l.get_label() for l in graphs]
ax1.legend(graphs, legend_labels, loc='upper left',
 		  ncol=1, fancybox=True, shadow=False, numpoints = 1)

ax1.set_title('f) Antarctic Peninsula')

show()