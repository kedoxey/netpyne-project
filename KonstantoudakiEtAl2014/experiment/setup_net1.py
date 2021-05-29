import os
from netpyne import specs, sim


# GABA gain
GABAAgain = 1
GABABgain = 20

# GABA synsPerConn
GABAAsynsPerConn = 0
GABABsynsPerConn = 0


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
maxsyn1 = 1             # IN-IN GABAIN
maxsyn2 = 12            # PC-IN 
maxsyn3 = 15            # IN-PC soma GABA A+B
maxsyn4 = 15            # IN-PC dend1 GABA A+B
maxsyn5 = 14            # PC-CB
maxsyn6 = 7             # PC-CR
maxsyn7 = 2             # CR-CB GABA A+B
maxsyn8 = 12            # CB-PC GABA A+B
maxsyn9 = 10            # CR-PC GABA A+B

# number of cells
pcells = 16
fscells = 2
rscells = 1
iscells = 1


netParams = specs.NetParams()  # object of class NetParams to store the network parameters
simConfig = specs.SimConfig()

netParams.popParams['PYR_pop'] = {'cellModel': 'PYR_cell', 'cellType': 'PYR',  'numCells': pcells, 'ynormRange':[0.80,0.90]}
netParams.popParams['FSin_pop'] = {'cellModel': 'FS_cell', 'cellType': 'FSin',  'numCells': fscells, 'ynormRange':[0.9,0.95]}
netParams.popParams['RSin_pop'] = {'cellModel': 'RS_cell', 'cellType': 'RSin',  'numCells': rscells, 'ynormRange':[0.75,0.80]}
netParams.popParams['ISin_pop'] = {'cellModel': 'IS_cell', 'cellType': 'ISin',  'numCells': iscells, 'ynormRange':[0.70,0.75]}

netParams.importCellParams(
        label='PYR',
        conds={'cellType': 'PYR', 'cellModel': 'PYR_cell'},
        fileName='pfc_pc_temp.hoc',
        cellName='Pcell',
        importSynMechs=True)

netParams.importCellParams(
        label='FSin',
        conds={'cellType': 'FSin', 'cellModel': 'FS_cell'},
        fileName='incell.hoc',
        cellName='INcell',
        importSynMechs=True)
# netParams.cellParams.FSin.secs.soma.mechs.pas.e = -73

netParams.importCellParams(
        label='RSin',
        conds={'cellType': 'RSin', 'cellModel': 'RS_cell'},
        fileName='cb.hoc',
        cellName='CBcell',
        importSynMechs=True)
# netParams.cellParams.RSin.secs.soma.mechs.pas.e = -64

netParams.importCellParams(
        label='ISin',
        conds={'cellType': 'ISin', 'cellModel': 'IS_cell'},
        fileName='cr.hoc',
        cellName='CRcell',
        importSynMechs=True)
# netParams.cellParams.ISin.secs.soma.mechs.pas.e = -70

print(netParams.cellParams.keys())

netParams.synMechParams['AMPA'] = {'mod': 'GLU'}
netParams.synMechParams['AMPAIN'] = {'mod': 'GLUIN'}
netParams.synMechParams['GABAA'] = {'mod': 'GABAa'}
netParams.synMechParams['GABAIN'] = {'mod': 'GABAain'}
netParams.synMechParams['NMDA'] = {'mod': 'NMDA'}
netParams.synMechParams['NMDAIN'] = {'mod': 'NMDAIN'}
netParams.synMechParams['GABAB'] = {'mod': 'GABAb'}

netParams.defaultThreshold = -20

# -------------------- PC-PC AMPA --------------------
netParams.connParams['PYR->PYR-AMPA'] = {
        'preConds': {'pop': 'PYR_pop'},
        'postConds': {'pop': 'PYR_pop'},
        'sec': 'dend_0',
        'synMech': 'AMPA',
        'weight': ampaweight,
        'synsPerConn': maxsyn,
        'delay': 'normal(0.96, 0.11)'
}
# -------------------- PC-PC NMDA --------------------
netParams.connParams['PYR-> PYR-NMDA'] = {
        'preConds': {'pop': 'PYR_pop'},
        'postConds': {'pop': 'PYR_pop'},
        'sec': 'dend_0',
        'synMech': 'NMDA',
        'weight': nmdaweight,
        'synsPerConn': maxsyn,
        'delay': 'normal(1.33, 0.13)'
}

# -------------------- IN-IN --------------------
netParams.connParams['FSin->FSin'] = {
        'preConds': {'pop': 'FSin_pop'},
        'postConds': {'pop': 'FSin_pop'},
        'sec': 'soma',
        'synMech': 'GABAIN',
        'weight': autogabaweight,
        'synsPerConn': maxsyn1,
        'delay': 'normal(1.76, 0.07)'
}

