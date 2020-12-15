#Program determines the correlation between the GMST anomaly and SO regions

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

def TrendRemover(time, data, trend_type):
	"""Removes trend of choice"""
	
	rank = polyfit(time, data, trend_type)
	fitting = 0.0 
		
	for rank_i in range(len(rank)):
			
		fitting += rank[rank_i] * (time**(len(rank) - 1 - rank_i))

	data -= fitting
	
	return data

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

def CorrelationLag(series_1, series_2, lag_length = 50, name_series_1 = 'Series 1', Plot = True):
	"""Returns the correlation coefficient while lagging both series to each other
	time can be selected and is by default 50 time units"""
	
	lag_1, lag_2 = [], []
	correlation_1, correlation_2 = [], []
	trend_1, trend_2 = [], []
	error_low_1, error_high_1, error_low_2, error_high_2 = [], [], [], []

	for lag_i in range(lag_length+1): #Lagging the time series in both directions
		correlation_1.append(np.corrcoef(series_1[:len(series_1)-lag_i],series_2[lag_i:])[0][1])
		lag_1.append(lag_i)
		correlation_2.append(np.corrcoef(series_2[:len(series_2)-lag_i],series_1[lag_i:])[0][1])
		lag_2.append(-lag_i)

		#Determine trend
		trend, base 	= polyfit(series_1[:len(series_1)-lag_i],series_2[lag_i:], 1)
		trend_1.append(trend)
		trend, base 	= polyfit(series_2[:len(series_2)-lag_i],series_1[lag_i:], 1)
		trend_2.append(trend)
		
		#Determine errors on correlation
		low, high = FisherTransformation(correlation_1[-1], len(series_1[:len(series_1)-lag_i]))
		error_low_1.append(correlation_1[-1] - low), error_high_1.append(high - correlation_1[-1])
		low, high = FisherTransformation(correlation_2[-1], len(series_2[:len(series_2)-lag_i]))
		error_low_2.append(correlation_2[-1] - low), error_high_2.append(high - correlation_2[-1])
	
	#Pasting the time series together where lag = 0 is removed from one series (double)
	lag, correlation, error_low, error_high, trend =  lag_2[::-1][:-1] + lag_1, correlation_2[::-1][:-1] + correlation_1, error_low_2[::-1][:-1] + error_low_1, error_high_2[::-1][:-1] + error_high_1, trend_2[::-1][:-1] + trend_1
	
	if Plot == False:
		return np.asarray(lag), np.asarray(correlation), np.asarray(error_low), np.asarray(error_high)

	print 'Correlation between the time series'
	print '		Lag 		=', lag[len(lag) - lag_length - 1]
	print '		Correlation 	=', correlation[len(lag) - lag_length - 1]
	print '		Lower error	=', error_low[len(lag) - lag_length - 1]
	print '		Upper error	=', error_high[len(lag) - lag_length - 1]
	print '         Trend           =', trend[len(lag) - lag_length - 1]

	print
	print 'Maximum correlation between the time series'
	print '		Lag 		=', lag[argmax(correlation)]
	print '		Correlation 	=', correlation[argmax(correlation)]
	print '		Lower error	=', error_low[argmax(correlation)]
	print '		Upper error	=', error_high[argmax(correlation)]
	print '         Trend           =', trend[argmax(correlation)]

	print
	print 'Minimum correlation between the time series'
	print '		Lag 		=', lag[argmin(correlation)]
	print '		Correlation 	=', correlation[argmin(correlation)]
	print '		Lower error	=', error_low[argmin(correlation)]
	print '		Upper error	=', error_high[argmin(correlation)]
	print '         Trend           =', trend[argmin(correlation)]

	return 0, 0, 0

	bottom, height 	= -0.95, 2.0
	middle		= 0
	left		= -1.0/3.0 * max(lag)
	right		= 1.0/25.0 * max(lag)

	axvline(x=0,color='k',ls='dashed')
	axhline(y=0,color='k',ls='dashed')

	text(right, bottom, name_series_1+' leads', horizontalalignment='left',verticalalignment='bottom')
	text(left, bottom, name_series_1+' lags',horizontalalignment='left',verticalalignment='bottom')		

	plot(lag, correlation, '-r', linewidth = 2.0)
	fill_between(lag, np.asarray(correlation) - np.asarray(error_low), np.asarray(correlation) + np.asarray(error_high), alpha=0.4, edgecolor='r', facecolor='r')	

	xlabel('Lag (months)')
	ylabel("Correlation coefficient")
	ylim([-1, 1])

	show()

