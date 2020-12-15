#Program plots the Southern Ocean regions

from pylab import *
import numpy
import datetime
import time
import glob, os
import math
import netCDF4 as netcdf
import matplotlib.colors as colors
from mpl_toolkits.basemap import Basemap

#-----------------------------------------------------------------------------------------
#--------------------------------MAIN SCRIPT STARTS HERE----------------------------------
#-----------------------------------------------------------------------------------------

lon_East_Antarctica_1	= np.arange(-10, 175, 0.1)
lat_East_Antarctica_1	= np.zeros(len(lon_East_Antarctica_1)) - 65.0
lon_East_Antarctica_2	= np.asarray([175, 175])
lat_East_Antarctica_2	= np.asarray([-65.0, -76.0])
lon_East_Antarctica_3	= np.arange(-10, 175, 0.1)[::-1]
lat_East_Antarctica_3	= np.zeros(len(lon_East_Antarctica_1)) - 76.0
lon_East_Antarctica_4	= np.asarray([-10, -10])
lat_East_Antarctica_4	= np.asarray([-75.9, -65.1])

lon_East_Antarctica	= np.append(lon_East_Antarctica_1, lon_East_Antarctica_2)
lat_East_Antarctica	= np.append(lat_East_Antarctica_1, lat_East_Antarctica_2)
lon_East_Antarctica	= np.append(lon_East_Antarctica, lon_East_Antarctica_3)
lat_East_Antarctica	= np.append(lat_East_Antarctica, lat_East_Antarctica_3)
lon_East_Antarctica	= np.append(lon_East_Antarctica, lon_East_Antarctica_4)
lat_East_Antarctica	= np.append(lat_East_Antarctica, lat_East_Antarctica_4)

lon_Ross_1		= np.arange(160, 212, 0.1)
lat_Ross_1		= np.zeros(len(lon_Ross_1)) - 76.0
lon_Ross_2		= np.asarray([212, 212])
lat_Ross_2		= np.asarray([-76, -80.0])
lon_Ross_3		= np.arange(160, 212, 0.1)[::-1]
lat_Ross_3		= np.zeros(len(lon_Ross_3)) - 80.0
lon_Ross_4		= np.asarray([160, 160])
lat_Ross_4		= np.asarray([-79.9, -76.1])

lon_Ross		= np.append(lon_Ross_1, lon_Ross_2)
lat_Ross		= np.append(lat_Ross_1, lat_Ross_2)
lon_Ross		= np.append(lon_Ross, lon_Ross_3)
lat_Ross		= np.append(lat_Ross, lat_Ross_3)
lon_Ross		= np.append(lon_Ross, lon_Ross_4)
lat_Ross		= np.append(lat_Ross, lat_Ross_4)

lon_Amundsen_1		= np.arange(212, 283, 0.1)
lat_Amundsen_1		= np.zeros(len(lon_Amundsen_1)) - 70.0
lon_Amundsen_2		= np.arange(283, 290, 0.1)
lat_Amundsen_2		= np.linspace(-70, -68.8, num = len(lon_Amundsen_2))
lon_Amundsen_3		= np.asarray([290, 290])
lat_Amundsen_3		= np.asarray([-68.8, -76])
lon_Amundsen_4		= np.arange(212, 290, 0.1)[::-1]
lat_Amundsen_4		= np.zeros(len(lon_Amundsen_4)) - 76.0
lon_Amundsen_5		= np.asarray([212, 212])
lat_Amundsen_5		= np.asarray([-75.9, -70.1])

lon_Amundsen		= np.append(lon_Amundsen_1, lon_Amundsen_2)
lat_Amundsen		= np.append(lat_Amundsen_1, lat_Amundsen_2)
lon_Amundsen		= np.append(lon_Amundsen, lon_Amundsen_3)
lat_Amundsen		= np.append(lat_Amundsen, lat_Amundsen_3)
lon_Amundsen		= np.append(lon_Amundsen, lon_Amundsen_4)
lat_Amundsen		= np.append(lat_Amundsen, lat_Amundsen_4)
lon_Amundsen		= np.append(lon_Amundsen, lon_Amundsen_5)
lat_Amundsen		= np.append(lat_Amundsen, lat_Amundsen_5)


