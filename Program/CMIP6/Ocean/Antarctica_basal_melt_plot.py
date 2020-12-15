#Program plots the Antarctic basal melt for the HR-CESM, LR-CESM and CMIP6

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
directory_CMIP6      = '../../../Data/CMIP6/'
directory_cesm       = '../../../Data/HR-CESM/'
directory_cesm_low   = '../../../Data/LR-CESM/'

def ReadinData(filename):
	"""Reads-in the data"""

	TEMP_data 	= netcdf.Dataset(filename, 'r')

	#Writing data to correct variable	
	time		= TEMP_data.variables['time'][:]  
	per_levels	= TEMP_data.variables['PER_LEVELS'][:] 
	SLR_1		= TEMP_data.variables['SLR_1'][:] * 100.0	
	SLR_2		= TEMP_data.variables['SLR_2'][:] * 100.0	
	SLR_3		= TEMP_data.variables['SLR_3'][:] * 100.0 		
	SLR_4		= TEMP_data.variables['SLR_4'][:] * 100.0		
	SLR_5		= TEMP_data.variables['SLR_5'][:] * 100.0	
	SLR_total	= TEMP_data.variables['SLR_total'][:] * 100.0	

	TEMP_data.close()

	#Take the LARMIP model mean
	SLR_1		= np.mean(SLR_1, axis = 0)
	SLR_2		= np.mean(SLR_2, axis = 0)
	SLR_3		= np.mean(SLR_3, axis = 0)
	SLR_4		= np.mean(SLR_4, axis = 0)
	SLR_5		= np.mean(SLR_5, axis = 0)
	SLR_total	= np.mean(SLR_total, axis = 0)

	#Return the 50% percentile level
	return time, SLR_1[7], SLR_2[7], SLR_3[7], SLR_4[7], SLR_5[7], SLR_total[7]

#-----------------------------------------------------------------------------------------
#--------------------------------MAIN SCRIPT STARTS HERE----------------------------------
#-----------------------------------------------------------------------------------------

lower_model_bound	= 3 #Retain the lower (and upper) sorted model for percentile levels

#-----------------------------------------------------------------------------------------
	
#Get the model names and path
models = glob.glob(directory_CMIP6+'*')
models.sort()

for model_i in range(len(models)):
	#Only retain the model names
	models[model_i]	= models[model_i][len(directory_CMIP6):]

higher_model_bound	= len(models) - lower_model_bound
lower_per_bound		= lower_model_bound / float(len(models) - 1) * 100.0
lower_per_bound		= str(int(np.round(lower_per_bound, 0)))
higher_per_bound	= str(100 - int(lower_per_bound))

for model_i in range(len(models)):
	#For each model get the all the files
	filename	= directory_CMIP6+models[model_i]+'/Ocean/Antarctica_basal_melt_SLR.nc'
	
	time_year, SLR_1, SLR_2, SLR_3, SLR_4, SLR_5, SLR_total = ReadinData(filename)

	if model_i == 0:
		#First file
		SLR_1_all	= ma.masked_all((len(models), len(time_year)))
		SLR_2_all	= ma.masked_all((len(models), len(time_year)))
		SLR_3_all	= ma.masked_all((len(models), len(time_year)))
		SLR_4_all	= ma.masked_all((len(models), len(time_year)))
		SLR_5_all	= ma.masked_all((len(models), len(time_year)))
		SLR_total_all	= ma.masked_all((len(models), len(time_year)))

		SLR_1_high	= ma.masked_all((len(models), len(time_year)))
		SLR_2_high	= ma.masked_all((len(models), len(time_year)))
		SLR_3_high	= ma.masked_all((len(models), len(time_year)))
		SLR_4_high	= ma.masked_all((len(models), len(time_year)))
		SLR_5_high	= ma.masked_all((len(models), len(time_year)))
		SLR_total_high	= ma.masked_all((len(models), len(time_year)))

	#Save the data for each model
	SLR_1_all[model_i]	= SLR_1
	SLR_2_all[model_i]	= SLR_2
	SLR_3_all[model_i]	= SLR_3
	SLR_4_all[model_i]	= SLR_4
	SLR_5_all[model_i]	= SLR_5
	SLR_total_all[model_i]	= SLR_total

	if models[model_i] == 'AWI-CM-1-1-MR' or models[model_i] == 'CNRM-CM6-1-HR' or models[model_i] == 'GFDL-CM4' or models[model_i] == 'GFDL-ESM4' or models[model_i] == 'MPI-ESM1-2-HR':
		#Save the data for each high-resolution model (< 50 km)
		SLR_1_high[model_i]	= SLR_1
		SLR_2_high[model_i]	= SLR_2
		SLR_3_high[model_i]	= SLR_3
		SLR_4_high[model_i]	= SLR_4
		SLR_5_high[model_i]	= SLR_5
		SLR_total_high[model_i]	= SLR_total