def FisherTransformation(correlation, size_length):
	"""Determines error on correlation coefficient"""
	
	z = 0.5 * log((1.0 + correlation) / (1.0 - correlation)) #Fisher transformation
	
	error = 1.0/(sqrt(size_length - 3.0)) #Standard error

	err_low, err_up = z - 1.96 * error, z + 1.96 * error #95 Confidence interval
	
	err_low = (e**(2.0 * err_low) - 1.0) / (e**(2.0 * err_low) + 1.0) #Fisher inverse transformation
	err_up = (e**(2.0 * err_up) - 1.0) / (e**(2.0 * err_up) + 1.0)
	
	return err_low, err_up

def SignificanceCorrelationLag(series_1, series_2, lag_length = 50, name_series_1 = 'Series 1'):
	#Computes the significance of the lag

	lag, corr, corr_low, corr_high = CorrelationLag(series_1, series_2, lag_length, name_series_1, Plot = False)

	#Make empty array's to keep track of your significant lag
	significance_level 	= ma.masked_all(len(lag))
	
	for lag_i in range(len(lag)):

		#First determine the auto-correlation for each time series
		auto_lag	= np.arange(30)
		auto_corr_1	= np.zeros(30)
		auto_corr_2	= np.zeros(30)

		for lag_j in range(len(auto_lag)):

			if lag[lag_i] < 0:
				#If series 2 leads series 1
				auto_series_1	= series_1[-lag[lag_i]:] #Lag is negative, adjust with minus
				auto_series_2 	= series_2[:len(series_2) + lag[lag_i]]

			else:
				#If series 1 leads series 2
				auto_series_1	= series_1[:len(series_1) - lag[lag_i]]
				auto_series_2 	= series_2[lag[lag_i]:]

			#Remove quadratic trend for determining the degrees of freedom
			auto_series_1	= TrendRemover(np.arange(len(auto_series_1)), auto_series_1, 2)
			auto_series_2	= TrendRemover(np.arange(len(auto_series_2)), auto_series_2, 2)

			#Determine the auto-correlation
			auto_corr_1[lag_j] = np.corrcoef(auto_series_1[0:len(auto_series_1)-lag_j], auto_series_1[lag_j:])[0][1]
			auto_corr_2[lag_j] = np.corrcoef(auto_series_2[0:len(auto_series_2)-lag_j], auto_series_2[lag_j:])[0][1]

		#Determine the e-folding time for each time series and keep the maximum
		e_1	= np.where(auto_corr_1 < 1.0/np.e)[0][0]
		e_2	= np.where(auto_corr_2 < 1.0/np.e)[0][0]
		e_max	= max(e_1, e_2)

		#Determine the degrees of freedom and corresponding critical value
		dof	= len(auto_series_1) / e_max
		t_crit 	= stats.t.ppf(1 - 0.05, dof - 2)

		#Determine the minimum correlation to exceed the critical value
		corr_min 			= t_crit * np.sqrt( 1.0 / (dof - 2.0 + t_crit**2.0))
		significance_level[lag_i]	= corr_min

	return lag, corr, significance_level

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

month_start	= 1 	#1 = January, 2 = February, 3 = March, ..., 13 = January (+ 1), ...
month_end	= 12	#12 = December, 13 = January (+ 1), 14 = February (+ 1), ...

#-----------------------------------------------------------------------------------------


TEMP_data = netcdf.Dataset(directory_cesm+'Ocean/TEMP_Southern_Ocean_Regions.nc', 'r')

#Writing data to correct variable	
time	              = TEMP_data.variables['time'][:]     	
temp_cesm             = TEMP_data.variables['TEMP'][:] 	

