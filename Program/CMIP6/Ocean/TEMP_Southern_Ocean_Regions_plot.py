#Program plots the temperature anomalies of the five southern ocean regions

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
directory_CMIP6 	    = '../../../Data/CMIP6/'
directory_cesm		    = '../../../Data/HR-CESM/'
directory_cesm_control	    = '../../../Data/HR-CESM_Control/'
directory_cesm_low	    = '../../../Data/LR-CESM/'
directory_cesm_low_control  = '../../../Data/LR-CESM_Control/'

def ReadinData(filename):
	"""Reads-in the data"""

	TEMP_data 	= netcdf.Dataset(filename, 'r')

	#Writing data to correct variable	
	time		= TEMP_data.variables['time'][:]     	
	temp		= TEMP_data.variables['TEMP'][:] 	

	TEMP_data.close()

	#-----------------------------------------------------------------------------------------
		
	#Take yearly averages
	time_year, temp_1	= YearlyConverter(time, temp[:, 0])
	time_year, temp_2	= YearlyConverter(time, temp[:, 1])
	time_year, temp_3	= YearlyConverter(time, temp[:, 2])
	time_year, temp_4	= YearlyConverter(time, temp[:, 3])
	time_year, temp_5	= YearlyConverter(time, temp[:, 4])
	
	return time_year, temp_1, temp_2, temp_3, temp_4, temp_5


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

def TrendRemoverControl(time, control_data, data):
	"""Removes Control Simulation"""

	time		= np.arange(len(time))

	#Determine the detrended time series
	trend, base 	= polyfit(time, control_data, 1)
	data		= data - ((trend * time) + base)

	return data

#-----------------------------------------------------------------------------------------
#--------------------------------MAIN SCRIPT STARTS HERE----------------------------------
#-----------------------------------------------------------------------------------------

month_start		= 1 	#1 = January, 2 = February, 3 = March, ..., 13 = January (+ 1), ...
month_end		= 12	#12 = December, 13 = January (+ 1), 14 = February (+ 1), ...

lower_model_bound	= 3 #Retain the lower (and upper) sorted model for percentile levels
#-----------------------------------------------------------------------------------------
	
#Get the model names and path
models = glob.glob(directory_CMIP6+'*')
models.sort()

for model_i in range(len(models)):
	#Only retain the model names
	models[model_i]	= models[model_i][len(directory_CMIP6):]

print len(models)

higher_model_bound	= len(models) - lower_model_bound
lower_per_bound		= lower_model_bound / float(len(models) - 1) * 100.0
lower_per_bound		= str(int(np.round(lower_per_bound, 0)))
higher_per_bound	= str(100 - int(lower_per_bound))

