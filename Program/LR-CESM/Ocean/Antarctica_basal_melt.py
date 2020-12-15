#Program determines the Antarctic basal melt

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

def TrendRemoverControl(time, control_data, data):
	"""Removes linear trend, keeps the original values"""

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

TEMP_data = netcdf.Dataset(directory+'Ocean/TEMP_Southern_Ocean_Regions.nc', 'r')

#Writing data to correct variable	
time	= TEMP_data.variables['time'][:]     	
temp	= TEMP_data.variables['TEMP'][:] 	

TEMP_data.close()

TEMP_data = netcdf.Dataset(directory+'../LR-CESM_Control/Ocean/TEMP_Southern_Ocean_Regions.nc', 'r')

#Writing data to correct variable	
time_control	= TEMP_data.variables['time'][:]     	
temp_control	= TEMP_data.variables['TEMP'][:] 	

TEMP_data.close()

#Get the model names and path
models = glob.glob(directory+'../LARMIP/RFunctions/RF*R1.dat')
models.sort()

for model_i in range(len(models)):
	#Only retain the model names
	index_start	= models[model_i].find('RF_') + 3
	index_end	= models[model_i].find('_BM08')
	models[model_i]	= models[model_i][index_start:index_end]

#-----------------------------------------------------------------------------------------

#Take yearly averages
time_year, temp_1	= YearlyConverter(time, temp[:, 0])
time_year, temp_2	= YearlyConverter(time, temp[:, 1])
time_year, temp_3	= YearlyConverter(time, temp[:, 2])
time_year, temp_4	= YearlyConverter(time, temp[:, 3])
time_year, temp_5	= YearlyConverter(time, temp[:, 4])

#Take yearly averages
time_control_year, temp_control_1	= YearlyConverter(time_control, temp_control[:, 0])
time_control_year, temp_control_2	= YearlyConverter(time_control, temp_control[:, 1])
time_control_year, temp_control_3	= YearlyConverter(time_control, temp_control[:, 2])
time_control_year, temp_control_4	= YearlyConverter(time_control, temp_control[:, 3])
time_control_year, temp_control_5	= YearlyConverter(time_control, temp_control[:, 4])

#Take the anomalies with respect to the Control simulation
temp_1		= TrendRemoverControl(time_year, temp_control_1, temp_1)
temp_2		= TrendRemoverControl(time_year, temp_control_2, temp_2)
temp_3		= TrendRemoverControl(time_year, temp_control_3, temp_3)
temp_4		= TrendRemoverControl(time_year, temp_control_4, temp_4)
temp_5		= TrendRemoverControl(time_year, temp_control_5, temp_5)

#Empty arrays for all the models
SLR_1_all	= ma.masked_all((len(models), len(per_levels), len(time_year)))
SLR_2_all	= ma.masked_all((len(models), len(per_levels), len(time_year)))
SLR_3_all	= ma.masked_all((len(models), len(per_levels), len(time_year)))
SLR_4_all	= ma.masked_all((len(models), len(per_levels), len(time_year)))
SLR_5_all	= ma.masked_all((len(models), len(per_levels), len(time_year)))
SLR_total_all	= ma.masked_all((len(models), len(per_levels), len(time_year)))

#-----------------------------------------------------------------------------------------

for model_i in range(len(models)):
	#Loop over each Ice Sheet model
	print model_i
	
	for region_i in range(1, 6):
		#Loop over each region
		filename	= directory+'../LARMIP/RFunctions/RF_'+models[model_i]+'_BM08_R'+str(region_i)+'.dat'
		
		with open(filename) as f:
			#Read in the region paramters
			exec('RF_'+str(region_i)+' = np.array([float(row) for row in f])')
		
			#Only retain the last 101 years (2000 - 2100), CESM is only forced for this period
			exec('RF_'+str(region_i)+' = RF_'+str(region_i)+'[99:]')
	
	#Empty arrays for the ensembles
	SLR_1		= ma.masked_all((surrogates, len(time_year)))
	SLR_2		= ma.masked_all((surrogates, len(time_year)))
	SLR_3		= ma.masked_all((surrogates, len(time_year)))
	SLR_4		= ma.masked_all((surrogates, len(time_year)))
	SLR_5		= ma.masked_all((surrogates, len(time_year)))
	SLR_total	= ma.masked_all((surrogates, len(time_year)))

	for surr_i in range(surrogates):

		#Basal melt
		mass_1	= np.random.uniform(low = 7.0, high = 16, size = len(time_year)) * temp_1
		mass_2	= np.random.uniform(low = 7.0, high = 16, size = len(time_year)) * temp_2
		mass_3	= np.random.uniform(low = 7.0, high = 16, size = len(time_year)) * temp_3
		mass_4	= np.random.uniform(low = 7.0, high = 16, size = len(time_year)) * temp_4
		mass_5	= np.random.uniform(low = 7.0, high = 16, size = len(time_year)) * temp_5

		#Set negative values to zero
		mass_1[mass_1 < 0]	= 0.0
		mass_2[mass_2 < 0]	= 0.0
		mass_3[mass_3 < 0]	= 0.0
		mass_4[mass_4 < 0]	= 0.0
		mass_5[mass_5 < 0]	= 0.0

		#Now determine the sea level rise
		for time_i in range(len(time_year)):
			#Take the integral
			SLR_1[surr_i, time_i]	 = np.sum(mass_1[:time_i + 1] * RF_1[:time_i + 1])
			SLR_2[surr_i, time_i]	 = np.sum(mass_2[:time_i + 1] * RF_2[:time_i + 1])
			SLR_3[surr_i, time_i]	 = np.sum(mass_3[:time_i + 1] * RF_3[:time_i + 1])
			SLR_4[surr_i, time_i]	 = np.sum(mass_4[:time_i + 1] * RF_4[:time_i + 1])
			SLR_5[surr_i, time_i]	 = np.sum(mass_5[:time_i + 1] * RF_5[:time_i + 1])
			SLR_total[surr_i, time_i]= SLR_1[surr_i, time_i] + SLR_2[surr_i, time_i] + SLR_3[surr_i, time_i] + SLR_4[surr_i, time_i] + SLR_5[surr_i, time_i]

	#Sort all the sea level rise contributions
	SLR_1		= np.sort(SLR_1, axis = 0)
	SLR_2		= np.sort(SLR_2, axis = 0)
	SLR_3		= np.sort(SLR_3, axis = 0)
	SLR_4		= np.sort(SLR_4, axis = 0)
	SLR_5		= np.sort(SLR_5, axis = 0)
	SLR_total	= np.sort(SLR_total, axis = 0)

	#Take the percentile and save the output for the corresponding model
	SLR_1_all[model_i]	= SLR_1[per_index]
	SLR_2_all[model_i]	= SLR_2[per_index]
	SLR_3_all[model_i]	= SLR_3[per_index]
	SLR_4_all[model_i]	= SLR_4[per_index]
	SLR_5_all[model_i]	= SLR_5[per_index]
	SLR_total_all[model_i]	= SLR_total[per_index]