TEMP_data.close()

TEMP_data = netcdf.Dataset(directory_cesm_control+'/Ocean/TEMP_Southern_Ocean_Regions.nc', 'r')

#Writing data to correct variable	
temp_cesm_control	= TEMP_data.variables['TEMP'][:] 	

TEMP_data.close()
#-----------------------------------------------------------------------------------------

TEMP_data = netcdf.Dataset(directory_cesm_low+'Ocean/TEMP_Southern_Ocean_Regions.nc', 'r')

#Writing data to correct variable	
temp_cesm_low	        = TEMP_data.variables['TEMP'][:] 	

TEMP_data.close()

TEMP_data = netcdf.Dataset(directory_cesm_low_control+'/Ocean/TEMP_Southern_Ocean_Regions.nc', 'r')

#Writing data to correct variable	
temp_cesm_low_control	= TEMP_data.variables['TEMP'][:] 	

TEMP_data.close()

#-----------------------------------------------------------------------------------------

HEAT_data = netcdf.Dataset(directory_cesm+'Atmosphere/TEMP_2m.nc', 'r')

temp_global_cesm		= HEAT_data.variables['TEMP'][:] 			

HEAT_data.close()

HEAT_data = netcdf.Dataset(directory_cesm_control+'Atmosphere/TEMP_2m.nc', 'r')

#Only get the relevant years (i.e. 200 - 300 (or 2000 - 2100))
temp_global_cesm_control	= HEAT_data.variables['TEMP'][2388:3600] 			

HEAT_data.close()

#-----------------------------------------------------------------------------------------

HEAT_data = netcdf.Dataset(directory_cesm_low+'Atmosphere/TEMP_2m.nc', 'r')

temp_global_cesm_low	= HEAT_data.variables['TEMP'][:] 			

HEAT_data.close()

HEAT_data = netcdf.Dataset(directory_cesm_low_control+'Atmosphere/TEMP_2m.nc', 'r')

temp_global_cesm_low_control	= HEAT_data.variables['TEMP'][:] 			

HEAT_data.close()

#-----------------------------------------------------------------------------------------

#Take yearly averages
time_year, temp_1_cesm		= YearlyConverter(time, temp_cesm[:, 0])
time_year, temp_2_cesm		= YearlyConverter(time, temp_cesm[:, 1])
time_year, temp_3_cesm		= YearlyConverter(time, temp_cesm[:, 2])
time_year, temp_4_cesm		= YearlyConverter(time, temp_cesm[:, 3])
time_year, temp_5_cesm		= YearlyConverter(time, temp_cesm[:, 4])
time_year, temp_global_cesm	= YearlyConverter(time, temp_global_cesm)

#Take yearly averages
time_year, temp_1_cesm_control		= YearlyConverter(time, temp_cesm_control[:, 0])
time_year, temp_2_cesm_control		= YearlyConverter(time, temp_cesm_control[:, 1])
time_year, temp_3_cesm_control		= YearlyConverter(time, temp_cesm_control[:, 2])
time_year, temp_4_cesm_control		= YearlyConverter(time, temp_cesm_control[:, 3])
time_year, temp_5_cesm_control		= YearlyConverter(time, temp_cesm_control[:, 4])
time_year, temp_global_cesm_control	= YearlyConverter(time, temp_global_cesm_control)

#Take the anomalies with respect to the control simulation
temp_1_cesm		= TrendRemoverControl(time_year, temp_1_cesm_control, temp_1_cesm)
temp_2_cesm		= TrendRemoverControl(time_year, temp_2_cesm_control, temp_2_cesm)
temp_3_cesm		= TrendRemoverControl(time_year, temp_3_cesm_control, temp_3_cesm)
temp_4_cesm		= TrendRemoverControl(time_year, temp_4_cesm_control, temp_4_cesm)
temp_5_cesm		= TrendRemoverControl(time_year, temp_5_cesm_control, temp_5_cesm)
temp_global_cesm	= TrendRemoverControl(time_year, temp_global_cesm_control, temp_global_cesm)

#-----------------------------------------------------------------------------------------