for model_i in range(len(models)):
	#For each model get the all the files
	filename	= directory_CMIP6+models[model_i]+'/Ocean/TEMP_Southern_Ocean_Regions.nc'
	filename_control= directory_CMIP6+models[model_i]+'/Ocean/TEMP_Southern_Ocean_Regions_Control.nc'

	time_year, temp_1, temp_2, temp_3, temp_4, temp_5 = ReadinData(filename)
	time_year, temp_1_control, temp_2_control, temp_3_control, temp_4_control, temp_5_control = ReadinData(filename_control)

	#Determine the anomalies with respect to control time mean
	temp_1	= TrendRemoverControl(time_year, temp_1_control, temp_1)
	temp_2	= TrendRemoverControl(time_year, temp_2_control, temp_2)
	temp_3	= TrendRemoverControl(time_year, temp_3_control, temp_3)
	temp_4	= TrendRemoverControl(time_year, temp_4_control, temp_4)
	temp_5	= TrendRemoverControl(time_year, temp_5_control, temp_5)

	if model_i == 0:
		#First file
		temp_1_all	= ma.masked_all((len(models), len(time_year)))
		temp_2_all	= ma.masked_all((len(models), len(time_year)))
		temp_3_all	= ma.masked_all((len(models), len(time_year)))
		temp_4_all	= ma.masked_all((len(models), len(time_year)))
		temp_5_all	= ma.masked_all((len(models), len(time_year)))

		temp_1_high	= ma.masked_all((len(models), len(time_year)))
		temp_2_high	= ma.masked_all((len(models), len(time_year)))
		temp_3_high	= ma.masked_all((len(models), len(time_year)))
		temp_4_high	= ma.masked_all((len(models), len(time_year)))
		temp_5_high	= ma.masked_all((len(models), len(time_year)))

	#Save the data for each model
	temp_1_all[model_i]	= temp_1
	temp_2_all[model_i]	= temp_2
	temp_3_all[model_i]	= temp_3
	temp_4_all[model_i]	= temp_4
	temp_5_all[model_i]	= temp_5

	if models[model_i] == 'AWI-CM-1-1-MR' or models[model_i] == 'CNRM-CM6-1-HR' or models[model_i] == 'GFDL-CM4' or models[model_i] == 'GFDL-ESM4' or models[model_i] == 'MPI-ESM1-2-HR':
		#Save the data for each high-resolution model
		temp_1_high[model_i]	= temp_1
		temp_2_high[model_i]	= temp_2
		temp_3_high[model_i]	= temp_3
		temp_4_high[model_i]	= temp_4
		temp_5_high[model_i]	= temp_5

#Sort from high to low
temp_1_all	= np.sort(temp_1_all, axis = 0)
temp_2_all	= np.sort(temp_2_all, axis = 0)
temp_3_all	= np.sort(temp_3_all, axis = 0)
temp_4_all	= np.sort(temp_4_all, axis = 0)
temp_5_all	= np.sort(temp_5_all, axis = 0)

#-----------------------------------------------------------------------------------------

time_year_cesm, temp_1, temp_2, temp_3, temp_4, temp_5 = ReadinData(directory_cesm+'Ocean/TEMP_Southern_Ocean_Regions.nc')
time_year_cesm_control, temp_1_control, temp_2_control, temp_3_control, temp_4_control, temp_5_control = ReadinData(directory_cesm_control+'Ocean/TEMP_Southern_Ocean_Regions.nc')

#Determine the anomalies with respect to control time mean
temp_1_cesm 	= TrendRemoverControl(time_year_cesm, temp_1_control, temp_1)
temp_2_cesm	= TrendRemoverControl(time_year_cesm, temp_2_control, temp_2)
temp_3_cesm	= TrendRemoverControl(time_year_cesm, temp_3_control, temp_3)
temp_4_cesm	= TrendRemoverControl(time_year_cesm, temp_4_control, temp_4)
temp_5_cesm	= TrendRemoverControl(time_year_cesm, temp_5_control, temp_5)

time_year_cesm_low, temp_1, temp_2, temp_3, temp_4, temp_5 = ReadinData(directory_cesm_low+'Ocean/TEMP_Southern_Ocean_Regions.nc')
time_year_cesm_low_control, temp_1_control, temp_2_control, temp_3_control, temp_4_control, temp_5_control = ReadinData(directory_cesm_low_control+'Ocean/TEMP_Southern_Ocean_Regions.nc')

#Determine the anomalies with respect to control time mean
temp_1_cesm_low	= TrendRemoverControl(time_year_cesm_low, temp_1_control, temp_1)
temp_2_cesm_low	= TrendRemoverControl(time_year_cesm_low, temp_2_control, temp_2)
temp_3_cesm_low	= TrendRemoverControl(time_year_cesm_low, temp_3_control, temp_3)
temp_4_cesm_low	= TrendRemoverControl(time_year_cesm_low, temp_4_control, temp_4)
temp_5_cesm_low	= TrendRemoverControl(time_year_cesm_low, temp_5_control, temp_5)

#-----------------------------------------------------------------------------------------

fig, ax1		= subplots()

