# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 20:59:19 2021

@author: bagus
"""

#Libraries
from netCDF4 import Dataset
import pandas as pd
import glob
import h5py

#Bounding Latitude and Longitude (Bali Selatan)
tes = Dataset(r'C:/Users/bagus/Desktop/Skripsi/Data/Bali Selatan/new/A2002187.L3m_DAY_CHL.x_chlor_a.nc')
tes_lon = tes.variables['lon'][:]
tes_lat = tes.variables['lat'][:]
panjang = len(tes_lon) * len(tes_lat)

#Dataframes untuk Keterangan Titik dan Koordinatnya
columns = ['Titik', 'Latitude', 'Longitude']
keterangan = pd.DataFrame(columns=columns)

#Mengambil Titik Koordinat Tiap Titik
a = 0
titik = 1
for i in tes_lat:
  for j in tes_lon:
    keterangan.loc[a, 'Longitude'] = j
    keterangan.loc[a, 'Latitude'] = i
    keterangan.loc[a, 'Titik'] = titik
    titik += 1
    a += 1

#Koordinat Data Keseluruhan
tes1 = Dataset(r'C:/Users/bagus/Desktop/Skripsi/Data/Daily/Indonesia_Chl-a/A2002185.L3m_DAY_CHL.x_chlor_a.nc')
lon_data = tes1.variables['lon'][:]
lat_data = tes1.variables['lat'][:]

#Mengambil Index Koordinat Terdekat
lon_index=[]
lat_index=[]
for set_lon in tes_lon:
    sq_diff_lon = (lon_data - set_lon)**2
    min_index_lon = sq_diff_lon.argmin()
    lon_index.append(min_index_lon)

for set_lat in tes_lat:
    sq_diff_lat = (lat_data - set_lat)**2
    min_index_lat = sq_diff_lat.argmin()
    lat_index.append(min_index_lat)

#Dataframe untuk Data
columns_name = ['Date']
df = pd.DataFrame(columns=columns_name)

#Mengambil Nilai Klorofil - a di Bali Selatan
n=0
for file in glob.glob('C:/Users/bagus/Desktop/Skripsi/Data/Daily/Indonesia_Chl-a/*.nc'):
  data = Dataset(file, 'r')
  time = data.time_coverage_start
  date = time[:10]
  df.loc[n, 'Date'] = date
  chl_a_data = data.variables['chlor_a'][:]

  counter = 1 
  for i in lat_index:
    for j in lon_index:
      col = str(counter)
      chl = chl_a_data[i,j]
      df.loc[n, col] = chl
      counter+=1
  n+=1