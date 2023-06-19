export CO_SIM_ROOT_PATH="/home/vagrant/multiscale-cosim"
export CO_SIM_MODULES_ROOT_PATH="${CO_SIM_ROOT_PATH}/myremotefork/TVB-NEST-usecase1"
export CO_SIM_USE_CASE_ROOT_PATH="${CO_SIM_MODULES_ROOT_PATH}"
export PYTHONPATH=${CO_SIM_USE_CASE_ROOT_PATH}:/home/vagrant/multiscale-cosim/site-packages:/home/vagrant/multiscale-cosim/nest/lib/python3.8/site-packages
#/home/vagrant/multiscale-cosim/site-packages:/home/vagrant/multiscale-cosim/TVB-NEST-usecase1

### FOR TESTING ###
export CO_SIM_TEST_PATH="${CO_SIM_ROOT_PATH}/myremotefork/TVB-NEST-usecase1/test"
export CO_SIM_TEST_SETTINGS="${CO_SIM_TEST_PATH}/XML/global_settings.xml"
export CO_SIM_TEST_PLAN="${CO_SIM_TEST_PATH}/XML/model_plan.xml"

export PATH=/home/vagrant/multiscale-cosim/nest/bin:${PATH}

#pytest -s -v --global-settings=${CO_SIM_TEST_PATH}/XML/global_settings.xml --action-plan=${CO_SIM_TEST_PATH}/XML/model_plan.xml script.py 

pytest -s -v script.py