graph_CMIP6		= ax1.plot_date(time_year, np.mean(temp_1_all, axis = 0), '-k', linewidth = 2.0, label = 'CMIP6')
graph_CMIP6_HR		= ax1.plot_date(time_year, np.mean(temp_1_high, axis = 0), '--k', linewidth = 2.0, label = 'HR-CMIP6')
ax1.fill_between(time_year, np.min(temp_1_all, axis = 0), np.max(temp_1_all, axis = 0), alpha=0.2, edgecolor='k', facecolor='k')
ax1.fill_between(time_year, temp_1_all[lower_model_bound], temp_1_all[higher_model_bound], alpha=0.2, edgecolor='k', facecolor='k')

graph_HR_CESM		= ax1.plot_date(time_year, temp_1_cesm, '-r', linewidth = 2.0, label = 'HR-CESM')
graph_LR_CESM		= ax1.plot_date(time_year, temp_1_cesm_low, '-b', linewidth = 2.0, label = 'LR-CESM')	

ax1.set_xlabel('Model year')
ax1.set_ylabel('Temperature anomaly ($^{\circ}$C)')
ax1.set_ylim(-2, 2)
ax1.grid()

ax1.set_xticks([datetime.datetime(1, 1, 1).toordinal(),
		datetime.datetime(10, 1, 1).toordinal(),
		datetime.datetime(20, 1, 1).toordinal(),
		datetime.datetime(30, 1, 1).toordinal(), 
		datetime.datetime(40, 1, 1).toordinal(),
		datetime.datetime(50, 1, 1).toordinal(), 
		datetime.datetime(60, 1, 1).toordinal(),
		datetime.datetime(70, 1, 1).toordinal(),
		datetime.datetime(80, 1, 1).toordinal(),
		datetime.datetime(90, 1, 1).toordinal(),
		datetime.datetime(100, 1, 1).toordinal()])

graphs	      = graph_HR_CESM + graph_LR_CESM + graph_CMIP6 + graph_CMIP6_HR

legend_labels = [l.get_label() for l in graphs]
ax1.legend(graphs, legend_labels, loc='lower left',
 		  ncol=1, fancybox=True, shadow=False, numpoints = 1)

ax2 = fig.add_axes([0.6, 0.15, 0.2, 0.2])

ax2.set_ylim(-0.1, 1.1)
ax2.set_xlim(0, 2.6)
ax2.axis('off')

x_legend	= np.arange(1, 2.51, 0.1)
ax2.fill_between(x_legend, 0, 1, color ='k', alpha = 0.2)
ax2.fill_between(x_legend, 0.25, 0.75, color = 'k', alpha = 0.2)
ax2.plot(x_legend, 0.5 + np.zeros(len(x_legend)), linestyle = '-', color = 'k', linewidth = 3.0)


ax2.text(0.2, 0,'Min', color ='k',fontsize=15,ha='right',va='center')
ax2.plot([0.22, 1], [0, 0], '--k', linewidth = 0.5)

ax2.text(0.4, 0.25, lower_per_bound+'$\%$', color ='k',fontsize=15,ha='right',va='center')
ax2.plot([0.42, 1], [0.25, 0.25], '--k', linewidth = 0.5)

ax2.text(0.6, 0.5,'Mean', color ='k',fontsize=15,ha='right',va='center')
ax2.plot([0.62, 1], [0.5, 0.5], '--k', linewidth = 0.5)

ax2.text(0.4, 0.75, higher_per_bound+'$\%$', color ='k',fontsize=15,ha='right',va='center')
ax2.plot([0.42, 1], [0.75, 0.75], '--k', linewidth = 0.5)

ax2.text(0.2, 1,'Max', color ='k',fontsize=15,ha='right',va='center')
ax2.plot([0.22, 1], [1, 1], '--k', linewidth = 0.5)

ax1.set_title('b) East Antarctica')

#-----------------------------------------------------------------------------------------

fig, ax1		= subplots()

