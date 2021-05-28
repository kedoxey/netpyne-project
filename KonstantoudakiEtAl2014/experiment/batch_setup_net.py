from netpyne import specs, sim
from cfg_net import cfg

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

# -------------------- PC-PC AMPA --------------------
netParams.connParams['PYR->PYR-AMPA'] = {
        'preConds': {'pop': 'PYR_pop'},
        'postConds': {'pop': 'PYR_pop'},
        'sec': 'dend_0',
        'synMech': 'AMPA',
        'weight': cfg.ampaweight,
        'synsPerConn': maxsyn,
        'delay': cfg.delayPcAMPA
}
# -------------------- PC-PC NMDA --------------------
netParams.connParams['PYR-> PYR-NMDA'] = {
        'preConds': {'pop': 'PYR_pop'},
        'postConds': {'pop': 'PYR_pop'},
        'sec': 'dend_0',
        'synMech': 'NMDA',
        'weight': cfg.nmdaweight,
        'synsPerConn': maxsyn,
        'delay': cfg.delayPcNMDA
}

# -------------------- IN-IN --------------------
netParams.connParams['FSin->FSin'] = {
        'preConds': {'pop': 'FSin_pop'},
        'postConds': {'pop': 'FSin_pop'},
        'sec': 'soma',
        'synMech': 'GABAIN',
        'weight': cfg.autogabaweight,
        'synsPerConn': maxsyn1,
        'delay': cfg.delayFs
}

# -------------------- PC-IN AMPAin --------------------
netParams.connParams['PYR->FSin-AMPAin'] = {
        'preConds': {'pop': 'PYR_pop'},
        'postConds': {'pop': 'FSin_pop'},
        'sec': 'dend',
        'synMech': 'AMPAIN',
        'weight': cfg.ampaweightin,
        'synsPerConn': maxsyn2,
        'delay': cfg.delayPcInAMPA
}
# -------------------- PC-IN NMDAin --------------------
netParams.connParams['PYR->FSin-NMDAin'] = {
        'preConds': {'pop': 'PYR_pop'},
        'postConds': {'pop': 'FSin_pop'},
        'sec': 'dend',
        'synMech': 'NMDAIN',
        'weight': cfg.nmdaweightin,
        'synsPerConn': maxsyn2,
        'delay': cfg.delayPcInNMDA
}

# -------------------- IN-PC soma GABAa --------------------
netParams.connParams['FSin->PYR-GABAa'] = {
        'preConds': {'pop': 'FSin_pop'},
        'postConds': {'pop': 'PYR_pop'},
        'sec': 'soma',
        'synMech': 'GABAA',
        'weight': cfg.gabaweight,
        'synsPerConn': maxsyn3,
        'delay': cfg.delayInPcGABAa
}
# -------------------- IN-PC soma GABAb --------------------
netParams.connParams['FSin->PYR-GABAb'] = {
        'preConds': {'pop': 'FSin_pop'},
        'postConds': {'pop': 'PYR_pop'},
        'sec': 'soma',
        'synMech': 'GABAB',
        'weight': cfg.gabaweightb,
        'synsPerConn': maxsyn3,
        'delay': cfg.delayInPcGABAb
}

# -------------------- IN-PC dend1 GABAa --------------------
netParams.connParams['FSin->PYR-GABAa'] = {
        'preConds': {'pop': 'FSin_pop'},
        'postConds': {'pop': 'PYR_pop'},
        'sec': 'dend_1',
        'synMech': 'GABAA',
        'weight': cfg.gabaweight,
        'synsPerConn': maxsyn4,
        'delay': cfg.delayInPcGABAa
}
# -------------------- IN-PC dend1 GABAb --------------------
netParams.connParams['FSin->PYR-GABAb'] = {
        'preConds': {'pop': 'FSin_pop'},
        'postConds': {'pop': 'PYR_pop'},
        'sec': 'dend_1',
        'synMech': 'GABAB',
        'weight': cfg.gabaweightb,
        'synsPerConn': maxsyn4,
        'delay': cfg.delayInPcGABAb
}

