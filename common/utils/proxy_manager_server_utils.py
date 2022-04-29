# ------------------------------------------------------------------------------
#  Copyright 2020 Forschungszentrum Jülich GmbH and Aix-Marseille Université
# "Licensed to the Apache Software Foundation (ASF) under one or more contributor
#  license agreements; and to You under the Apache License, Version 2.0. "
# ------------------------------------------------------------------------------

from multiprocessing.managers import BaseManager
from EBRAINS_RichEndpoint.Application_Companion.common_enums import Response


# NOTE: later change these hardcoded values to be set during runtime
IP = '127.0.0.1'
PORT = 50000
KEY = b'secret'

def connect(ip, port, key):
    class Manager(BaseManager): pass
    Manager.register('ServiceRegistryManager')
    proxy_manager_client = Manager(address=(ip, port), authkey=key)
    try:
        proxy_manager_client.connect()
    except ConnectionRefusedError as e:
        # Case a: connection is refused. print the exception and
        # return Error response to terminate
        print(e)
        return Response.ERROR
    
    # Case b: connection is established. Get proxy to registry manager
    return proxy_manager_client

def get_registry_proxy(proxy_manager_client, log_settings, configurations_manager):
    return proxy_manager_client.ServiceRegistryManager(log_settings, configurations_manager)

def terminate_with_error(exception):
    print(f"EXCEPTION: {exception}\n\n")
    # raise RuntimeError exception to terminate
    raise RuntimeError