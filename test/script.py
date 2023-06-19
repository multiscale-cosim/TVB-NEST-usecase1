
from dataclasses import dataclass
import numpy as np

from EBRAINS_ConfigManager.workflow_configurations_manager.xml_parsers import enums
from ms_manager import MSManager

import common.args as cmd_args
import os,sys, pytest, argparse
import copy
GLOBAL_DICT={"global_settings":os.environ["CO_SIM_TEST_SETTINGS"],
             "action_plan":os.environ["CO_SIM_TEST_PLAN"]}

class MyARGS:
    def __init__(self, dict=None):
        if dict is not None:
            for k,v in dict.items():
                setattr(self,k,v)


########################
class TestCoSimulator():

    def test_cosim(self):

        args = MyARGS(GLOBAL_DICT)
        
        ms_manager = MSManager()
        ms_manager.__args = args

        #print(vars(ms_manager.__args))

        print(ms_manager.__args.global_settings)
        print(ms_manager.__args.global_settings)

        #assert ms_manager_rc == enums.CoSimulatorReturnCodes.OK
        #ms_manager.run()
        #print(ms_manager.__args == None)
        
        if ms_manager.__args == None:
            print("ddddd")


        assert True


