<div align="center" id="top"> 
  <img src="../../../misc/logo.jpg" alt="Modular Science: Multi-scale Co-simulation" />

  &#xa0;

  <!-- <a href="git@github.com:multiscale-cosim/TVB-NEST-usecase1.git">Demo</a> -->
</div>

<h1 align="center">Modular Science: Multi-scale Co-simulation</h1>

<p align="center">
  <img alt="Github top language" src="https://img.shields.io/github/languages/top/multiscale-cosim/TVB-NEST-usecase1?color=56BEB8" />

  <img alt="Github language count" src="https://img.shields.io/github/languages/count/multiscale-cosim/TVB-NEST-usecase1?color=56BEB8" />

  <img alt="Repository size" src="https://img.shields.io/github/repo-size/multiscale-cosim/TVB-NEST-usecase1?color=56BEB8" />

  <img alt="License" src="https://img.shields.io/github/license/multiscale-cosim/TVB-NEST-usecase1?color=56BEB8" />

  <img alt="Github issues" src="https://img.shields.io/github/issues/multiscale-cosim/TVB-NEST-usecase1?color=56BEB8" />

  <img alt="Github forks" src="https://img.shields.io/github/forks/multiscale-cosim/TVB-NEST-usecase1?color=56BEB8" />

  <img alt="Github stars" src="https://img.shields.io/github/stars/multiscale-cosim/TVB-NEST-usecase1?color=56BEB8" />
</p>

## Status

<h4 align="center"> 
	🚧  Multi-scale Co-simulation - TVB-NEST-usecase1 🚧
</h4> 

<hr>

<p align="center">
  <a href="#dart-about">About</a> &#xa0; | &#xa0; 
  <a href="#sparkles-features">Features</a> &#xa0; | &#xa0;
  <a href="#rocket-technologies">Technologies</a> &#xa0; | &#xa0;
  <a href="#white_check_mark-Dependencies">Dependencies</a> &#xa0; | &#xa0;
  <a href="#checkered_flag-starting">Getting Started</a> &#xa0; | &#xa0;
  <a href="#memo-license">License</a> &#xa0; | &#xa0;
  <a href="https://github.com/multiscale-cosim" target="_blank">Author</a> &#xa0; | &#xa0;
  <a href="https://github.com/multiscale-cosim" target="_blank">Acknowledgement</a>
</p>

<br>

## :dart: About ##

The modular Science Framework is to facilitate the domain scinetists to deploy, integrate, orchestrate and intuitive &
interactive control of larger complex workflows (comprises a number of independant application kernels running in parallel) executing on heterogeneous HPC platforms. The framework comprises a set of following micro-services like independent applications:

* <a href="/python/Application_Companion"> Rich Endpoint </a>
* <a href="/python/Orchestrator"> InterscaleHub </a>
* <a href="/python/Orchestrator/command_steering_service.py"> Configurations Manager </a>
* <a href="/python/Orchestrator/command_steering_service.py"> Launcher </a>

## :sparkles: Features ##

fill the section here

## :rocket: Technologies ##

The following tools were used in this project:

- [Python](https://www.python.org/)
- [CMake](https://cmake.org/)
- [C++](https://isocpp.org/)
- [Makefile](https://www.gnu.org/software/make/manual/make.html)

## :white_check_mark: Dependencies ##

Before starting :checkered_flag:, you need to have [Python](https://www.python.org/) and [CMake](https://cmake.org/) installed.

## :checkered_flag: Getting Started ##

-- --
INSTALLATION: Check [INSTALL.md](https://github.com/multiscale-cosim/TVB-NEST-usecase1/blob/main/INSTALL.md)
-- --
### Run usecase on JUSUF

| folder | files | description |
| ------ | ------ | ------ |
| *installation/* | *bootstrap_hpc.sh* | execute to load modules and install dependencies |
| *run_usecase/* | *launch_singlenode_alphabrunel.sh* | runs the cosimulation alphabrunel network on a single compute node |

Important:
 1) Install in your personal prject directory, e.g. /p/project/cslns/sontheimer1
 2) Allocate interactive compute node, e.g. `salloc --account slns --partition develgpus --nodes=1`
 3) Run usecase script from the TVB-NEST-usecase1 directory, where main.py is located
 
 -- --

## :memo: License ##

This project is under license from Apache License, Version 2.0. For more details, see the [LICENSE](LICENSE) file.


Made by <a href="https://github.com/multiscale-cosim" target="_blank">Multiscale Co-simulation team</a>.

## :memo: Acknowledgement ##


&#xa0;

<a href="#top">Back to top</a>