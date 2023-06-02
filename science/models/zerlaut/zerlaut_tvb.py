
import numpy as np, numpy.random as rgn
from mpi4py import MPI
import os, sys, time, pathlib, json

import logging
#logging.getLogger('numba').setLevel(logging.WARNING)
#logging.getLogger('tvb').setLevel(logging.ERROR)

import tvb.simulator.lab as lab
from nest_elephant_tvb.Tvb.modify_tvb import Zerlaut as Zerlaut
from nest_elephant_tvb.Tvb.modify_tvb.Interface_co_simulation_parallel import Interface_co_simulation
from nest_elephant_tvb.Tvb.helper_function_zerlaut import ECOG,findVec
from nest_elephant_tvb.Tvb.wrapper_TVB import simulate_tvb

from science.parameters.zerlaut.model_parameters_tvb import Parameters as ParametersTVB
from EBRAINS_ConfigManager.global_configurations_manager.xml_parsers.default_directories_enum import DefaultDirectories

class ZerlautTVB:
    def __init__(self, p_configurations_manager, p_log_settings, sci_params, path_parameter):
            self._log_settings = p_log_settings
            self._configurations_manager = p_configurations_manager
            self.__logger = self._configurations_manager.load_log_configurations(
                name="ZerlautTvb",
                log_configurations=self._log_settings,
                target_directory=DefaultDirectories.SIMULATION_RESULTS)
            self.__sci_params = sci_params

            self.__results_path = self._configurations_manager.get_directory(
            directory=DefaultDirectories.SIMULATION_RESULTS)

            #TODO Nest needed to be launched first, because parameter depencendy, "path"
            self.__params = ParametersTVB(results_path=self.__results_path)


    def configure(self,nest_to_tvb_address,tvb_to_nest_address):
        self.nest_to_tvb_address=nest_to_tvb_address
        self.tvb_to_nest_address=tvb_to_nest_address
        self.simulator = self.__init()
        #TODO: step_size or min delay?
        # - param_tvb_monitor['parameter_TemporalAverage']['period'] = param_nest['sim_resolution'] * 10.0
        # - param_tvb_monitor['parameter_Bold']['period']
        return self.__params.param_co_simulation['synchronization']

    def simulate(self):
        self.__run_mpi()
    