lon_Weddell_1		= np.arange(298, 350, 0.1)
lat_Weddell_1		= np.zeros(len(lon_Weddell_1)) - 72.0
lon_Weddell_2		= np.asarray([350, 350])
lat_Weddell_2		= np.asarray([-72, -80.0])
lon_Weddell_3		= np.arange(298, 350, 0.1)[::-1]
lat_Weddell_3		= np.zeros(len(lon_Weddell_3)) - 80.0
lon_Weddell_4		= np.asarray([298, 298])
lat_Weddell_4		= np.asarray([-79.9, -72.1])

lon_Weddell		= np.append(lon_Weddell_1, lon_Weddell_2)
lat_Weddell		= np.append(lat_Weddell_1, lat_Weddell_2)
lon_Weddell		= np.append(lon_Weddell, lon_Weddell_3)
lat_Weddell		= np.append(lat_Weddell, lat_Weddell_3)
lon_Weddell		= np.append(lon_Weddell, lon_Weddell_4)
lat_Weddell		= np.append(lat_Weddell, lat_Weddell_4)

lon_Peninsula_1		= np.arange(298, 304, 0.1)
lat_Peninsula_1		= np.zeros(len(lon_Peninsula_1)) - 66
lon_Peninsula_2		= np.asarray([304, 304])
lat_Peninsula_2		= np.asarray([-66, -70.0])
lon_Peninsula_3		= np.arange(298, 304, 0.1)[::-1]
lat_Peninsula_3		= np.zeros(len(lon_Peninsula_3)) - 70.0
lon_Peninsula_4		= np.asarray([298, 298])
lat_Peninsula_4		= np.asarray([-69.9, -66.1])

lon_Peninsula		= np.append(lon_Peninsula_1, lon_Peninsula_2)
lat_Peninsula		= np.append(lat_Peninsula_1, lat_Peninsula_2)
lon_Peninsula		= np.append(lon_Peninsula, lon_Peninsula_3)
lat_Peninsula		= np.append(lat_Peninsula, lat_Peninsula_3)
lon_Peninsula		= np.append(lon_Peninsula, lon_Peninsula_4)
lat_Peninsula		= np.append(lat_Peninsula, lat_Peninsula_4)


#-----------------------------------------------------------------------------------------
fig, ax		= subplots()

m = Basemap(projection='spstere',boundinglat=-60,lon_0=180,resolution='i',  area_thresh=0.01) 

x, y	= m(lon_East_Antarctica, lat_East_Antarctica)
fill(x, y, facecolor='lightsalmon', edgecolor='orangered', linewidth=2)
x, y	= m(lon_Ross, lat_Ross)
fill(x, y, facecolor='lightskyblue', edgecolor='dodgerblue', linewidth=2)
x, y	= m(lon_Amundsen, lat_Amundsen)
fill(x, y, facecolor='lightcoral', edgecolor='firebrick', linewidth=2)
x, y	= m(lon_Weddell, lat_Weddell)
fill(x, y, facecolor='lightgreen', edgecolor='forestgreen', linewidth=2)
x, y	= m(lon_Peninsula, lat_Peninsula)
fill(x, y, facecolor='mediumpurple', edgecolor='darkmagenta', linewidth=2)

m.drawcoastlines(linewidth=0.5)
m.drawcountries()
m.fillcontinents(color='snow',lake_color='#99ffff')
m.drawmapboundary(fill_color='azure')

m.drawparallels(np.arange(-80,81,20),labels=[0,0,0,0])
m.drawmeridians(np.arange(-180,180,30),labels=[1,1,0,1])


x, y = m(90, -75)
plt.text(x, y, 'East Antarctica', color ='orangered', fontsize=18,ha='center',va='center', rotation=-90)
x, y = m(180, -81)
plt.text(x, y, 'Ross Region', color ='dodgerblue', fontsize=18,ha='center',va='center', rotation=0)
x, y = m(230, -62)
plt.text(x, y, 'Amundsen\nRegion', color ='firebrick', fontsize=18,ha='center',va='center', rotation=0)
x, y = m(335, -85)
plt.text(x, y, 'Weddell\nRegion', color ='forestgreen', fontsize=18,ha='center',va='center', rotation=0)
x, y = m(315, -64)
plt.text(x, y, 'Antarctic\nPeninsula', color ='darkmagenta', fontsize=18,ha='center',va='center', rotation=0)

ax.set_title('a) Southern Ocean regions')
show()