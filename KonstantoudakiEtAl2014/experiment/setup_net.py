from netpyne import specs, sim
import random
from itertools import repeat

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

netParams.popParams['PYR_pop'] = {'cellModel': 'PYR_cell', 'cellType': 'PYR',  'numCells': pcells}
netParams.popParams['FSin_pop'] = {'cellModel': 'FS_cell', 'cellType': 'FSin',  'numCells': fscells}
netParams.popParams['RSin_pop'] = {'cellModel': 'RS_cell', 'cellType': 'RSin',  'numCells': rscells}
netParams.popParams['ISin_pop'] = {'cellModel': 'IS_cell', 'cellType': 'ISin',  'numCells': iscells}

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

netParams.importCellParams(
        label='RSin',
        conds={'cellType': 'RSin', 'cellModel': 'RS_cell'},
        fileName='cb.hoc',
        cellName='CBcell',
        importSynMechs=True)

netParams.importCellParams(
        label='ISin',
        conds={'cellType': 'ISin', 'cellModel': 'IS_cell'},
        fileName='cr.hoc',
        cellName='CRcell',
        importSynMechs=True)

print(netParams.cellParams.keys())

netParams.synMechParams['AMPA'] = {'mod': 'GLU'}
netParams.synMechParams['AMPAIN'] = {'mod': 'GLUIN'}
netParams.synMechParams['GABAA'] = {'mod': 'GABAa'}
netParams.synMechParams['GABAIN'] = {'mod': 'GABAain'}
netParams.synMechParams['NMDA'] = {'mod': 'NMDA'}
netParams.synMechParams['NMDAIN'] = {'mod': 'NMDAIN'}
netParams.synMechParams['GABAB'] = {'mod': 'GABAb'}

netParams.defaultThreshold = -20

# autapses
# ampa random seed = 3, nmda random seed = 124
random.seed(3)
ampa_delay = random.gauss(0.96, 0.11)
random.seed(124)
nmda_delay = random.gauss(1.33, 0.13)
netParams.connParams['autapses'] = {
        'preConds': {'pop': 'PYR_pop'},
        'postConds': {'pop': 'PYR_pop'},
        'sec': 'dend_0',
        'synMech': ['AMPA', 'NMDA'],
        # 'weight': list(repeat([list(repeat(ampaweight, automaxsyn)), list(repeat(nmdaweight, automaxsyn))], 16)),
        'weight': list(repeat([ampaweight, nmdaweight], 16)),
        'synsPerConn': automaxsyn,
        # 'delay': list(repeat([list(repeat(random.gauss(0.96, 0.11), automaxsyn)),
        #                         list(repeat(random.gauss(1.33, 0.13), automaxsyn))], 16)),
        'delay': list(repeat(['normal(0.96, 0.11)', 'normal(1.33, 0.13)'], 16)),
        # 'delay': list(repeat([ampa_delay, nmda_delay], 16)),
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
        # 'weight': [list(repeat(ampaweight, maxsyn)), list(repeat(nmdaweight, maxsyn))],
        'weight': [ampaweight, nmdaweight],
        'synsPerConn': maxsyn,
        # 'delay': [5, 5],
        # 'delay': [list(repeat(random.gauss(0.96, 0.11), maxsyn)), list(repeat(random.gauss(1.33, 0.13), maxsyn))]
        # 'delay': ['normal(0.96, 0.11)', 'normal(1.33, 0.13)']
        'delay': [ampa_delay, nmda_delay]
}

# IN-IN
# random seed = -100
random.seed(-100)
gabain_delay = random.gauss(1.76, 0.07)
netParams.connParams['FSin->FSin'] = {
        'preConds': {'pop': 'FSin_pop'},
        'postConds': {'pop': 'FSin_pop'},
        'sec': 'soma',
        'synMech': ['GABAIN'],
        # 'weight': list(repeat(autogabaweight, maxsyn1)),
        'weight': autogabaweight,
        'synsPerConn': maxsyn1,
        # 'delay': [5],
        # 'delay': list(repeat(random.gauss(1.76, 0.07), maxsyn1))
        'delay': 'normal(1.76, 0.07)'
        # 'delay': gabain_delay
}