graph_CMIP6		= ax1.plot_date(time_year, np.mean(temp_2_all, axis = 0), '-k', linewidth = 2.0, label = 'CMIP6')
graph_CMIP6_HR		= ax1.plot_date(time_year, np.mean(temp_2_high, axis = 0), '--k', linewidth = 2.0, label = 'HR-CMIP6')
ax1.fill_between(time_year, np.min(temp_2_all, axis = 0), np.max(temp_2_all, axis = 0), alpha=0.2, edgecolor='k', facecolor='k')
ax1.fill_between(time_year, temp_2_all[lower_model_bound], temp_2_all[higher_model_bound], alpha=0.2, edgecolor='k', facecolor='k')

graph_HR_CESM		= ax1.plot_date(time_year, temp_2_cesm, '-r', linewidth = 2.0, label = 'HR-CESM')
graph_LR_CESM		= ax1.plot_date(time_year, temp_2_cesm_low, '-b', linewidth = 2.0, label = 'LR-CESM')

ax1.set_xlabel('Model year')
ax1.set_ylabel('Temperature anomaly ($^{\circ}$C)')
ax1.set_ylim(-2, 2)
ax1.grid()

ax1.set_xticks([datetime.datetime(1, 1, 1).toordinal(),
		datetime.datetime(10, 1, 1).toordinal(),
		datetime.datetime(20, 1, 1).toordinal(),
		datetime.datetime(30, 1, 1).toordinal(), 
		datetime.datetime(40, 1, 1).toordinal(),
		datetime.datetime(50, 1, 1).toordinal(), 
		datetime.datetime(60, 1, 1).toordinal(),
		datetime.datetime(70, 1, 1).toordinal(),
		datetime.datetime(80, 1, 1).toordinal(),
		datetime.datetime(90, 1, 1).toordinal(),
		datetime.datetime(100, 1, 1).toordinal()])

graphs	      = graph_HR_CESM + graph_LR_CESM + graph_CMIP6 + graph_CMIP6_HR

legend_labels = [l.get_label() for l in graphs]
ax1.legend(graphs, legend_labels, loc='lower left',
 		  ncol=1, fancybox=True, shadow=False, numpoints = 1)

ax2 = fig.add_axes([0.6, 0.15, 0.2, 0.2])

ax2.set_ylim(-0.1, 1.1)
ax2.set_xlim(0, 2.6)
ax2.axis('off')

x_legend	= np.arange(1, 2.51, 0.1)
ax2.fill_between(x_legend, 0, 1, color ='k', alpha = 0.2)
ax2.fill_between(x_legend, 0.25, 0.75, color = 'k', alpha = 0.2)
ax2.plot(x_legend, 0.5 + np.zeros(len(x_legend)), linestyle = '-', color = 'k', linewidth = 3.0)


ax2.text(0.2, 0,'Min', color ='k',fontsize=15,ha='right',va='center')
ax2.plot([0.22, 1], [0, 0], '--k', linewidth = 0.5)

ax2.text(0.4, 0.25, lower_per_bound+'$\%$', color ='k',fontsize=15,ha='right',va='center')
ax2.plot([0.42, 1], [0.25, 0.25], '--k', linewidth = 0.5)

ax2.text(0.6, 0.5,'Mean', color ='k',fontsize=15,ha='right',va='center')
ax2.plot([0.62, 1], [0.5, 0.5], '--k', linewidth = 0.5)

ax2.text(0.4, 0.75, higher_per_bound+'$\%$', color ='k',fontsize=15,ha='right',va='center')
ax2.plot([0.42, 1], [0.75, 0.75], '--k', linewidth = 0.5)

ax2.text(0.2, 1,'Max', color ='k',fontsize=15,ha='right',va='center')
ax2.plot([0.22, 1], [1, 1], '--k', linewidth = 0.5)

ax1.set_title('c) Ross Region')

#-----------------------------------------------------------------------------------------

fig, ax1		= subplots()

