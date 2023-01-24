#!/bin/bash

# if we are on hpc systems
module --force purge
module load Stages/2022 GCCcore/.11.2.0  GCC/11.2.0 ParaStationMPI/5.5.0-1 Python/3.9.6 mpi4py/3.1.3 CMake/3.21.1 ZeroMQ/4.3.4

# we are in location/where/user/cloned/TVB-NEST-usecase1/installation
mkdir -p cosim_build
mkdir -p ../slurm_logs

CO_SIM_ROOT_PATH= ${PWD}/cosim_build
CO_SIM_DEPENDENCIES=${CO_SIM_ROOT_PATH}/site-packages
CO_SIM_NEST_BUILD=${CO_SIM_ROOT_PATH}/nest-build
CO_SIM_NEST=${CO_SIM_ROOT_PATH}/nest

mkdir -p ${CO_SIM_DEPENDENCIES}
mkdir -p ${CO_SIM_NEST_BUILD}

# ###
# TVB
# ###
pip install --target=${CO_SIM_DEPENDENCIES} tvb-data==2.0 tvb-gdist==2.1.0 tvb-library==2.2 tvb-contrib==2.2

# ########
# ELEPHANT
# ########
pip install --target=${CO_SIM_DEPENDENCIES} elephant

#
# WARNING: typing.py package produce conflict/issue with Co-Sim simulators
#
rm -f ${CO_SIM_DEPENDENCIES}/typing.py

# ####
# NEST
# ####
cd ${CO_SIM_NEST_BUILD}
cmake \
    -DCMAKE_INSTALL_PREFIX:PATH=${CO_SIM_NEST} \
    ${CO_SIM_ROOT_PATH}/../nest-simulator/ \
    -Dwith-mpi=ON \
    -Dwith-openmp=ON \
    -Dwith-readline=ON \
    -Dwith-ltdl=/p/software/jusuf/stages/2022/software/libtool/2.4.6 \
    -Dcythonize-pynest=ON \
    -DPYTHON_EXECUTABLE=/p/software/jusuf/stages/2022/software/Python/3.9.6-GCCcore-11.2.0/bin/python3.9 \
    -DPYTHON_INCLUDE_DIR=/p/software/jusuf/stages/2022/software/Python/3.9.6-GCCcore-11.2.0/include/python3.9 \
    -DPYTHON_LIBRARY=/p/software/jusuf/stages/2022/software/Python/3.9.6-GCCcore-11.2.0/lib/libpython3.9.so

make -j 16
make install
