killall -9 srun
killall -9 python3
module --force purge

module load Stages/2022 GCCcore/.11.2.0 GCC/11.2.0 ParaStationMPI/5.5.0-1 Python/3.9.6 mpi4py/3.1.3 CMake/3.21.1 ZeroMQ/4.3.4

export CO_SIM_ROOT_PATH="$PROJECT_<project>/${LOGNAME}/multiscale-cosim"
export CO_SIM_USE_CASE_ROOT_PATH="${CO_SIM_ROOT_PATH}/cosim-repos/TVB-NEST-usecase1"
export CO_SIM_NEST=${CO_SIM_ROOT_PATH}/nest

export PATH=${CO_SIM_NEST}/bin:${PATH}
export PYTHONPATH=${PYTHONPATH}:${CO_SIM_NEST}/lib64/python3.9/site-packages
export PYTHONPATH=${PYTHONPATH}:${CO_SIM_ROOT_PATH}/site-packages
export PYTHONPATH=${PYTHONPATH}:${CO_SIM_USE_CASE_ROOT_PATH}

srun -n 1 --exact python3 main.py --global-settings EBRAINS_WorkflowConfigurations/global_settings/global_settings.xml --action-plan EBRAINS_WorkflowConfigurations/plans/cosim_alpha_brunel_hpc.xml
