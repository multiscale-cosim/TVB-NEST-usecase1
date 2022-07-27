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
import json
import os
import time


class Parameters:
    def __init__(self, path):
        self.__path_to_parameters_file = self.__get_path_to_parameters_file(path)
        self.__cosim_parameters = self.__load_parameters_from_json()

    @property
    def cosim_parameters(self): return self.__cosim_parameters

    # @property
    # def path(self): return self.__path

    def __get_path_to_parameters_file(self, path):
        # path_to_self = os.path.dirname(__file__)
        return (path + '/parameter.json')

    def __load_parameters_from_json(self):
        # check if file is already created
        while not os.path.exists(self.__path_to_parameters_file):
            print(f'{self.__path_to_parameters_file} does not exist yet, retrying in 1 second')
            time.sleep(1)

        # file is already created
        with open(self.__path_to_parameters_file) as f:
            return json.load(f)
