 #Program determines the spatial correlation and RMS
 
from pylab import *
import numpy
import datetime
import time
import glob, os
import math
import netCDF4 as netcdf
import matplotlib.colors as colors
from scipy import stats
import matplotlib.tri as tri

#Making pathway to folder with all data
directory	= '../../../Data/CMIP6/'
directory_cesm 	= '../../../Data/HR-CESM/'

def MaskedFilled(lon, lat, field):
	"""Interpolate the masked elements for interpolation for Antarctica"""

	for lon_i in range(len(lon)):
		#First fill the complete Antarctic continent
		#Get the index where the first time the ocean is reached
		lat_index		= np.where(field[:, lon_i].mask == False)[0][0]

		#Fill Antarctica with the value at the coast for each longitude
		field[:lat_index, lon_i]	= field[lat_index, lon_i]

	#Get the indices for all masked elements
	mask_index = np.where(field.mask == True)

	for mask_i in range(len(mask_index[0])):
		#Get the lon/lat index for masked element
		lat_index, lon_index	= mask_index[0][mask_i], mask_index[1][mask_i]

		#Get all the points around masked element
		field_mask	= field[lat_index - 1:lat_index + 2, lon_index - 1:lon_index + 2]

		field[lat_index, lon_index]	= np.mean(field_mask)

	return field

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

lat_max		= -60

depth_min	= 250
depth_max	= 450

#-----------------------------------------------------------------------------------------
	
#Get the model names and path
models = glob.glob(directory+'*')
models.sort()

for model_i in range(len(models)):
	#Only retain the model names
	models[model_i]	= models[model_i][len(directory):]

#-----------------------------------------------------------------------------------------

#Get the lon, lat field from the high-resolution CESM simulation
HEAT_data 	= netcdf.Dataset(directory_cesm+'Ocean/TEMP_Southern_Ocean_year_2071-2100_depth_250-450m.nc', 'r')

lon_cesm	= HEAT_data.variables['lon'][:] 			
lat_cesm	= HEAT_data.variables['lat'][:] 			
temp_cesm	= HEAT_data.variables['TEMP'][:] 

HEAT_data.close()

#Fill complete field for interpolation
temp_cesm		= MaskedFilled(lon_cesm, lat_cesm, temp_cesm)

#Retain field to maximum latitude
lat_max_index	= (fabs(lat_cesm - lat_max)).argmin() + 5
lat_cesm	= lat_cesm[:lat_max_index]
temp_cesm	= temp_cesm[:lat_max_index]

#Add periodic zonal boundaries for interpolation
lon_cesm, temp_cesm = PeriodicBoundaries(lon_cesm, lat_cesm, temp_cesm, 2)

#Make 1D for interpolation
lon_cesm, lat_cesm	= np.meshgrid(lon_cesm, lat_cesm)
lon_cesm		= lon_cesm.ravel()
lat_cesm		= lat_cesm.ravel()
temp_cesm		= temp_cesm.ravel()

#Triangulate the grid of the CESM
triang 		= tri.Triangulation(lon_cesm, lat_cesm)
temp_cesm 	= tri.LinearTriInterpolator(triang, temp_cesm)

#-----------------------------------------------------------------------------------------

#Empty arrays for each CMIP6 model
corr_all	= ma.masked_all(len(models))
rms_all		= ma.masked_all(len(models))

