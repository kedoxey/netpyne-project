from netpyne import specs
from netpyne.batch import Batch

params = specs.ODict()

params['ampaweightcr'] = [0.000046, 0.00046]

b = Batch(params=params, cfgFile='cfg_net.py', netParamsFile='batch_setup_net.py')

b.batchLabel = 'ampaweightcr'
b.saveFolder = 'ampaweightcr_batch'
b.method = 'grid'
b.runCfg = {'type': 'mpi_bulletin', 'script': 'batch_init.py', 'skip': True}

b.run()
