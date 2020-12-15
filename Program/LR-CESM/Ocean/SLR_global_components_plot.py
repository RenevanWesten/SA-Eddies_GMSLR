#Program plots the GMSLR components

from pylab import *
import numpy
import datetime
import time
import glob, os
import math
import netCDF4 as netcdf
import matplotlib.colors as colors
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

#Making pathway to folder with all data
directory = '../../../Data/LR-CESM/'

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

HEAT_data = netcdf.Dataset(directory+'Ocean/SMB_Greenland.nc', 'r')

#Writing data to correct variable	
time		= HEAT_data.variables['time'][:] 			
Greenland	= HEAT_data.variables['SLR_Greenland'][7] 	#Take the 50%-percentile

HEAT_data.close()

#-----------------------------------------------------------------------------------------	

HEAT_data = netcdf.Dataset(directory+'Ocean/SMB_Glaciers.nc', 'r')

#Writing data to correct variable	
time		= HEAT_data.variables['time'][:] 			
Glaciers	= HEAT_data.variables['SLR_Glaciers'][7] 	#Take the 50%-percentile	

HEAT_data.close()

#-----------------------------------------------------------------------------------------	

HEAT_data = netcdf.Dataset(directory+'Ocean/SMB_Antarctica.nc', 'r')

#Writing data to correct variable	
time		= HEAT_data.variables['time'][:] 		
Antarctica_SMB	= HEAT_data.variables['SLR_Antarctica'][7] 	#Take the 50%-percentile

HEAT_data.close()

HEAT_data = netcdf.Dataset(directory+'Ocean/Antarctica_basal_melt_SLR.nc', 'r')

#Writing data to correct variable	
time		= HEAT_data.variables['time'][:] 		
Antarctica_melt	= HEAT_data.variables['SLR_total'][:, 7] * 100.0	#Take the 50%-percentile

HEAT_data.close()

#Take the LARMIP model mean
Antarctica_melt	= np.mean(Antarctica_melt, axis = 0)

#Take the sum of the Basal melt and SMB
Antarctica	= Antarctica_SMB + Antarctica_melt

#-----------------------------------------------------------------------------------------	

HEAT_data 	= netcdf.Dataset(directory+'Ocean/SSH_global_steric.nc', 'r')

time_rcp	= HEAT_data.variables['time'][:] 
steric		= HEAT_data.variables['SSH'][:] * 100.0		#Centimeter

HEAT_data.close()

HEAT_data 	= netcdf.Dataset(directory+'../LR-CESM_Control/Ocean/SSH_global_steric.nc', 'r')

steric_control	= HEAT_data.variables['SSH'][:] * 100.0		#Centimeter

HEAT_data.close()

#Take yearly averages
time_year, steric		= YearlyConverter(time_rcp, steric)
steric				= steric - steric[0]
time_year, steric_control	= YearlyConverter(time_rcp, steric_control)
steric_control			= steric_control - steric_control[0]

#Remove drift from control simulation
steric				= steric - steric_control

#-----------------------------------------------------------------------------------------	

#Now add all the components
total	= Greenland + Glaciers + Antarctica + steric

fig, ax	= subplots()

ax.fill_between(time, 0, steric, facecolor='lightcoral', edgecolor='firebrick')
ax.fill_between(time, steric, steric + Glaciers, facecolor='mediumpurple', edgecolor='darkmagenta')
ax.fill_between(time, steric + Glaciers, steric + Glaciers + Greenland, facecolor='lightsalmon', edgecolor='orangered')
ax.fill_between(time, steric + Glaciers + Greenland, steric + Glaciers + Greenland + Antarctica, facecolor='lightskyblue', edgecolor='dodgerblue')
ax.plot_date(time, total, '-k', linewidth = 3.0)

ax.set_xlabel('Model year')
ax.set_ylabel('Global mean sea-level rise (cm)')
ax.set_ylim(-1, 50)
ax.grid()

ax.set_xticks([datetime.datetime(2000, 1, 1).toordinal(),
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

ax.set_title('b) LR-CESM')

total_graph		= mlines.Line2D([], [], color='black', linewidth = 3.0, label = 'Total')
steric_graph 		= mpatches.Patch(facecolor='lightcoral', edgecolor='firebrick', label='Steric')
glaciers_graph		= mpatches.Patch(facecolor='mediumpurple', edgecolor='darkmagenta', label='Glaciers')
greenland_graph		= mpatches.Patch(facecolor='lightsalmon', edgecolor='orangered', label='Greenland')
antarctica_graph	= mpatches.Patch(facecolor='lightskyblue', edgecolor='dodgerblue', label='Antarctica')

ax.legend(handles=[total_graph, antarctica_graph, greenland_graph, glaciers_graph, steric_graph], loc='upper left', ncol=1, fancybox=True, shadow=False)
show()