#Sort from high to low
SLR_1_all	= np.sort(SLR_1_all, axis = 0)
SLR_2_all	= np.sort(SLR_2_all, axis = 0)
SLR_3_all	= np.sort(SLR_3_all, axis = 0)
SLR_4_all	= np.sort(SLR_4_all, axis = 0)
SLR_5_all	= np.sort(SLR_5_all, axis = 0)
SLR_total_all	= np.sort(SLR_total_all, axis = 0)

#-----------------------------------------------------------------------------------------

time_year_cesm, SLR_1_cesm, SLR_2_cesm, SLR_3_cesm, SLR_4_cesm, SLR_5_cesm, SLR_total_cesm = ReadinData(directory_cesm+'Ocean/Antarctica_basal_melt_SLR.nc')
time_year_cesm_low, SLR_1_cesm_low, SLR_2_cesm_low, SLR_3_cesm_low, SLR_4_cesm_low, SLR_5_cesm_low, SLR_total_cesm_low = ReadinData(directory_cesm_low+'Ocean/Antarctica_basal_melt_SLR.nc')

#-----------------------------------------------------------------------------------------

fig, ax1		= subplots()

graph_CMIP6		= ax1.plot_date(time_year, np.mean(SLR_total_all, axis = 0), '-k', linewidth = 2.0, label = 'CMIP6')
graph_CMIP6_HR		= ax1.plot_date(time_year, np.mean(SLR_total_high, axis = 0), '--k', linewidth = 2.0, label = 'HR-CMIP6')
ax1.fill_between(time_year, np.min(SLR_total_all, axis = 0), np.max(SLR_total_all, axis = 0), alpha=0.2, edgecolor='k', facecolor='k')
ax1.fill_between(time_year, SLR_total_all[lower_model_bound], SLR_total_all[higher_model_bound], alpha=0.2, edgecolor='k', facecolor='k')

graph_HR_CESM		= ax1.plot_date(time_year, SLR_total_cesm, '-r', linewidth = 2.0, label = 'HR-CESM')
graph_LR_CESM		= ax1.plot_date(time_year, SLR_total_cesm_low, '-b', linewidth = 2.0, label = 'LR-CESM')	

ax1.set_xlabel('Model year')
ax1.set_ylabel('Global mean sea-level rise (cm)')
ax1.set_ylim(-2, 40)
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
legend_1	= ax1.legend(graphs, legend_labels, loc='upper left', ncol=1, fancybox=True, shadow=False, numpoints = 1)

ax2 = fig.add_axes([0.2, 0.4, 0.2, 0.2])

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

ax1.set_title('a) Total')
#-----------------------------------------------------------------------------------------

fig, ax1		= subplots()

graph_CMIP6		= ax1.plot_date(time_year, np.mean(SLR_1_all, axis = 0), '-k', linewidth = 2.0, label = 'CMIP6')
graph_CMIP6_HR		= ax1.plot_date(time_year, np.mean(SLR_1_high, axis = 0), '--k', linewidth = 2.0, label = 'HR-CMIP6')
ax1.fill_between(time_year, np.min(SLR_1_all, axis = 0), np.max(SLR_1_all, axis = 0), alpha=0.2, edgecolor='k', facecolor='k')
ax1.fill_between(time_year, SLR_1_all[lower_model_bound], SLR_1_all[higher_model_bound], alpha=0.2, edgecolor='k', facecolor='k')

graph_HR_CESM		= ax1.plot_date(time_year, SLR_1_cesm, '-r', linewidth = 2.0, label = 'HR-CESM')
graph_LR_CESM		= ax1.plot_date(time_year, SLR_1_cesm_low, '-b', linewidth = 2.0, label = 'LR-CESM')	

ax1.set_xlabel('Model year')
ax1.set_ylabel('Global mean sea-level rise (cm)')
ax1.set_ylim(-0.3, 6)
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
ax1.legend(graphs, legend_labels, loc='upper left',
 		  ncol=1, fancybox=True, shadow=False, numpoints = 1)

ax2 = fig.add_axes([0.2, 0.4, 0.2, 0.2])

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

graph_CMIP6		= ax1.plot_date(time_year, np.mean(SLR_2_all, axis = 0), '-k', linewidth = 2.0, label = 'CMIP6')
graph_CMIP6_HR		= ax1.plot_date(time_year, np.mean(SLR_2_high, axis = 0), '--k', linewidth = 2.0, label = 'HR-CMIP6')
ax1.fill_between(time_year, np.min(SLR_2_all, axis = 0), np.max(SLR_2_all, axis = 0), alpha=0.2, edgecolor='k', facecolor='k')
ax1.fill_between(time_year, SLR_2_all[lower_model_bound], SLR_2_all[higher_model_bound], alpha=0.2, edgecolor='k', facecolor='k')

