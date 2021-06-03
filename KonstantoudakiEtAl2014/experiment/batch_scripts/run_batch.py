from netpyne import specs
from netpyne.batch import Batch

params = specs.ODict()

params['GABAgain'] = [1.0, 2.0, 3.0, 6.0, 9.0]

b = Batch(params=params, cfgFile='cfg_net.py', netParamsFile='batch_setup_net.py')

b.batchLabel = 'GABAgain'
b.saveFolder = 'GABAgain_batch'
b.method = 'grid'
b.runCfg = {'type': 'mpi_bulletin', 'script': 'batch_init.py', 'skip': True}

b.run()
