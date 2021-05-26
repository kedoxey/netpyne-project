from netpyne import specs, sim
from netpyne.specs.simConfig import SimConfig

# weight params
ampaweightpr = 0.00008
ampaweight = 0.000065
ampaweightin = 0.000085
gabaweight = 0.00083
gabaweightb = gabaweight*0.35
gabaweightcrcb = 0.0083*0.25
gabaweightcb = 0.0006*1.5
gabaweightcr = 0.00087*3
autogabaweight = 0.0073*0.35
nmdaweight = ampaweight*21.5
nmdaweightin = ampaweightin*0.52
ampaweightcb = 0.000029
nmdaweightcb = ampaweightcb*0.86
ampaweightcr = 0.000046
nmdaweightcr = ampaweightcr*2.2

# number of synapses
inmaxsyn = 120          # initial stim
maxsyn = 24             # PC-PC
automaxsyn = 8          # autapses
maxsyn1 = 1             # IN-IN
maxsyn2 = 12            # PC-IN 
maxsyn3 = 15            # IN-PC soma
maxsyn4 = 15            # IN-PC dend1
maxsyn5 = 14            # PC-CB
maxsyn6 = 7             # PC-CR
maxsyn7 = 2             # CR-CB
maxsyn8 = 12            # CB-PC
maxsyn9 = 10            # CR-PC

# number of cells
pcells = 16
fscells = 2
rscells = 1
iscells = 1

netParams = specs.NetParams()  # object of class NetParams to store the network parameters
simConfig = specs.SimConfig() 

netParams.importCellParams(
        label='PYR',
        conds={'cellType': 'PYR', 'cellModel': 'Pcell'},
        fileName='pfc_pc_temp.hoc',
        cellName='Pcell',
        importSynMechs=True)

netParams.importCellParams(
        label='FSin',
        conds={'cellType': 'FSin', 'cellModel': 'INcell'},
        fileName='incell.hoc',
        cellName='INcell',
        importSynMechs=True)

netParams.importCellParams(
        label='RSin',
        conds={'cellType': 'RSin', 'cellModel': 'CBcell'},
        fileName='cb.hoc',
        cellName='CBcell',
        importSynMechs=True)

netParams.importCellParams(
        label='ISin',
        conds={'cellType': 'ISin', 'cellModel': 'CRcell'},
        fileName='cr.hoc',
        cellName='CRcell',
        importSynMechs=True)

print(netParams.cellParams.keys())

netParams.popParams['PYR_pop'] = {'cellModel': 'Pcell', 'cellType': 'PYR',  'numCells': pcells}
netParams.popParams['FSin_pop'] = {'cellModel': 'INcell', 'cellType': 'FSin',  'numCells': fscells}
netParams.popParams['RSin_pop'] = {'cellModel': 'CBcell', 'cellType': 'RSin',  'numCells': rscells}
netParams.popParams['ISin_pop'] = {'cellModel': 'CRcell', 'cellType': 'ISin',  'numCells': iscells}

netParams.synMechParams['AMPA'] = {'mod': 'GLU', 'Cmax': 1.0, 'Cdur': 0.3, 'Alpha': 10, 'Beta': 0.11, 'Erev': 0}
netParams.synMechParams['AMPAIN'] = {'mod': 'GLUIN', 'Cmax': 1.0, 'Cdur': 0.3, 'Alpha': 10, 'Beta': 0.18, 'Erev': 0}
netParams.synMechParams['GABAA'] = {'mod': 'GABAa', 'Cmax': 1.0, 'Cdur': 1.0, 'Alpha': 5, 'Beta': 0.18, 'Erev': -80}
netParams.synMechParams['GABAIN'] = {'mod': 'GABAain', 'Cmax': 1.0, 'Cdur': 1.0, 'Alpha': 5, 'Beta': 0.18, 'Erev': -80}
netParams.synMechParams['NMDA'] = {'mod': 'NMDA', 'Cmax': 1.0, 'Cdur': 0.3, 'Alpha': 4, 'Beta': 0.015, 'e': 0, 'mg': 1.0}
netParams.synMechParams['NMDAIN'] = {'mod': 'NMDAIN', 'Cmax': 1.0, 'Cdur': 0.3, 'Alpha': 4, 'Beta': 0.02, 'e': 0, 'mg': 1.0}
netParams.synMechParams['GABAB'] = {'mod': 'GABAb', 'Cmax': 10, 'Cdur': 10, 'Alpha': 0.001, 'Beta': 0.0047, 'Erev': -80}

netParams.defaultThreshold = -20

# autapses
# ampa random seed = 3, nmda random seed = 124
netParams.connParams['autapses'] = {
        'preConds': {'pop': 'PYR_pop'},
        'postConds': {'pop': 'PYR_pop'},
        'sec': 'dend_0',
        'synMech': ['AMPA', 'NMDA'],
        'weight': [ampaweight, nmdaweight],
        'delay': [5, 5],  # ['normal(0.96, 0.11)','normal(1.33, 0.13)'],
        'probability': maxsyn / (pcells * pcells),
        'connList': [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 9],
                     [10, 10], [11, 11], [12, 12], [13, 13], [14, 14], [15, 15]]
}

# PC-PC
# in net.hoc, $1 = 0
# ampa random seed = 3, nmda random seed = 124
netParams.connParams['PYR-> PYR'] = {  # S -> M
        'preConds': {'pop': 'PYR_pop'},
        'postConds': {'pop': 'PYR_pop'},
        'sec': 'dend_0',
        'synMech': ['AMPA', 'NMDA'],
        'weight': [ampaweight, nmdaweight],
        'delay': [5, 5],  # ['normal(0.96, 0.11)','normal(1.33, 0.13)'],
        'probability': maxsyn/(pcells*pcells)
}

