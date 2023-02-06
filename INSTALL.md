# Content
* TVB-NEST-usecase1 installation guide
  1. [HPC systems](#TVB-NEST-usecase1-installation-on-HPC-systems)
  2. [Local systems](#TVB-NEST-usecase1-installation-on-local-systems)
* [Troubleshooting](#Troubleshooting)
* [Q&A](#Q&A)

---

# TVB-NEST-usecase1 installation on HPC systems

##### IMPORTANT: In case one of the referenced scripts throws syntax error, it could be that `dash` is being used instead of `bash`. some explanations why could be found on: https://wiki.ubuntu.com/DashAsBinSh

## STEP 1
### Preparing the installation/running location.
creating the installation directory:\
i.e.
 ``` sh
$ cd /p/projects/<jsc.project.name>/<user.name>
$ mkdir <work.dir.name>
$ cd < work.dir.name>
```
e.g.
``` sh
$ cd /p/projects/cslns/slns013
$ mkdir multiscale-cosim
$ cd multiscale-cosim
```

## STEP 2
### Getting the Co-Simulation Framework
cloning the TVB-NEST-usecase1 repository along with the required submodules\
``` sh
$ git clone --recurse-submodules --jobs 16 https://github.com/multiscale-cosim/TVB-NEST-usecase1.git
```

## STEP 3
### Setting-up the run-time environment
executing the installation script in order to set up the run-time environment\
i.e.
``` sh
$ sh ./TVB-NEST-usecase1/installation/bootstrap_hpc.sh
```

## STEP 4 (OPTIONAL)
### Testing installation 
executing short tests which import TVB and NEST python packages
#### 4.1. Loading HPC modules and setting CO_SIM_* variables
``` sh
$ source ./TVB-NEST-usecase1/installation/tests/co_sim_vars.source
```

#### 4.2. TVB testing
``` sh
$ python3 ./TVB-NEST-usecase1/installation/tests/tvb_test.py
```
Expected output:
``` sh
TVB on Python OKAY!
```

#### 4.3. NEST testing
``` sh
$ python3 ./TVB-NEST-usecase1/installation/tests/nest_test.py
```
Expected output:
``` sh
...            SimulationManager::run [Info]:
    Simulation finished.
NEST on Python OKAY!
```

---

# TVB-NEST-usecase1 installation on local systems

## Step 1
### 1.1 Download and install Vagrant and Virtualbox
- Install [Vagrant version 2.2.19](https://www.vagrantup.com/) or higher
- Install [Virtualbox version 6.1](https://www.virtualbox.org/) or higher

### 1.2 Create directory
e.g.
``` sh
mkdir -p /home/<user.name>cosim/vagrant
cd /home/<user.name>cosim/vagrant
```

### 1.3 Download/create vagrantfile and installation script
copy both scripts into your vagrant directory:
<details>
  <summary>Vagrantfile</summary>
  
  ``` sh
  # -*- mode: ruby -*-
  # vi: set ft=ruby :

  # All Vagrant configuration is done below. The "2" in Vagrant.configure
  # configures the configuration version (we support older styles for
  # backwards compatibility). Please don't change it unless you know what
  # you're doing.
  Vagrant.configure("2") do |config|
    # The most common configuration options are documented and commented below.
    # For a complete reference, please see the online documentation at
    # https://docs.vagrantup.com.

    # Every Vagrant development environment requires a box. You can search for
    # boxes at https://vagrantcloud.com/search.
    config.vm.box = "ubuntu/focal64"

    # vagrant ouput name on console (during installation)
    config.vm.define "cosim_ubuntu_vm"

    # Disable automatic box update checking. If you disable this, then
    # boxes will only be checked for updates when the user runs
    # `vagrant box outdated`. This is not recommended.
    # config.vm.box_check_update = false

    # Create a forwarded port mapping which allows access to a specific port
    # within the machine from a port on the host machine. In the example below,
    # accessing "localhost:8080" will access port 80 on the guest machine.
    # NOTE: This will enable public access to the opened port
    # config.vm.network "forwarded_port", guest: 80, host: 8080

    # NEST Server (v3.4) / NEST Module of Insite (v2)
    config.vm.network "forwarded_port", guest: 5000, host: 52425
    # NEST Desktop (v3.2)
    config.vm.network "forwarded_port", guest: 54286, host: 54286
    # Access Node of Insite (v2)
    config.vm.network "forwarded_port", guest: 8080, host: 52056
    # CoSim Server (v0.1)
    config.vm.network "forwarded_port", guest: 52428, host: 52428

    # Create a forwarded port mapping which allows access to a specific port
    # within the machine from a port on the host machine and only allow access
    # via 127.0.0.1 to disable public access
    # config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"

    # Create a private network, which allows host-only access to the machine
    # using a specific IP.
    # config.vm.network "private_network", ip: "192.168.33.10"

    # Create a public network, which generally matched to bridged network.
    # Bridged networks make the machine appear as another physical device on
    # your network.
    # config.vm.network "public_network"

    # Share an additional folder to the guest VM. The first argument is
    # the path on the host to the actual folder. The second argument is
    # the path on the guest to mount the folder. And the optional third
    # argument is a set of non-required options.
    config.vm.synced_folder "./shared", "/home/vagrant/shared_data"

    # Provider-specific configuration so you can fine-tune various
    # backing providers for Vagrant. These expose provider-specific options.
    # Example for VirtualBox:
    #
    config.vm.provider "virtualbox" do |vb|
      # Display the VirtualBox GUI when booting the machine
      vb.gui = false
      # name of the VirtualBox GUI
      vb.name = "cosim_ubuntu_gui"

      # Customize the amount of memory on the VM:
      vb.memory = "8192"

      #number of cpus
      vb.cpus = "8"
    end
    #
    # View the documentation for the provider you are using for more
    # information on available options.

    # Enable provisioning with a shell script. Additional provisioners such as
    # Ansible, Chef, Docker, Puppet and Salt are also available. Please see the
    # documentation for more information about their specific syntax and use.
    # config.vm.provision "shell", inline: <<-SHELL
    #   apt-get update
    #   apt-get install -y apache2
    # SHELL
    config.vm.provision "shell", path: "bootstrap.sh"
   end
  ```
 </details>
 <details>
  <summary>Bootstrap</summary>
  
  ``` sh
# ------------------------------------------------------------------------------
#  Copyright 2020 Forschungszentrum Jülich GmbH and Aix-Marseille Université
# "Licensed to the Apache Software Foundation (ASF) under one or more contributor
#  license agreements; and to You under the Apache License, Version 2.0. "
#
# Forschungszentrum Jülich
#  Institute: Institute for Advanced Simulation (IAS)
#    Section: Jülich Supercomputing Centre (JSC)
#   Division: High Performance Computing in Neuroscience
# Laboratory: Simulation Laboratory Neuroscience
#       Team: Multi-scale Simulation and Design
#
# ------------------------------------------------------------------------------
#
# This research was supported by the EBRAINS research infrastructure, 
# funded from the European Union’s Horizon 2020 Framework Programme for Research and Innovation
# under the Specific Grant Agreement No. 785907 (Human Brain Project SGA2) 
# and No. 945539 (Human Brain Project SGA3).
#

############################
### PACKAGE INSTALLATION ###
############################
# TODO: check versions -- specify versions
apt-get update
apt upgrade
apt-get install build-essential
# -> gcc-9,g++-9: 9.3.0-17ubuntu1~20.04
# -> make: 4.2.1-1.2
apt-get install -y doxygen # 1.8.17-0ubuntu2
apt-get install -y git
apt-get install -y emacs
# NOTE: python 3.8.10-0ubuntu1~20.04.2 is preinstalled
apt-get install -y python3-pip
apt-get install -y python3-all-dev
apt-get install -y python3.8-venv
apt-get install -y cmake # 3.16.3-1ubuntu1
# NOTE: ltdl, readline, boost, gsl (for nest)
apt-get install -y libltdl-dev
apt-get install -y libreadline-dev
apt-get install -y libboost-all-dev
apt-get install -y libgsl-dev

apt-get install -y mpich # 3.3.2-2build1

# TODO: temporary solution:
# both openmpi and mpich were installed and openmpi had higher priority.
# one way to change the default of mpicc and mpirun/mpiexec is to change the alternative:
echo "1" | update-alternatives --config mpi # --> choose mpich
echo "1" | update-alternatives --config mpirun # --> choose mpich

#######################
### PYTHON PACKAGES ###
#######################
pip3 install numba
pip3 install requests
pip3 install wheel
pip3 install cython
#pip3 install numpy # numpy-1.21.x as numba dependecy
pip3 install scipy
pip3 install mpi4py # mpi4py-3.1.3
pip3 install pillow
pip3 install nose
pip3 install elephant # +neo, +quantities dependency
pip3 install matplotlib # for PyNEST
# pip3 install IPython # for PyNEST 

# install ZeroMQ
pip3 install pyzmq

#################
### GIT SETUP ###
#################
ssh-keyscan github.com >> /home/vagrant/.ssh/known_hosts
# TODO: discussion about multiscale-cosim-team git account and usage
# email/github: multiscale.cosim@gmail.com
# pw: fdL;3+b\
# TODO: discussion about the tvb submodule (in template and usecase)

# create repository directoriy for later...
mkdir /home/vagrant/multiscale-cosim-repos
cd /home/vagrant/multiscale-cosim-repos

#####################################
### TEMPLATE/USECASE REPOSITORIES ###
#####################################
# Template -- integration test and simplest example:
git clone --recurse-submodules https://github.com/sontheimer/ModularScience-Cosim-Template.git

# Usecase Development -- usecase repositoris created from template
git clone --recurse-submodules https://github.com/sontheimer/TVB-NEST-usecase1.git

#########################
### NEST INSTALLATION ###
#########################
# TODO: find out if we should (of have to) use a python_venv specific for NEST

# Dependencies for NEST Server
pip3 install flask
pip3 install flask-cors
pip3 install RestrictedPython
pip3 install gunicorn

# Dependencies for NEST Server MPI
pip3 install docopt
pip3 install mpi4py

# Install NEST Desktop
pip install nest-desktop

mkdir /home/vagrant/nest-simulator-build/
cd /home/vagrant/nest-simulator-build/

cmake -DCMAKE_INSTALL_PREFIX:PATH=/home/vagrant/nest_installed/ /home/vagrant/multiscale-cosim-repos/TVB-NEST-usecase1/nest-simulator/ \
-Dwith-mpi=ON \
-Dwith-openmp=ON \
-Dwith-readline=ON \
-Dwith-ltdl=ON \
-Dcythonize-pynest=ON \
-DPYTHON_EXECUTABLE=/usr/bin/python3.8 \
-DPYTHON_INCLUDE_DIR=/usr/include/python3.8 \
-DPYTHON_LIBRARY=/usr/lib/x86_64-linux-gnu/libpython3.8.so

# number of processes can be increased, note: memory on the VM should be increased accordingly to avoid crashes
# Environment variable: $(nproc)
make -j 8
make install
# make installcheck 
# default: Error: PyNEST testing requested, but 'pytest' cannot be run.
# default: Testing also requires the 'pytest-xdist' and 'pytest-timeout' extensions.
# set environment variables
#echo 'source /home/vagrant/nest_installed/bin/nest_vars.sh' >> ~/.bashrc 
echo -e "\e[1;34mINFO -- NEST INSTALLATION COMPLETE!"

########################
### TVB INSTALLATION ###
########################
# required python packages already installed
pip3 install tvb-data==2.0 tvb-gdist==2.1.0 tvb-library==2.2 tvb-contrib==2.2
echo -e "\e[1;34mINFO -- TVB INSTALLATION COMPLETE!"

###########################
### COSIM REPOSITORIES  ###
###########################
cd /home/vagrant/multiscale-cosim-repos
# MS-Cosim Development:
# forks of the 'main' EBRAINS-cosim* repositories for development, regular updates and releases expected. 
git clone https://github.com/sontheimer/EBRAINS_Launcher.git
git clone https://github.com/sontheimer/EBRAINS_ConfigManager.git
git clone https://github.com/sontheimer/EBRAINS_InterscaleHUB.git
git clone https://github.com/sontheimer/EBRAINS_RichEndpoint.git
git clone https://github.com/sontheimer/EBRAINS_WorkflowConfigurations.git

#set rights to execute git commands
chmod -R 777 /home/vagrant/multiscale-cosim-repos

#echo 'export CO_SIM_ROOT_PATH=/home/vagrant/multiscale-cosim-repos' >> ~/.bashrc
#echo 'export CO_SIM_MODULES_ROOT_PATH=${CO_SIM_ROOT_PATH}' >> ~/.bashrc
#echo 'export CO_SIM_USE_CASE_ROOT_PATH=${CO_SIM_ROOT_PATH}/TVB-NEST-usecase1' >> ~/.bashrc

###############
### CLEANUP ###
###############
# nest
rm -r /home/vagrant/nest-simulator-build/
# ...

# setup complete message:
echo -e "\e[1;34mINFO -- BASIC SETUP COMPLETE!"
echo -e "\e[1;34mINFO -- Please configure your personal git account to complete the setup of the development environment!"

  ```
</details>

- create directory to synch data between VM and physical OS (e.g. `vagrant/shared`, see line 49 in Vagrantfile)

### 1.4 Start the virtual machine and installation process
- run the following command from the newly created directory
``` sh
vagrant up
```
- the installation process will take several minutes.
- after installation is complete, access the VM by running
``` sh
vagrant ssh
```

---

# TROUBLESHOOTING
* WIP

---

# Q&A
* WIP