graph_CMIP6		= ax1.plot_date(time_year, np.mean(temp_3_all, axis = 0), '-k', linewidth = 2.0, label = 'CMIP6')
graph_CMIP6_HR		= ax1.plot_date(time_year, np.mean(temp_3_high, axis = 0), '--k', linewidth = 2.0, label = 'HR-CMIP6')
ax1.fill_between(time_year, np.min(temp_3_all, axis = 0), np.max(temp_3_all, axis = 0), alpha=0.2, edgecolor='k', facecolor='k')
ax1.fill_between(time_year, temp_3_all[lower_model_bound], temp_3_all[higher_model_bound], alpha=0.2, edgecolor='k', facecolor='k')

graph_HR_CESM		= ax1.plot_date(time_year, temp_3_cesm, '-r', linewidth = 2.0, label = 'HR-CESM')
graph_LR_CESM		= ax1.plot_date(time_year, temp_3_cesm_low, '-b', linewidth = 2.0, label = 'LR-CESM')	

ax1.set_xlabel('Model year')
ax1.set_ylabel('Temperature anomaly ($^{\circ}$C)')
ax1.set_ylim(-2, 2)
ax1.grid()

ax1.set_xticks([datetime.datetime(1, 1, 1).toordinal(),
		datetime.datetime(10, 1, 1).toordinal(),
		datetime.datetime(20, 1, 1).toordinal(),
		datetime.datetime(30, 1, 1).toordinal(), 
		datetime.datetime(40, 1, 1).toordinal(),
		datetime.datetime(50, 1, 1).toordinal(), 
		datetime.datetime(60, 1, 1).toordinal(),
		datetime.datetime(70, 1, 1).toordinal(),
		datetime.datetime(80, 1, 1).toordinal(),
		datetime.datetime(90, 1, 1).toordinal(),
		datetime.datetime(100, 1, 1).toordinal()])

graphs	      = graph_HR_CESM + graph_LR_CESM + graph_CMIP6 + graph_CMIP6_HR

legend_labels = [l.get_label() for l in graphs]
ax1.legend(graphs, legend_labels, loc='lower left',
 		  ncol=1, fancybox=True, shadow=False, numpoints = 1)

ax2 = fig.add_axes([0.6, 0.15, 0.2, 0.2])

ax2.set_ylim(-0.1, 1.1)
ax2.set_xlim(0, 2.6)
ax2.axis('off')

x_legend	= np.arange(1, 2.51, 0.1)
ax2.fill_between(x_legend, 0, 1, color ='k', alpha = 0.2)
ax2.fill_between(x_legend, 0.25, 0.75, color = 'k', alpha = 0.2)
ax2.plot(x_legend, 0.5 + np.zeros(len(x_legend)), linestyle = '-', color = 'k', linewidth = 3.0)


ax2.text(0.2, 0,'Min', color ='k',fontsize=15,ha='right',va='center')
ax2.plot([0.22, 1], [0, 0], '--k', linewidth = 0.5)

ax2.text(0.4, 0.25, lower_per_bound+'$\%$', color ='k',fontsize=15,ha='right',va='center')
ax2.plot([0.42, 1], [0.25, 0.25], '--k', linewidth = 0.5)

ax2.text(0.6, 0.5,'Mean', color ='k',fontsize=15,ha='right',va='center')
ax2.plot([0.62, 1], [0.5, 0.5], '--k', linewidth = 0.5)

ax2.text(0.4, 0.75, higher_per_bound+'$\%$', color ='k',fontsize=15,ha='right',va='center')
ax2.plot([0.42, 1], [0.75, 0.75], '--k', linewidth = 0.5)

ax2.text(0.2, 1,'Max', color ='k',fontsize=15,ha='right',va='center')
ax2.plot([0.22, 1], [1, 1], '--k', linewidth = 0.5)

ax1.set_title('d) Amundsen Region')
#-----------------------------------------------------------------------------------------

