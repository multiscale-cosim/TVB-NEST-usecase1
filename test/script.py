from dataclasses import dataclass
import numpy as np

from EBRAINS_ConfigManager.workflow_configurations_manager.xml_parsers import enums
from ms_manager import MSManager

import common.args as cmd_args
import os,sys, pytest, argparse

#import test.models.TVB_NEST_1 as usc_1


GLOBAL_DICT={"global_settings":os.environ["CO_SIM_TEST_SETTINGS"],
             "action_plan":os.environ["CO_SIM_TEST_PLAN"]}

class MyARGS:
    def __init__(self, dict=None):
        if dict is not None:
            for k,v in dict.items():
                setattr(self,k,v)

########################
class TestCoSimulator():
    def test_cosim_general(self):

        ms_manager = MSManager()
        ms_manager.__args = MyARGS(GLOBAL_DICT)

        assert ms_manager.__args.global_settings == GLOBAL_DICT["global_settings"]
        assert ms_manager.__args.action_plan == GLOBAL_DICT["action_plan"]

class TestUseCase():
    def test_NEST_TVB_1(self):
        #TODO
        assert True

    def test_NEST_TVB_2(self):
        #TODO
        assert True
    
    def test_Arbor(self):
        #TODO
        assert True
    
    def test_LFPy(self):
        #TODO
        assert True
    
    def test_NEST_Desktop_Insite(self):
        #TODO
        assert True