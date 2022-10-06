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

from action_adapters_alphabrunel.nest_simulator.utils_function import get_data
from common.utils.security_utils import check_integrity
from action_adapters_alphabrunel.parameters import Parameters
from EBRAINS_RichEndpoint.Application_Companion.common_enums import SteeringCommands
from EBRAINS_RichEndpoint.Application_Companion.common_enums import INTEGRATED_SIMULATOR_APPLICATION as SIMULATOR
from EBRAINS_RichEndpoint.Application_Companion.common_enums import INTEGRATED_INTERSCALEHUB_APPLICATION as INTERSCALE_HUB
from EBRAINS_ConfigManager.global_configurations_manager.xml_parsers.default_directories_enum import DefaultDirectories
from EBRAINS_ConfigManager.global_configurations_manager.xml_parsers.configurations_manager import ConfigurationsManager
from EBRAINS_ConfigManager.workflow_configuraitons_manager.xml_parsers.xml2class_parser import Xml2ClassParser
from EBRAINS_InterscaleHUB.Interscale_hub.interscalehub_enums import DATA_EXCHANGE_DIRECTION

import nest
import nest.raster_plot
import matplotlib.pyplot as plt


class NESTAdapter:
    def __init__(self, p_configurations_manager, p_log_settings,
                 p_interscalehub_addresses,
                 sci_params_xml_path_filename=None):
        self._log_settings = p_log_settings
        self._configurations_manager = p_configurations_manager
        self.__logger = self._configurations_manager.load_log_configurations(
            name="NEST_Adapter",
            log_configurations=self._log_settings,
            target_directory=DefaultDirectories.SIMULATION_RESULTS)
        self.__path_to_parameters_file = self._configurations_manager.get_directory(
            directory=DefaultDirectories.SIMULATION_RESULTS)

        # Loading scientific parameters into an object
        self.__sci_params = Xml2ClassParser(sci_params_xml_path_filename, self.__logger)
        self.__parameters = Parameters(self.__path_to_parameters_file)

        # The MPI port_name needs to be in string format and must be sent to
        # nest-simulator in the following pattern:

        # "endpoint_address":<port name>

        # Initialize port_names in the format as per nest-simulator
        self.__init_port_names(p_interscalehub_addresses)
        self.__logger.info("initialized")

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

    def __configure_nest(self, simulator):
        """
        configure NEST before the simulation
        modify example of https://simulator.simulator.readthedocs.io/en/stable/_downloads/482ad6e1da8dc084323e0a9fe6b2c7d1/brunel_alpha_simulator.py
        :param simulator: nest simulator
        :return:
        """

        # create the neurons and the devices
        # neuron_params = self.__parameters.neuron_params

        nodes_ex = simulator.Create(
            model=self.__sci_params.nodes_model['model'],
            n=self.__sci_params.nb_neurons,
            params=self.__sci_params.nodes_model['params'])

        nodes_in = simulator.Create(
            model=self.__sci_params.nodes_model['model'],
            n=self.__sci_params.nodes_model['total_inhibitory_nodes'],
            params=self.__sci_params.nodes_model['params'])

        #
        # noise poisson_generator
        #
        noise = simulator.Create(model=self.__sci_params.noise_model['model'],
                                 params=self.__sci_params.noise_model['params'])

        #
        # Spikes' Models
        #
        espikes = simulator.Create(self.__sci_params.spike_recorder_device)
        ispikes = simulator.Create(self.__sci_params.spike_recorder_device)

        espikes.set(label=self.__sci_params.excitatory_spikes_model['model'],
                    record_to=self.__sci_params.excitatory_spikes_model['record_to'])
        ispikes.set(label=self.__sci_params.inhibitory_spikes_model['model'],
                    record_to=self.__sci_params.inhibitory_spikes_model['record_to'])

        #
        # Creating the connection
        # simulator.CopyModel("static_synapse", "excitatory", {"weight":  20.68015524367846, "delay": 1.5})
        simulator.CopyModel(
            existing=self.__sci_params.predefined_synapse,
            new=self.__sci_params.excitatory_model['synapse'],
            params=self.__sci_params.excitatory_model['params'])
        # simulator.CopyModel("static_synapse", "inhibitory", {"weight": -103.4007762183923, "delay": 1.5})
        simulator.CopyModel(
            existing=self.__sci_params.predefined_synapse,
            new=self.__sci_params.inhibitory_model['synapse'],
            params=self.__sci_params.inhibitory_model['params'])

        # conn_params_ex = {'rule': 'fixed_indegree', 'indegree': 10}
        # conn_params_in = {'rule': 'fixed_indegree', 'indegree': 2}
        simulator.Connect(pre=nodes_ex,
                          post=nodes_ex + nodes_in,
                          conn_spec=self.__sci_params.excitatory_connection['params'],
                          syn_spec=self.__sci_params.excitatory_connection['syn_spec'])
        simulator.Connect(pre=nodes_in,
                          post=nodes_ex + nodes_in,
                          conn_spec=self.__sci_params.inhibitory_connection['params'],
                          syn_spec=self.__sci_params.inhibitory_connection['syn_spec'])

        # simulator.Connect(noise, nodes_ex, syn_spec="excitatory")
        simulator.Connect(
            pre=noise,
            post=nodes_ex,
            syn_spec=self.__sci_params.excitatory_model['synapse'])

        # simulator.Connect(noise, nodes_in, syn_spec="excitatory")
        simulator.Connect(
            pre=noise,
            post=nodes_in,
            syn_spec=self.__sci_params.excitatory_model['synapse'])  # is the usage of 'excitatory' OK?

        # simulator.Connect(nodes_ex[:50], espikes, syn_spec="excitatory")
        simulator.Connect(
            pre=nodes_ex[:50],
            post=espikes,
            syn_spec=self.__sci_params.excitatory_model['synapse'])

        # simulator.Connect(nodes_in[:25], ispikes, syn_spec="excitatory")
        simulator.Connect(
            pre=nodes_in[:25],
            post=ispikes,
            syn_spec=self.__sci_params.excitatory_model['synapse'])

        # conn_params_ex = self.__parameters.connection_param_ex
        # conn_params_in = self.__parameters.connection_param_in
        simulator.Connect(
            nodes_ex,
            nodes_ex + nodes_in,
            conn_spec=self.__sci_params.excitatory_connection['params'],
            syn_spec=self.__sci_params.excitatory_connection['syn_spec'])
        simulator.Connect(
            nodes_in,
            nodes_ex + nodes_in,
            conn_spec=self.__sci_params.inhibitory_connection['params'],
            syn_spec=self.__sci_params.inhibitory_connection['syn_spec'])

        # Co-Simulation Devices
        # input_to_simulator = simulator.Create("spike_generator", self.__parameters.nb_neurons,
        #                                       params={'stimulus_source': 'mpi',
        #                                               'label': '/../transformation/spike_generator'})
        input_to_simulator = simulator.Create(model=self.__sci_params.input_to_simulator['model'],
                                              n=self.__sci_params.nb_neurons,
                                              params={'stimulus_source': 'mpi',
                                                      'label': self.__interscalehub_tvb_to_nest_address})
        # output_from_simulator = simulator.Create("spike_recorder",
        #                                          params={"record_to": "mpi",
        #                                                  'label': '/../transformation/spike_detector'})
        output_from_simulator = simulator.Create("spike_recorder",
                                                 params={"record_to": "mpi",
                                                         'label': self.__interscalehub_nest_to_tvb_address})
        
        # simulator.Connect(input_to_simulator, nodes_ex, {'rule': 'one_to_one'},
        #                   {"weight": 20.68015524367846, "delay": 0.1})
        simulator.Connect(pre=input_to_simulator,
                          post=nodes_ex,
                          conn_spec=self.__sci_params.input_to_simulator['conn_spec'],
                          syn_spec=self.__sci_params.input_to_simulator['syn_spec'])
        # simulator.Connect(nodes_ex, output_from_simulator, {'rule': 'all_to_all'},
        #                   {"weight": 1.0, "delay": 0.1})
        simulator.Connect(pre=nodes_ex,
                          post=output_from_simulator,
                          conn_spec=self.__sci_params.output_from_simulator['conn_spec'],
                          syn_spec=self.__sci_params.output_from_simulator['syn_spec'])

        return espikes, input_to_simulator, output_from_simulator

    def execute_init_command(self):
        self.__logger.debug("executing INIT command")
        nest.ResetKernel()
        nest.SetKernelStatus(
            {"data_path": self.__parameters.path + '/nest/',
             "overwrite_files": True, "print_time": True,
             "resolution": self.__parameters.resolution})

        self.__logger.info("configure the network")
        espikes, input_to_simulator, output_from_simulator = \
            self.__configure_nest(nest)

        self.__logger.info("preparing the simulator, and "
                           "establishing the connections")
        nest.Prepare()
        self.__logger.info("connections are made")
        self.__logger.debug("INIT command is executed")
        return self.__parameters.time_synch  # minimum step size for simulation

    def execute_start_command(self):
        self.__logger.debug("executing START command")
        count = 0.0
        self.__logger.debug('starting simulation')
        while count * self.__parameters.time_synch < self.__parameters.simulation_time:
            self.__logger.info(f"simulation run counter: {count+1}")
            nest.Run(self.__parameters.time_synch)
            count += 1

        self.__logger.info('nest simulation is finished')
        self.__logger.info("cleaning up NEST")
        nest.Cleanup()
        # self.execute_end_command()

    def execute_end_command(self):
        self.__logger.info("plotting the result")
        if nest.Rank() == 0:
            # plot if there is data available
            data = get_data(self.__logger, self.__parameters.path + '/nest/')
            if data is not None:
                nest.raster_plot.from_data(data)
                plt.savefig(self.__parameters.path + "/figures/plot_nest.png")
                self.__logger.debug("data is plotted")
            else:  # Case: there is no data is to there to plot
                try:
                    # raise an exception to log with traceback
                    raise RuntimeError
                except RuntimeError:
                    self.__logger.exception("No data to plot")

        self.__logger.debug("post processing is done")