fig, ax1		= subplots()

graph_CMIP6		= ax1.plot_date(time_year, np.mean(temp_4_all, axis = 0), '-k', linewidth = 2.0, label = 'CMIP6')
graph_CMIP6_HR		= ax1.plot_date(time_year, np.mean(temp_4_high, axis = 0), '--k', linewidth = 2.0, label = 'HR-CMIP6')
ax1.fill_between(time_year, np.min(temp_4_all, axis = 0), np.max(temp_4_all, axis = 0), alpha=0.2, edgecolor='k', facecolor='k')
ax1.fill_between(time_year, temp_4_all[lower_model_bound], temp_4_all[higher_model_bound], alpha=0.2, edgecolor='k', facecolor='k')

graph_HR_CESM		= ax1.plot_date(time_year, temp_4_cesm, '-r', linewidth = 2.0, label = 'HR-CESM')
graph_LR_CESM		= ax1.plot_date(time_year, temp_4_cesm_low, '-b', linewidth = 2.0, label = 'LR-CESM')	

ax1.set_xlabel('Model year')
ax1.set_ylabel('Temperature anomaly ($^{\circ}$C)')
ax1.set_ylim(-2, 2)
ax1.grid()

ax1.set_xticks([datetime.datetime(1, 1, 1).toordinal(),
		datetime.datetime(10, 1, 1).toordinal(),
		datetime.datetime(20, 1, 1).toordinal(),
		datetime.datetime(30, 1, 1).toordinal(), 
		datetime.datetime(40, 1, 1).toordinal(),
		datetime.datetime(50, 1, 1).toordinal(), 
		datetime.datetime(60, 1, 1).toordinal(),
		datetime.datetime(70, 1, 1).toordinal(),
		datetime.datetime(80, 1, 1).toordinal(),
		datetime.datetime(90, 1, 1).toordinal(),
		datetime.datetime(100, 1, 1).toordinal()])

graphs	      = graph_HR_CESM + graph_LR_CESM + graph_CMIP6 + graph_CMIP6_HR

legend_labels = [l.get_label() for l in graphs]
ax1.legend(graphs, legend_labels, loc='lower left',
 		  ncol=1, fancybox=True, shadow=False, numpoints = 1)

ax2 = fig.add_axes([0.6, 0.15, 0.2, 0.2])

ax2.set_ylim(-0.1, 1.1)
ax2.set_xlim(0, 2.6)
ax2.axis('off')

x_legend	= np.arange(1, 2.51, 0.1)
ax2.fill_between(x_legend, 0, 1, color ='k', alpha = 0.2)
ax2.fill_between(x_legend, 0.25, 0.75, color = 'k', alpha = 0.2)
ax2.plot(x_legend, 0.5 + np.zeros(len(x_legend)), linestyle = '-', color = 'k', linewidth = 3.0)


ax2.text(0.2, 0,'Min', color ='k',fontsize=15,ha='right',va='center')
ax2.plot([0.22, 1], [0, 0], '--k', linewidth = 0.5)

ax2.text(0.4, 0.25, lower_per_bound+'$\%$', color ='k',fontsize=15,ha='right',va='center')
ax2.plot([0.42, 1], [0.25, 0.25], '--k', linewidth = 0.5)

ax2.text(0.6, 0.5,'Mean', color ='k',fontsize=15,ha='right',va='center')
ax2.plot([0.62, 1], [0.5, 0.5], '--k', linewidth = 0.5)

ax2.text(0.4, 0.75, higher_per_bound+'$\%$', color ='k',fontsize=15,ha='right',va='center')
ax2.plot([0.42, 1], [0.75, 0.75], '--k', linewidth = 0.5)

ax2.text(0.2, 1,'Max', color ='k',fontsize=15,ha='right',va='center')
ax2.plot([0.22, 1], [1, 1], '--k', linewidth = 0.5)

ax1.set_title('e) Weddell Region')
#-----------------------------------------------------------------------------------------

