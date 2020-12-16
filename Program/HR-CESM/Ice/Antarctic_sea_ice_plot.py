#Program plots the Antarctic sea-ice fraction

from pylab import *
import numpy
import datetime
import time
import glob, os
import math
import netCDF4 as netcdf
import matplotlib.colors as colors
from mpl_toolkits.basemap import Basemap

#Making pathway to folder with all data
directory 		= '../../../Data/HR-CESM/'
directory_SSMR_SSMI 	= '../../../Data/SSMR_SSMI/'

#-----------------------------------------------------------------------------------------
#--------------------------------MAIN SCRIPT STARTS HERE----------------------------------
#-----------------------------------------------------------------------------------------	

ICE_data = netcdf.Dataset(directory+'Ice/Antarctic_September_sea_ice_fraction.nc', 'r')

lon	= ICE_data.variables['lon'][:]    
lat	= ICE_data.variables['lat'][:]    
ice_1	= ICE_data.variables['AICE_2000-2029'][:]    
ice_2	= ICE_data.variables['AICE_2071-2100'][:]    

ICE_data.close()

#-----------------------------------------------------------------------------------------

ICE_data = netcdf.Dataset(directory_SSMR_SSMI+'Ice/Antarctic_September_sea_ice_extent.nc', 'r')

#Take the time-mean (1993 - 2018) sea-ice extent
lon_SSMR_SSMI	= ICE_data.variables['lon'][:]    
lat_ice_extent	= np.mean(ICE_data.variables['ICE'][:], axis = 0)     	

ICE_data.close()

for lon_i in range(len(lon_SSMR_SSMI)):
	#Now interpolate ice extent to cesm coordinates
	if (lat_ice_extent[lon_i] is ma.masked) == False:
		#Get the lon index of the following non-masked element	

		for lon_j in range(lon_i + 1, len(lon_SSMR_SSMI)):
			if (lat_ice_extent[lon_j] is ma.masked) == False:

				if lon_i + 1 == lon_j:
					#No inteprolation is needed, two adjacent points
					break

				#Interpolate in-between
				lat_ice_rc			= (lat_ice_extent[lon_j] - lat_ice_extent[lon_i]) / (lon_j - lon_i)
				lat_ice_extent[lon_i:lon_j]	= np.arange(0, lon_j - lon_i) * lat_ice_rc + lat_ice_extent[lon_i]

				#Break the j-loop
				break
#-----------------------------------------------------------------------------------------

fig, ax		= subplots()

m = Basemap(projection='spstere',boundinglat=-53,lon_0=180,resolution='i',  area_thresh=0.01) 

m.drawcoastlines(linewidth=0.5)
m.drawcountries()
m.fillcontinents(color='#cc9966', lake_color='#99ffff')
#m.drawmapboundary(fill_color='azure')

m.drawparallels(np.arange(-80,81,20),labels=[0,0,0,0])
m.drawmeridians(np.arange(-180,180,30),labels=[1,0,0,1])


x, y	= np.meshgrid(lon, lat)
x, y	= m(x, y)
CS	= m.contourf(x, y, ice_1, levels = np.arange(15, 100.01, 2.5), extend = 'min', cmap = 'Blues_r')
cbar	= m.colorbar(CS, ticks = [15, 20, 40, 60, 80, 100])
cbar.set_label('Sea-ice fraction ($\%$)')

x, y	= m(lon_SSMR_SSMI, lat_ice_extent)
m.plot(x, y, '-r', linewidth = 3.0, label = 'SSMR-SSM/I')

ax.legend(loc = 'lower left', ncol=1, fancybox=True, shadow=False, numpoints = 1)
ax.set_title('c) HR-CESM, September model year 2000 - 2029')

#-----------------------------------------------------------------------------------------

fig, ax		= subplots()

m = Basemap(projection='spstere',boundinglat=-53,lon_0=180,resolution='i',  area_thresh=0.01) 

m.drawcoastlines(linewidth=0.5)
m.drawcountries()
m.fillcontinents(color='#cc9966', lake_color='#99ffff')
#m.drawmapboundary(fill_color='azure')

m.drawparallels(np.arange(-80,81,20),labels=[0,0,0,0])
m.drawmeridians(np.arange(-180,180,30),labels=[1,0,0,1])


x, y	= np.meshgrid(lon, lat)
x, y	= m(x, y)
CS	= m.contourf(x, y, ice_2, levels = np.arange(15, 100.01, 2.5), extend = 'min', cmap = 'Blues_r')
cbar	= m.colorbar(CS, ticks = [15, 20, 40, 60, 80, 100])
cbar.set_label('Sea-ice fraction ($\%$)')

x, y	= m(lon_SSMR_SSMI, lat_ice_extent)
m.plot(x, y, '-r', linewidth = 3.0, label = 'SSMR-SSM/I')

ax.legend(loc = 'lower left', ncol=1, fancybox=True, shadow=False, numpoints = 1)
ax.set_title('e) HR-CESM, September model year 2071 - 2100')

show()