#Program plots the Antarctic sea-ice area

from pylab import *
import numpy
import datetime
import time
import glob, os
import math
import netCDF4 as netcdf
import matplotlib.colors as colors

#Making pathway to folder with all data
directory_cesm		    = '../../../Data/HR-CESM/'
directory_cesm_control	    = '../../../Data/HR-CESM_Control/'
directory_cesm_low	    = '../../../Data/LR-CESM/'
directory_cesm_low_control  = '../../../Data/LR-CESM_Control/'
directory_SSMR_SSMI	    = '../../../Data/SSMR_SSMI/'

def ReadinData(filename):

	ICE_data 	= netcdf.Dataset(filename, 'r')

	time		= ICE_data.variables['time'][:]     
	antarctic	= ICE_data.variables['Antarctic'][:]
	
	ICE_data.close()

	return time, antarctic

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
	data_min_year	= ma.masked_all(len(time_year))
	data_max_year	= ma.masked_all(len(time_year))

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
		data_min_year[year_i]		= np.min(data[year_i * 12 + month_start - 1: year_i * 12 + month_end])
		data_max_year[year_i]		= np.max(data[year_i * 12 + month_start - 1: year_i * 12 + month_end])

	return time_year, data_year, data_min_year, data_max_year

#-----------------------------------------------------------------------------------------
#--------------------------------MAIN SCRIPT STARTS HERE----------------------------------
#-----------------------------------------------------------------------------------------	

month_start	= 1
month_end	= 12

#-----------------------------------------------------------------------------------------
time_cesm, antarctic_cesm		                = ReadinData(directory_cesm+'Ice/Ice_Area.nc')
time_cesm_control, antarctic_cesm_control	        = ReadinData(directory_cesm_control+'Ice/Ice_Area.nc')
time_cesm_low, antarctic_cesm_low		        = ReadinData(directory_cesm_low+'Ice/Ice_Area.nc')
time_cesm_low_control, antarctic_cesm_low_control	= ReadinData(directory_cesm_low_control+'Ice/Ice_Area.nc')
time, antarctic				                = ReadinData(directory_SSMR_SSMI+'Ice/Ice_Area.nc')
#-----------------------------------------------------------------------------------------

time_cesm_year, antarctic_cesm_year, antarctic_min_cesm_year, antarctic_max_cesm_year			                                = YearlyConverter(time_cesm, antarctic_cesm, month_start, month_end)
time_cesm_control_year, antarctic_cesm_control_year, antarctic_min_cesm_control_year, antarctic_max_cesm_control_year	                = YearlyConverter(time_cesm_control, antarctic_cesm_control, month_start, month_end)
time_cesm_low_year, antarctic_cesm_low_year, antarctic_min_cesm_low_year, antarctic_max_cesm_low_year			                = YearlyConverter(time_cesm_low, antarctic_cesm_low, month_start, month_end)
time_cesm_low_control_year, antarctic_cesm_low_control_year, antarctic_min_cesm_low_control_year, antarctic_max_cesm_low_control_year	= YearlyConverter(time_cesm_low_control, antarctic_cesm_low_control, month_start, month_end)
time_year, antarctic_year, antarctic_min_year, antarctic_max_year					                                = YearlyConverter(time, antarctic, month_start, month_end)

print 'HR-CESM Control:', antarctic_max_cesm_control_year.min(), antarctic_max_cesm_control_year.max()
print 'LR-CESM Control:', antarctic_max_cesm_low_control_year.min(), antarctic_max_cesm_low_control_year.max()
#-----------------------------------------------------------------------------------------
fig, ax = plt.subplots()

ax.fill_between(time_cesm_year, antarctic_year.min() / 1000000, antarctic_year.max() / 1000000, alpha=0.2, edgecolor='b', facecolor='b')
SSMR_SSMI_graph	= ax.plot_date(time_cesm_year, np.zeros(len(time_cesm_year)) + np.mean(antarctic_year) / 1000000, '-b', linewidth = 2.0, label = 'SSMR-SSM/I')

ax.fill_between(time_cesm_year, antarctic_min_year.min() / 1000000, antarctic_min_year.max() / 1000000, alpha=0.2, edgecolor='b', facecolor='b')
ax.plot_date(time_cesm_year, np.zeros(len(time_cesm_year)) + np.mean(antarctic_min_year) / 1000000, ':b', linewidth = 3.0, label = 'SSMR-SSM/I')

ax.fill_between(time_cesm_year, antarctic_max_year.min() / 1000000, antarctic_max_year.max() / 1000000, alpha=0.2, edgecolor='b', facecolor='b')
ax.plot_date(time_cesm_year, np.zeros(len(time_cesm_year)) + np.mean(antarctic_max_year) / 1000000, '--b', linewidth = 2.0, label = 'SSMR-SSM/I')

plot_date(time_cesm_year, antarctic_min_cesm_control_year / 1000000, ':k', linewidth = 3.0)
plot_date(time_cesm_year, antarctic_max_cesm_control_year / 1000000, '--k', linewidth = 2.0)
plot_date(time_cesm_year, antarctic_min_cesm_year / 1000000, ':r', linewidth = 3.0)
plot_date(time_cesm_year, antarctic_max_cesm_year / 1000000, '--r', linewidth = 2.0)

