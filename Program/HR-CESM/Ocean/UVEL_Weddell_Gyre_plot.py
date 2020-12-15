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

depth_crop		= 1000
factor_depth_crop	= 4

vel_crop		= 10
factor_vel_crop		= 5

#-----------------------------------------------------------------------------------------

HEAT_data = netcdf.Dataset(directory+'/Ocean/UVEL_section_lon_'+str(lon_section)+'E.nc', 'r')

#Writing data to correct variable	
lat			= HEAT_data.variables['lat'][:]  
depth			= HEAT_data.variables['depth'][:]     	
vel_1			= HEAT_data.variables['UVEL_2000-2029'][:]		
vel_2			= HEAT_data.variables['UVEL_2071-2100'][:]		

HEAT_data.close()

#-----------------------------------------------------------------------------------------

#Rescale the time-mean velocity over 2000 - 2029
vel_1_2	    = ma.masked_all((len(depth), len(lat)))
depth_2	    = np.zeros(len(depth))

for depth_i in range(len(depth)):
	for lat_i in range(len(lat)):

		if vel_1[depth_i, lat_i] > vel_crop:
			#Rescale the velocity
			vel_1_2[depth_i, lat_i]	=  ((vel_1[depth_i, lat_i] - vel_crop) / factor_vel_crop) + vel_crop

		elif vel_1[depth_i, lat_i] < -vel_crop:
			#Rescale the velocity
			vel_1_2[depth_i, lat_i]	=  ((vel_1[depth_i, lat_i] -- vel_crop) / factor_vel_crop) - vel_crop

		else:
			vel_1_2[depth_i, lat_i]	=  vel_1[depth_i, lat_i]

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

CS	= ax.contourf(x, y, vel_1_2, levels, extend = 'both', cmap = 'RdBu_r')
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

fig, ax	= subplots()

ax.fill_between([-lat_min, -lat_max], y1 = np.zeros(2) + depth[0], y2 = np.zeros(2) + depth[-1], color = 'gray', alpha = 0.50)


levels	= np.arange(-10, 10.1, 1)
x, y	= np.meshgrid(-lat, depth_2)

#Take the difference between 2071 - 2100 and 2000 - 2029
CS	= ax.contourf(x, y, vel_2 - vel_1, levels, extend = 'both', cmap = 'PuOr_r')
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