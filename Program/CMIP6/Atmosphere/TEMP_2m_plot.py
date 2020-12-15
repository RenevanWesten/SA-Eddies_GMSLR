#Program plots the 2-meter global mean surface temperature anomaly

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

def ReadinDataGMST(filename):
	"""Reads-in the data"""

	TEMP_data 	= netcdf.Dataset(filename, 'r')

	#Writing data to correct variable	
	time		= TEMP_data.variables['time'][:]     	
	temp		= TEMP_data.variables['TEMP'][:] 	

	TEMP_data.close()
		
	#Take yearly averages
	time_year, temp	= YearlyConverter(time, temp)
	
	return time_year, temp

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
	"""Remove the control simulation"""

	time		= np.arange(len(time))

	#Determine the detrended time series
	trend, base 	= polyfit(time, control_data, 1)
	data		= data - ((trend * time) + base)

	return data

#-----------------------------------------------------------------------------------------
#--------------------------------MAIN SCRIPT STARTS HERE----------------------------------
#-----------------------------------------------------------------------------------------

month_start	        = 1 	#1 = January, 2 = February, 3 = March, ..., 13 = January (+ 1), ...
month_end	        = 12	#12 = December, 13 = January (+ 1), 14 = February (+ 1), ...

lower_model_bound	= 3	#Retain the lower (and upper) sorted model for percentile levels

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
	filename_GMST		= directory_CMIP6+models[model_i]+'/Atmosphere/TEMP_2m.nc'
	filename_GMST_control	= directory_CMIP6+models[model_i]+'/Atmosphere/TEMP_2m_Control.nc'

	time_year, temp		= ReadinDataGMST(filename_GMST)
	time_year, temp_control	= ReadinDataGMST(filename_GMST_control)

	if model_i == 0:
		#First file
		temp_all		= ma.masked_all((len(models), len(time_year)))
		temp_control_all	= ma.masked_all((len(models), len(time_year)))
		temp_high		= ma.masked_all((len(models), len(time_year)))

	#Save the data for each model
	temp_all[model_i]		= TrendRemoverControl(time_year, temp_control, temp)
	temp_control_all[model_i]	= temp_control

	if models[model_i] == 'AWI-CM-1-1-MR' or models[model_i] == 'CNRM-CM6-1-HR' or models[model_i] == 'GFDL-CM4' or models[model_i] == 'GFDL-ESM4' or models[model_i] == 'MPI-ESM1-2-HR':
		#Save the data for each high-resolution model
		temp_high[model_i]	= TrendRemoverControl(time_year, temp_control, temp)

#Sort from high to low
temp_all		= np.sort(temp_all, axis = 0)
temp_control_all	= np.sort(temp_control_all, axis = 0)
#-----------------------------------------------------------------------------------------
#Get the RCP simulations
time_year_cesm, temp_GMST_cesm			= ReadinDataGMST(directory_cesm+'Atmosphere/TEMP_2m.nc')
time_year_cesm_low, temp_GMST_cesm_low 		= ReadinDataGMST(directory_cesm_low+'Atmosphere/TEMP_2m.nc')

#Get the control simulations
time_year_cesm_control, temp_GMST_cesm_control 		= ReadinDataGMST(directory_cesm_control+'Atmosphere/TEMP_2m.nc')
time_year_cesm_control, temp_GMST_cesm_control		= time_year_cesm_control[199:], temp_GMST_cesm_control[199:]
time_year_cesm_low_control, temp_GMST_cesm_low_control 	= ReadinDataGMST(directory_cesm_low_control+'Atmosphere/TEMP_2m.nc')

#Remove control
temp_GMST_cesm		= TrendRemoverControl(time_year_cesm, temp_GMST_cesm_control, temp_GMST_cesm)
temp_GMST_cesm_low	= TrendRemoverControl(time_year_cesm_low, temp_GMST_cesm_low_control, temp_GMST_cesm_low)
#-----------------------------------------------------------------------------------------

fig, ax1		= subplots()

graph_CMIP6		= ax1.plot_date(time_year, np.mean(temp_all, axis = 0), '-k', linewidth = 2.0, label = 'CMIP6')
graph_CMIP6_HR		= ax1.plot_date(time_year, np.mean(temp_high, axis = 0), '--k', linewidth = 2.0, label = 'HR-CMIP6')
ax1.fill_between(time_year, np.min(temp_all, axis = 0), np.max(temp_all, axis = 0), alpha=0.2, edgecolor='k', facecolor='k')
ax1.fill_between(time_year, temp_all[lower_model_bound], temp_all[higher_model_bound], alpha=0.2, edgecolor='k', facecolor='k')

graph_HR_CESM		= ax1.plot_date(time_year, temp_GMST_cesm, '-r', linewidth = 2.0, label = 'HR-CESM')
graph_LR_CESM		= ax1.plot_date(time_year, temp_GMST_cesm_low, '-b', linewidth = 2.0, label = 'LR-CESM')

ax1.set_xlabel('Model year')
ax1.set_ylabel('Temperature anomaly ($^{\circ}$C)')
ax1.set_ylim(-5, 5)
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

ax1.set_title('a) Global mean surface temperature')

#-----------------------------------------------------------------------------------------

fig, ax1		= subplots()

graph_CMIP6		= ax1.plot_date(time_year, np.mean(temp_control_all, axis = 0), '-k', linewidth = 2.0, label = 'CMIP6 Control')
ax1.fill_between(time_year, np.min(temp_control_all, axis = 0), np.max(temp_control_all, axis = 0), alpha=0.2, edgecolor='k', facecolor='k')
ax1.fill_between(time_year, temp_control_all[lower_model_bound], temp_control_all[higher_model_bound], alpha=0.2, edgecolor='k', facecolor='k')

graph_HR_CESM		= ax1.plot_date(time_year, temp_GMST_cesm_control, '-r', linewidth = 2.0, label = 'HR-CESM Control')
graph_LR_CESM		= ax1.plot_date(time_year, temp_GMST_cesm_low_control, '-b', linewidth = 2.0, label = 'LR-CESM Control')

ax1.set_xlabel('Model year')
ax1.set_ylabel('Temperature ($^{\circ}$C)')
ax1.set_ylim(12, 17.5)
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

graphs	      = graph_HR_CESM + graph_LR_CESM + graph_CMIP6

legend_labels = [l.get_label() for l in graphs]
ax1.legend(graphs, legend_labels, loc='upper left',
 		  ncol=1, fancybox=True, shadow=False, numpoints = 1)

ax2 = fig.add_axes([0.6, 0.65, 0.2, 0.2])

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

ax1.set_title('a) Global mean surface temperature')
show()