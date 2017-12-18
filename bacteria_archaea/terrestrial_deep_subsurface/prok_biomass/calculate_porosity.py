# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 09:26:54 2017

@author: yinonbaron
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import  gmean
def func(x,a,b,c):
    return a*np.exp(-b*x)+c

def frac_func(x0,x1,a,b,c):
    integral = lambda x: -a/b*np.exp(-b*x) + c*x
    int_x = integral(x1) - integral(x0)
    int_total = integral(2000) - integral(0)
    fraction = int_x/int_total
    return fraction


data = pd.read_csv('gleeson_porosity_data.csv', skiprows=1)
popt, pcov = curve_fit(func, data['Depth [m]'], data['Porosity'],bounds=(0, [1., 1., 0.5]))
popt, pcov = curve_fit(func, data['Depth [m]'], data['Porosity'],bounds=(0, [1., 1., 0.5]))
print(popt)
plt.plot(data['Depth [m]'], data['Porosity'], 'b-', label='data')
plt.plot(data['Depth [m]'], func(data['Depth [m]'], *popt), 'r-', label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))

data1 = pd.read_csv('gleeson_fraction_gw_data.csv', skiprows=1)
popt1, pcov = curve_fit(func, data1['depth [m]'], data1['fraction'],bounds=(0, [0.2, 2., 0.5]))
print(popt1)
#plt.scatter(data1['depth [m]'], data['fraction'], label='data')
#plt.plot(data1['depth [m]'].sort_values(), func(data1['depth [m]'].sort_values(), *popt1), 'r-', label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))

lower_depth_range = np.linspace(0,1750,8)
upper_depth_range = np.linspace(250,2000,8)
for ix, y in enumerate(lower_depth_range):
    print(frac_func(lower_depth_range[ix],upper_depth_range[ix], *popt))
    print(frac_func(lower_depth_range[ix],upper_depth_range[ix], *popt1))
    
    
# Load original data from figure 1 of McMahon & Parnell
mp_data = pd.read_csv('terrestrial_deep_subsurface_prok_cell_num.csv',skiprows=1)

# Define depth bins every 250 meter 
bins = np.linspace(0,2000,9)

# Filter deeper then 2km
mp_data_filt = mp_data[mp_data['Depth [m]'] < 2000]

# Bin data based on depth bins
mp_data_filt['Depth bin'] = pd.cut(mp_data_filt['Depth [m]'],bins)
depth_binned = mp_data_filt.groupby('Depth bin')

# Calculate the mean concentration at each depth bin
bin_mean = depth_binned['Cell concentration [cells mL-1]'].mean().dropna()
bin_geo_mean = depth_binned['Cell concentration [cells mL-1]'].apply(gmean)

def depth_func(x,a,b):
    return np.exp(-(x-a)/b)
#xdata = bins[1:-1]-125
#popt2, pcov2 = curve_fit(depth_func, xdata, bin_mean,bounds= ([100,100],[10000,10000]))
#plt.figure()
#plt.semilogy(xdata,bin_mean,'.')
#plt.semilogy(xdata,depth_func(bins[1:-1]-125, *popt2),'r')
#print(popt2)
#
#residuals = bin_mean- depth_func(xdata, *popt2)
#ss_res = np.sum(residuals**2)
#ss_tot = np.sum((bin_mean-np.mean(bin_mean))**2)
#r_squared = 1 - (ss_res / ss_tot)
#print(r_squared)
#

def depth_func_log(x, a, b):
    return np.log(a) - b*x

xdata = bins[1:-1]-125
#popt2, pcov2 = curve_fit(depth_func, xdata, bin_geo_mean[:-1],bounds= ([100,100],[10000,10000]))
popt2, pcov2 = curve_fit(depth_func_log, xdata, np.log(bin_geo_mean[:-1]))
#popt2, pcov2 = curve_fit(depth_func_log, xdata, np.log(bin_mean),bounds= ([0,0],[1000000,1]))
plt.figure()
plt.semilogy(xdata,bin_geo_mean[:-1],'.')
plt.semilogy(xdata,np.exp(depth_func_log(xdata, *popt2)),'r')
#plt.semilogy(xdata,np.exp(depth_func(np.log(xdata), *popt2)),'r')
print(popt2)
mp_func = lambda x: np.exp(-(x-5771.2)/390.6)
#plt.semilogy(xdata,mp_func(xdata),'r')
residuals = np.log(bin_geo_mean[:-1])- depth_func_log(xdata, *popt2)
ss_res = np.sum(residuals**2)
ss_tot = np.sum((np.log(bin_geo_mean[:-1])-np.log(np.mean(bin_geo_mean[:-1])))**2)
r_squared = 1 - (ss_res / ss_tot)
print(r_squared)

residuals = np.log(bin_mean)- np.log(mp_func(xdata))
ss_res = np.sum(residuals**2)
ss_tot = np.sum((np.log(bin_mean)-np.log(np.mean(bin_mean)))**2)
r_squared = 1 - (ss_res / ss_tot)
print(r_squared)

plt.figure()
plt.plot(xdata,np.log(bin_mean),'.')
plt.plot(xdata,np.log(mp_func(xdata)))