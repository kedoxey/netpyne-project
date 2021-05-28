from netpyne import sim

# read cfg and netParams from command line arguments if available; otherwise use default
simConfig, netParams = sim.readCmdLineArgs(simConfigDefault='cfg_net.py', netParamsDefault='batch_setup_net.py')

# Create network and run simulation
sim.createSimulateAnalyze(netParams=netParams, simConfig=simConfig)
