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

from basic_adapter import BasicAdapter

from EBRAINS_RichEndpoint.application_companion.common_enums import SteeringCommands, COMMANDS
from EBRAINS_RichEndpoint.application_companion.common_enums import INTEGRATED_SIMULATOR_APPLICATION as SIMULATOR

from EBRAINS_RichEndpoint.application_companion.common_enums import INTEGRATED_INTERSCALEHUB_APPLICATION as INTERSCALE_HUB
from EBRAINS_ConfigManager.global_configurations_manager.xml_parsers.default_directories_enum import DefaultDirectories
from EBRAINS_ConfigManager.global_configurations_manager.xml_parsers.configurations_manager import ConfigurationsManager
from EBRAINS_ConfigManager.workflow_configurations_manager.xml_parsers.xml2class_parser import Xml2ClassParser
from EBRAINS_InterscaleHUB.common.interscalehub_enums import DATA_EXCHANGE_DIRECTION


import nest
import nest.raster_plot
import matplotlib.pyplot as plt
from science.models.zerlaut.zerlaut_nest import ZerlautNest


class NESTAdapter(BasicAdapter):
    #def __init__(self, p_configurations_manager, p_log_settings,
    #             p_interscalehub_addresses,
    #             is_monitoring_enabled,
    #             sci_params_xml_path_filename=None):

    def __init__(self, cmd_param, sci_params_xml_path_filename=None):
        super().__init__(self.__class__.__name__,cmd_param, sci_params_xml_path_filename)
        
        self.nest_network = None

    def execute_init_command(self):
        self.__logger.debug("executing INIT command")
        # 1. configure simulation model
        self.__logger.info("configure the network")
       
        self.nest_network = ZerlautNest(p_configurations_manager=self._configurations_manager,
                                p_log_settings=self._log_settings,
                                sci_params=self.__sci_params,
                                path_parameter=self.__path_to_parameters_file)
        # TODO: checks parameters
        list_spike_detector, min_delay = self.nest_network.configure(self.__interscalehub_nest_to_tvb_address,
                                                                    self.__interscalehub_tvb_to_nest_address)

        self.__logger.info("preparing the simulator, and establishing the connections")
        self.__log_message("connections are made")
        self.__logger.debug("INIT command is executed")

        # 2. return with local minimum step size
        return self.__parameters.time_synch  # minimum step size for simulation
    
    def execute_start_command(self, global_minimum_step_size):
        self.__logger.debug("executing START command")
        if self.__is_monitoring_enabled:  # NOTE WIP may be changed
            self.__resource_usage_monitor.start_monitoring()

        self.__logger.debug(f'global_minimum_step_size: {global_minimum_step_size}')
        self.__logger.debug('starting simulation')

        self.nest_network.simulate()
        
    def execute_end_command(self):
        if self.__is_monitoring_enabled:  # NOTE WIP may be changed
            self.__resource_usage_monitor.stop_monitoring()
        if nest.Rank() == 0:       
            self.__logger.info("plotting the result")
   
        self.__logger.debug("post processing is done")
        
if __name__ == "__main__":
    if len(sys.argv) == 6:
        nest_adapter = NESTAdapter(cmd_param=sys.argv)

        # 4. execute 'INIT' command which is implicit with when laucnhed
        local_minimum_step_size = nest_adapter.execute_init_command()

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

        # convert the received string to dictionary
        control_command = ast.literal_eval(user_action_command.strip())

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

    """
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
    """