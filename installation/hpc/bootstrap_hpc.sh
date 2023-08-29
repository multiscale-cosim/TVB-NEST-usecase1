#!/bin/bash

#
# ASSUMPTION: current location is where use git cloned TVB-NEST-usecase1 repository
# pwd=/location/where/user/cloned
# the following subdirectories will be created then:
#  /TVB-NEST-usecase1
#  /site-packages
#  /nest-build
#  /nest-installed
#  /nest-simulator

PWDPATH=`pwd`
[ -w ${PWDPATH} ] || (echo "${PWDPATH} is not writable"; exit 1)

# ########### #
# HPC MODULES #
# ########### #
module --force purge
module load Stages/2022 GCCcore/.11.2.0  GCC/11.2.0 \
	ParaStationMPI/5.5.0-1 Python/3.9.6 mpi4py/3.1.3 CMake/3.21.1 ZeroMQ/4.3.4

CO_SIM_ROOT_PATH=${PWDPATH}
CO_SIM_DEPENDENCIES=${CO_SIM_ROOT_PATH}/site-packages
CO_SIM_NEST_BUILD=${CO_SIM_ROOT_PATH}/nest-build
CO_SIM_NEST=${CO_SIM_ROOT_PATH}/nest-installed

mkdir -p ${CO_SIM_DEPENDENCIES}

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
HPC_SYSTEM_NAME=`hostname`
HPC_SYSTEM_NAME=${HPC_SYSTEM_NAME##*.}
git clone https://github.com/nest/nest-simulator.git
cd nest-simulator
# 9cb3cb: Merge pull request from VRGroupRWTH/feature/device_label (https://github.com/nest/nest-simulator/commit/9cb3cb2ec1cc76e278ed7e9a8850609fdb443cae) 
# TODO: Needed until NEST v3.6 release to incorporate the aforementioned pull request.
git checkout 9cb3cb
cd ..
mkdir -p ${CO_SIM_NEST} ${CO_SIM_NEST_BUILD}; cd ${CO_SIM_NEST_BUILD}

cmake \
    -DCMAKE_INSTALL_PREFIX:PATH=${CO_SIM_NEST} \
    ${CO_SIM_ROOT_PATH}/nest-simulator \
    -Dwith-mpi=ON \
    -Dwith-openmp=ON \
    -Dwith-readline=ON \
    -Dwith-ltdl=ON \
    -Dcythonize-pynest=ON \
    -DPYTHON_EXECUTABLE=/usr/bin/python3.10 \
    -DPYTHON_INCLUDE_DIR=/usr/include/python3.10 \
    -DPYTHON_LIBRARY=/usr/lib/x86_64-linux-gnu/libpython3.10.so

make -j 16
make install
cd ${CO_SIM_ROOT_PATH}
