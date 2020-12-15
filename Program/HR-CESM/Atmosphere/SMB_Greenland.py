#Program computes the surface mass balance of Greenland

from pylab import *
import numpy
import datetime
import time
import glob, os
import math
import netCDF4 as netcdf
import matplotlib.colors as colors

#Making pathway to folder with all data
directory_cesm 	        = '../../../Data/HR-CESM/'
directory_cesm_control 	= '../../../Data/HR-CESM_Control/'

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

TEMP_data = netcdf.Dataset(directory_cesm+'Atmosphere/SNOW_Greenland.nc', 'r')

time		= TEMP_data.variables['time'][:]     
snow		= TEMP_data.variables['SNOW'][:] 	

TEMP_data.close()

TEMP_data = netcdf.Dataset(directory_cesm_control+'Atmosphere/SNOW_Greenland.nc', 'r')

snow_control	= TEMP_data.variables['SNOW'][:] 	

TEMP_data.close()

#-----------------------------------------------------------------------------------------

TEMP_data = netcdf.Dataset(directory_cesm+'Atmosphere/TEMP_600_hPa_Greenland.nc', 'r')

temp		= TEMP_data.variables['TEMP'][:]

TEMP_data.close()

TEMP_data = netcdf.Dataset(directory_cesm_control+'Atmosphere/TEMP_600_hPa_Greenland.nc', 'r')

temp_control	= TEMP_data.variables['TEMP'][:]

TEMP_data.close()

#-----------------------------------------------------------------------------------------

#Total snowfall over the entire year
time_year, snow_year		= YearlyConverter(time, snow, 1, 12, yearly_sum = True)
time_year, snow_control_year	= YearlyConverter(time, snow_control, 1, 12, yearly_sum = True)

#Determine the anomaly with respect to the control simulation
snow_year			= TrendRemoverControl(time_year, snow_control_year, snow_year)

#Temperature at 600 hPa over June, Jule and August
time_year, temp_year		= YearlyConverter(time, temp, 6, 8)
time_year, temp_control_year	= YearlyConverter(time, temp_control, 6, 8)

#Determine the anomaly with respect to the control simulation
temp_year			= TrendRemoverControl(time_year, temp_control_year, temp_year)

#Set negative temperatures anomalies to zero, so melt = 0 in these cases
temp_year[temp_year < 0]	= 0.0

#-----------------------------------------------------------------------------------------

#Empty arrays
mass_loss_all		= ma.masked_all((surrogates, len(time_year)))
SLR_all			= ma.masked_all((surrogates, len(time_year)))

for surr_i in range(surrogates):
	#Melt in Gigaton and adjust for dynamics
	melt		= -(84.2 * temp_year) - (2.4 * temp_year**2.0) - (1.6 * temp_year**3.0)
	melt_dyn	= melt * np.random.uniform(low = 1.0, high = 1.15, size = len(time_year))

	#Get the total surface mass balance
	rate	= snow_year * 1000.0 / 10**12.0 + melt_dyn

	#Determine the cumulative rate
	total		= np.zeros(len(time_year))
	total[0]	= rate[0] / 361.8

	for time_i in range(1, len(time_year)):
		#Determine the cumulative rate, total sea level rise
		total[time_i]	= total[time_i - 1] + rate[time_i] / 361.8

	SLR_all[surr_i]	= -total

#-----------------------------------------------------------------------------------------

fig, ax1	= subplots()

Snow_graph	= ax1.plot_date(time_year, snow_year  * 1000.0 / 10**12.0, '-b', linewidth = 2.0, label = 'Snow')
Melt_graph	= ax1.plot_date(time_year, melt, '-r', linewidth = 2.0, label = 'Melt')
Total_graph	= ax1.plot_date(time_year, snow_year * 1000.0 / 10**12.0 + melt, '-k', linewidth = 2.0, label = 'Total')

ax1.set_xlabel('Model year')
ax1.set_ylabel('Surface mass balance anomaly (GT year$^{-1}$)')
ax1.set_ylim(-700, 200)
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

graphs	      = Snow_graph + Melt_graph + Total_graph

legend_labels = [l.get_label() for l in graphs]
ax1.legend(graphs, legend_labels, loc='lower left',
 		  ncol=1, fancybox=True, shadow=False, numpoints = 1)

ax1.set_title('a) HR-CESM')
show()

#-----------------------------------------------------------------------------------------

#Sort by surrogates
SLR_all			= np.sort(SLR_all, axis = 0)

#Take the percentile
SLR_all_per		= SLR_all[per_index]
#-----------------------------------------------------------------------------------------

TEMP_data = netcdf.Dataset(directory+'Ocean/SMB_Greenland.nc', 'w')
TEMP_data.createDimension('PER_LEVELS', len(per_levels))
TEMP_data.createDimension('time', len(time_year))

TEMP_data.createVariable('time', float, ('time'), zlib=True)
TEMP_data.createVariable('PER_LEVELS', float, ('PER_LEVELS'), zlib=True)
TEMP_data.createVariable('SLR_Greenland', float, ('PER_LEVELS', 'time'), zlib=True)

TEMP_data.variables['PER_LEVELS'].longname	= 'Percentile levels'
TEMP_data.variables['SLR_Greenland'].longname	= 'Sea level Rise by all Glaciers'

TEMP_data.variables['time'].units 		= 'Days since 0001-01-01 00:00:00 UTC'
TEMP_data.variables['PER_LEVELS'].units 	= '%'
TEMP_data.variables['SLR_Greenland'].units 	= 'cm'

#Writing data to correct variable	
TEMP_data.variables['time'][:]     		= time_year
TEMP_data.variables['PER_LEVELS'][:] 		= per_levels
TEMP_data.variables['SLR_Greenland'][:] 	= SLR_all_per / 10.0

TEMP_data.close()