graph_HR_CESM		= ax1.plot_date(time_year, SLR_2_cesm, '-r', linewidth = 2.0, label = 'HR-CESM')
graph_LR_CESM		= ax1.plot_date(time_year, SLR_2_cesm_low, '-b', linewidth = 2.0, label = 'LR-CESM')	

ax1.set_xlabel('Model year')
ax1.set_ylabel('Global mean sea-level rise (cm)')
ax1.set_ylim(-0.5, 10)
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
ax1.legend(graphs, legend_labels, loc='upper left',
 		  ncol=1, fancybox=True, shadow=False, numpoints = 1)

ax2 = fig.add_axes([0.2, 0.4, 0.2, 0.2])

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

graph_CMIP6		= ax1.plot_date(time_year, np.mean(SLR_3_all, axis = 0), '-k', linewidth = 2.0, label = 'CMIP6')
graph_CMIP6_HR		= ax1.plot_date(time_year, np.mean(SLR_3_high, axis = 0), '--k', linewidth = 2.0, label = 'HR-CMIP6')
ax1.fill_between(time_year, np.min(SLR_3_all, axis = 0), np.max(SLR_3_all, axis = 0), alpha=0.2, edgecolor='k', facecolor='k')
ax1.fill_between(time_year, SLR_3_all[lower_model_bound], SLR_3_all[higher_model_bound], alpha=0.2, edgecolor='k', facecolor='k')

graph_HR_CESM		= ax1.plot_date(time_year, SLR_3_cesm, '-r', linewidth = 2.0, label = 'HR-CESM')
graph_LR_CESM		= ax1.plot_date(time_year, SLR_3_cesm_low, '-b', linewidth = 2.0, label = 'LR-CESM')	

ax1.set_xlabel('Model year')
ax1.set_ylabel('Global mean sea-level rise (cm)')
ax1.set_ylim(-0.2, 4)
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
ax1.legend(graphs, legend_labels, loc='upper left',
 		  ncol=1, fancybox=True, shadow=False, numpoints = 1)

ax2 = fig.add_axes([0.2, 0.4, 0.2, 0.2])

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

graph_CMIP6		= ax1.plot_date(time_year, np.mean(SLR_4_all, axis = 0), '-k', linewidth = 2.0, label = 'CMIP6')
graph_CMIP6_HR		= ax1.plot_date(time_year, np.mean(SLR_4_high, axis = 0), '--k', linewidth = 2.0, label = 'HR-CMIP6')
ax1.fill_between(time_year, np.min(SLR_4_all, axis = 0), np.max(SLR_4_all, axis = 0), alpha=0.2, edgecolor='k', facecolor='k')
ax1.fill_between(time_year, SLR_4_all[lower_model_bound], SLR_4_all[higher_model_bound], alpha=0.2, edgecolor='k', facecolor='k')

graph_HR_CESM		= ax1.plot_date(time_year, SLR_4_cesm, '-r', linewidth = 2.0, label = 'HR-CESM')
graph_LR_CESM		= ax1.plot_date(time_year, SLR_4_cesm_low, '-b', linewidth = 2.0, label = 'LR-CESM')	

ax1.set_xlabel('Model year')
ax1.set_ylabel('Global mean sea-level rise (cm)')
ax1.set_ylim(-1.5, 30)
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
ax1.legend(graphs, legend_labels, loc='upper left',
 		  ncol=1, fancybox=True, shadow=False, numpoints = 1)

ax2 = fig.add_axes([0.2, 0.4, 0.2, 0.2])

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

graph_CMIP6		= ax1.plot_date(time_year, np.mean(SLR_5_all, axis = 0), '-k', linewidth = 2.0, label = 'CMIP6')
graph_CMIP6_HR		= ax1.plot_date(time_year, np.mean(SLR_5_high, axis = 0), '--k', linewidth = 2.0, label = 'HR-CMIP6')
ax1.fill_between(time_year, np.min(SLR_5_all, axis = 0), np.max(SLR_5_all, axis = 0), alpha=0.2, edgecolor='k', facecolor='k')
ax1.fill_between(time_year, SLR_5_all[lower_model_bound], SLR_5_all[higher_model_bound], alpha=0.2, edgecolor='k', facecolor='k')

graph_HR_CESM		= ax1.plot_date(time_year, SLR_5_cesm, '-r', linewidth = 2.0, label = 'HR-CESM')
graph_LR_CESM		= ax1.plot_date(time_year, SLR_5_cesm_low, '-b', linewidth = 2.0, label = 'LR-CESM')	

ax1.set_xlabel('Model year')
ax1.set_ylabel('Global mean sea-level rise (cm)')
ax1.set_ylim(-0.1, 2)
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
ax1.legend(graphs, legend_labels, loc='upper left',
 		  ncol=1, fancybox=True, shadow=False, numpoints = 1)

ax2 = fig.add_axes([0.2, 0.4, 0.2, 0.2])

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