# PC-IN
# random seed = 0
random.seed(0)
ampain_delay = random.gauss(0.6, 0.2)
nmdain_delay = random.gauss(0.6, 0.2)
netParams.connParams['PYR->FSin'] = {
        'preConds': {'pop': 'PYR_pop'},
        'postConds': {'pop': 'FSin_pop'},
        'sec': 'dend',
        'synMech': ['AMPAIN', 'NMDAIN'],
        # 'weight': [list(repeat(ampaweightin, maxsyn2)), list(repeat(nmdaweightin, maxsyn2))],
        'weight': [ampaweightin, nmdaweightin],
        'synsPerConn': maxsyn2,
        # 'delay': [5, 5],
        # 'delay': [list(repeat(random.gauss(0.6, 0.2), maxsyn2)), list(repeat(random.gauss(0.6, 0.2), maxsyn2))]
        # 'delay': ['normal(0.6, 0.2)', 'normal(0.6, 0.2)']
        'delay': [ampain_delay, nmdain_delay]
}

# IN-PC soma
# random seed = 0
netParams.connParams['FSin->PYR'] = {
        'preConds': {'pop': 'FSin_pop'},
        'postConds': {'pop': 'PYR_pop'},
        'sec': 'soma',
        'synMech': ['GABAA', 'GABAB'],
        # 'weight': [list(repeat(gabaweight, maxsyn3)), list(repeat(gabaweightb, maxsyn3))],
        'weight': [gabaweight, gabaweightb],
        'synsPerConn': maxsyn3,
        # 'delay': [5, 5],
        # 'delay': [list(repeat(random.gauss(1.8, 0.8), maxsyn3)), list(repeat(random.gauss(1.8, 0.8), maxsyn3))]
        # 'delay': ['normal(1.8, 0.8)', 'normal(1.8, 0.8)']
        'delay': [random.gauss(1.8, 0.8), random.gauss(1.8, 0.8)]
}

# IN-PC dend1
# random seed = 0
netParams.connParams['FSin->PYR'] = {
        'preConds': {'pop': 'FSin_pop'},
        'postConds': {'pop': 'PYR_pop'},
        'sec': 'dend_1',
        'synMech': ['GABAA', 'GABAB'],
        # 'weight': [list(repeat(gabaweight, maxsyn4)), list(repeat(gabaweightb, maxsyn4))],
        'weight': [gabaweight, gabaweightb],
        'synsPerConn': maxsyn4,
        # 'delay': [5, 5],
        # 'delay': [list(repeat(random.gauss(1.8, 0.8), maxsyn4)), list(repeat(random.gauss(1.8, 0.8), maxsyn4))]
        # 'delay': ['normal(1.8, 0.8)', 'normal(1.8, 0.8)']
        'delay': [random.gauss(1.8, 0.8), random.gauss(1.8, 0.8)]
}

# PC-CB
# random seed = 0
netParams.connParams['PYR->RSin'] = {
        'preConds': {'pop': 'PYR_pop'},
        'postConds': {'pop': 'RSin_pop'},
        'sec': 'dend',
        'synMech': ['AMPAIN', 'NMDA'],
        # 'weight': [list(repeat(ampaweightcb, maxsyn5)), list(repeat(nmdaweightcb, maxsyn5))],
        'weight': [ampaweightcb, nmdaweightcb],
        'synsPerConn': maxsyn5,
        # 'delay': [5, 5],
        # 'delay': [list(repeat(random.gauss(0.6, 0.2), maxsyn5)), list(repeat(random.gauss(0.6, 0.2), maxsyn5))]
        # 'delay': ['normal(0.6, 0.2)', 'normal(0.6, 0.2)']
        'delay': [ampain_delay, nmdain_delay]
}

