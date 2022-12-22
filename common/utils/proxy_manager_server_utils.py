# -----------------------------------------------------------------------------
#  Copyright 2020 Forschungszentrum Jülich GmbH
# "Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements; and to You under the Apache License,
# Version 2.0. "
#
# Forschungszentrum Jülich
#  Institute: Institute for Advanced Simulation (IAS)
#    Section: Jülich Supercomputing Centre (JSC)
#   Division: High Performance Computing in Neuroscience
# Laboratory: Simulation Laboratory Neuroscience
#       Team: Multi-scale Simulation and Design
# -----------------------------------------------------------------------------
from common.utils import networking_utils


# NOTE: later change these hardcoded values to be set during runtime
# IP = '127.0.0.1'
#IP = '10.0.2.15'
IP = networking_utils.my_ip()
PORT = 59010
KEY = b'secret'