# -------------------- PC-IN AMPAin --------------------
netParams.connParams['PYR->FSin-AMPAin'] = {
        'preConds': {'pop': 'PYR_pop'},
        'postConds': {'pop': 'FSin_pop'},
        'sec': 'dend',
        'synMech': 'AMPAIN',
        'weight': ampaweightin,
        'synsPerConn': maxsyn2,
        'delay': 'normal(0.6, 0.2)'
}
# -------------------- PC-IN NMDAin --------------------
netParams.connParams['PYR->FSin-NMDAin'] = {
        'preConds': {'pop': 'PYR_pop'},
        'postConds': {'pop': 'FSin_pop'},
        'sec': 'dend',
        'synMech': 'NMDAIN',
        'weight': nmdaweightin,
        'synsPerConn': maxsyn2,
        'delay': 'normal(0.6, 0.2)'
}

# -------------------- IN-PC soma GABAa --------------------
netParams.connParams['FSin->PYR-GABAa'] = {
        'preConds': {'pop': 'FSin_pop'},
        'postConds': {'pop': 'PYR_pop'},
        'sec': 'soma',
        'synMech': 'GABAA',
        'weight': gabaweight * GABAAgain,
        'synsPerConn': maxsyn3+GABAAsynsPerConn,
        'delay': 'normal(1.8, 0.8)'
}
# -------------------- IN-PC soma GABAb --------------------
netParams.connParams['FSin->PYR-GABAb'] = {
        'preConds': {'pop': 'FSin_pop'},
        'postConds': {'pop': 'PYR_pop'},
        'sec': 'soma',
        'synMech': 'GABAB',
        'weight': gabaweightb * GABABgain,
        'synsPerConn': maxsyn3+GABABsynsPerConn,
        'delay': 'normal(1.8, 0.8)'
}

# -------------------- IN-PC dend1 GABAa --------------------
netParams.connParams['FSin->PYR-GABAa'] = {
        'preConds': {'pop': 'FSin_pop'},
        'postConds': {'pop': 'PYR_pop'},
        'sec': 'dend_1',
        'synMech': 'GABAA',
        'weight': gabaweight * GABAAgain,
        'synsPerConn': maxsyn4+GABAAsynsPerConn,
        'delay': 'normal(1.8, 0.8)'
}
# -------------------- IN-PC dend1 GABAb --------------------
netParams.connParams['FSin->PYR-GABAb'] = {
        'preConds': {'pop': 'FSin_pop'},
        'postConds': {'pop': 'PYR_pop'},
        'sec': 'dend_1',
        'synMech': 'GABAB',
        'weight': gabaweightb * GABABgain,
        'synsPerConn': maxsyn4+GABABsynsPerConn,
        'delay': 'normal(1.8, 0.8)'
}

# -------------------- PC-CB AMPAin --------------------
netParams.connParams['PYR->RSin-AMPAin'] = {
        'preConds': {'pop': 'PYR_pop'},
        'postConds': {'pop': 'RSin_pop'},
        'sec': 'dend',
        'synMech': 'AMPAIN',
        'weight': ampaweightcb,
        'synsPerConn': maxsyn5,
        'delay': 'normal(0.6, 0.2)'
}
# -------------------- PC-CB NMDA --------------------
netParams.connParams['PYR->RSin-NMDA'] = {
        'preConds': {'pop': 'PYR_pop'},
        'postConds': {'pop': 'RSin_pop'},
        'sec': 'dend',
        'synMech': 'NMDA',
        'weight': nmdaweightcb,
        'synsPerConn': maxsyn5,
        'delay': 'normal(0.6, 0.2)'
}

# -------------------- PC-CR AMPAin --------------------
netParams.connParams['PYR->ISin-AMPAin'] = {
        'preConds': {'pop': 'PYR_pop'},
        'postConds': {'pop': 'ISin_pop'},
        'sec': 'dend_0',
        'synMech': 'AMPAIN',
        'weight': ampaweightcr,
        'synsPerConn': maxsyn6,
        'delay': 'normal(0.6, 0.2)'
}
# -------------------- PC-CR NMDA --------------------
netParams.connParams['PYR->ISin-NMDA'] = {
        'preConds': {'pop': 'PYR_pop'},
        'postConds': {'pop': 'ISin_pop'},
        'sec': 'dend_0',
        'synMech': 'NMDA',
        'weight': nmdaweightcr,
        'synsPerConn': maxsyn6,
        'delay': 'normal(0.6, 0.2)'
}

# -------------------- CR-CB GABAa --------------------
netParams.connParams['ISin->RSin'] = {
        'preConds': {'pop': 'ISin_pop'},
        'postConds': {'pop': 'RSin_pop'},
        'sec': 'dend',
        'synMech': 'GABAIN',
        'weight': gabaweightcrcb,
        'synsPerConn': maxsyn7,
        'delay': 'normal(1.8, 0.8)'
}


