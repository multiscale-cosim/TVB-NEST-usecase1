# ------------------------------------------------------------------------------
#  Copyright 2020 Forschungszentrum Jülich GmbH and Aix-Marseille Université
# "Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements; and to You under the Apache License,
# Version 2.0. "
#
# Forschungszentrum Jülich
# Institute: Institute for Advanced Simulation (IAS)
# Section: Jülich Supercomputing Centre (JSC)
# Division: High Performance Computing in Neuroscience
# Laboratory: Simulation Laboratory Neuroscience
# Team: Multi-scale Simulation and Design
# ------------------------------------------------------------------------------
import os
import sys
import pickle
import base64
import ast

from mpi4py import MPI

from common.utils.security_utils import check_integrity
from action_adapters_alphabrunel.resource_usage_monitor_adapter import ResourceMonitorAdapter
from action_adapters_alphabrunel.nest_simulator.utils_function import get_data
from action_adapters_alphabrunel.parameters import Parameters

from science.models.brunel_alpha.brunel_alpha_nest import BrunelAlphaHPC

from EBRAINS_RichEndpoint.application_companion.common_enums import SteeringCommands, COMMANDS
from EBRAINS_RichEndpoint.application_companion.common_enums import INTEGRATED_SIMULATOR_APPLICATION as SIMULATOR
from EBRAINS_RichEndpoint.application_companion.common_enums import INTEGRATED_INTERSCALEHUB_APPLICATION as INTERSCALE_HUB
from EBRAINS_ConfigManager.global_configurations_manager.xml_parsers.default_directories_enum import DefaultDirectories
from EBRAINS_ConfigManager.global_configurations_manager.xml_parsers.configurations_manager import ConfigurationsManager
from EBRAINS_ConfigManager.workflow_configurations_manager.xml_parsers.xml2class_parser import Xml2ClassParser
from EBRAINS_InterscaleHUB.Interscale_hub.interscalehub_enums import DATA_EXCHANGE_DIRECTION

import nest
import nest.raster_plot
import matplotlib.pyplot as plt