HR_CESM_Control_graph	= plot_date(time_cesm_year, antarctic_cesm_control_year / 1000000, '-k', linewidth = 2.0, label = 'HR-CESM Control')
HR_CESM_graph	        = plot_date(time_cesm_year, antarctic_cesm_year / 1000000, '-r', linewidth = 2.0, label = 'HR-CESM')

ax.set_xlabel('Model year')
ax.set_ylabel(r'Sea-ice area ($\times 10^6$ km$^2$)')
ax.set_ylim(-1, 25)
title('a) HR-CESM')
grid()

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

graphs	      	= HR_CESM_graph + HR_CESM_Control_graph + SSMR_SSMI_graph

legend_labels 	= [l.get_label() for l in graphs]
legend_1	= ax.legend(graphs, legend_labels, bbox_to_anchor=(1.01, 1.08), ncol=1, fancybox=True, shadow=False, numpoints = 1)

graph_max	= plot_date([time_cesm_year[1], time_cesm_year[1]], [-100, -100], '--k', linewidth = 2.0, label = 'Max')
graph_mean	= plot_date([time_cesm_year[1], time_cesm_year[1]], [-100, -100], '-k', linewidth = 2.0, label = 'Mean')
graph_min	= plot_date([time_cesm_year[1], time_cesm_year[1]], [-100, -100], ':k', linewidth = 3.0, label = 'Min')

graphs	      	= graph_max + graph_mean + graph_min

legend_labels 	= [l.get_label() for l in graphs]
legend_2	= ax.legend(graphs, legend_labels, bbox_to_anchor=(0.218, 1.08), ncol=1, fancybox=True, shadow=False, numpoints = 1)
ax.add_artist(legend_1)

fig, ax = plt.subplots()

ax.fill_between(time_cesm_year, antarctic_year.min() / 1000000, antarctic_year.max() / 1000000, alpha=0.2, edgecolor='b', facecolor='b')
SSMR_SSMI_graph	= ax.plot_date(time_cesm_year, np.zeros(len(time_cesm_year)) + np.mean(antarctic_year) / 1000000, '-b', linewidth = 2.0, label = 'SSMR-SSM/I')

ax.fill_between(time_cesm_year, antarctic_min_year.min() / 1000000, antarctic_min_year.max() / 1000000, alpha=0.2, edgecolor='b', facecolor='b')
ax.plot_date(time_cesm_year, np.zeros(len(time_cesm_year)) + np.mean(antarctic_min_year) / 1000000, ':b', linewidth = 3.0, label = 'SSMR-SSM/I')

ax.fill_between(time_cesm_year, antarctic_max_year.min() / 1000000, antarctic_max_year.max() / 1000000, alpha=0.2, edgecolor='b', facecolor='b')
ax.plot_date(time_cesm_year, np.zeros(len(time_cesm_year)) + np.mean(antarctic_max_year) / 1000000, '--b', linewidth = 2.0, label = 'SSMR-SSM/I')

plot_date(time_cesm_year, antarctic_min_cesm_low_control_year / 1000000, ':k', linewidth = 3.0)
plot_date(time_cesm_year, antarctic_max_cesm_low_control_year / 1000000, '--k', linewidth = 2.0)
plot_date(time_cesm_year, antarctic_min_cesm_low_year / 1000000, ':r', linewidth = 3.0)
plot_date(time_cesm_year, antarctic_max_cesm_low_year / 1000000, '--r', linewidth = 2.0)

LR_CESM_Control_graph	= plot_date(time_cesm_year, antarctic_cesm_low_control_year / 1000000, '-k', linewidth = 2.0, label = 'LR-CESM Control')
LR_CESM_graph	        = plot_date(time_cesm_year, antarctic_cesm_low_year / 1000000, '-r', linewidth = 2.0, label = 'LR-CESM')

ax.set_xlabel('Model year')
ax.set_ylabel(r'Sea-ice area ($\times 10^6$ km$^2$)')
ax.set_ylim(-1, 25)
title('b) LR-CESM')
grid()

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


graphs	      	= LR_CESM_graph + LR_CESM_Control_graph + SSMR_SSMI_graph

legend_labels 	= [l.get_label() for l in graphs]
legend_1	= ax.legend(graphs, legend_labels, bbox_to_anchor=(1.01, 1.08), ncol=1, fancybox=True, shadow=False, numpoints = 1)


graph_max	= plot_date([time_cesm_year[1], time_cesm_year[1]], [-100, -100], '--k', linewidth = 2.0, label = 'Max')
graph_mean	= plot_date([time_cesm_year[1], time_cesm_year[1]], [-100, -100], '-k', linewidth = 2.0, label = 'Mean')
graph_min	= plot_date([time_cesm_year[1], time_cesm_year[1]], [-100, -100], ':k', linewidth = 3.0, label = 'Min')

graphs	      	= graph_max + graph_mean + graph_min

legend_labels 	= [l.get_label() for l in graphs]
legend_2	= ax.legend(graphs, legend_labels, bbox_to_anchor=(0.218, 1.08), ncol=1, fancybox=True, shadow=False, numpoints = 1)
ax.add_artist(legend_1)

show()