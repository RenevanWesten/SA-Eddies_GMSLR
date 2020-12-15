#Program plots the subsurface Southern Ocean temperature anomaly

from pylab import *
import numpy
import datetime
import time
import glob, os
import math
import netCDF4 as netcdf
import matplotlib.colors as colors
from scipy import stats
from mpl_toolkits.basemap import Basemap

#Making pathway to folder with all data
directory 		= '../../../Data/CMIP6/'

def PeriodicBoundaries(lon, lat, field, lon_grids = 1):
	"""Add periodic zonal boundaries"""

	#Empty field with additional zonal boundaries
	lon_2	= np.zeros(len(lon[0]) + lon_grids * 2)
	lon_2	= ma.masked_all((len(lat), len(lon_2)))
	lat_2	= ma.masked_all(shape(lon_2))
	field_2	= ma.masked_all(shape(lon_2))
	
	#Get the left boundary, which is the right boundary of the original field
	lon_2[:, :lon_grids]	= lon[:, -lon_grids:] - 360.0
	lat_2[:, :lon_grids]	= lat[:, -lon_grids:]
	field_2[:, :lon_grids]	= field[:, -lon_grids:]

	#Same for the right boundary
	lon_2[:, -lon_grids:]	= lon[:, :lon_grids] + 360.0
	lat_2[:, -lon_grids:]	= lat[:, :lon_grids]
	field_2[:, -lon_grids:]	= field[:, :lon_grids]

	#And the complete field
	lon_2[:, lon_grids:-lon_grids]		= lon
	lat_2[:, lon_grids:-lon_grids] 		= lat
	field_2[:, lon_grids:-lon_grids] 	= field

	return lon_2, lat_2, field_2	

#-----------------------------------------------------------------------------------------
#--------------------------------MAIN SCRIPT STARTS HERE----------------------------------
#-----------------------------------------------------------------------------------------

depth_min	= 250
depth_max	= 450

#-----------------------------------------------------------------------------------------
	
#Get the model names and path
models = glob.glob(directory+'*')
models.sort()

for model_i in range(len(models)):
	#Only retain the model names
	models[model_i]	= models[model_i][len(directory):]

for model_i in range(len(models)):
	#For each model get the all the files

	print models[model_i]
	HEAT_data = netcdf.Dataset(directory+models[model_i]+'/Ocean/TEMP_Southern_Ocean_year_72-101_depth_'+str(depth_min)+'-'+str(depth_max)+'m.nc', 'r')

	lon		= HEAT_data.variables['lon'][:] 			
	lat		= HEAT_data.variables['lat'][:] 			
	temp		= HEAT_data.variables['TEMP'][:]		
	
	HEAT_data.close()

	#-----------------------------------------------------------------------------------------

	if models[model_i] == 'CMCC-CM2-SR5' or models[model_i] == 'CNRM-CM6-1' or models[model_i] == 'CNRM-ESM2-1' or models[model_i] == 'IPSL-CM6A-LR':
		#The boundaries have no data
		lon	= lon[:, 1:-1]
		lat	= lat[:, 1:-1]
		temp	= temp[:, 1:-1]

	elif models[model_i] == 'MPI-ESM1-2-HAM' or models[model_i] == 'MPI-ESM1-2-LR':
		#Adjust manually
		lon_2			= lon[:, :140]
		lon_2[lon_2 > 100]	= lon_2[lon_2 > 100] - 360.0
		lon[:, :140]		= lon_2
	else:

		if lon.min() < 0:
			#Negative longitudes
			lon[lon < 0]	= lon[lon < 0] + 360.0

		if np.any(fabs(lon[-1, 1:] - lon[-1, :-1]) > 300):
			#Only a jump from 360 - 0, get the maximum latiude
			lon_max_jump	=  lon[:, -1].max()

			#Increase longitude by 360 degrees
			lon[lon <= lon_max_jump]	= lon[lon <= lon_max_jump] + 360.0

		if lon.min() > 180:
			#Shift the complete field back by 360 degrees
			lon 	= lon - 360.0

	if models[model_i] == 'CNRM-CM6-1-HR' or models[model_i] == 'EC-Earth3-Veg' or models[model_i] == 'MPI-ESM1-2-HR':
		#Adjust first two latitude	
		lon[:, :2]	+= - 360.0

	#Additional periodic zonal boundary
	lon, lat, temp	= PeriodicBoundaries(lon, lat, temp, 3)

	#-----------------------------------------------------------------------------------------
	
	fig, ax		= subplots()

	m = Basemap(projection='spstere',boundinglat=-60,lon_0=180,resolution='i',  area_thresh=0.01) 

	m.drawcoastlines(linewidth=0.5)
	m.drawcountries()
	m.fillcontinents(color='#cc9966', lake_color='#99ffff')
	#m.drawmapboundary(fill_color='azure')

	m.drawparallels(np.arange(-80,81,20),labels=[0,0,0,0])
	m.drawmeridians(np.arange(-180,180,30),labels=[1,0,0,1])


	#x, y	= np.meshgrid(lon, lat)
	x, y	= m(lon, lat)
	CS	= m.contourf(x, y, temp, levels = np.arange(-2, 2.01, 0.1), extend = 'both', cmap = 'RdBu_r')
	cbar	= m.colorbar(CS, ticks = np.arange(-2, 2.01, 1))
	cbar.set_label('Temperature anomaly ($^{\circ}$C)')

	ax.set_title(models[model_i])

        show()

