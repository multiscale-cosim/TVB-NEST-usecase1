#export PYTHONPATH=/home/vagrant/nest_installed/lib/python3.8/site-packages:/home/vagrant/multiscale-cosim-repos/TVB-NEST-usecase1:/home/vagrant/multiscale-cosim-repos/TVB-NEST-usecase1/EBRAINS-Config-Manager:/home/vagrant/multiscale-cosim-repos/TVB-NEST-usecase1/EBRAINS-Launcher:/home/vagrant/multiscale-cosim-repos/TVB-NEST-usecase1/EBRAINS-RichEndpoint:/home/vagrant/multiscale-cosim-repos/TVB-NEST-usecase1/cosim_example_demos/TVB-NEST-demo:/home/vagrant/multiscale-cosim-repos/TVB-NEST-usecase1/EBRAINS-InterscaleHUB
# export HOME=/home/vagrant/multiscale-cosim-repos/my_forks/TVB-NEST-usecase1
export CO_SIM_ROOT_PATH="/home/vagrant/multiscale-cosim-repos/my_forks"
export CO_SIM_MODULES_ROOT_PATH="${CO_SIM_ROOT_PATH}/TVB-NEST-usecase1"
export CO_SIM_USE_CASE_ROOT_PATH="${CO_SIM_MODULES_ROOT_PATH}"
export PYTHONPATH=/home/vagrant/nest_installed/lib/python3.8/site-packages:/home/vagrant/multiscale-cosim-repos/my_forks/TVB-NEST-usecase1

rm -r /home/vagrant/multiscale-cosim-repos/my_forks/TVB-NEST-usecase1/result_sim


# python3 main.py --global-settings /home/vagrant/multiscale-cosim-repos/TVB-NEST-usecase1/EBRAINS_WorkflowConfigurations/global_settings/global_settings.xml --action-plan /home/vagrant/multiscale-cosim-repos/TVB-NEST-usecase1/EBRAINS_WorkflowConfigurations/plans/nest_to_tvb_cosim_on_local.xml --parameters /home/vagrant/multiscale-cosim-repos/TVB-NEST-usecase1/EBRAINS_WorkflowConfigurations/parameters/nest_to_tvb_parameters.xml
# python3 main.py --global-settings $HOME/EBRAINS_WorkflowConfigurations/global_settings/global_settings.xml --action-plan $HOME/EBRAINS_WorkflowConfigurations/plans/nest_to_tvb_cosim_on_local.xml
python3 main.py --global-settings $CO_SIM_USE_CASE_ROOT_PATH/EBRAINS_WorkflowConfigurations/global_settings/global_settings.xml --action-plan $CO_SIM_USE_CASE_ROOT_PATH/EBRAINS_WorkflowConfigurations/plans/cosim_alpha_brunel_on_local.xml
