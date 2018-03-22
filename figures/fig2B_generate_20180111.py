# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 17:20:55 2016

@author: yinonbaron
"""
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.rc('xtick', labelsize=20) 
y = [0,0.8]
#x1 = np.array([1.3/7.,5.7/7.])
#x2 = np.array([450./500,50./500])
#l1 = 0.5-x1/2
#l2 = 0.5-x2/2


x1 = np.array([1.24,5.1])
x2 = np.array([450,22])
l1 = 4-x1/2.
l2 = 235-x2/2.

fig, axes = plt.subplots(nrows=2, sharey=True)
#axes[0].barh(y,x1, left=l1)
#axes[1].barh(y,x2, left=l2)
axes[0].barh(y,x1, left=0)
axes[1].barh(y,x2, left=0)

plt.xlabel('Gt C',fontsize=20)
axes[0].set_xlim([0,8])
axes[1].set_xlim([0,470])
plt.show()

