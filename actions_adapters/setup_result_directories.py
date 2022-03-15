#  Copyright 2020 Forschungszentrum Jülich GmbH and Aix-Marseille Université
# "Licensed to the Apache Software Foundation (ASF) under one or more contributor license agreements; and to You under the Apache License, Version 2.0. "

import os
import json
import copy
from common.utils import directory_utils
# from actions_adapters.tvb_simulator.utils_tvb import self.create_folder


class SetupResultDirectories:
    '''
        sets up the cosimulationb parameters and directories to save the output
    '''
    def __init__(self):
        parameter_default = {"co_simulation": False,
                             "path": "",
                             "simulation_time": 30.0,
                             "level_log": 1,
                             "resolution": 0.1,
                             "nb_neurons": [100]
                            }

        ### NOTE: temporary result folder creation, change with refactoring
        path_file = os.path.dirname(__file__)
        self.create_folder(path_file + "/../result_sim/")
        self.create_folder(path_file + "/../result_sim/co-simulation/")

        # Setup Co-simulation and run!
        #path_file = os.path.dirname(__file__)
        parameter_co_simulation = copy.copy(parameter_default)
        parameter_co_simulation['path'] = path_file + "/../result_sim/co-simulation/"
        parameter_co_simulation.update({
            "co_simulation": True,
            # parameter for the synchronization between simulators
            "time_synchronization": 1.2,
            "id_nest_region": [0],
            # parameter for the transformation of data between scale
            "nb_brain_synapses": 1,
            'id_first_neurons': [1],
            "save_spikes": True,
            "save_rate": True,
        })
        self.setup_directories(parameter_co_simulation)

    def setup_directories(self, parameters):
        '''
        run the simulation
        :param parameters: parameters of the simulation
        :return:
        '''
        path = parameters['path']
        # start to create the repertory for the simulation
        self.create_folder(path)
        self.create_folder(path + "/log")
        self.create_folder(path + '/nest')
        self.create_folder(path + '/tvb')
        self.create_folder(path + '/transformation')
        self.create_folder(path + '/transformation/spike_detector/')
        self.create_folder(path + '/transformation/send_to_tvb/')
        self.create_folder(path + '/transformation/spike_generator/')
        self.create_folder(path + '/transformation/receive_from_tvb/')
        self.create_folder(path + '/figures')
        self.save_parameter(parameters)

    def save_parameter(self, parameters):
        """
        save the parameters of the simulations in json file
        :param parameters: dictionary of parameters
        :return: nothing
        """
        # save the value of all parameters
        f = open(parameters['path'] + '/parameter.json', "wt")
        json.dump(parameters, f)
        f.close()

    def create_folder(self, path): return directory_utils.safe_makedir(path)