fig, ax1		= subplots()

graph_CMIP6		= ax1.plot_date(time_year, np.mean(temp_5_all, axis = 0), '-k', linewidth = 2.0, label = 'CMIP6')
graph_CMIP6_HR		= ax1.plot_date(time_year, np.mean(temp_5_high, axis = 0), '--k', linewidth = 2.0, label = 'HR-CMIP6')
ax1.fill_between(time_year, np.min(temp_5_all, axis = 0), np.max(temp_5_all, axis = 0), alpha=0.2, edgecolor='k', facecolor='k')
ax1.fill_between(time_year, temp_5_all[lower_model_bound], temp_5_all[higher_model_bound], alpha=0.2, edgecolor='k', facecolor='k')

graph_HR_CESM		= ax1.plot_date(time_year, temp_5_cesm, '-r', linewidth = 2.0, label = 'HR-CESM')
graph_LR_CESM		= ax1.plot_date(time_year, temp_5_cesm_low, '-b', linewidth = 2.0, label = 'LR-CESM')

ax1.set_xlabel('Model year')
ax1.set_ylabel('Temperature anomaly ($^{\circ}$C)')
ax1.set_ylim(-2, 2)
ax1.grid()

ax1.set_xticks([datetime.datetime(1, 1, 1).toordinal(),
		datetime.datetime(10, 1, 1).toordinal(),
		datetime.datetime(20, 1, 1).toordinal(),
		datetime.datetime(30, 1, 1).toordinal(), 
		datetime.datetime(40, 1, 1).toordinal(),
		datetime.datetime(50, 1, 1).toordinal(), 
		datetime.datetime(60, 1, 1).toordinal(),
		datetime.datetime(70, 1, 1).toordinal(),
		datetime.datetime(80, 1, 1).toordinal(),
		datetime.datetime(90, 1, 1).toordinal(),
		datetime.datetime(100, 1, 1).toordinal()])

graphs	      = graph_HR_CESM + graph_LR_CESM + graph_CMIP6 + graph_CMIP6_HR

legend_labels = [l.get_label() for l in graphs]
ax1.legend(graphs, legend_labels, loc='lower left',
 		  ncol=1, fancybox=True, shadow=False, numpoints = 1)

ax2 = fig.add_axes([0.6, 0.15, 0.2, 0.2])

ax2.set_ylim(-0.1, 1.1)
ax2.set_xlim(0, 2.6)
ax2.axis('off')

x_legend	= np.arange(1, 2.51, 0.1)
ax2.fill_between(x_legend, 0, 1, color ='k', alpha = 0.2)
ax2.fill_between(x_legend, 0.25, 0.75, color = 'k', alpha = 0.2)
ax2.plot(x_legend, 0.5 + np.zeros(len(x_legend)), linestyle = '-', color = 'k', linewidth = 3.0)


ax2.text(0.2, 0,'Min', color ='k',fontsize=15,ha='right',va='center')
ax2.plot([0.22, 1], [0, 0], '--k', linewidth = 0.5)

ax2.text(0.4, 0.25, lower_per_bound+'$\%$', color ='k',fontsize=15,ha='right',va='center')
ax2.plot([0.42, 1], [0.25, 0.25], '--k', linewidth = 0.5)

ax2.text(0.6, 0.5,'Mean', color ='k',fontsize=15,ha='right',va='center')
ax2.plot([0.62, 1], [0.5, 0.5], '--k', linewidth = 0.5)

ax2.text(0.4, 0.75, higher_per_bound+'$\%$', color ='k',fontsize=15,ha='right',va='center')
ax2.plot([0.42, 1], [0.75, 0.75], '--k', linewidth = 0.5)

ax2.text(0.2, 1,'Max', color ='k',fontsize=15,ha='right',va='center')
ax2.plot([0.22, 1], [1, 1], '--k', linewidth = 0.5)

ax1.set_title('f) Antarctic Peninsula')
show()