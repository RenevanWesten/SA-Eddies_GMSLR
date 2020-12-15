#Program determines the GMSLR contribution of Antarctica

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
directory_cesm 	        = '../../../Data/LR-CESM/'
directory_cesm_control 	= '../../../Data/LR-CESM_Control/'

def YearlyConverter(time, data, month_start = 1, month_end = 12, yearly_sum = False):
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

		if yearly_sum:
			#Take the yearly sum over the months of choice
			data_year[year_i]		= np.sum(data[year_i * 12 + month_start - 1: year_i * 12 + month_end], axis = 0)

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
temp_global	= HEAT_data.variables['TEMP'][:] 			

HEAT_data.close()

HEAT_data = netcdf.Dataset(directory_cesm_control+'Atmosphere/TEMP_2m.nc', 'r')

temp_global_control	= HEAT_data.variables['TEMP'][:] 			

HEAT_data.close()

#-----------------------------------------------------------------------------------------
HEAT_data = netcdf.Dataset(directory_cesm+'Atmosphere/TEMP_Antarctica.nc', 'r')

temp		= HEAT_data.variables['TEMP'][:] 			

HEAT_data.close()

HEAT_data = netcdf.Dataset(directory_cesm_control+'Atmosphere/TEMP_Antarctica.nc', 'r')

temp_control		= HEAT_data.variables['TEMP'][:] 			

HEAT_data.close()

#-----------------------------------------------------------------------------------------

HEAT_data = netcdf.Dataset(directory_cesm+'Atmosphere/SNOW_Antarctica.nc', 'r')

snow		= HEAT_data.variables['SNOW'][:] 

HEAT_data.close()

HEAT_data = netcdf.Dataset(directory_cesm_control+'Atmosphere/SNOW_Antarctica.nc', 'r')

snow_control	= HEAT_data.variables['SNOW'][:] 

HEAT_data.close()

#-----------------------------------------------------------------------------------------

time_year, temp_global 		= YearlyConverter(time, temp_global)
time_year, temp_global_control 	= YearlyConverter(time, temp_global_control)
time_year, temp 		= YearlyConverter(time, temp)
time_year, temp_control 	= YearlyConverter(time, temp_control)
time_year, snow			= YearlyConverter(time, snow, yearly_sum = True)
time_year, snow_control		= YearlyConverter(time, snow_control, yearly_sum = True)

temp_global	= TrendRemoverControl(time_year, temp_global_control, temp_global)
temp		= TrendRemoverControl(time_year, temp_control, temp)
snow		= TrendRemoverControl(time_year, snow_control, snow)

#Warming rate Antarctica surface temperature versus global mean surface temperature
print 'TEMP ratio:', stats.linregress(temp_global, temp)[0]

#Precipitation rate increase
print 'SNOW ratio:', stats.linregress(temp, snow / np.mean(snow_control) * 100.0)[0]

#Empty arrays
mass_loss_all		= ma.masked_all((surrogates, len(time_year)))
SLR_all			= ma.masked_all((surrogates, len(time_year)))

for surr_i in range(surrogates):

	#The increase dynamics by accumulation (i.e. snow) leads to more loss
	mass_loss		= np.random.uniform(low = 0.0, high = 0.35, size = len(time_year)) * snow
	mass_loss_all[surr_i]	= mass_loss
	
	for time_i in range(len(time_year)):
		SLR_all[surr_i, time_i]		= np.sum(mass_loss[:time_i + 1]) - np.sum(snow[:time_i + 1])

	#Convert to sea level rise equivalent
	SLR_all[surr_i]	= SLR_all[surr_i] * 1000.0 / 10**12.0 / 361.8

#Sort all the sea level rise contribution
mass_loss_all	= np.sort(mass_loss_all, axis = 0)
SLR_all		= np.sort(SLR_all, axis = 0)

#Take the percentile
mass_loss_all_per	= mass_loss_all[per_index]
SLR_all_per		= SLR_all[per_index]

#-----------------------------------------------------------------------------------------

TEMP_data = netcdf.Dataset(directory+'Ocean/SMB_Antarctica.nc', 'w')
TEMP_data.createDimension('PER_LEVELS', len(per_levels))
TEMP_data.createDimension('time', len(time_year))

TEMP_data.createVariable('time', float, ('time'), zlib=True)
TEMP_data.createVariable('PER_LEVELS', float, ('PER_LEVELS'), zlib=True)
TEMP_data.createVariable('SLR_Antarctica', float, ('PER_LEVELS', 'time'), zlib=True)

TEMP_data.variables['PER_LEVELS'].longname	= 'Percentile levels'
TEMP_data.variables['SLR_Antarctica'].longname	= 'Sea level Rise by Antarctica'

TEMP_data.variables['time'].units 		= 'Days since 0001-01-01 00:00:00 UTC'
TEMP_data.variables['PER_LEVELS'].units 	= '%'
TEMP_data.variables['SLR_Antarctica'].units 	= 'cm'

#Writing data to correct variable	
TEMP_data.variables['time'][:]     		= time_year
TEMP_data.variables['PER_LEVELS'][:] 		= per_levels
TEMP_data.variables['SLR_Antarctica'][:] 	= SLR_all_per / 10.0

TEMP_data.close()