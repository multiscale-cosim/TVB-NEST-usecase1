from dataclasses import dataclass
import numpy as np

from EBRAINS_ConfigManager.global_configurations_manager.xml_parsers.default_directories_enum import DefaultDirectories

@dataclass
class Simulator_1_Parameters():
    list_spikes= np.random.choice([0, 1], size=(10,), p=[1./3, 2./3])

class Simulator_1():
    def __init__(self, p_configurations_manager, p_log_settings, sci_params, path_parameter):
            self._log_settings = p_log_settings
            self._configurations_manager = p_configurations_manager
            self.__logger = self._configurations_manager.load_log_configurations(
                name="Simulator1",
                log_configurations=self._log_settings,
                target_directory=DefaultDirectories.SIMULATION_RESULTS)
            
            self.__sci_params = sci_params
            self.__params = Simulator_1_Parameters()
            self.results_path = path_parameter

    def configure(self,sim1_to_sim2_address,sim2_to_sim1_address):

        self.__logger.info('configuration 1 done!')
    
    def simulate(self):
        self.__logger.info('start the simulation 1')
        #TODO MPI

        self.__logger.info('exit')