if __name__ == "__main__":
    # TODO better handling of arguments parsing
    # unpickle configurations_manager object
    configurations_manager = pickle.loads(base64.b64decode(sys.argv[2]))
    # unpickle log_settings
    log_settings = pickle.loads(base64.b64decode(sys.argv[3]))
    # get science parameters XML file path
    p_sci_params_xml_path_filename = sys.argv[4]
    # get interscalehub connection details
    p_interscalehub_address = pickle.loads(base64.b64decode(sys.argv[5]))

    # security check of pickled objects
    # it raises an exception, if the integrity is compromised
    check_integrity(configurations_manager, ConfigurationsManager)
    check_integrity(log_settings, dict)
    check_integrity(p_interscalehub_address, list)

    # everything is fine, configure simulator
    nest_adapter = NESTAdapter(configurations_manager, log_settings,
                               p_interscalehub_address,
                               sci_params_xml_path_filename=p_sci_params_xml_path_filename)

    local_minimum_step_size = nest_adapter.execute_init_command()

    # send local minimum step size to Application Manager as a response to INIT
    # NOTE Application Manager expects a string in the following format:
    # {'PID': <pid>, 'LOCAL_MINIMUM_STEP_SIZE': <step size>}
    pid_and_local_minimum_step_size = \
        {SIMULATOR.PID.name: os.getpid(),
         SIMULATOR.LOCAL_MINIMUM_STEP_SIZE.name: local_minimum_step_size}
    # Application Manager will read the stdout stream via PIPE
    print(f'{pid_and_local_minimum_step_size}')

    # fetch next command from Application Manager
    user_action_command = input()
    # execute if steering command is START
    if SteeringCommands[user_action_command] == SteeringCommands.START:
        nest_adapter.execute_start_command()
        nest_adapter.execute_end_command()
        sys.exit(0)
    else:
        # TODO raise and log the exception with traceback and terminate with
        # error if received an unknown steering command
        print(f'unknown steering command: '
              f'{SteeringCommands[user_action_command]}',
              file=sys.stderr)
        sys.exit(1)
