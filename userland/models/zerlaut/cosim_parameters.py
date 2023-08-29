from dataclasses import dataclass

@dataclass(frozen=True)
class CoSimParameters:
    """
        Data class for defining the parameter values for Zerlaut Model
    """
    param_co_simulation = {"co_simulation": True,
                                "simulation_time": 30.0,
                                "level_log": 1,
                                "resolution": 0.1,
                                "nb_neuron_by_region": 1000,
                                "synchronization": 3.5,
                                "id_region_nest": [1,2],
                                "multimeter": False,
                                "record_spike": False,
                                "sigma_V_0": 200.0,
                                'g':[1.0], 'mean_I_ext': [100.0],
                                "begin":0.0, "end":210}