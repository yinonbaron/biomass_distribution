# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 17:20:55 2016

@author: yinonbaron
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib
from openpyxl import load_workbook
matplotlib.rc('xtick', labelsize=20) 
y = [0,0.8]
data = pd.read_excel('../results.xlsx','Fig2C')

with pd.ExcelWriter('../results.xlsx', engine='openpyxl') as writer:
        writer.book = load_workbook('../results.xlsx',data_only=True)
        writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)
    
        # Feed results to Table 1 & Fig1
        raw_data = pd.DataFrame(writer.sheets['Fig2C'].values)

#x1 = np.array([1.3/7.,5.7/7.])
#x2 = np.array([450./500,50./500])
#l1 = 0.5-x1/2
#l2 = 0.5-x2/2


x1 = np.array([1.26,4.91])
x2 = np.array([450,21.8])
l1 = 4-x1/2.
l2 = 235-x2/2.

fig, axes = plt.subplots(nrows=2, sharey=True)
#axes[0].barh(y,x1, left=l1)
#axes[1].barh(y,x2, left=l2)
axes[0].barh(y,x1, left=0)
axes[1].barh(y,x2, left=0)

plt.xlabel('Gt C',fontsize=20)
axes[0].set_xlim([0,8])
axes[1].set_xlim([0,480])
plt.show()