class NESTAdapter:
    def __init__(self, p_configurations_manager, p_log_settings,
                 p_interscalehub_addresses,
                 is_monitoring_enabled,
                 sci_params_xml_path_filename=None):
        self._log_settings = p_log_settings
        self._configurations_manager = p_configurations_manager
        self.__logger = self._configurations_manager.load_log_configurations(
            name="NEST_Adapter",
            log_configurations=self._log_settings,
            target_directory=DefaultDirectories.SIMULATION_RESULTS)
        self.__path_to_parameters_file = self._configurations_manager.get_directory(
            directory=DefaultDirectories.SIMULATION_RESULTS)

        # MPI rank
        self.__comm = MPI.COMM_WORLD
        self.__rank = self.__comm.Get_rank()
        self.__my_pid = os.getpid()
        self.__logger.info(f"__DEBUG__ size: {self.__comm.Get_size()}, my rank: {self.__rank}, "
                           f"host_name:{os.uname()}")
        # Loading scientific parameters into an object
        self.__sci_params = Xml2ClassParser(sci_params_xml_path_filename, self.__logger)
        self.__parameters = Parameters(self.__path_to_parameters_file)
        self.__is_monitoring_enabled = is_monitoring_enabled
        if self.__is_monitoring_enabled:
            self.__resource_usage_monitor = ResourceMonitorAdapter(self._configurations_manager,
                                                               self._log_settings,
                                                               self.pid,
                                                               "NEST")
        # NOTE The MPI port_name needs to be in string format and must be sent to
        # nest-simulator in the following pattern:
        # "endpoint_address":<port name>

        # Initialize port_names in the format as per nest-simulator
        self.__init_port_names(p_interscalehub_addresses)
        self.__simulator = BrunelAlphaHPC(self._log_settings,
                                            self._configurations_manager,
                                            self.__interscalehub_tvb_to_nest_address,
                                            self.__interscalehub_nest_to_tvb_address)
        self.__log_message("initialized")

    @property
    def rank(self):
        return self.__rank
    
    @property
    def pid(self):
        return self.__my_pid

    def __log_message(self, msg):
        "helper function to control the log emissions as per rank"
        if self.rank == 0:        
            self.__logger.info(msg)
        else:
            self.__logger.debug(msg)

    def __init_port_names(self, interscalehub_addresses):
        '''
        helper function to prepare the port_names in the following format:

        "endpoint_address":<port name>
        '''
        for interscalehub in interscalehub_addresses:
            self.__logger.debug(f"running interscalehub: {interscalehub}")
            # NEST_TO_TVB RECEIVER endpoint
            if interscalehub.get(
                    INTERSCALE_HUB.DATA_EXCHANGE_DIRECTION.name) ==\
                    DATA_EXCHANGE_DIRECTION.NEST_TO_TVB.name:
                # get mpi port name
                self.__interscalehub_nest_to_tvb_address =\
                    "endpoint_address:"+interscalehub.get(
                        INTERSCALE_HUB.MPI_CONNECTION_INFO.name)
                self.__logger.debug("Interscalehub_nest_to_tvb_address: "
                                    f"{self.__interscalehub_nest_to_tvb_address}")

            # TVB_TO_NEST SENDER endpoint
            elif interscalehub.get(
                    INTERSCALE_HUB.DATA_EXCHANGE_DIRECTION.name) ==\
                    DATA_EXCHANGE_DIRECTION.TVB_TO_NEST.name:
                # get mpi port name
                self.__interscalehub_tvb_to_nest_address =\
                    "endpoint_address:"+interscalehub.get(
                        INTERSCALE_HUB.MPI_CONNECTION_INFO.name)
                self.__logger.debug("Interscalehub_tvb_to_nest_address: "
                                    f"{self.__interscalehub_tvb_to_nest_address}")

    def execute_init_command(self):
        self.__logger.debug("executing INIT command")
        # 1. configure simulation model
        self.__logger.info("configure the network")
        ###########################################
        # TODO call science/models/<model_nest>.py for setting up network configuraions
        
        #### sample old code starts
        
        # nest.ResetKernel()
        # nest.SetKernelStatus(
        #     {"data_path": self.__parameters.path + '/nest/',
        #      "overwrite_files": True, "print_time": True,
        #      "resolution": self.__parameters.resolution})
        # self.__configure_nest(nest)
        # setup connections with InterscaleHub
        self.__logger.info("preparing the simulator, and "
                           "establishing the connections")
        
        self.__simulator.build_network()
        # nest.Prepare()
        #### sample old code ends
        
        ############################################
        self.__log_message("connections are made")
        self.__logger.debug("INIT command is executed")
        # 2. return with local minimum step size
        return self.__parameters.time_synch  # minimum step size for simulation
    
    def execute_start_command(self, global_minimum_step_size):
        self.__logger.debug("executing START command")
        if self.__is_monitoring_enabled:  # NOTE WIP may be changed
            self.__resource_usage_monitor.start_monitoring()
        self.__logger.debug(f'global_minimum_step_size: {global_minimum_step_size}')
        count = 0.0
        self.__logger.debug('starting simulation')
        ############################################
        # TODO call science/models/<model_nest>.py to run simulation step
        
        #### sample old code starts
        
        # while count * global_minimum_step_size < self.__parameters.simulation_time:
        #     self.__log_message(f"simulation run counter: {count+1}")
        #     nest.Run(self.__parameters.time_synch)
        #     count += 1

        # self.__log_message('nest simulation is finished')
        # self.__log_message("cleaning up NEST")
        # nest.Cleanup()
        
        #### sample old code ends
        
        ############################################
        self.__simulator.run_simulation(global_minimum_step_size)
        # self.execute_end_command()

    def execute_end_command(self):
        if self.__is_monitoring_enabled:  # NOTE WIP may be changed
            self.__resource_usage_monitor.stop_monitoring()
        if nest.Rank() == 0:
        ############################################
            # TODO call science/models/<model_nest>.py for post processing
            
            #### sample old code starts
            
            # plot if there is data available
            self.__logger.info("plotting the result")
            # data = get_data(self.__logger, self.__parameters.path + '/nest/')
            # if data is not None:
            #     nest.raster_plot.from_data(data)
            #     plt.savefig(self.__parameters.path + "/figures/plot_nest.png")
            #     self.__logger.debug("data is plotted")
            # else:  # Case: there is no data is to there to plot
            #     try:
            #         # raise an exception to log with traceback
            #         raise RuntimeError
            #     except RuntimeError:
            #         self.__logger.exception("No data to plot")

        #### sample old code ends
        
        ############################################
        self.__logger.debug("post processing is done")


