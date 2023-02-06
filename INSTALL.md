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
* 123

---

# TROUBLESHOOTING
* WIP

---

# Q&A
* WIP