# -------------------- PC-CB AMPAin --------------------
netParams.connParams['PYR->RSin-AMPAin'] = {
        'preConds': {'pop': 'PYR_pop'},
        'postConds': {'pop': 'RSin_pop'},
        'sec': 'dend',
        'synMech': 'AMPAIN',
        'weight': cfg.ampaweightcb,
        'synsPerConn': maxsyn5,
        'delay': cfg.delayPcCbAMPA
}
# -------------------- PC-CB NMDA --------------------
netParams.connParams['PYR->RSin-NMDA'] = {
        'preConds': {'pop': 'PYR_pop'},
        'postConds': {'pop': 'RSin_pop'},
        'sec': 'dend',
        'synMech': 'NMDA',
        'weight': cfg.nmdaweightcb,
        'synsPerConn': maxsyn5,
        'delay': cfg.delayPcCbNMDA
}

# -------------------- PC-CR AMPAin --------------------
netParams.connParams['PYR->ISin-AMPAin'] = {
        'preConds': {'pop': 'PYR_pop'},
        'postConds': {'pop': 'ISin_pop'},
        'sec': 'dend_0',
        'synMech': 'AMPAIN',
        'weight': cfg.ampaweightcr,
        'synsPerConn': maxsyn6,
        'delay': cfg.delayPcCrAMPA
}
# -------------------- PC-CR NMDA --------------------
netParams.connParams['PYR->ISin-NMDA'] = {
        'preConds': {'pop': 'PYR_pop'},
        'postConds': {'pop': 'ISin_pop'},
        'sec': 'dend_0',
        'synMech': 'NMDA',
        'weight': cfg.nmdaweightcr,
        'synsPerConn': maxsyn6,
        'delay': cfg.delayPcCrNMDA
}

# -------------------- CR-CB --------------------
netParams.connParams['ISin->RSin'] = {
        'preConds': {'pop': 'ISin_pop'},
        'postConds': {'pop': 'RSin_pop'},
        'sec': 'dend',
        'synMech': 'GABAA',
        'weight': cfg.gabaweightcrcb,
        'synsPerConn': maxsyn7,
        'delay': cfg.delayCrCbGABAa
}

# -------------------- CB-PC --------------------
netParams.connParams['RSin->PYR'] = {
        'preConds': {'pop': 'RSin_pop'},
        'postConds': {'pop': 'PYR_pop'},
        'sec': 'dend_2',
        'synMech': 'GABAA',
        'weight': cfg.gabaweightcb,
        'synsPerConn': maxsyn8,
        'delay': cfg.delayCbPcGABAa
}

# -------------------- CR-PC --------------------
netParams.connParams['ISin->PYR'] = {
        'preConds': {'pop': 'ISin_pop'},
        'postConds': {'pop': 'PYR_pop'},
        'sec': 'dend_2',
        'synMech': 'GABAA',
        'weight': cfg.gabaweightcr,
        'synsPerConn': maxsyn9,
        'delay': cfg.delayCrPcGABAa
}

for gid in range(0, 16):
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
                'weight': cfg.ampaweightpr,
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
        'weight': cfg.ampaweightpr,
        'synsPerConn': inmaxsyn,
        'delay': 10,
        'sec': 'dend_1',
        'loc': 'uniform(0,1)'
}
netParams.stimTargetParams['nc2'] = {
        'source': 'ns1',
        'conds': {'cellType': 'PYR', 'cellModel': 'PYR_cell'},
        'synMech': 'NMDA',
        'weight': cfg.ampaweightpr*5,
        'synsPerConn': inmaxsyn,
        'delay': 10,
        'sec': 'dend_1',
        'loc': 'uniform(0,1)'
}