#Take yearly averages
time_year, temp_1_cesm_low		= YearlyConverter(time, temp_cesm_low[:, 0])
time_year, temp_2_cesm_low		= YearlyConverter(time, temp_cesm_low[:, 1])
time_year, temp_3_cesm_low		= YearlyConverter(time, temp_cesm_low[:, 2])
time_year, temp_4_cesm_low		= YearlyConverter(time, temp_cesm_low[:, 3])
time_year, temp_5_cesm_low		= YearlyConverter(time, temp_cesm_low[:, 4])
time_year, temp_global_cesm_low	        = YearlyConverter(time, temp_global_cesm_low)

#Take yearly averages
time_year, temp_1_cesm_low_control	= YearlyConverter(time, temp_cesm_low_control[:, 0])
time_year, temp_2_cesm_low_control	= YearlyConverter(time, temp_cesm_low_control[:, 1])
time_year, temp_3_cesm_low_control	= YearlyConverter(time, temp_cesm_low_control[:, 2])
time_year, temp_4_cesm_low_control	= YearlyConverter(time, temp_cesm_low_control[:, 3])
time_year, temp_5_cesm_low_control	= YearlyConverter(time, temp_cesm_low_control[:, 4])
time_year, temp_global_cesm_low_control	= YearlyConverter(time, temp_global_cesm_low_control)

#Take the anomalies with respect to the control simulation
temp_1_cesm_low		= TrendRemoverControl(time_year, temp_1_cesm_low_control, temp_1_cesm_low)
temp_2_cesm_low		= TrendRemoverControl(time_year, temp_2_cesm_low_control, temp_2_cesm_low)
temp_3_cesm_low		= TrendRemoverControl(time_year, temp_3_cesm_low_control, temp_3_cesm_low)
temp_4_cesm_low		= TrendRemoverControl(time_year, temp_4_cesm_low_control, temp_4_cesm_low)
temp_5_cesm_low		= TrendRemoverControl(time_year, temp_5_cesm_low_control, temp_5_cesm_low)
temp_global_cesm_low	= TrendRemoverControl(time_year, temp_global_cesm_low_control, temp_global_cesm_low)

#-----------------------------------------------------------------------------------------

#Apparently, you need to adapt the script (only the region numbers) for each region below...
lag, corr_cesm, sig_level_cesm		= CorrelationLag(temp_global_cesm, temp_1_cesm, 50)
lag, corr_cesm_low, sig_level_cesm_low	= CorrelationLag(temp_global_cesm_low, temp_1_cesm_low, 50)

lag, corr_cesm, sig_level_cesm		= SignificanceCorrelationLag(temp_global_cesm, temp_1_cesm, 50)
lag, corr_cesm_low, sig_level_cesm_low	= SignificanceCorrelationLag(temp_global_cesm_low, temp_1_cesm_low, 50)

fig, ax	= subplots()

ax.grid()
ax.axvline(x=0,color='k')
ax.axhline(y=0,color='k')		

HR_CESM_graph 	= ax.plot(lag, corr_cesm, '-r', linewidth = 2.0, label = 'HR-CESM')
LR_CESM_graph 	= ax.plot(lag, corr_cesm_low, '-b', linewidth = 2.0, label = 'LR-CESM')

ax.plot(lag, sig_level_cesm, '--r', linewidth = 2.0)
ax.plot(lag, -sig_level_cesm, '--r', linewidth = 2.0)
ax.plot(lag, sig_level_cesm_low, '--b', linewidth = 2.0)
ax.plot(lag, -sig_level_cesm_low, '--b', linewidth = 2.0)

ax.set_xlabel('Lag (years)')
ax.set_ylabel("Lag-correlation coefficient")
ax.set_xlim(0, 50)
ax.set_ylim(-1, 1)

graphs	      = HR_CESM_graph + LR_CESM_graph

legend_labels = [l.get_label() for l in graphs]
ax.legend(graphs, legend_labels, loc='lower right',
 		  ncol=1, fancybox=True, shadow=False, numpoints = 1)

ax.set_title('a) East Antarctica')
show()