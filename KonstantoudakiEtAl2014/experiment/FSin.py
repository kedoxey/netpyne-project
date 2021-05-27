#!/usr/bin/env python
# coding: utf-8

# In[1]:


from netpyne import specs, sim
import random
from itertools import repeat
# weight params
autogabaweight = 0.0073*0.35


netParams = specs.NetParams()  # object of class NetParams to store the network parameters
simConfig = specs.SimConfig()


# In[69]:


netParams.importCellParams(
        label='FSin',
        conds={'cellType': 'FSin', 'cellModel': 'FS_cell'},
        fileName='incell.hoc',
        cellName='INcell',
        importSynMechs=True)


# In[70]:


netParams.popParams['FSin_pop'] = {'cellModel': 'FS_cell', 'cellType': 'FSin',  'numCells': 2}


# In[123]:


netParams.synMechParams['GABAIN'] = {'mod': 'GABAain'}


# In[146]:


netParams.connParams['FSin_autapses'] = {
        'preConds': {'pop':'FSin_pop'},
        'postConds': {'pop': 'FSin_pop'},
        'sec': 'soma',
        'synMech': ['GABAIN'],
        'weight': 1,#autogabaweight,
        'synsPerConn': 1,
        'delay': random.gauss(1.76, 0.07),
'connList':[[0,1]]
    }


# In[147]:


simConfig.duration = 1000
simConfig.dt = 0.025
simConfig.verbose = False
simConfig.recordStep = 0.1
simConfig.savePickle = False
# Recording/plotting parameters
simConfig.recordTraces = {'V_soma':{'sec': 'soma','loc': 0.5,'var': 'v'},
                          'ca_soma': {'sec': 'soma', 'loc': 0.5, 'var': 'cai'},
                         'k_soma': {'sec': 'soma', 'loc': 0.5, 'var': 'ik'},
                         'na_soma': {'sec': 'soma', 'loc': 0.5, 'var': 'ina'},
                         
                         }
simConfig.recordStim = True
simConfig.analysis['plotTraces'] = {'include': ['allCells'],'saveFig':'plotTraces_output.png'}


# In[148]:


sim.createSimulateAnalyze(netParams=netParams, simConfig=simConfig)
sim.analysis.plotConn(feature='numConns',groupBy='cell',saveFig='plotConn.png')


# In[ ]:




