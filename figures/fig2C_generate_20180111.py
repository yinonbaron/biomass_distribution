# -*- coding: utf-8 -*-
"""
Created on Wed May 17 10:29:39 2017

@author: yinonbaron
"""

# -*- coding: utf-8 -*-
"""
Created on Tue May 16 13:51:01 2017

@author: yinonbaron
"""

import matplotlib.pyplot as plt
import numpy as np

data = np.array([[450,0.36,0], 
                 [12,0.6,0.6],
                 [1.6,1.8,0.6],
                 [0.6,1.9,0],
                 [8,1.5,65],
                 [1,0.3,7]
                 ])
norm_data = data/np.matrix(data.sum(axis=1)).T
fig, ax = plt.subplots(nrows=1)
p1 = plt.barh(np.arange(6.1,0.1,-1),norm_data[:,0],color='#9f764d')
p2 = plt.barh(np.arange(6.1,0.1,-1),norm_data[:,1],left=norm_data[:,0], color='#2a66ff')
p3 = plt.barh(np.arange(6.1,0.1,-1),norm_data[:,2],left=norm_data[:,0]+norm_data[:,1], color='#373737')


plt.yticks(np.arange(6.5,0.5,-1), ('plants', 'Fungi', 'Protists','Animals', 'Bacteria','Archaea'))
plt.legend((p1[0], p2[0],p3[0]), ('Terrestrial', 'Marine','Deep Subsurface'),loc='upper left')

plt.xlabel('Fraction of biomass')


ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)

ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')

plt.show()