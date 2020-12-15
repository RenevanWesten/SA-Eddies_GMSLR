#Program plots the barotropic streamfunction and wind-stress curl field.

from pylab import *
import numpy
import datetime
import time
import glob, os
import math
import netCDF4 as netcdf
import matplotlib.colors as colors
from mpl_toolkits.basemap import Basemap
from scipy.ndimage import gaussian_filter

#Making pathway to folder with all data
directory 	= '../../../Data/HR-CESM/'

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

HEAT_data = netcdf.Dataset(directory+'Ocean/Barotropic_streamfunction_Southern_Ocean_year_2000-2029.nc', 'r')

lon_1		= HEAT_data.variables['lon'][:] 		
lat_1		= HEAT_data.variables['lat'][:] 		
BSF_1		= HEAT_data.variables['BSF'][:]

HEAT_data.close()

HEAT_data = netcdf.Dataset(directory+'Ocean/Barotropic_streamfunction_Southern_Ocean_year_2071-2100.nc', 'r')

BSF_2		= HEAT_data.variables['BSF'][:]

HEAT_data.close()

#Add periodic boundaries for plot
lon_new, BSF_1		= PeriodicBoundaries(lon_1, lat_1, BSF_1)
lon_1, BSF_2		= PeriodicBoundaries(lon_1, lat_1, BSF_2)

#-----------------------------------------------------------------------------------------

HEAT_data = netcdf.Dataset(directory+'Ocean/Wind_stress_curl_Southern_Ocean_year_2000-2029.nc', 'r')

lon_2	        = HEAT_data.variables['lon'][:] 			
lat_2		= HEAT_data.variables['lat'][:] 			
wind_1		= HEAT_data.variables['WIND'][:]

HEAT_data.close()

HEAT_data = netcdf.Dataset(directory+'Ocean/Wind_stress_curl_Southern_Ocean_year_2071-2100.nc', 'r')
			
wind_2		= HEAT_data.variables['WIND'][:]

HEAT_data.close()

#Add periodic boundaries for plot
lon_new, wind_1		= PeriodicBoundaries(lon_2, lat_2, wind_1, 100)
lon_2, wind_2		= PeriodicBoundaries(lon_2, lat_2, wind_2, 100)
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------

fig, ax = plt.subplots()

m = Basemap(projection='spstere',boundinglat=-40,lon_0=180,resolution='i',  area_thresh=0.01) 

m.drawcoastlines(linewidth=0.5)
m.drawcountries()
m.fillcontinents(color='#cc9966', lake_color='#99ffff')
#m.drawmapboundary(fill_color='azure')

m.drawparallels(np.arange(-80,81,20),labels=[0,0,0,0])
m.drawmeridians(np.arange(-180,180,30),labels=[1,0,0,1])

x, y	= np.meshgrid(lon_1, lat_1)
x, y	= m(x, y)

levels	= np.arange(-20, 200.01, 5)

CS	= m.contourf(x, y, BSF_1, levels, extend = 'both', cmap = 'Spectral_r')
cbar 	= m.colorbar(CS, ticks = np.arange(-20, 201, 20))
cbar.set_label('Barotropic streamfunction (Sv)')
ax.set_title('a) HR-CESM, 2000 - 2029')

x, y		= np.meshgrid(lon_2, lat_2)
x, y		= m(x, y)
wind_climate	= gaussian_filter(wind_1, sigma = 20)
wind_climate	= ma.masked_array(wind_climate, mask = wind_1.mask)

CS1		= m.contour(x, y, wind_climate * 10**7.0, levels = [0], colors = 'gray', linewidths = 2.5, label = '0')
CS1	        = m.plot([-1, -1], [-1, -1], 'gray', linewidth = 2.5, label = '0$_{\mathrm{ref}}$')

graphs	      = CS1

legend_labels = [l.get_label() for l in graphs]
legend_1      = ax.legend(graphs, legend_labels, bbox_to_anchor=(0.48, 0.51), ncol=1, numpoints = 1)

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------

fig, ax = plt.subplots()

m = Basemap(projection='spstere',boundinglat=-40,lon_0=180,resolution='i',  area_thresh=0.01) 

m.drawcoastlines(linewidth=0.5)
m.drawcountries()
m.fillcontinents(color='#cc9966', lake_color='#99ffff')
#m.drawmapboundary(fill_color='azure')

m.drawparallels(np.arange(-80,81,20),labels=[0,0,0,0])
m.drawmeridians(np.arange(-180,180,30),labels=[1,0,0,1])

x, y	= np.meshgrid(lon_1, lat_1)
x, y	= m(x, y)
levels	= np.arange(-6, 6.01, 0.5)

BSF_diff = BSF_2 - BSF_1

for lat_i in range(len(lat_1)):
	for lon_i in range(len(lon_1)):

		if BSF_diff[lat_i, lon_i] > 3.0:
			#Rescale the BSF difference
			BSF_diff[lat_i, lon_i]	= 3.0 + (BSF_diff[lat_i, lon_i] - 3.0) / 5.0

		if BSF_diff[lat_i, lon_i] < -3.0:
			#Rescale the BSF difference
			BSF_diff[lat_i, lon_i]	= -3.0 + (BSF_diff[lat_i, lon_i] - -3.0) / 5.0

CS	= m.contourf(x, y, BSF_diff, levels, extend = 'both', cmap = 'RdBu_r')
cbar 	= m.colorbar(CS, ticks = np.arange(-6, 6.01, 1))
cbar.ax.set_yticklabels([-18, -13, -8, -3, -2, 1, 0, 1, 2, 3, 8, 13, 18])
cbar.set_label('Barotropic streamfunction difference (Sv)')
ax.set_title('c) HR-CESM, 2071 - 2100 minus 2000 - 2029')

x, y	= np.meshgrid(lon_2, lat_2)
x, y	= m(x, y)

#Using the previous wind stress
CS2_test	= m.contour(x, y, wind_climate * 10**7.0, levels = [0], colors = 'gray', linestyles = '-', linewidths = 2.5, label = '0')

#Determine next wind stress curl isolines
wind_climate	= gaussian_filter(wind_2, sigma = 20)
wind_climate	= ma.masked_array(wind_climate, mask = wind_1.mask)

CS2		= m.contour(x, y, wind_climate * 10**7.0, levels = [0], colors = 'k', linewidths = 2.5, label = '0')
CS2		= m.plot([-1, -1], [-1, -1], '-k', linewidth = 2.5, label = '0')
CS1		= m.plot([-1, -1], [-1, -1], 'gray', linewidth = 2.5, label = '0$_{\mathrm{ref}}$')

graphs	      = CS1 + CS2

legend_labels = [l.get_label() for l in graphs]
legend_1      = ax.legend(graphs, legend_labels, bbox_to_anchor=(0.48, 0.51), ncol=1, numpoints = 1)

show()