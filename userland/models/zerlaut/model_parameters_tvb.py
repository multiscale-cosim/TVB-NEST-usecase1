from dataclasses import dataclass

from science.parameters.zerlaut.model_parameters_nest import Parameters as ParameterNest
from cosim_parameters import CoSimParameters

@dataclass
class Parameters(CoSimParameters):
    parameters = {}
    
    #param_co_simulation = ParameterNest.param_co_simulation 
    param_nest = ParameterNest.param_nest
    param_nest_connection = ParameterNest.param_nest_connection
    param_nest_topology = ParameterNest.param_nest_topology
    #param_tvb_model = ParameterNest.param_tvb_model

    # link between parameter in nest :
    param_nest_background = ParameterNest.param_nest_background
    param_nest_background['weight_poisson'] = ParameterNest.param_nest_connection['weight_local']
    parameters['param_nest_background'] = param_nest_background

    # link between parameter of TVB and parameter of NEST :

    ## connection
    param_tvb_connection = {} #parameters['param_tvb_connection']
    param_tvb_connection['path_distance'] = param_nest_connection['path_distance']
    param_tvb_connection['path_weight'] = param_nest_connection['path_weight']
    param_tvb_connection['nb_region'] = param_nest_topology['nb_region']
    param_tvb_connection['velocity'] = param_nest_connection['velocity']
    parameters['param_tvb_connection'] = param_tvb_connection

    ## coupling
    param_tvb_coupling = {} #parameters['param_tvb_coupling']
    param_tvb_coupling['a'] = param_nest_connection['weight_global']
    parameters['param_tvb_coupling'] = param_tvb_coupling

    ## integrator and noise
    param_tvb_integrator = {} #parameters['param_tvb_integrator']
    param_tvb_integrator['sim_resolution'] = param_nest['sim_resolution']
    param_tvb_integrator['seed'] = param_nest['master_seed'] - 1
    param_tvb_integrator['seed_init'] = param_nest['master_seed'] - 2
    parameters['param_tvb_integrator'] = param_tvb_integrator

    #TODO: It comes from test_nest.py
    # parameter for the model of the node : ZERLAUT model / Mean field AdEX
    param_tvb_model = {
        # order of the model
        'order': 2,
        # 'g_L':param_nest_topology['param_neuron_excitatory']['g_L']
        # 'E_L_e':param_nest_topology['param_neuron_excitatory']['E_L']
        # 'E_L_i':param_nest_topology['param_neuron_inhibitory']['E_L']
        # 'C_m':param_nest_topology['param_neuron_excitatory']['C_m']
        # 'b_e':param_nest_topology['param_neuron_excitatory']['b']
        # 'a_e':param_nest_topology['param_neuron_excitatory']['a']
        # 'b_i':param_nest_topology['param_neuron_inhibitory']['b']
        # 'a_i':param_nest_topology['param_neuron_inhibitory']['a']
        # 'tau_w_e':param_nest_topology['param_neuron_excitatory']['tau_w']
        # 'tau_w_i':param_nest_topology['param_neuron_inhibitory']['tau_w']
        # 'E_e':param_nest_topology['param_neuron_excitatory']['E_ex']
        # 'E_i':param_nest_topology['param_neuron_excitatory']['E_in']
        # 'Q_e':param_nest_connection['weight_local']
        # 'Q_i':param_nest_connection['weight_local']*param_nest_connection['g']
        # 'tau_e':param_nest_topology['param_neuron_excitatory']['tau_syn_ex']
        # 'tau_i':param_nest_topology['param_neuron_excitatory']['tau_syn_in']
        # 'N_tot':param_nest_topology['nb_neuron_by_region']
        # 'p_connect_e':param_nest_connection['p_connect']
        # 'p_connect_i':param_nest_connection['p_connect']
        # 'g':param_nest_topology['percentage_inhibitory']
        # 'K_ext_e':param_nest_connection['nb_external_synapse']
        # Time constant of the model
        'T': 20.0,
        # Polynome for excitatory neurons | WARNING :should be change when the parameter of neurons change)
        'P_e': [-0.05059317, 0.0036078, 0.01794401, 0.00467008, 0.00098553, 0.0082953, -0.00985289, -0.02600252,
                -0.00274499, -0.01051463],
        # Polynome for inhibitory neurons | WARNING: should be change when the parameter of neurons change)
        'P_i': [-5.96722865e-02, 7.15675508e-03, 4.28252163e-03, 9.25089702e-03, 1.16632197e-06, -1.00659310e-02,
                3.89257235e-03, 4.45787751e-04, 4.20050937e-03, 4.37359879e-03],
        'tau_OU': 5.0,
        'weight_noise': 10.5*1e-5,
        "excitatory_extern": 0.0,
        # initial condition, should be simmilar than nest
        'initial_condition': {"E": [0.100, 0.001], "I": [0.0, 0.0], "C_ii": [0.0, 0.0], "W_e": [0.0, 0.0],
                            "C_ee": [0.0, 0.0], "C_ei": [0.0, 0.0], "W_i": [0.0, 0.0]},
    }

    ## parameter of the model
    param_tvb_model['g_L'] = param_nest_topology['param_neuron_excitatory']['g_L'] 
    param_tvb_model['E_L_e'] = param_nest_topology['param_neuron_excitatory']['E_L']
    param_tvb_model['E_L_i'] = param_nest_topology['param_neuron_inhibitory']['E_L']
    param_tvb_model['C_m'] = param_nest_topology['param_neuron_excitatory']['C_m']
    param_tvb_model['b_e'] = param_nest_topology['param_neuron_excitatory']['b']
    param_tvb_model['a_e'] = param_nest_topology['param_neuron_excitatory']['a']
    param_tvb_model['b_i'] = param_nest_topology['param_neuron_inhibitory']['b']
    param_tvb_model['a_i'] = param_nest_topology['param_neuron_inhibitory']['a']
    param_tvb_model['tau_w_e'] = param_nest_topology['param_neuron_excitatory']['tau_w']
    param_tvb_model['tau_w_i'] = param_nest_topology['param_neuron_inhibitory']['tau_w']
    param_tvb_model['E_e'] = param_nest_topology['param_neuron_excitatory']['E_ex']
    param_tvb_model['E_i'] = param_nest_topology['param_neuron_excitatory']['E_in']
    param_tvb_model['Q_e'] = param_nest_connection['weight_local']
    param_tvb_model['Q_i'] = param_nest_connection['weight_local'] * param_nest_connection['g']
    param_tvb_model['tau_e'] = param_nest_topology['param_neuron_excitatory']['tau_syn_ex']
    param_tvb_model['tau_i'] = param_nest_topology['param_neuron_excitatory']['tau_syn_in']
    param_tvb_model['N_tot'] = param_nest_topology['nb_neuron_by_region']
    param_tvb_model['p_connect_e'] = param_nest_connection['p_connect']
    param_tvb_model['p_connect_i'] = param_nest_connection['p_connect']
    param_tvb_model['g'] = param_nest_topology['percentage_inhibitory']
    param_tvb_model['K_ext_e'] = param_nest_connection['nb_external_synapse']
    parameters['param_tvb_model'] = param_tvb_model

    ## code from 
    # /home/vagrant/multiscale-cosim/myremotefork/TVB-NEST-usecase1/science/models/zerlaut/zerlaut_nest.pytest_nest.py
    #

    # parameter TVB for the monitors
    param_tvb_monitor = {
        # the time of simulation in each file
        'save_time': 20.0,
        # use or not the Raw monitor
        'Raw': True,
        # Use or not the Temporal Average Monitor
        'TemporalAverage': False,
        # Parameter for Temporal Average Monitor
        'parameter_TemporalAverage': {
            'variables_of_interest': [0, 1, 2, 3],
            'period': param_nest['sim_resolution']*10.0 # 1s assuming the step size is 0.1 ms
        },
        # Use or not the Bold Monitor
        'Bold': False,
        # Paramter for the Bold Monitor
        'parameter_Bold': {
            'variables_of_interest': [0],
            'period':param_nest['sim_resolution']*20000.0 # 20 min assuming the step size is 0.1 ms
        },
        'ECOG': False,
        'parameter_ECOG': {
            # 'path': , # path of sensor
            # 'path_volume': , # path of text file with the volume size of each region (1 by line)
            # 'scaling':,
            # 'sigma_noise'
        },
    }
    
    ## monitor
    #param_tvb_monitor = parameters['param_tvb_monitor']
    #param_tvb_monitor['parameter_TemporalAverage']['period'] = param_nest['sim_resolution'] * 10.0
    #param_tvb_monitor['parameter_Bold']['period'] = param_nest['sim_resolution'] * 20000.0
    #parameters['param_tvb_monitor'] = param_tvb_monitor

    #Modifing result path after the initialization
    def __post_init__(self, results_path):
        # Parameter for the transformer 
        if self.param_co_simulation['co-simulation']:
            # parameters for the transformation TVB to Nest
            if 'param_TR_tvb_to_nest' in self.parameters.keys():
                param_TR_tvb_to_nest = self.parameters['param_TR_tvb_to_nest']
            else:
                param_TR_tvb_to_nest = {}
            param_TR_tvb_to_nest['level_log'] = self.param_co_simulation['level_log']
            param_TR_tvb_to_nest['seed'] = self.param_nest['master_seed'] - 3
            param_TR_tvb_to_nest['nb_synapses'] = self.param_nest_connection['nb_external_synapse']
            self.parameters['param_TR_tvb_to_nest'] = param_TR_tvb_to_nest

            # parameters for the transformation nest to TVB
            if 'param_TR_nest_to_tvb' in self.parameters.keys():
                param_TR_nest_to_tvb = self.parameters['param_TR_nest_to_tvb']
            else:
                param_TR_nest_to_tvb = {}
            if not 'init' in param_TR_nest_to_tvb.keys():
                path_spikes = results_path + '/init_spikes.npy'# TODO: change to sel
                init_spikes = np.zeros((int(self.param_co_simulation['synchronization'] / self.param_nest['sim_resolution']), 1))
                np.save(path_spikes, init_spikes)
                param_TR_nest_to_tvb['init'] = path_spikes
            param_TR_nest_to_tvb['resolution'] = self.param_nest['sim_resolution']
            param_TR_nest_to_tvb['nb_neurons'] = self.param_nest_topology['nb_neuron_by_region'] * (
                        1 - self.param_nest_topology['percentage_inhibitory'])
            param_TR_nest_to_tvb['synch'] = self.param_co_simulation['synchronization']
            param_TR_nest_to_tvb['width'] = self.param_tvb_model['T']
            param_TR_nest_to_tvb['level_log'] = self.param_co_simulation['level_log']
            self.parameters['param_TR_nest_to_tvb'] = param_TR_nest_to_tvb

        if self.param_co_simulation['record_MPI']:
            if 'param_record_MPI' in self.parameters.keys():
                param_record_MPI = self.parameters['param_record_MPI']
            else:
                param_record_MPI = {}
            param_record_MPI['resolution'] = self.param_nest['sim_resolution']
            param_record_MPI['synch'] = self.param_co_simulation['synchronization']
            param_record_MPI['level_log'] = self.param_co_simulation['level_log']
            self.parameters['param_record_MPI'] = param_record_MPI
