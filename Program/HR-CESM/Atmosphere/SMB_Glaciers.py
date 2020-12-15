#Program computes the surface mass balance of all the glaciers

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
directory_cesm 	        = '../../../Data/HR-CESM/'
directory_cesm_control 	= '../../../Data/HR-CESM_Control/'

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

def TrendRemoverControl(time, control_data, data):
	"""Removes trend from Control simulation"""

	time		= np.arange(len(time))

	#Determine the detrended time series
	trend, base 	= polyfit(time, control_data, 1)
	data		= data - ((trend * time) + base)

	return data

#-----------------------------------------------------------------------------------------
#--------------------------------MAIN SCRIPT STARTS HERE----------------------------------
#-----------------------------------------------------------------------------------------

surrogates	= 2500

#The percentile levels
per_levels	= np.asarray([0.0, 0.5, 1.0, 2.5, 5.0, 10.0, 25.0, 50.0, 75.0, 90.0, 95.0, 97.5, 99.0, 99.5, 100])

#Convert to index
per_index	= (per_levels * surrogates / 100.0).astype(int)
per_index[-1]	= surrogates - 1

#-----------------------------------------------------------------------------------------

HEAT_data = netcdf.Dataset(directory_cesm+'Atmosphere/TEMP_2m.nc', 'r')

time		= HEAT_data.variables['time'][:] 			
temp		= HEAT_data.variables['TEMP'][:] 			

HEAT_data.close()

HEAT_data = netcdf.Dataset(directory_cesm_control+'Atmosphere/TEMP_2m.nc', 'r')

#Only get model year 200 - 300 (i.e. HR-CESM Control)
temp_control	= HEAT_data.variables['TEMP'][2388:3600] 			

HEAT_data.close()

#Take yearly averges and retain anomalies with respect to control simulation 
time_year, temp 	= YearlyConverter(time, temp)
time_year, temp_control = YearlyConverter(time, temp_control)
temp			= TrendRemoverControl(time_year, temp_control, temp)

#-----------------------------------------------------------------------------------------

#Set negative temperature anomalies to zero for the integration
temp[temp < 0]	= 0.0

temp_integral	= np.zeros(len(time_year))
temp_variance	= np.zeros(len(time_year))
glaciers_1_all	= ma.masked_all((surrogates, len(time_year)))
glaciers_2_all	= ma.masked_all((surrogates, len(time_year)))
glaciers_3_all	= ma.masked_all((surrogates, len(time_year)))
glaciers_4_all	= ma.masked_all((surrogates, len(time_year)))
glaciers_all	= ma.masked_all((4, surrogates, len(time_year)))

for time_i in range(len(time_year)):
	temp_integral[time_i]	= np.sum(temp[:time_i + 1])
	temp_variance[time_i]	= 0.20 * temp_integral[time_i]

for surr_i in range(surrogates):
	#Loop over each surrogate
	temp_surrogate	= np.random.normal(loc = temp_integral, scale = temp_variance)

	glaciers_1_all[surr_i]	= 3.02 * (temp_surrogate)**0.733
	glaciers_2_all[surr_i]	= 4.96 * (temp_surrogate)**0.685
	glaciers_3_all[surr_i]	= 5.45 * (temp_surrogate)**0.676
	glaciers_4_all[surr_i]	= 3.44 * (temp_surrogate)**0.742

	glaciers_all[0, surr_i]	= 3.02 * (temp_surrogate)**0.733
	glaciers_all[1, surr_i]	= 4.96 * (temp_surrogate)**0.685
	glaciers_all[2, surr_i]	= 5.45 * (temp_surrogate)**0.676
	glaciers_all[3, surr_i]	= 3.44 * (temp_surrogate)**0.742

#-----------------------------------------------------------------------------------------
#Take the model mean
glaciers_all	= np.mean(glaciers_all, axis = 0)

#Sort by surrogates
glaciers_all	= np.sort(glaciers_all, axis = 0)

#Take the percentile
glaciers_all_per	= glaciers_all[per_index]

#-----------------------------------------------------------------------------------------

TEMP_data = netcdf.Dataset(directory+'Ocean/SMB_Glaciers.nc', 'w')
TEMP_data.createDimension('PER_LEVELS', len(per_levels))
TEMP_data.createDimension('time', len(time_year))

TEMP_data.createVariable('time', float, ('time'), zlib=True)
TEMP_data.createVariable('PER_LEVELS', float, ('PER_LEVELS'), zlib=True)
TEMP_data.createVariable('SLR_Glaciers', float, ('PER_LEVELS', 'time'), zlib=True)

TEMP_data.variables['PER_LEVELS'].longname	= 'Percentile levels'
TEMP_data.variables['SLR_Glaciers'].longname	= 'Sea level Rise by all Glaciers'

TEMP_data.variables['time'].units 		= 'Days since 0001-01-01 00:00:00 UTC'
TEMP_data.variables['PER_LEVELS'].units 	= '%'
TEMP_data.variables['SLR_Glaciers'].units 	= 'cm'

#Writing data to correct variable	
TEMP_data.variables['time'][:]     		= time_year
TEMP_data.variables['PER_LEVELS'][:] 		= per_levels
TEMP_data.variables['SLR_Glaciers'][:] 		= glaciers_all_per / 10.0

TEMP_data.close()