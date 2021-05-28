from netpyne import specs

cfg = specs.SimConfig()

# weights
cfg.ampaweightpr = 0.00008
cfg.ampaweight = 0.000065
cfg.ampaweightin = 0.000085
cfg.gabaweight = 0.00083
cfg.gabaweightb = cfg.gabaweight*0.35
cfg.gabaweightcrcb = 0.0083*0.25
cfg.gabaweightcb = 0.0006*1.5
cfg.gabaweightcr = 0.00087*3
cfg.autogabaweight = 0.0073*0.35
cfg.nmdaweight = cfg.ampaweight*21.5
cfg.nmdaweightin = cfg.ampaweightin*0.52
cfg.ampaweightcb = 0.000029
cfg.nmdaweightcb = cfg.ampaweightcb*0.86
cfg.ampaweightcr = 0.000046
cfg.nmdaweightcr = cfg.ampaweightcr*2.2

# delays
cfg.delayPcAMPA = 'normal(0.96, 0.11)'
cfg.delayPcNMDA = 'normal(1.33, 0.13)'
cfg.delayFs = 'normal(1.76, 0.07)'
cfg.delayPcInAMPA = 'normal(0.6, 0.2)'
cfg.delayPcInNMDA = 'normal(0.6, 0.2)'
cfg.delayInPcGABAa = 'normal(1.8, 0.8)'
cfg.delayInPcGABAb = 'normal(1.8, 0.8)'
cfg.delayPcCbAMPA = 'normal(0.6, 0.2)'
cfg.delayPcCbNMDA = 'normal(0.6, 0.2)'
cfg.delayPcCrAMPA = 'normal(0.6, 0.2)'
cfg.delayPcCrNMDA = 'normal(0.6, 0.2)'
cfg.delayCrCbGABAa = 'normal(1.8, 0.8)'
cfg.delayCbPcGABAa = 'normal(1.8, 0.8)'
cfg.delayCrPcGABAa = 'normal(1.8, 0.8)'

# Simulation options
cfg.hParams['celsius'] = 34
cfg.allowSelfConns = False
cfg.duration = 1000
cfg.dt = 0.025
cfg.verbose = False
cfg.recordTraces = {'V_soma': {'sec': 'soma', 'loc': 0.5, 'var': 'v'}}
cfg.recordStep = 1
cfg.saveJson = True
cfg.analysis['plotRaster'] = {'orderInverse': True, 'saveFig': True}
cfg.analysis['plotTraces'] = {'include': ['PYR_pop', 'FSin_pop', 'RSin_pop', 'ISin_pop'], 'saveFig': True}
cfg.analysis['plotConn'] = {'groupBy': 'cell', 'feature': 'numConns', 'saveFig': True}

cfg.saveDataInclude = ['simData']