# PC-CR
# random seed = 0
netParams.connParams['PYR->ISin'] = {
        'preConds': {'pop': 'PYR_pop'},
        'postConds': {'pop': 'ISin_pop'},
        'sec': 'dend_0',
        'synMech': ['AMPAIN', 'NMDA'],
        # 'weight': [list(repeat(ampaweightcr, maxsyn6)), list(repeat(nmdaweightcr, maxsyn6))],
        'weight': [ampaweightcr, nmdaweightcr],
        'synsPerConn': maxsyn6,
        # 'delay': [5, 5],
        # 'delay': [list(repeat(random.gauss(0.6, 0.2), maxsyn6)), list(repeat(random.gauss(0.6, 0.2), maxsyn6))]
        # 'delay': ['normal(0.6, 0.2)', 'normal(0.6, 0.2)']
        'delay': [ampain_delay, nmdain_delay]
}

# CR-CB
# random seed = 0
gabaa_delay = random.gauss(1.8, 0.8)
netParams.connParams['ISin->RSin'] = {
        'preConds': {'pop': 'ISin_pop'},
        'postConds': {'pop': 'RSin_pop'},
        'sec': 'dend',
        'synMech': ['GABAA'],
        # 'weight': list(repeat(gabaweightcrcb, maxsyn7)),
        'weight': gabaweightcrcb,
        'synsPerConn': maxsyn7,
        # 'delay': [5],
        # 'delay': list(repeat(random.gauss(1.8, 0.8), maxsyn7))
        'delay': 'normal(1.8, 0.8)'
        # 'delay': gabaa_delay
}

# CB-PC
# random seed = 0
netParams.connParams['RSin->PYR'] = {
        'preConds': {'pop': 'RSin_pop'},
        'postConds': {'pop': 'PYR_pop'},
        'sec': 'dend_2',
        'synMech': ['GABAA'],
        # 'weight': list(repeat(gabaweightcb, maxsyn8)),
        'weight': gabaweightcb,
        'synsPerConn': maxsyn8,
        # 'delay': [5],
        # 'delay': list(repeat(random.gauss(1.8, 0.8), maxsyn8))
        'delay': 'normal(1.8, 0.8)'
        # 'delay': gabaa_delay
}

# CR-PC
# random seed = 0
netParams.connParams['ISin->PYR'] = {
        'preConds': {'pop': 'ISin_pop'},
        'postConds': {'pop': 'PYR_pop'},
        'sec': 'dend_2',
        'synMech': ['GABAA'],
        # 'weight': list(repeat(gabaweightcr, maxsyn9)),
        'weight': gabaweightcr,
        'synsPerConn': maxsyn9,
        # 'delay': [5],
        # 'delay': list(repeat(random.gauss(1.8, 0.8), maxsyn9))
        'delay': 'normal(1.8, 0.8)'
        # 'delay': gabaa_delay
}

netParams.stimSourceParams['ns1'] = {
        'type': 'NetStim',
        # 'rate': 100,
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

simConfig.duration = 1000
simConfig.dt = 0.025
simConfig.verbose = False
simConfig.recordTraces = {'V_soma': {'sec': 'soma', 'loc': 0.5, 'var': 'v'}}
simConfig.recordStep = 1
simConfig.savePickle = False
simConfig.analysis['plotRaster'] = {'orderInverse': True, 'saveFig': 'output/raster.png'}
simConfig.analysis['plotTraces'] = {'include': ['PYR_pop', 'FSin_pop', 'RSin_pop', 'ISin_pop'], 'saveFig': 'output/traces.png'}

sim.createSimulateAnalyze(netParams=netParams, simConfig=simConfig)

# sa = sim.analysis
# sa.plotTraces()
