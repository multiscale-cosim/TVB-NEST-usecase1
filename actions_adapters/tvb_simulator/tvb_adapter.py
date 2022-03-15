#  Copyright 2020 Forschungszentrum Jülich GmbH and Aix-Marseille Université
# "Licensed to the Apache Software Foundation (ASF) under one or more contributor license agreements; and to You under the Apache License, Version 2.0. "
import numpy
import sys
import os
import tvb.simulator.lab as lab
import matplotlib.pyplot as plt
from tvb.contrib.cosimulation.cosimulator import CoSimulator
from tvb.contrib.cosimulation.cosim_monitors import CosimCoupling

from cosim_example_demos.TVB_NEST_demo.tvb_sim.utils_tvb import create_logger
import cosim_example_demos.TVB_NEST_demo.tvb_sim.wrapper_TVB_mpi as Wrapper
from EBRAINS_RichEndpoint.Application_Companion.common_enums import SteeringCommands
from EBRAINS_RichEndpoint.Application_Companion.common_enums import INTEGRATED_SIMULATOR_APPLICATION as SIMULATOR
from actions_adapters.parameters import Parameters


numpy.random.seed(125)


class TVBAdapter:

    def __init__(self):
        self.__parameters = Parameters()
        self.__simulator = None
        self.__logger = create_logger(
            self.__parameters.path,
            'TVB',
            self.__parameters.log_level)
        self.__logger.info("initialized")

        
    def __configure(self, time_synch=0.1, id_nest_region=None, dt=0.1):
        """
        configure TVB before the simulation
        modify example of https://github.com/the-virtual-brain/tvb-root/blob/master/tvb_documentation/tutorials/tutorial_s1_region_simulation.ipynb
        :param co_simulation: boolean for checking if the co-simulation is active or not
        :param time_synch: time of synchronization between simulator
        :param id_nest_region: id of the region simulated with NEST
        :param dt: size fo the integration step
        :return:
        """
        oscilator = lab.models.Generic2dOscillator()
        white_matter = lab.connectivity.Connectivity.from_file()
        white_matter.speed = numpy.array([4.0])
        white_matter_coupling = lab.coupling.Linear(a=numpy.array([0.154]))
        heunint = lab.integrators.HeunDeterministic(dt=dt)
        what_to_watch = (lab.monitors.Raw(),)
        # special monitor for MPI
        simulator = CoSimulator(
            voi=numpy.array([0]),               # coupling with Excitatory firing rate
            synchronization_time=time_synch,    # time of synchronization time between simulators
            # monitor for the coupling between simulators
            cosim_monitors=(CosimCoupling(coupling=white_matter_coupling),),
            proxy_inds=numpy.array(id_nest_region, dtype=int),  # id of the proxy node
            model=oscilator, connectivity=white_matter,
            coupling=white_matter_coupling,
            integrator=heunint, monitors=what_to_watch
        )
        simulator.configure()
        return simulator

    def execute_init_command(self):
        self.__logger.debug("executing INIT command")
        self.__simulator = self.__configure(
            self.__parameters.time_synch,
            self.__parameters.id_nest_region,
            self.__parameters.resolution)
        self.__simulator.simulation_length = self.__parameters.simulation_time
        self.__logger.debug("INIT command is executed")
        return self.__parameters.time_synch  # minimum step size for simulation 
    
    
    def execute_start_command(self):
        self.__logger.debug("executing START command")
        (raw_results,) = Wrapper.run_mpi(
            self.__simulator,
            self.__parameters.path,
            self.__logger)           
        self.__logger.debug('TVB simulation is finished')
        return raw_results


    def execute_end_command(self, raw_results):
        self.__logger.info("plotting the result")
        plt.figure(1)
        plt.plot(raw_results[0], raw_results[1][:, 0, :, 0] + 3.0)
        plt.title("Raw -- State variable 0")
        plt.savefig(self.__parameters.path+"/figures/plot_tvb.png")
        
        self.__logger.debug("post processing is done")


