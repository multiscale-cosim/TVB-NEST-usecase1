
from mpi4py import MPI
from abc import ABC, abstractmethod

class BasicAdapter(ABC): 
    def __init__(self):
        self.name = name
        self.id = id

        # MPI rank
        self.__comm = MPI.COMM_WORLD
        self.__rank = self.__comm.Get_rank()
        self.__my_pid = os.getpid()
        self.__logger.info(f"__DEBUG__ size: {self.__comm.Get_size()}, my rank: {self.__rank}, "
                           f"host_name:{os.uname()}")

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