# -------------------- CB-PC GABAa --------------------
netParams.connParams['RSin->PYR'] = {
        'preConds': {'pop': 'RSin_pop'},
        'postConds': {'pop': 'PYR_pop'},
        'sec': 'dend_2',
        'synMech': 'GABAA',
        'weight': gabaweightcb * GABAAgain,
        'synsPerConn': maxsyn8+GABAAsynsPerConn,
        'delay': 'normal(1.8, 0.8)'
}
# -------------------- CB-PC GABAb --------------------
netParams.connParams['RSin->PYR'] = {
        'preConds': {'pop': 'RSin_pop'},
        'postConds': {'pop': 'PYR_pop'},
        'sec': 'dend_2',
        'synMech': 'GABAB',
        'weight': gabaweightcb * 0.35 * GABABgain,
        'synsPerConn': maxsyn8+GABABsynsPerConn,
        'delay': 'normal(1.8, 0.8)'
}

# -------------------- CR-PC GABAa --------------------
netParams.connParams['ISin->PYR'] = {
        'preConds': {'pop': 'ISin_pop'},
        'postConds': {'pop': 'PYR_pop'},
        'sec': 'dend_2',
        'synMech': 'GABAA',
        'weight': gabaweightcr * GABAAgain,
        'synsPerConn': maxsyn9+GABAAsynsPerConn,
        'delay': 'normal(1.8, 0.8)'
}
# -------------------- CR-PC GABAb --------------------
netParams.connParams['ISin->PYR'] = {
        'preConds': {'pop': 'ISin_pop'},
        'postConds': {'pop': 'PYR_pop'},
        'sec': 'dend_2',
        'synMech': 'GABAB',
        'weight': gabaweightcr * 0.35 * GABABgain,
        'synsPerConn': maxsyn9+GABABsynsPerConn,
        'delay': 'normal(1.8, 0.8)'
}

for gid in range(0, pcells+fscells+rscells+iscells):
        netParams.stimSourceParams[f'noise_source-{gid}'] = {
                'type': 'NetStim',
                'rate': 100,
                'start': 0,
                'noise': 1
        }
        netParams.stimTargetParams[f'noise->{gid}'] = {
                'source': f'noise_source-{gid}',
                'conds': {'cellList': [gid]},
                'synMech': 'AMPA',
                'weight': ampaweightpr,
                'synsPerConn': 1,
                'delay': 5,
                'sec': 'soma',
                'loc': 'uniform(0, 1)'
        }

netParams.stimSourceParams['ns1'] = {
        'type': 'NetStim',
        'interval': 50,
        'number': 10,
        'start': 0,
        'noise': 0
}
netParams.stimTargetParams['nc1'] = {
        'source': 'ns1',
        'conds': {'cellType': 'PYR', 'cellModel': 'PYR_cell'},
        'synMech': 'AMPA',
        'weight': ampaweightpr,
        'synsPerConn': inmaxsyn,
        'delay': 10,
        'sec': 'dend_1',
        'loc': 'uniform(0,1)'
}
netParams.stimTargetParams['nc2'] = {
        'source': 'ns1',
        'conds': {'cellType': 'PYR', 'cellModel': 'PYR_cell'},
        'synMech': 'NMDA',
        'weight': ampaweightpr*5,
        'synsPerConn': inmaxsyn,
        'delay': 10,
        'sec': 'dend_1',
        'loc': 'uniform(0,1)'
}


simConfig.hParams['celsius'] = 34
simConfig.saveDataInclude=['netParams', 'netCells', 'netPops', 'simConfig' 'simData']
simConfig.saveTxt=True
simConfig.allowSelfConns = True
simConfig.duration = 1000
simConfig.dt = 0.025
simConfig.verbose = False
simConfig.recordTraces = {'V_soma': {'sec': 'soma', 'loc': 0.5, 'var': 'v'}}
simConfig.recordStep = 1
simConfig.savePickle = False

simConfig.analysis['plotRaster'] = {'orderInverse': True, 'saveFig': '/users/k1926552/Documents/FINAL/netpyne-project/KonstantoudakiEtAl2014/experiment/Results/raster.png','showFig':False}
simConfig.analysis['plotTraces'] = {'include': [('PYR_pop', [0]), ('FSin_pop', [0]), ('RSin_pop', [0]), ('ISin_pop', [0])],'oneFigPer': 'trace', 'overlay': False, 'saveFig': '/users/k1926552/Documents/FINAL/netpyne-project/KonstantoudakiEtAl2014/experiment/Results/traces.png','showFig':False}
simConfig.analysis['plotSpikeStats'] = {'saveFig': '/users/k1926552/Documents/FINAL/netpyne-project/KonstantoudakiEtAl2014/experiment/Results/spike-stats.png','showFig':False}

simConfig.analysis['plotConn'] = {'groupBy': 'cell', 'saveFig':'/users/k1926552/Documents/FINAL/netpyne-project/KonstantoudakiEtAl2014/experiment/Results/conn.png','showFig':False}


sim.createSimulateAnalyze(netParams=netParams, simConfig=simConfig)