if __name__ == "__main__":
    
    tvb_adapter = TVBAdapter()
    local_minimum_step_size = tvb_adapter.execute_init_command()
     # send local minimum step size to Application Manager as a response to INIT
    # NOTE Application Manager expects a string in the following format:
    # {'PID': <int>, 'LOCAL_MINIMUM_STEP_SIZE': <float>}
    pid_and_local_minimum_step_size = \
        {SIMULATOR.PID.name: os.getpid(),
        SIMULATOR.LOCAL_MINIMUM_STEP_SIZE.name: local_minimum_step_size}

    # Application Manager will read the stdout stream via PIPE
    # NOTE the communication with Application Manager via PIPES will be
    # changed to some other mechanism
    print(f'{pid_and_local_minimum_step_size}')
    user_action_command = input()
    # execute if steering command is START
    if SteeringCommands[user_action_command] == SteeringCommands.START:
        raw_results = tvb_adapter.execute_start_command()
        tvb_adapter.execute_end_command(raw_results)
        sys.exit(0)
    else:
        # TODO raise and log the exception with traceback and terminate with
        # error if received an unknown steering command
        print(f'unknown steering command: '
              f'{SteeringCommands[user_action_command]}',
              file=sys.stderr)
        sys.exit(1)

# /************************************************************************************************************/
# def run_example(co_simulation, path, time_synch=0.1, simtime=1000.0, level_log=1,id_nest_region=[0],dt=0.1):
#         """
#         run the example for TVB
#         :param co_simulation: boolean for checking if the co-simulation is active or not
#         :param path: path of the result of the simulation
#         # parameters for the co-simulation
#         :param time_synch: time of synchronization between simulator
#         :param simtime: time of simulation
#         :param level_log: level of the log
#         :param id_nest_region: id of the region simulated with NEST
#         :param dt: size fo the integration step
#         :return:
#         """
#         # logger = create_logger(path, 'tvb', level_log)
#         # logger.info("configure the network")
#         simulator = configure(co_simulation, time_synch, id_nest_region,dt)
#         simulator.simulation_length = simtime

#         logger.info("start the simulation")
#         if not co_simulation:
#             (RAW,) = simulator.run()
#         else:
#             (RAW,) = Wrapper.run_mpi(simulator, path, logger)

#         logger.info("plot the result")
#         plt.figure(1)
#         plt.plot(RAW[0], RAW[1][:, 0, :, 0] + 3.0)
#         plt.title("Raw -- State variable 0")
#         plt.savefig(path+"/figures/plot_tvb.png")


# if __name__ == "__main__":
   
#     if len(sys.argv) == 1:  # test the example
#         path_file = os.path.dirname(__file__)
#         create_folder(path_file+"/../../result_sim/tvb_only/")
#         create_folder(path_file+"/../../result_sim/tvb_only/log/")
#         create_folder(path_file+"/../../result_sim/tvb_only/figures/")
#         run_example(False, path_file+"/../../result_sim/tvb_only/")
#     elif len(sys.argv) == 2:  # run with parameters file
#         import json
#         path_file = os.path.dirname(__file__)
#         path = path_file+ '/../../result_sim/co-simulation/parameter.json'
#         with open(path) as f:
#             parameters = json.load(f)
#         if "time_synchronization" not in parameters.keys():
#            parameters['time_synchronization'] = -1
#         if "id_nest_region" not in parameters.keys():
#             parameters['id_nest_region'] = None
#         run_example(parameters['co_simulation'], parameters['path'], simtime=parameters['simulation_time'],
#                     level_log=parameters['level_log'], dt=parameters['resolution'],
#                     time_synch=parameters['time_synchronization'], id_nest_region=parameters['id_nest_region'])
#     elif len(sys.argv) == 6:  # run with parameter in command line
#         run_example(bool(int(sys.argv[1])), sys.argv[2], time_synch=float(sys.argv[3]),
#                     simtime=float(sys.argv[4]), level_log=int(sys.argv[5]))

# ************************************************************************************************************************/
