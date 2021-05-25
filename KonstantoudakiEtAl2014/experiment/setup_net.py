from netpyne import specs, sim

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
inmaxsyn = 120
maxsyn = 24
automaxsyn = 8
maxsyn1 = 1
maxsyn2 = 12
maxsyn3 = 15
maxsyn4 = 15
maxsyn5 = 14
maxsyn6 = 7
maxsyn7 = 2
maxsyn8 = 12
maxsyn9 = 10

netParams = specs.NetParams()  # object of class NetParams to store the network parameters
simConfig = specs.SimConfig() 

netParams.importCellParams(
        label='Pcell',
        conds={'cellType': 'Pyr_cell', 'cellModel': 'Pcell'},
        fileName='pfc_pc_temp.hoc',
        cellName='Pcell',
        importSynMechs=True)

netParams.importCellParams(
        label='INcell',
        conds={'cellType': 'FScell', 'cellModel': 'INcell'},
        fileName='incell.hoc',
        cellName='INcell',
        importSynMechs=True)

netParams.importCellParams(
        label='CRcell',
        conds={'cellType': 'IScell', 'cellModel': 'CRcell'},
        fileName='cr.hoc',
        cellName='CRcell',
        importSynMechs=True)

netParams.importCellParams(
        label='RScell',
        conds={'cellType': 'RScell', 'cellModel': 'CBcell'},
        fileName='cb.hoc',
        cellName='CBcell',
        importSynMechs=True)

print(netParams.cellParams.keys())

netParams.popParams['Pcell_pop'] = {'cellType': 'Pyr_cell', 'numCells': 16, 'cellModel': 'Pcell'}
netParams.popParams['INcell_pop'] = {'cellType': 'FScell', 'numCells': 2, 'cellModel': 'FScell'}
netParams.popParams['CRcell_pop'] = {'cellType': 'IScell', 'numCells': 1, 'cellModel': 'CRcell'}
netParams.popParams['CBcell_pop'] = {'cellType': 'RScell', 'numCells': 1, 'cellModel': 'CBcell'}

# TODO: add synMechs??
netParams.synMechParams['AMPA'] = {'mod': 'GLU', 'Cmax': 1.0, 'Cdur': 0.3, 'Alpha': 10, 'Beta': 0.11, 'Erev': 0}


# TODO: add connParams
netParams.connParams['Pcell_pop->INcell_pop'] = {    
        'preConds': {'pop': 'Pcell_pop'},
        'postConds': {'pop': 'INcell_pop'},
        'sec': 'dend_0',                  # target postsyn section
        'synMech': ['AMPA'],              # target synaptic mechanism
        'weight': [0.1],                 # synaptic weight
        'delay': [5],                     # transmission delay (ms)
        'probability': 0.1}             # probability of connection

# TODO: add stimulus
# netParams.stimSourceParams['ns1'] = {'type': 'NetStim', 'rate': 0.5, 'noise': 0}
# netParams.stimTargetParams['nc1'] = {'source': 'ns1', 'conds': {'cellModel': 'Pcell'}, 'weight': ampaweightpr, 'delay': 500, 'sec': 'dend'}
