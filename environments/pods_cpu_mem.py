#!/usr/bin/python
# Script name: usage_info.py

import re
from kubernetes import client, config

class K8Sstate():

    def get_state(self):

        config.load_kube_config()

        api = client.CustomObjectsApi()
        resource = api.list_namespaced_custom_object(group="metrics.k8s.io",version="v1beta1", namespace="php-apache", plural="pods")

        MAX_PODS = 11

        count = 0
        cpu = []
        mem = []

        for pod in resource["items"]:
            if pod['metadata']['name'].startswith('php-apache'):
                count += 1
                cpu.append(float(re.sub("[^0-9]", "", pod['containers'][0]['usage']['cpu'])))
                mem.append(float(re.sub("[^0-9]", "", pod['containers'][0]['usage']['memory'])))

        cpu += [0] * (MAX_PODS - len(cpu))
        mem += [0] * (MAX_PODS - len(mem))

        state = [count] + cpu + mem
        print(state)
        return state