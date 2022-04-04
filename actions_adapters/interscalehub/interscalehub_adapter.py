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
from actions_adapters.setup_result_directories import SetupResultDirectories
from EBRAINS_InterscaleHUB.Interscale_hub.InterscaleHub import InterscaleHub
from EBRAINS_InterscaleHUB.Interscale_hub.parameter import Parameter
from EBRAINS_ConfigManager.global_configurations_manager.xml_parsers.default_directories_enum import DefaultDirectories
from EBRAINS_ConfigManager.global_configurations_manager.xml_parsers.configurations_manager import ConfigurationsManager


def run_wrapper(direction, configurations_manager, log_settings):
    # direction
    # 1 --> nest to Tvb
    # 2 --> tvb to nest
    path = configurations_manager.get_directory(
                                        directory=DefaultDirectories.SIMULATION_RESULTS)
    param = Parameter(path)

    direction = int(direction) # NOTE: will be changed
    # direction = 1 # NOTE: will be changed
    # receive steering commands init,start,stop
    
    if direction == 1:
        # create directories to store parameter.json file, 
        # port information, and logs
        SetupResultDirectories(path)
    else:
        time.sleep(1)

    # 1) init InterscaleHUB
    # includes param setup, buffer creation
    hub = InterscaleHub(param, direction, configurations_manager, log_settings)
    
    # 2) Start signal
    # receive, pivot, transform, send
    hub.start()
    
    # 3) Stop signal
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
    sys.exit(run_wrapper(direction, configurations_manager, log_settings))