#-----------------------------------------------------------------------------------------

TEMP_data = netcdf.Dataset(directory+'Ocean/Antarctica_basal_melt_SLR_2.nc', 'w')
TEMP_data.createDimension('PER_LEVELS', len(per_levels))
TEMP_data.createDimension('MODELS', len(models))
TEMP_data.createDimension('time', len(time_year))

TEMP_data.createVariable('time', float, ('time'), zlib=True)
TEMP_data.createVariable('MODELS', float, ('MODELS'), zlib=True)
TEMP_data.createVariable('PER_LEVELS', float, ('PER_LEVELS'), zlib=True)
TEMP_data.createVariable('SLR_1', float, ('MODELS', 'PER_LEVELS', 'time'), zlib=True)
TEMP_data.createVariable('SLR_2', float, ('MODELS', 'PER_LEVELS', 'time'), zlib=True)
TEMP_data.createVariable('SLR_3', float, ('MODELS', 'PER_LEVELS', 'time'), zlib=True)
TEMP_data.createVariable('SLR_4', float, ('MODELS', 'PER_LEVELS', 'time'), zlib=True)
TEMP_data.createVariable('SLR_5', float, ('MODELS', 'PER_LEVELS', 'time'), zlib=True)
TEMP_data.createVariable('SLR_total', float, ('MODELS', 'PER_LEVELS', 'time'), zlib=True)

TEMP_data.variables['MODELS'].longname		= 'Model names'
TEMP_data.variables['PER_LEVELS'].longname	= 'Percentile levels'
TEMP_data.variables['SLR_1'].longname		= 'Sea level Rise by East Antarctica'
TEMP_data.variables['SLR_2'].longname		= 'Sea level Rise by Ross Sea'
TEMP_data.variables['SLR_3'].longname		= 'Sea level Rise by Amundsen Sea'
TEMP_data.variables['SLR_4'].longname		= 'Sea level Rise by Weddell Region'
TEMP_data.variables['SLR_5'].longname		= 'Sea level Rise by Antarctic Peninsula'
TEMP_data.variables['SLR_total'].longname	= 'Sea level Rise by Total'

TEMP_data.variables['time'].units 		= 'Days since 0001-01-01 00:00:00 UTC'
TEMP_data.variables['PER_LEVELS'].units 	= '%'
TEMP_data.variables['SLR_1'].units 		= 'meters'
TEMP_data.variables['SLR_2'].units 		= 'meters'
TEMP_data.variables['SLR_3'].units 		= 'meters'
TEMP_data.variables['SLR_4'].units 		= 'meters'
TEMP_data.variables['SLR_5'].units 		= 'meters'
TEMP_data.variables['SLR_total'].units 		= 'meters'

#Writing data to correct variable	
TEMP_data.variables['time'][:]     		= time_year
TEMP_data.variables['MODELS'][:] 		= np.arange(len(models)) + 1
TEMP_data.variables['PER_LEVELS'][:] 		= per_levels
TEMP_data.variables['SLR_1'][:] 		= SLR_1_all
TEMP_data.variables['SLR_2'][:] 		= SLR_2_all
TEMP_data.variables['SLR_3'][:] 		= SLR_3_all
TEMP_data.variables['SLR_4'][:] 		= SLR_4_all
TEMP_data.variables['SLR_5'][:] 		= SLR_5_all
TEMP_data.variables['SLR_total'][:] 		= SLR_total_all

TEMP_data.close()