for model_i in range(len(models)):
	#For each model get the all the files

	print model_i, models[model_i]
	HEAT_data = netcdf.Dataset(directory+models[model_i]+'/Ocean/TEMP_Southern_Ocean_year_72-101_depth_'+str(depth_min)+'-'+str(depth_max)+'m.nc', 'r')

	lon		= HEAT_data.variables['lon'][:] 			
	lat		= HEAT_data.variables['lat'][:] 
	area		= HEAT_data.variables['AREA'][:]				
	temp		= HEAT_data.variables['TEMP'][:]		
	
	HEAT_data.close()

	if models[model_i] == 'AWI-CM-1-1-MR':
                #Get the native grid for AWI-CM-1-1-MR
		HEAT_data = netcdf.Dataset(directory+models[model_i]+'/Ocean/TEMP_Southern_Ocean_depth_'+str(depth_min)+'-'+str(depth_max)+'m_native_grid.nc', 'r')

		lon		= HEAT_data.variables['lon'][:] 			
		lat		= HEAT_data.variables['lat'][:] 
		area		= HEAT_data.variables['AREA'][:]			
		temp		= HEAT_data.variables['TEMP'][:]	
		
		HEAT_data.close()
	#-----------------------------------------------------------------------------------------

	if models[model_i] == 'CMCC-CM2-SR5' or models[model_i] == 'CNRM-CM6-1' or models[model_i] == 'CNRM-ESM2-1' or models[model_i] == 'IPSL-CM6A-LR':
		#The boundaries have no data
		lon	= lon[:, 1:-1]
		lat	= lat[:, 1:-1]
		area	= area[:, 1:-1]
		temp	= temp[:, 1:-1]

	#Set all the negative latitudes to zero
	lon[lon < 0]	= lon[lon < 0] + 360.0


	if models[model_i] != 'AWI-CM-1-1-MR':
		#Get all the model output in the unravelled form
		#AWI-CM-1-1-MR is already in the unravelled form
		lon	= lon.ravel()
		lat	= lat.ravel()
		area	= area.ravel()
		temp	= temp.ravel()

	#-----------------------------------------------------------------------------------------
	#Get all the latiudes below 60S
	lat_index	= np.where(lat <= lat_max)[0]
	lon		= lon[lat_index]
	lat		= lat[lat_index]
	area		= area[lat_index]
	temp		= temp[lat_index]

	#Remove all the masked elements
	lon		= lon[temp.mask == False]
	lat		= lat[temp.mask == False]
	area		= area[temp.mask == False]
	temp		= temp[temp.mask == False]

	#-----------------------------------------------------------------------------------------
	#Interpolate on the CMIP6 grid for each of the models
	temp_cesm_CMIP6	= temp_cesm(lon, lat)

	#-----------------------------------------------------------------------------------------

	#Normalise area
	area_norm 	= area / np.sum(area)

	#Determine the area-weighted correlation
	temp_mean_1	= np.sum(area_norm * temp_cesm_CMIP6)
	temp_mean_2	= np.sum(area_norm * temp)
	temp_1		= temp_cesm_CMIP6 - temp_mean_1
	temp_2		= temp - temp_mean_2

	#Area-weighted covariances
	cov		= np.sum(area_norm * (temp_1 * temp_2))
	cov_1		= np.sum(area_norm * (temp_1 **2.0))
	cov_2		= np.sum(area_norm * (temp_2 **2.0))

	#Area-weighted correlation coefficient
	corr_all[model_i]	= cov / (np.sqrt(cov_1) * np.sqrt(cov_2))

	#Determine the area-weighted root mean square value
	rms_all[model_i]	= np.sqrt(np.sum(area_norm * (temp_cesm_CMIP6 - temp)**2.0))

#-----------------------------------------------------------------------------------------

TEMP_data = netcdf.Dataset(directory_cesm+'Ocean/TEMP_Southern_Ocean_HR-CESM_to_CMIP6.nc', 'w')
TEMP_data.createDimension('models', len(models))

TEMP_data.createVariable('models', float, ('models'), zlib=True)
TEMP_data.createVariable('CORR', float, ('models'), zlib=True)
TEMP_data.createVariable('RMS', float, ('models'), zlib=True)

TEMP_data.variables['CORR'].longname	= 'Area-weighted correlation coefficient'
TEMP_data.variables['RMS'].longname	= 'Area-weighted root mean square value'

TEMP_data.variables['RMS'].units 	= 'deg C'

#Writing data to correct variable	
TEMP_data.variables['models'][:]     	= np.arange(len(models))
TEMP_data.variables['CORR'][:] 		= corr_all
TEMP_data.variables['RMS'][:] 		= rms_all

TEMP_data.close()

