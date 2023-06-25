from dataclasses import dataclass
import numpy as np

from EBRAINS_ConfigManager.global_configurations_manager.xml_parsers.default_directories_enum import DefaultDirectories


############  MODEL  ###############

"""
# Adatper
- TVB adapter
- NEST adapter
- Hub adapter
"""



############  NEST  ###############

@dataclass
class Simulator_NEST_Parameters():
    list_spikes= np.random.choice([0, 1], size=(10,), p=[1./3, 2./3])

class Simulator_NEST():
    def __init__(self, p_configurations_manager, p_log_settings, sci_params, path_parameter):
            self._log_settings = p_log_settings
            self._configurations_manager = p_configurations_manager
            self.__logger = self._configurations_manager.load_log_configurations(
                name="SimulatorNEST",
                log_configurations=self._log_settings,
                target_directory=DefaultDirectories.SIMULATION_RESULTS)
            
            self.__sci_params = sci_params
            self.__params = Simulator_NEST_Parameters()
            self.results_path = path_parameter

    def configure(self,NEST_to_TVB_address,TVB_to_NEST_address):
        self.__logger.info('configuration NEST done!')
    
    def simulate(self):
        self.__logger.info('start the simulation NEST')
        #TODO MPI
        self.__logger.info('exit')

############  TVB  ###############

@dataclass
class Simulator_TVB_Parameters():
    regions_num = 68
    regions = np.random.uniform(low=10, high=200, size=(regions_num,))
    weights = np.random.uniform(low=0.5, high=200, size=(regions_num,))
    tract_lengths = np.random.uniform(low=0.5, high=200, size=(regions_num,))

class Simulator_TVB():
    def __init__(self, p_configurations_manager, p_log_settings, sci_params, path_parameter):
            self._log_settings = p_log_settings
            self._configurations_manager = p_configurations_manager
            self.__logger = self._configurations_manager.load_log_configurations(
                name="SimulatorTVB",
                log_configurations=self._log_settings,
                target_directory=DefaultDirectories.SIMULATION_RESULTS)
            
            self.__sci_params = sci_params
            self.__params = Simulator_TVB_Parameters()
            self.results_path = path_parameter

    def configure(self,NEST_to_TVB_address,TVB_to_NEST_address):

        self.__logger.info('configuration TVB done!')
    
    def simulate(self):
        self.__logger.info('start the simulation TVB')
        #TODO MPI

        self.__logger.info('exit')