if __name__ == "__main__":
    # TODO better handling of arguments parsing
    if len(sys.argv) == 6:        
        # 1. parse arguments
        # unpickle configurations_manager object
        configurations_manager = pickle.loads(base64.b64decode(sys.argv[1]))
        # unpickle log_settings
        log_settings = pickle.loads(base64.b64decode(sys.argv[2]))
        # get science parameters XML file path
        p_sci_params_xml_path_filename = sys.argv[3]
        # flag indicating whether resource usage monitoring is enabled
        is_monitoring_enabled = pickle.loads(base64.b64decode(sys.argv[4]))
        # get interscalehub connection details
        p_interscalehub_address = pickle.loads(base64.b64decode(sys.argv[5]))
        

        # 2. security check of pickled objects
        # it raises an exception, if the integrity is compromised
        check_integrity(configurations_manager, ConfigurationsManager)
        check_integrity(log_settings, dict)
        check_integrity(p_interscalehub_address, list)
        check_integrity(is_monitoring_enabled, bool)

        # 3. everything is fine, configure simulator
        nest_adapter = NESTAdapter(
            configurations_manager,
            log_settings,
            p_interscalehub_address,
            is_monitoring_enabled,
            sci_params_xml_path_filename=p_sci_params_xml_path_filename)

        # 4. execute 'INIT' command which is implicit with when laucnhed
        local_minimum_step_size = nest_adapter.execute_init_command()

        # 5. send the pid and the local minimum step size to Application Manager
        # as a response to 'INIT' as per protocol
        
        # NOTE Application Manager expects a string in the following format:
        # {'PID': <pid>, 'LOCAL_MINIMUM_STEP_SIZE': <step size>}

        # prepare the response
        my_rank = nest_adapter.rank
        if my_rank == 0:
            pid_and_local_minimum_step_size = \
                {SIMULATOR.PID.name: nest_adapter.pid,
                #SIMULATOR.PID.name: os.getpid(),
                SIMULATOR.LOCAL_MINIMUM_STEP_SIZE.name: local_minimum_step_size}
        
            # send the response
            # NOTE Application Manager will read the stdout stream via PIPE
            print(f'{pid_and_local_minimum_step_size}')

        # 6. fetch next command from Application Manager
        user_action_command = input()

        # NOTE Application Manager sends the control commands with parameters in
        # the following specific format as a string via stdio:
        # {'STEERING_COMMAND': {'<Enum SteeringCommands>': <Enum value>}, 'PARAMETERS': <value>}
        
        # For example:
        # {'STEERING_COMMAND': {'SteeringCommands.START': 2}, 'PARAMETERS': 1.2}        

        # convert the received string to dictionary
        control_command = ast.literal_eval(user_action_command.strip())
        # get steering command
        steering_command_dictionary = control_command.get(COMMANDS.STEERING_COMMAND.name)
        current_steering_command = next(iter(steering_command_dictionary.values()))
        
        # 7. execute if steering command is 'START'
        if current_steering_command == SteeringCommands.START:
            # fetch global minimum step size
            global_minimum_step_size = control_command.get(COMMANDS.PARAMETERS.name)
            # execute the command
            nest_adapter.execute_start_command(global_minimum_step_size)
            nest_adapter.execute_end_command()
            # exit with success code
            sys.exit(0)
        else:
            print(f'unknown command: {current_steering_command}', file=sys.stderr)
            sys.exit(1)
    else:
        print(f'missing argument[s]; required: 6, received: {len(sys.argv)}')
        print(f'Argument list received: {str(sys.argv)}')
        sys.exit(1)