# IN-IN
# random seed = -100
netParams.connParams['FSin->FSin'] = {
        'preConds': {'pop': 'FSin_pop'},
        'postConds': {'pop': 'FSin_pop'},
        'sec': 'soma',
        'synMech': ['GABAIN'],
        'weight': [autogabaweight],
        'delay': [5],  # ['normal(1.76, 0.07)'],
        'probability': maxsyn1 / (fscells * fscells)
}

# PC-IN
# random seed = 0
netParams.connParams['PYR->FSin'] = {
        'preConds': {'pop': 'PYR_pop'},
        'postConds': {'pop': 'FSin_pop'},
        'sec': 'dend',
        'synMech': ['AMPAIN', 'NMDAIN'],
        'weight': [ampaweightin, nmdaweightin],
        'delay': [5, 5],  # ['normal(0.6, 0.2)','normal(0.6, 0.2)'],
        'probability': maxsyn2 / (pcells * fscells)
}

# IN-PC soma
# random seed = 0
netParams.connParams['FSin->PYR'] = {
        'preConds': {'pop': 'FSin_pop'},
        'postConds': {'pop': 'PYR_pop'},
        'sec': 'soma',
        'synMech': ['GABAA', 'GABAB'],
        'weight': [gabaweight, gabaweightb],
        'delay': [5, 5],  # ['normal(1.8, 0.8)','normal(1.8, 0.8)'],
        'probability': maxsyn3 / (fscells * pcells)
}

# IN-PC dend1
# random seed = 0
netParams.connParams['FSin->PYR'] = {
        'preConds': {'pop': 'FSin_pop'},
        'postConds': {'pop': 'PYR_pop'},
        'sec': 'dend_1',
        'synMech': ['GABAA', 'GABAB'],
        'weight': [gabaweight, gabaweightb],
        'delay': [5, 5],  # ['normal(1.8, 0.8)','normal(1.8, 0.8)'],
        'probability': maxsyn4 / (fscells * pcells)
}

# PC-CB
# random seed = 0
netParams.connParams['PYR->RSin'] = {
        'preConds': {'pop': 'PYR_pop'},
        'postConds': {'pop': 'RSin_pop'},
        'sec': 'dend',
        'synMech': ['AMPAIN', 'NMDA'],
        'weight': [ampaweightcb, nmdaweightcb],
        'delay': [5, 5],  # ['normal(0.6, 0.2)','normal(0.6, 0.2)'],
        'probability': maxsyn5 / (pcells * rscells)
}

# PC-CR
# random seed = 0
netParams.connParams['PYR->ISin'] = {
        'preConds': {'pop': 'PYR_pop'},
        'postConds': {'pop': 'ISin_pop'},
        'sec': 'dend_0',
        'synMech': ['AMPAIN', 'NMDA'],
        'weight': [ampaweightcr, nmdaweightcr],
        'delay': [5, 5],  # ['normal(0.6, 0.2)','normal(0.6, 0.2)'],
        'probability': maxsyn6 / (pcells * iscells)
}

# CR-CB
# random seed = 0
netParams.connParams['ISin->RSin'] = {
        'preConds': {'pop': 'ISin_pop'},
        'postConds': {'pop': 'RSin_pop'},
        'sec': 'dend',
        'synMech': ['GABAA'],
        'weight': [gabaweightcrcb],
        'delay': [5],  # ['normal(1.8, 0.8)''],
        'probability': maxsyn7 / (iscells * rscells)
}

# CB-PC
# random seed = 0
netParams.connParams['RSin->PYR'] = {
        'preConds': {'pop': 'RSin_pop'},
        'postConds': {'pop': 'PYR_pop'},
        'sec': 'dend_2',
        'synMech': ['GABAA'],
        'weight': [gabaweightcb],
        'delay': [5],  # ['normal(1.8, 0.8)''],
        'probability': maxsyn8 / (rscells * pcells)
}

# CR-PC
# random seed = 0
netParams.connParams['ISin->PYR'] = {
        'preConds': {'pop': 'ISin_pop'},
        'postConds': {'pop': 'PYR_pop'},
        'sec': 'dend_2',
        'synMech': ['GABAA'],
        'weight': [gabaweightcr],
        'delay': [5],  # ['normal(1.8, 0.8)''],
        'probability': maxsyn9 / (iscells * pcells)
}

# TODO: add stimulus
netParams.stimSourceParams['ns1'] = {
        'type': 'NetStim',
        'rate': 10,
        'noise': 0
}
netParams.stimTargetParams['nc1'] = {
        'source': 'ns1',
        'conds': {'cellModel': 'Pcell'},
        'synMech': 'AMPA',
        'weight': ampaweightpr,
        'delay': 500,
        'sec': 'dend_1',
        'loc': 'uniform(0,1)'
}
netParams.stimTargetParams['nc2'] = {
        'source': 'ns1',
        'conds': {'cellModel': 'Pcell'},
        'synMech': 'NMDA',
        'weight': ampaweightpr*5,
        'delay': 500,
        'sec': 'dend_1',
        'loc': 'uniform(0,1)'
}

simConfig.duration = 1*1e3
simConfig.dt = 0.025
simConfig.verbose = False
simConfig.recordTraces = {'V_soma': {'sec': 'soma', 'loc': 0.5, 'var': 'v'}}
simConfig.recordStep = 1
simConfig.savePickle = False
simConfig.analysis['plotRaster'] = {'orderInverse': True, 'saveFig': 'tut_import_raster.png'} 
simConfig.analysis['plotTraces'] = {'include': ['pyr_pop']}   

sim.createSimulateAnalyze(netParams=netParams, simConfig=simConfig)
