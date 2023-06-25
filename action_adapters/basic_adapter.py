

import os,sys,pickle,base64

from mpi4py import MPI
from abc import ABC, abstractmethod

from common.utils.security_utils import check_integrity
from action_adapters_alphabrunel.resource_usage_monitor_adapter import ResourceMonitorAdapter
from action_adapters_alphabrunel.nest_simulator.utils_function import get_data
from action_adapters_alphabrunel.parameters import Parameters

#from EBRAINS_RichEndpoint.application_companion.common_enums import SteeringCommands, COMMANDS
#from EBRAINS_RichEndpoint.application_companion.common_enums import INTEGRATED_SIMULATOR_APPLICATION as SIMULATOR
from EBRAINS_RichEndpoint.application_companion.common_enums import INTEGRATED_INTERSCALEHUB_APPLICATION as INTERSCALE_HUB
from EBRAINS_ConfigManager.global_configurations_manager.xml_parsers.default_directories_enum import DefaultDirectories
from EBRAINS_ConfigManager.global_configurations_manager.xml_parsers.configurations_manager import ConfigurationsManager
from EBRAINS_ConfigManager.workflow_configurations_manager.xml_parsers.xml2class_parser import Xml2ClassParser
from EBRAINS_InterscaleHUB.Interscale_hub.interscalehub_enums import DATA_EXCHANGE_DIRECTION

class BasicAdapter(ABC): 
    #def __init__(self, log_settings, configurations_manager, p_interscalehub_addresses, app_name,
    #             is_monitoring_enabled=True, sci_params_xml_path_filename=None):
    
    #def __init__(self, app_name,**kwargs):
    def __init__(self, app_name, cmd_param, sci_params_xml_path_filename=None):

        self.app_name = app_name
        #kwargs.get('size')

        #kwargs_raw = sys.argv[1:]
        #kwargs = {key: val for key, val in zip(kwargs_raw[::3], kwargs_raw[1::len(sys.argv)])}


        # 1. parse arguments
        configurations_manager = pickle.loads(base64.b64decode(cmd_param[1]))
        log_settings = pickle.loads(base64.b64decode(cmd_param[2]))
        sci_params_xml_path_filename = cmd_param[3]
        is_monitoring_enabled = pickle.loads(base64.b64decode(cmd_param[4]))
        interscalehub_addresses = pickle.loads(base64.b64decode(cmd_param[5]))

        # 2. security check of pickled objects
        # it raises an exception, if the integrity is compromised
        check_integrity(configurations_manager, ConfigurationsManager)
        check_integrity(log_settings, dict)
        check_integrity(interscalehub_addresses, list)
        check_integrity(is_monitoring_enabled, bool)

        self._log_settings = log_settings
        self._configurations_manager = configurations_manager
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
                                                               self.app_name)
            
        # NOTE The MPI port_name needs to be in string format and must be sent to
        # nest-simulator in the following pattern:
        # "endpoint_address":<port name>

        # Initialize port_names in the format as per nest-simulator
        self.__init_port_names(interscalehub_addresses)
        """
        self.__simulator = BrunelAlphaHPC(self._log_settings,
                                            self._configurations_manager,
                                            self.__interscalehub_tvb_to_nest_address,
                                            self.__interscalehub_nest_to_tvb_address)"""
        self.__log_message("initialized")

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

    def parse_args(arguments):
        pass

    @property
    def rank(self):
        return self.__rank
    
    @property
    def pid(self):
        return self.__my_pid

    @abstractmethod
    def execute_init_command(self):
        pass

    @abstractmethod
    def execute_start_command(self):
        pass

    @abstractmethod
    def execute_end_command(self):
        pass

    