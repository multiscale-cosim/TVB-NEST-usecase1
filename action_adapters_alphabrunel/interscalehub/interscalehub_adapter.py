# ------------------------------------------------------------------------------
#  Copyright 2020 Forschungszentrum Jülich GmbH
# "Licensed to the Apache Software Foundation (ASF) under one or more contributor
#  license agreements; and to You under the Apache License, Version 2.0. "
#
# Forschungszentrum Jülich
#  Institute: Institute for Advanced Simulation (IAS)
#    Section: Jülich Supercomputing Centre (JSC)
#   Division: High Performance Computing in Neuroscience
# Laboratory: Simulation Laboratory Neuroscience
#       Team: Multi-scale Simulation and Design
#
# ------------------------------------------------------------------------------

import sys
import time
import pickle
import base64

from common.utils.security_utils import check_integrity
from action_adapters_alphabrunel.setup_result_directories import SetupResultDirectories
from EBRAINS_InterscaleHUB.Interscale_hub.manager_nest_to_tvb import NestToTvbManager
from EBRAINS_InterscaleHUB.Interscale_hub.manager_tvb_to_nest import TvbToNestManager
from EBRAINS_InterscaleHUB.Interscale_hub.interscalehub_enums import DATA_EXCHANGE_DIRECTION 
from EBRAINS_ConfigManager.global_configurations_manager.xml_parsers.default_directories_enum import DefaultDirectories
from EBRAINS_ConfigManager.global_configurations_manager.xml_parsers.configurations_manager import ConfigurationsManager


def run_wrapper(direction, configurations_manager, log_settings,
                sci_params_xml_path_filename=''):
    """
    starts the inter-scale hub to exchange data in direction provided as the
    parameter.
    """
    # direction
    # 1 --> nest to Tvb
    # 2 --> tvb to nest
    path = configurations_manager.get_directory(
                                        directory=DefaultDirectories.SIMULATION_RESULTS)
    # parameters = Parameter(path)
    parameters = {
                "co_simulation": True,
                "path": path,
                "simulation_time": 1000.0,
                "level_log": 1,
                # "resolution": 0.1, -> on interscale_hub.xml as dt
                # POD: is nb_neurons a functional parameter?
                # "nb_neurons": [100], -> on interscale_hub.xml, POD: is a Python's List required?
                # parameter for the synchronization between simulators
                # "time_synchronization": 1.2, -> on interscale_hub.xml
                "id_nest_region": [0],  # TO BE DONE: supporting Python's list on XML sci-params
                # parameter for the transformation of data between scale
                # "nb_brain_synapses": 1, -> on interscale_hub.xml
                'id_first_neurons': [1],
                "save_spikes": True,
                "save_rate": True,
                "width": 20.0,
                "id_first_spike_detector": 229
        }

    direction = int(direction)  # NOTE: will be changed

    # Case a: Nest to TVB inter-scale hub
    if direction == DATA_EXCHANGE_DIRECTION.NEST_TO_TVB:
        # create directories to store parameter.json file, 
        # port information, and logs
        SetupResultDirectories(path)  # NOTE: will be changed
        hub = NestToTvbManager(parameters,
                               configurations_manager,
                               log_settings,
                               sci_params_xml_path_filename=sci_params_xml_path_filename)

    # Case b: TVB to NEST inter-scale hub
    elif direction == DATA_EXCHANGE_DIRECTION.TVB_TO_NEST:
        # let the NEST_TO_TVB inter-scale hub to set up the directories and
        # parameters
        time.sleep(1)
        hub = TvbToNestManager(parameters,
                               configurations_manager,
                               log_settings,
                               sci_params_xml_path_filename=sci_params_xml_path_filename)

    # 1) init steering command
    # includes param setup, buffer creation
    # NOTE init is system action and so is done implicitly with the hub
    # initialization

    # 2) Start steering command
    # receive, pivot, transform, send
    hub.start()

    # 3) Stop steering command
    # disconnect and close ports
    hub.stop()

if __name__ == '__main__':
    # RunSetup()
    direction = sys.argv[1]
    configurations_manager = pickle.loads(base64.b64decode(sys.argv[2]))
    log_settings = pickle.loads(base64.b64decode(sys.argv[3]))
    # security check of pickled objects
    # it raises an exception, if the integrity is compromised
    check_integrity(configurations_manager, ConfigurationsManager)
    check_integrity(log_settings, dict)
    # everything is fine, run InterscaleHub
    sys.exit(run_wrapper(direction,
                         configurations_manager,
                         log_settings,
                         sci_params_xml_path_filename=sys.argv[4]))
