# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 22:52:10 2021

@author: bagus
"""
import os
os.environ["PROJ_LIB"] = "C:\\Users\\bagus\\anaconda3\\pkgs\\proj-7.2.0-h3e70539_0\\Library\\share"
from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset
import pandas as pd
import numpy as np
import PIL
from pylab import rcParams
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rc
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()
rcParams['axes.labelpad'] = 20 
rcParams['axes.titlesize'] = 20
rcParams['axes.titlepad'] = 20 
rcParams['figure.figsize'] = 20,20
sns.set(style='whitegrid', palette='muted', font_scale=1.5)

df_true = pd.read_csv('C:/Users/bagus/Desktop/Skripsi/Hasil Bali Selatan/CSV/Hasil Aktual.csv')
df_forecast = pd.read_csv('C:/Users/bagus/Desktop/Skripsi/Hasil Bali Selatan/CSV/Hasil Prediksi.csv')

aktual = np.zeros((366, 7, 10))
prediksi = np.zeros((366, 7, 10))

for x in range(0,366):
  for y in range(0,6):
    for z in range(0,9):
      col = str((y+1)*(z+1))
      aktual[x,y,z] = df_true.loc[x,col]
      #prediksi[x,y,z] = df_forecast.loc[x,col]

tes = Dataset(r'C:/Users/bagus/Desktop/Skripsi/Data/dataset-oc-glo-bio-multi-l4-chl_interpolated_4km_daily-rep_1626246099130.nc')
tes_lon = tes.variables['lon'][:]
tes_lat = tes.variables['lat'][:]

tes_lat = np.array(tes_lat)
tes_lon = np.array(tes_lon)
tes_lon = np.append(tes_lon,[115.3497])

lon,lat = np.meshgrid(tes_lon, tes_lat)

for i in range(0,366):
  mp = Basemap(projection = 'merc',
             llcrnrlon = 114.97917175,
             llcrnrlat =  -9.10417,
             urcrnrlon = 115.3497,
             urcrnrlat = -8.85417,
             resolution = 'i')

  x,y = mp(lon,lat)
  pararels = mp.drawparallels([-8.937, -9.062],labels=[1,0,0,0],linewidth=1.0,dashes=[1, 0])
  mp.drawmeridians([115.04076385,115.17028809,115.29981232],labels=[0,0,0,1],linewidth=1.0,dashes=[1, 0])
  for m in pararels:
    try:
      pararels[m][1][0].set_rotation(90)
    except:
        pass
  mp.drawmapboundary()
  mp.drawcoastlines()
  mp.fillcontinents(color='coral',lake_color='aqua')
  mp.drawcountries()  
  c_scheme = mp.pcolor(x,y, aktual[i,:,:],cmap = 'jet',vmin=0, vmax=30)
  cbar = mp.colorbar(c_scheme, location='bottom', pad='15%',label='Konsentrasi Klorofil - a (mg/m3)')
  cbar. set_ticks([0,2, 4, 6, 8,10])
  cbar.set_ticklabels(["0", "2", "4", "6","8",">10"])
  plt.clim(0, 10)
  plt.title('{}'.format(df_forecast.loc[i,'Date']),fontsize=25)
  plt.savefig(r'C:/Users/bagus/Desktop/Skripsi/Hasil Bali Selatan/Hasil Peta/Aktual/{}.jpg'.format(df_forecast.loc[i,'Date']))
  plt.clf()

prediksi_frames = []
aktual_frames = []
for day in df_forecast['Date']:
  aktual_new_frame = PIL.Image.open(r'C:/Users/bagus/Desktop/Skripsi/Hasil Bali Selatan/Hasil Peta/Aktual/{}.jpg'.format(day))
  #prediksi_new_frame = PIL.Image.open(r'C:/Users/bagus/Desktop/Skripsi/Hasil Bali Selatan/Hasil Peta/Prediksi/{}.jpg'.format(day))
  aktual_frames.append(aktual_new_frame)
  #prediksi_frames.append(prediksi_new_frame)

aktual_frames[0].save('C:/Users/bagus/Desktop/Skripsi/Hasil Bali Selatan/Hasil Peta/Aktual.gif', format='GIF',
                      append_images = aktual_frames[1:],
                      save_all=True, duration = 300, loop=0)
#prediksi_frames[0].save('C:/Users/bagus/Desktop/Skripsi/Hasil Bali Selatan/Hasil Peta/Prediksi.gif', format='GIF',
                        #append_images = prediksi_frames[1:],
                        #save_all=True, duration = 300, loop=0)  