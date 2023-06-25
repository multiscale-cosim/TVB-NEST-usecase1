from dataclasses import dataclass
from cosim_parameters import CoSimParameters

@dataclass(frozen=True)
class Parameters(CoSimParameters):

    # ALL commented parameters are linked parameter manage by parameters_manager.py
    # For the exploration of parameters never use the same name two times in the dictionary param

    # parameter for the cosimulations and parameters of the simulations
    """
    param_co_simulation = {
        # boolean for check if there are or not co-simulation
        'co-simulation': False,
        # number of MPI process for nest
        # select if nest is use or not
        'nb_MPI_nest': 1,
        # save or not nest( result with MPI )
        'record_MPI': False,
        # id of region simulate by nest
        'id_region_nest': [2, 5],
        # time of synchronization between node
        'synchronization': 1.0,  # Todo compute with the min of delay
        # level of log : debug 0, info 1, warning 2, error 3, critical 4
        'level_log': 1,
        # command to launch mpi executable:
        'mpi': ['mpirun'],  # example : ['mpirun'] , ['srun','-N','1']
        # Number of process for the transformation : 3 => MPI internal communication and 1 => thread internal communication
        # thread version doesn't work for cluster due to python interruption of MPI function
        'transformation_thread': False,
        # Optional parameters for running with sarus or docker images
        # 'singularity' : Nest_TVB_paper.simg
        # 'sarus':"sarus": ["sarus","run","--mount=type=bind,source=./case_asynchronous/,destination=./case_asynchronous/","load/library/PAPER_v1"]
    }
    """
    # parameter simulators
    param_nest = {
        # Resolution of the simulation (in ms).
        'sim_resolution': 0.1,
        # Masterseed for NEST and NumPy.
        'master_seed': 46,
        # Number of threads per MPI process.
        'total_num_virtual_procs': 3,
        # If True, data will be overwritten,
        # If False, a NESTError is raised if the files already exist.
        'overwrite_files': True,
        # Print the time progress, this should only be used when the simulation
        # is run on a local machine.
        'print_time': True,
        # verbosity of Nest :M_ALL=0, M_DEBUG=5, M_STATUS=7, M_INFO=10, M_WARNING=20, M_ERROR=30, M_FATAL=40, M_QUIET=100
        'verbosity': 20
    }

    # parameter for nest simulation
    param_nest_topology = {
        # number of region of simulated in the brain
        'nb_region': 10,
        # Number of neurons by region
        'nb_neuron_by_region': int(1e4),
        # Percentage of inhibitory neurons
        'percentage_inhibitory': 0.2,
        # Type of neuron
        'neuron_type': 'aeif_cond_exp',
        # Parameter of excitatory neuron (different to default value)
        # Some parameters are not use in TVB
        'param_neuron_excitatory': {
            'C_m': 200.0,
            't_ref': 5.0,
            'V_reset': -64.5,
            'E_L': -64.5,
            'g_L': 10.0,
            'I_e': 0.0,
            'a': 0.0,
            'b': 1.0,
            'Delta_T': 2.0,
            'tau_w': 500.0,
            'V_th': -50.0,
            'E_ex': 0.0,
            'tau_syn_ex': 5.0,
            'E_in': -80.0,
            'tau_syn_in': 5.0,
        },
        # Parameter for inhibitory neurons
        #  Some parameters are not use in TVB
        # Not implementation of the exploration parameter for inhibitory neurons
        'param_neuron_inhibitory': {
            'C_m': 200.0,
            't_ref': 5.0,
            'V_reset': -65.0,
            'E_L': -65.,
            'g_L': 10.0,
            'I_e': 0.0,
            'a': 0.0,
            'b': 0.0,
            'Delta_T': 0.5,
            'tau_w': 1.0,
            'V_th': -50.0,
            'E_ex': 0.0,
            'tau_syn_ex': 5.0,
            'E_in': -80.0,
            'tau_syn_in': 5.0,
        },
        # Mean of external input
        'mean_I_ext': 0.0,
        # Standard deviation of the external input
        'sigma_I_ext': 0.0,
        # Standard deviation of initial condition
        'sigma_V_0': 0.,
        # Mean deviation of initial condition
        'mean_w_0': 0.0,
    }

    param_nest_connection = {
        # Saving parameters : file for connection homogeneous
        'path_homogeneous': path + '/connection_homogeneous_',
        # Saving parameters : file for connection heterogenous
        'path_heterogeneous': path + '/connection_heterogeneous_',
        # weigth in the population from excitatory neurons
        'weight_local': 1.0,
        # ratio between excitatory weight and inhibitory weight
        'g': 3.5,
        # probability inside the region
        'p_connect': 0.05,
        # number of external synapse:
        'nb_external_synapse': 400,
        # path for the connectivity matrix (normalise in order to sum of input for region egual 1)
        'path_weight': path + '/weights.npy',
        # path for the distance matrix
        'path_distance': path + '/distance.npy',
        # path for the center of the node
        'path_centers': path + '/centres.txt',
        # path for the distance matrix
        'path_region_labels': path + '/region_labels.txt',
        # velocity of transmission in m/s
        'velocity': 3.0,
        # Weight between region
        'weight_global': 1.0,
    }

    param_nest_background = {
        # define if the simulation use or not a poisson generator
        'poisson': True,
        # rate of poisson
        'rate_ex': 400 * 1e-3 + 2.0 * 150,
        'rate_in': 200.0 * 1.e-3 + 0.0 * 150,
        # the weight on the connection
        # 'weight_poisson':param_nest_connection['weight_local'],
        # define if the simulation have or not noise
        'noise': False,
        # Mean of the noise in pA
        'mean_noise': 0.0,
        # Standard deviation of the noise
        'sigma_noise': 400.0,
        # the weight on the connection
        'weight_noise': 1.0,
        # stimulus
        'stimulus': False,
        # stimulus amplitude
        'stimulus_amplitude': 0.0,
        # stimulus time to start
        'stimulus_start': 0.0,
        # stimulus duration
        'stimulus_duration': 0.0,
        # stimulus populatin target
        'stimulus_target': 0,
        # multimeter => ask a lot of memory
        'multimeter': False,
        'multimeter_list': {'pop_1_ex_VM': (['V_m'], 0, 10), 'pop1_ex_W': (['w'], 0, 10),
                            'pop_1_in_VM': (['V_m'], 800, 810), 'pop1_in_W': (['w'], 800, 810)},
        'record_spike': False,
        'record_spike_list': {'pop_1_ex': (0, 799), 'pop_2_ex': (1000, 1799), 'pop_1_in': (800, 999),
                            'pop_2_in': (1800, 1999)},
    }
