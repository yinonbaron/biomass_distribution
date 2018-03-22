# -*- coding: utf-8 -*-
"""
Created on Tue May 16 13:51:01 2017

@author: yinonbaron
"""

import matplotlib.pyplot as plt
import numpy as np

data = np.array([[0.04,0.007],
        [0,0.1],
        [0,0.05]
        ])
fig, ax = plt.subplots(nrows=1)
p1 = plt.bar([0.1,1.1],data[0,:],0.8,color='#ff282d')
p2 = plt.bar([0.1,1.1],data[1,:],0.8,bottom=data[0,:],color='#b04e2d')
p3 = plt.bar([0.1,1.1],data[2,:],0.8,bottom=data[1,:]+data[0,:],color='#4250ff')


plt.xticks([0.5,1.], ('100,000 BP', 'present'))
plt.legend((p1[0], p2[0],p3[0]), ('Wild mammals', 'Livestock','Humans'),loc='upper left')
plt.ylabel('Biomass (Gt C)')



ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
plt.show()