from dataclasses import dataclass
import numpy as np

from EBRAINS_ConfigManager.global_configurations_manager.xml_parsers.default_directories_enum import DefaultDirectories

@dataclass
class Simulator_2_Parameters():
    regions_num = 68
    regions = np.random.uniform(low=10, high=200, size=(regions_num,))
    weights = np.random.uniform(low=0.5, high=200, size=(regions_num,))
    tract_lengths = np.random.uniform(low=0.5, high=200, size=(regions_num,))

class Simulator_2():
    def __init__(self, p_configurations_manager, p_log_settings, sci_params, path_parameter):
            self._log_settings = p_log_settings
            self._configurations_manager = p_configurations_manager
            self.__logger = self._configurations_manager.load_log_configurations(
                name="Simulator2",
                log_configurations=self._log_settings,
                target_directory=DefaultDirectories.SIMULATION_RESULTS)
            
            self.__sci_params = sci_params
            self.__params = Simulator_2_Parameters()
            self.results_path = path_parameter

    def configure(self,sim1_to_sim2_address,sim2_to_sim1_address):

        self.__logger.info('configuration 2 done!')
    
    def simulate(self):
        self.__logger.info('start the simulation 2')
        #TODO MPI

        self.__logger.info('exit')