###################################
    def __init(self):
        """
        Initialise the simulator with parameter
        :param param_tvb_connection : parameters for the connection
        :param param_tvb_coupling : parameters for the coupling between nodes
        :param param_tvb_integrator : parameters of the integrator and the noise
        :param param_tvb_model : parameters for the models of TVB
        :param param_tvb_monitor : parameters for TVB monitors
        :param cosim : if use or not mpi
        :return: the simulator initialize
        """
        ## initialise the random generator
        rgn.seed(self.__paramsparam_tvb_integrator['seed_init'] - 1)

        ## Model configuration
        if self.__paramsparam_tvb_model['order'] == 1:
            model = Zerlaut.ZerlautAdaptationFirstOrder(variables_of_interest='E I W_e W_i'.split())
        elif self.__params.param_tvb_model['order'] == 2:
            model = Zerlaut.ZerlautAdaptationSecondOrder(variables_of_interest='E I C_ee C_ei C_ii W_e W_i'.split())
        else:
            raise Exception('Bad order for the model')
        model.g_L = np.array(self.__params.param_tvb_model['g_L'])
        model.E_L_e = np.array(self.__params.param_tvb_model['E_L_e'])
        model.E_L_i = np.array(self.__params.param_tvb_model['E_L_i'])
        model.C_m = np.array(self.__params.param_tvb_model['C_m'])
        model.b_e = np.array(self.__params.param_tvb_model['b_e'])
        model.a_e = np.array(self.__params.param_tvb_model['a_e'])
        model.b_i = np.array(self.__params.param_tvb_model['b_i'])
        model.a_i = np.array(self.__params.param_tvb_model['a_i'])
        model.tau_w_e = np.array(self.__params.param_tvb_model['tau_w_e'])
        model.tau_w_i = np.array(self.__params.param_tvb_model['tau_w_i'])
        model.E_e = np.array(self.__params.param_tvb_model['E_e'])
        model.E_i = np.array(self.__params.param_tvb_model['E_i'])
        model.Q_e = np.array(self.__params.param_tvb_model['Q_e'])
        model.Q_i = np.array(self.__params.param_tvb_model['Q_i'])
        model.tau_e = np.array(self.__params.param_tvb_model['tau_e'])
        model.tau_i = np.array(self.__params.param_tvb_model['tau_i'])
        model.N_tot = np.array(self.__params.param_tvb_model['N_tot'])
        model.p_connect_e = np.array(self.__params.param_tvb_model['p_connect_e'])
        model.p_connect_i = np.array(self.__params.param_tvb_model['p_connect_i'])
        model.g = np.array(self.__params.param_tvb_model['g'])
        model.T = np.array(self.__params.param_tvb_model['T'])
        model.P_e = np.array(self.__params.param_tvb_model['P_e'])
        model.P_i = np.array(self.__params.param_tvb_model['P_i'])
        model.K_ext_e = np.array(self.__params.param_tvb_model['K_ext_e'])
        model.K_ext_i = np.array(0)
        model.tau_OU = np.array(self.__params.param_tvb_model['tau_OU'])
        model.weight_noise = np.array(self.__params.param_tvb_model['weight_noise'])
        model.external_input_ex_ex = np.array(self.__params.param_tvb_model['excitatory_extern'])
        model.external_input_in_ex = np.array(self.__params.param_tvb_model['excitatory_extern'])
        model.external_input_in_ex = np.array(0.0)
        model.external_input_in_in = np.array(0.0)
        model.state_variable_range['E'] = np.array(self.__params.param_tvb_model['initial_condition']['E'])
        model.state_variable_range['I'] = np.array(self.__params.param_tvb_model['initial_condition']['I'])
        if self.__params.param_tvb_model['order'] == 2:
            model.state_variable_range['C_ee'] = np.array(self.__params.param_tvb_model['initial_condition']['C_ee'])
            model.state_variable_range['C_ei'] = np.array(self.__params.param_tvb_model['initial_condition']['C_ei'])
            model.state_variable_range['C_ii'] = np.array(self.__params.param_tvb_model['initial_condition']['C_ii'])
        model.state_variable_range['W_e'] = np.array(self.__params.param_tvb_model['initial_condition']['W_e'])
        model.state_variable_range['W_i'] = np.array(self.__params.param_tvb_model['initial_condition']['W_i'])

        ## Connection
        nb_region = int(self.__params.param_tvb_connection['nb_region'])
        tract_lengths = np.load(self.__params.param_tvb_connection['path_distance'])
        weights = np.load(self.__params.param_tvb_connection['path_weight'])
        if 'path_region_labels' in self.__params.param_tvb_connection.keys():
            region_labels = np.loadtxt(self.__params.param_tvb_connection['path_region_labels'], dtype=str)
        else:
            region_labels = np.array([], dtype=np.dtype('<U128'))
        if 'path_centers' in self.__params.param_tvb_connection.keys():
            centers = np.loadtxt(self.__params.param_tvb_connection['path_centers'])
        else:
            centers = np.array([])
        if 'orientation' in self.__params.param_tvb_connection.keys() and self.__params.param_tvb_connection['orientation']:
            orientation = []
            for i in np.transpose(centers):
                orientation.append(findVec(i, np.mean(centers, axis=1)))
            orientation = np.array(orientation)
        else:
            orientation = None
        if 'path_cortical' in self.__params.param_tvb_connection.keys():
            cortical = np.load(self.__params.param_tvb_connection['path_cortical'])
        else:
            cortical = None
        connection = lab.connectivity.Connectivity(number_of_regions=nb_region,
                                                tract_lengths=tract_lengths[:nb_region, :nb_region],
                                                weights=weights[:nb_region, :nb_region],
                                                region_labels=region_labels,
                                                centres=centers.T,
                                                cortical=cortical,
                                                orientations=orientation)
        # if 'normalised' in param_tvb_connection.keys() or param_tvb_connection['normalised']:
        #     connection.weights = connection.weights / np.sum(connection.weights, axis=0)
        connection.speed = np.array(self.__params.param_tvb_connection['velocity'])

        ## Coupling
        coupling = lab.coupling.Linear(a=np.array(self.__params.param_tvb_coupling['a']),
                                    b=np.array(0.0))

        ## Integrator
        # add gaussian noise to the noise of the model
        noise = lab.noise.Additive(
            nsig=np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]),
            ntau=0.0,
            noise_seed = self.__params.param_tvb_integrator['seed']
        )
        noise.random_stream.seed(self.__params.param_tvb_integrator['seed'])
        integrator = lab.integrators.HeunStochastic(noise=noise, dt=self.__params.param_tvb_integrator['sim_resolution'])

        ## Monitors
        monitors = []
        if self.__params.param_tvb_monitor['Raw']:
            monitors.append(lab.monitors.Raw())
        if self.__params.param_tvb_monitor['TemporalAverage']:
            monitor_TAVG = lab.monitors.TemporalAverage(
                variables_of_interest=self.__params.param_tvb_monitor['parameter_TemporalAverage']['variables_of_interest'],
                period=self.__params.param_tvb_monitor['parameter_TemporalAverage']['period'])
            monitors.append(monitor_TAVG)
        if self.__params.param_tvb_monitor['Bold']:
            monitor_Bold = lab.monitors.Bold(
                variables_of_interest=np.array(self.__params.param_tvb_monitor['parameter_Bold']['variables_of_interest']),
                period=self.__params.param_tvb_monitor['parameter_Bold']['period'])
            monitors.append(monitor_Bold)
        if self.__params.param_tvb_monitor['ECOG']:
            volume = np.loadtxt(self.__params.param_tvb_monitor['parameter_ECOG']['path_volume'])[:nb_region]  # volume of the regions
            monitors.append(ECOG().from_file(self.__params.param_tvb_monitor['parameter_ECOG']['path'],
                                            self.__params.param_tvb_monitor['parameter_ECOG']['scaling'],
                                            volume=volume
        
                                            ))
        
        # special monitor for MPI
        monitor_IO = Interface_co_simulation(
            id_proxy=self.__params.param_co_simulation['id_region_nest'],
            time_synchronize=self.__params.param_co_simulation['synchronization']
        )
        
        monitors.append(monitor_IO)

        # initialize the simulator:
        simulator = lab.simulator.Simulator(model=model, connectivity=connection,
                                            coupling=coupling, integrator=integrator, monitors=monitors
                                            )
        simulator.configure()
        # save the initial condition
        np.save(self.__params.param_tvb_monitor['path_result'] + '/step_init.npy', simulator.history.buffer)
        # end edit
        return simulator
    
    def __run_mpi(self):#, init, path
        """
        return the result of the simulation between the wanted time
        :param init: function of the initialisation of TVB simulator
        :param path: the folder of the simulation
        """
        # take the parameters of the simulation from the saving file
        #with open(path + '/parameter.json') as f:
        #    parameters = json.load(f)

        #param_co_simulation =  parameters['param_co_simulation'] 
        #param_tvb_connection =  parameters['param_tvb_connection']
        #param_tvb_coupling = parameters['param_tvb_coupling']
        #param_tvb_integrator = parameters['param_tvb_integrator']
        #param_tvb_model = parameters['param_tvb_model']
        #param_tvb_monitor = parameters['param_tvb_monitor']

        # TODO: define it
        #result_path = parameters['result_path']
        end = self.__params.param_co_simulation['end'] 

        # configuration of the logger
        #logger = create_logger(path, 'tvb', param_co_simulation['level_log'])

        # initialise the TVB
        self.__params.param_tvb_monitor['path_result'] = self.__results_path + '/tvb/'
        id_proxy = self.__params.param_co_simulation['id_region_nest']
        time_synch = self.__params.param_co_simulation['synchronization']
        #path_send = self.__result_path + "/transformation/send_to_tvb/"
        #path_receive = self.__result_path + "/transformation/receive_from_tvb/"
        self.__simulator = self.__init() 

        # configure for saving result of TVB
        # check how many monitor it's used
        nb_monitor = self.__params.param_tvb_monitor['Raw'] + self.__params.param_tvb_monitor['TemporalAverage'] + self.__params.param_tvb_monitor['Bold'] \
                    + self.__params.param_tvb_monitor['ECOG']
        if self.__params.param_tvb_monitor['save_time'] > 0:
            # initialise the variable for the saving the result
            save_result = []
            for i in range(nb_monitor):  # the input output monitor
                save_result.append([])

        # init MPI :
        data = None  # data for the proxy node (no initialisation in the parameter)
        comm_receive = []
        for i in id_proxy:
            comm_receive.append(self.__init_mpi(self.nest_to_tvb_address))# path_send + str(i) + ".txt"
        comm_send = []
        for i in id_proxy:
            comm_send.append(self.__init_mpi(self.tvb_to_nest_address))#path_receive + str(i) + ".txt"

        self.__logger.info("send initialisation of TVB : prepare data")
        initialisation_data = []
        for i in np.arange(0, np.rint(time_synch / self.simulator.integrator.dt), 1, dtype=np.int):
            initialisation_data.append(self.simulator._loop_compute_node_coupling(i)[:, id_proxy, :])
        initialisation_data = np.concatenate(initialisation_data)
        time_init = [0, time_synch]
        self.__logger.info("send initialisation of TVB : send data")
        for index, comm in enumerate(comm_send):
            self.__send_mpi(comm, time_init, initialisation_data[:, index] * 1e3)

        # the loop of the simulation
        count = 0
        count_save = 0
        while count * time_synch < end:  # FAT END POINT
            self.__logger.info(" TVB receive data start")
            # receive MPI data
            data_value = []
            for comm in comm_receive:
                receive = self.__receive_mpi(comm)
                time_data = receive[0]
                data_value.append(receive[1])
            self.__logger.info(" TVB receive data values")
            data = np.empty((2,), dtype=object)
            nb_step = np.rint((time_data[1] - time_data[0]) / self.__params.param_tvb_integrator['sim_resolution'])
            nb_step_0 = np.rint(
                time_data[0] / self.__params.param_tvb_integrator['sim_resolution']) + 1  # start at the first time step not at 0.0
            time_data = np.arange(nb_step_0, nb_step_0 + nb_step, 1) * self.__params.param_tvb_integrator['sim_resolution']
            data_value = np.swapaxes(np.array(data_value), 0, 1)[:, :]
            if data_value.shape[0] != time_data.shape[0]:
                raise (Exception('Bad shape of data'))
            data[:] = [time_data, data_value]

            self.__logger.info(" TVB start simulation " + str(count * time_synch))
            nest_data = []
            for result in self.simulator(simulation_length=time_synch, proxy_data=data):
                for i in range(nb_monitor):
                    if self.__params.param_tvb_monitor['save_time'] > 0 and result[i] is not None:
                        save_result[i].append(result[i])
                nest_data.append([result[-1][0], result[-1][1]])

                # save the result in file
                # check if the time for saving at some time step
                if self.__params.param_tvb_monitor['save_time'] > 0 and result[-1][0] >= self.__params.param_tvb_monitor['save_time'] * (
                        count_save + 1):
                    np.save(self.__params.param_tvb_monitor['path_result'] + '/step_' + str(count_save) + '.npy', save_result)
                    save_result = []
                    for i in range(nb_monitor):
                        save_result.append([])
                    count_save += 1
            self.__logger.info(" TVB end simulation")

            # prepare to send data with MPI
            nest_data = np.array(nest_data)
            times = [nest_data[0, 0], nest_data[-1, 0]]
            rate = np.concatenate(nest_data[:, 1])
            for index, comm in enumerate(comm_send):
                self.__send_mpi(comm, times, rate[:, index] * 1e3)

            # increment of the loop
            count += 1
        # save the last part
        self.__logger.info(" TVB finish")
        if self.__params.param_tvb_monitor['save_time'] > 0:
            np.save(self.__params.param_tvb_monitor['path_result'] + '/step_' + str(count_save) + '.npy', save_result)
        for index, comm in enumerate(comm_send):
            self.__logger.info('end comm send')
            self.__end_mpi(comm, self.tvb_to_nest_address, True)#self.__result_path + "/transformation/receive_from_tvb/" + str(id_proxy[index]) + ".txt"
        for index, comm in enumerate(comm_receive):
            self.__logger.info('end comm receive')
            self.__end_mpi(comm, self.nest_to_tvb_address, False)#self.__result_path + "/transformation/send_to_tvb/" + str(id_proxy[index]) + ".txt"
        self.__logger.info(" TVB exit")
        return


    ## MPI function for receive and send data
    def __init_mpi(self, port):
        """
        initialise MPI connection
        :param path: path of the file for the port
        :param logger: logger of the modules
        :return:
        """

        self.__logger.info("wait connection " + port)
        comm = MPI.COMM_WORLD.Connect(port)
        self.__logger.info('connect to ' + port)
        return comm


    def __send_mpi(self, comm, times, data):
        """
        send mpi data
        :param comm: MPI communicator
        :param times: times of values
        :param data: rates inputs
        :param logger: logger of wrapper
        :return:nothing
        """
        self.__logger.info("start send")
        status_ = MPI.Status()
        # wait until the transformer accept the connections
        accept = False
        while not accept:
            req = comm.irecv(source=0, tag=0)
            accept = req.wait(status_)
            self.__logger.info("send accept")
        source = status_.Get_source()  # the id of the excepted source
        self.__logger.info("get source")
        data = np.ascontiguousarray(data, dtype='d')  # format the rate for sending
        shape = np.array(data.shape[0], dtype='i')  # size of data
        times = np.array(times, dtype='d')  # time of starting and ending step
        comm.Send([times, MPI.DOUBLE], dest=source, tag=0)
        comm.Send([shape, MPI.INT], dest=source, tag=0)
        comm.Send([data, MPI.DOUBLE], dest=source, tag=0)
        self.__logger.info("end send")


    def __receive_mpi(self, comm):
        """
            receive proxy values the
        :param comm: MPI communicator
        :param logger: logger of wrapper
        :return: rate of all proxy
        """
        self.__logger.info("start receive")
        status_ = MPI.Status()
        # send to the transformer : I want the next part
        req = comm.isend(True, dest=0, tag=0)
        req.wait()
        time_step = np.empty(2, dtype='d')
        comm.Recv([time_step, 2, MPI.DOUBLE], source=0, tag=MPI.ANY_TAG, status=status_)
        # get the size of the rate
        size = np.empty(1, dtype='i')
        comm.Recv([size, MPI.INT], source=0, tag=0)
        # get the rate
        rates = np.empty(size, dtype='d')
        comm.Recv([rates, size, MPI.DOUBLE], source=0, tag=MPI.ANY_TAG, status=status_)
        self.__logger.info("end receive " + str(time_step))
        # print the summary of the data
        if status_.Get_tag() == 0:
            return time_step, rates
        else:
            return None  # TODO take in count


    def __end_mpi(self, comm, path, sending):
        """
        ending the communication
        :param comm: MPI communicator
        :param path: for the close the port
        :param sending: if the transformer is for sending or receiving data
        :param logger: logger of the module
        :return: nothing
        """
        # read the port before the deleted file
        fport = open(path, "r")
        port = fport.readline()
        fport.close()
        # different ending of the transformer
        if sending:
            self.__logger.info("TVB close connection send " + port)
            sys.stdout.flush()
            status_ = MPI.Status()
            # wait until the transformer accept the connections
            self.__logger.info("TVB send check")
            accept = False
            while not accept:
                req = comm.irecv(source=0, tag=0)
                accept = req.wait(status_)
            self.__logger.info("TVB send end simulation")
            source = status_.Get_source()  # the id of the excepted source
            times = np.array([0., 0.], dtype='d')  # time of starting and ending step
            comm.Send([times, MPI.DOUBLE], dest=source, tag=1)
            comm.Barrier()
        else:
            self.__logger.info("TVB close connection receive " + port)
            # send to the transformer : I want the next part
            req = comm.isend(True, dest=0, tag=1)
            req.wait()
            comm.Barrier()
        # closing the connection at this end
        self.__logger.info("TVB disconnect communication")
        comm.Disconnect()
        self.__logger.info("TVB close " + port)
        MPI.Close_port(port)
        self.__logger.info("TVB close connection " + port)
        return