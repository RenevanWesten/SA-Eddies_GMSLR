#Program plots the zonal velocity of the Weddell Gyre

from pylab import *
import numpy
import datetime
import time
import glob, os
import math
import netCDF4 as netcdf

#Making pathway to folder with all data
directory = '../../../Data/HR-CESM/'

#-----------------------------------------------------------------------------------------
#--------------------------------MAIN SCRIPT STARTS HERE----------------------------------
#-----------------------------------------------------------------------------------------

lon_section		= 320

lat_min			= -80
lat_max			= -40

month_start		= 1
month_end		= 12

depth_crop		= 1000
factor_depth_crop	= 4

vel_crop		= 10
factor_vel_crop		= 5

#-----------------------------------------------------------------------------------------

HEAT_data = netcdf.Dataset(directory+'/Ocean/UVEL_section_lon_'+str(lon_section)+'E.nc', 'r')

#Writing data to correct variable	
time			= HEAT_data.variables['time'][:]    
lat			= HEAT_data.variables['lat'][:]  
depth			= HEAT_data.variables['depth'][:]     	
u_vel			= HEAT_data.variables['UVEL'][:]		

HEAT_data.close()

total = np.sum(fabs(u_vel), axis = 0)

for time_i in range(len(time)):
	#Set 0.0 to masked elements
	u_vel[time_i]	= ma.masked_where(total == 0.0, u_vel[time_i])
	
#-----------------------------------------------------------------------------------------

#Take twice the amount of years for the month day
month_days	= np.asarray([31., 28., 31., 30., 31., 30., 31., 31., 30., 31., 30., 31., 31., 28., 31., 30., 31., 30., 31., 31., 30., 31., 30., 31.])
month_days	= month_days[month_start - 1:month_end]
month_days	= month_days / np.sum(month_days)

#Fill the array's with the same dimensions
month_days_all	= ma.masked_all((len(month_days), len(depth), len(lat)))

for month_i in range(len(month_days)):
	month_days_all[month_i]		= month_days[month_i]

if month_end <= 12:
	#Normal average over a single year, for example, February 100 - December 100
	time_year		= np.zeros(len(time) / 12)

else:
	#If you take the average, for example, over November 100 - May 101
	#Take year 101 as the average over this period
	#There is one year less compared to the period analysed
	time_year		= np.zeros(len(time) / 12 - 1)

u_vel_year		= ma.masked_all((len(time_year), len(depth), len(lat)))

for year_i in range(len(time_year)):
	#The year is defined as the current year
	year			= int(str(datetime.date.fromordinal(int(time[year_i * 12])))[0:4])

	if month_end	>= 13:
		#If average is taken over, for example, November 100 - May 101, the year is defined as 101
		year = year + 1

	time_year[year_i] 	= datetime.datetime(year, 1, 1).toordinal()

	#Determine the time mean over the months of choice
	u_vel_year[year_i]	= np.sum(u_vel[year_i * 12 + month_start - 1: year_i * 12 + month_end] * month_days_all, axis = 0)

#-----------------------------------------------------------------------------------------

#Take the time-mean velocity over 2000 - 2029
vel_mean_1	= np.mean(u_vel_year[0:30], axis = 0)
vel_mean_2	= ma.masked_all((len(depth), len(lat)))
depth_2		= np.zeros(len(depth))

for depth_i in range(len(depth)):
	for lat_i in range(len(lat)):

		if vel_mean_1[depth_i, lat_i] > vel_crop:
			#Rescale the velocity
			vel_mean_2[depth_i, lat_i]	=  ((vel_mean_1[depth_i, lat_i] - vel_crop) / factor_vel_crop) + vel_crop

		elif vel_mean_1[depth_i, lat_i] < -vel_crop:
			#Rescale the velocity
			vel_mean_2[depth_i, lat_i]	=  ((vel_mean_1[depth_i, lat_i] -- vel_crop) / factor_vel_crop) - vel_crop

		else:
			vel_mean_2[depth_i, lat_i]	=  vel_mean_1[depth_i, lat_i]

for depth_i in range(len(depth_2)):

	if depth[depth_i] > depth_crop:
		#Determine the new depth levels
		depth_2[depth_i]	=  ((depth[depth_i] - depth_crop) / factor_depth_crop) + depth_crop

	else:
		depth_2[depth_i]	= depth[depth_i]

#-----------------------------------------------------------------------------------------

fig, ax	= subplots()

ax.fill_between([-lat_min, -lat_max], y1 = np.zeros(2) + depth[0], y2 = np.zeros(2) + depth[-1], color = 'gray', alpha = 0.50)

levels	= np.arange(-20, 20.1, 1)
x, y	= np.meshgrid(-lat, depth_2)

CS	= ax.contourf(x, y, vel_mean_2, levels, extend = 'both', cmap = 'RdBu_r')
cbar	= colorbar(CS, ticks = np.arange(-20, 21, 5))
cbar.ax.set_yticklabels([-50, -35, -10, -5, 0, 5, 10, 35, 50])
cbar.set_label('Zonal velocity (cm s$^{-1}$)')

ax.set_xlabel('Latitude ($^{\circ}$S)')
ax.set_ylabel('Depth (m)')

ax.set_xlim(-lat_min, -lat_max)
ax.set_ylim(((5500 - depth_crop) / factor_depth_crop) + depth_crop, 0)
ax.set_title('a) HR-CESM, 2000 - 2029')

labels =  ax.get_yticks()

for label_i in range(len(labels)):

	if labels[label_i] > depth_crop:
		#Rescale the xlabels
		labels[label_i]	= ((labels[label_i] - depth_crop) * factor_depth_crop) + depth_crop

labels	= labels.astype(int)
ax.set_yticklabels(labels)

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------

fig, ax	= subplots()

ax.fill_between([-lat_min, -lat_max], y1 = np.zeros(2) + depth[0], y2 = np.zeros(2) + depth[-1], color = 'gray', alpha = 0.50)


levels	= np.arange(-10, 10.1, 1)
x, y	= np.meshgrid(-lat, depth_2)

#Take the difference between 2071 - 2100 and 2000 - 2029
CS	= ax.contourf(x, y, np.mean(u_vel_year[71:101], axis = 0) - vel_mean_1, levels, extend = 'both', cmap = 'PuOr_r')
cbar	= colorbar(CS, ticks = np.arange(-10, 10.1, 2))
cbar.set_label('Zonal velocity difference (cm s$^{-1}$)')

ax.set_xlabel('Latitude ($^{\circ}$S)')
ax.set_ylabel('Depth (m)')

ax.set_xlim(-lat_min, -lat_max)
ax.set_ylim(((5500 - depth_crop) / factor_depth_crop) + depth_crop, 0)
ax.set_title('c) HR-CESM, 2071 - 2100 minus 2000 - 2029')

labels =  ax.get_yticks()

for label_i in range(len(labels)):

	if labels[label_i] > depth_crop:
		#Rescale the xlabels
		labels[label_i]	= ((labels[label_i] - depth_crop) * factor_depth_crop) + depth_crop

labels	= labels.astype(int)
ax.set_yticklabels(labels)

show()