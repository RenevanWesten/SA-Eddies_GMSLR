#Program plots the time-mean (2000 - 2100) temperature difference with the Mercator

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
directory = '../../../Data/HR-CESM_Control/'

def PeriodicBoundaries(lon, lat, field, lon_grids = 1):
	"""Add periodic zonal boundaries"""

	#Empty field with additional zonal boundaries
	lon_2			= np.zeros(len(lon) + lon_grids * 2)
	field_2			= ma.masked_all((len(lat), len(lon_2)))
	
	#Get the left boundary, which is the right boundary of the original field
	lon_2[:lon_grids]	= lon[-lon_grids:] - 360.0
	field_2[:, :lon_grids]	= field[:, -lon_grids:]

	#Same for the right boundary
	lon_2[-lon_grids:]	= lon[:lon_grids] + 360.0
	field_2[:, -lon_grids:]	= field[:, :lon_grids]

	#And the complete field
	lon_2[lon_grids:-lon_grids]		= lon
	field_2[:, lon_grids:-lon_grids] 	= field

	return lon_2, field_2	

#-----------------------------------------------------------------------------------------
#--------------------------------MAIN SCRIPT STARTS HERE----------------------------------
#-----------------------------------------------------------------------------------------

depth_min	= 250
depth_max	= 450

#-----------------------------------------------------------------------------------------

HEAT_data = netcdf.Dataset(directory+'Ocean/TEMP_Southern_Ocean_Mercator_difference.nc', 'r')

lon	= HEAT_data.variables['lon'][:] 			
lat	= HEAT_data.variables['lat'][:] 			
temp	= HEAT_data.variables['TEMP'][:]		

HEAT_data.close()

lon, temp	= PeriodicBoundaries(lon, lat, temp)

#-----------------------------------------------------------------------------------------

fig, ax		= subplots()

m = Basemap(projection='spstere',boundinglat=-60,lon_0=180,resolution='i',  area_thresh=0.01) 

m.drawcoastlines(linewidth=0.5)
m.drawcountries()
m.fillcontinents(color='#cc9966',lake_color='#99ffff')
m.drawmapboundary(fill_color='azure')

m.drawparallels(np.arange(-80,81,20),labels=[0,0,0,0])
m.drawmeridians(np.arange(-180,180,30),labels=[1,0,0,1])


x, y	= np.meshgrid(lon, lat)
x, y	= m(x, y)
CS	= m.contourf(x, y, temp, levels = np.arange(-3, 3.01, 0.2), extend = 'both', cmap = 'RdBu_r')
cbar	= m.colorbar(CS, ticks = np.arange(-3, 3.01, 1))
cbar.set_label('Temperature difference ($^{\circ}$C)')

ax.set_title('e) HR-CESM Control minus Mercator')

show()