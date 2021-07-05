#!/usr/bin/python
# Script name: usage_info.py

from kubernetes import client, config

config.load_kube_config()

api = client.CustomObjectsApi()
k8s_pods = api.list_cluster_custom_object("metrics.k8s.io", "v1beta1", "pods")


for stats in k8s_pods['items']:
    print("Node Name: %s\tCPU: %s\tMemory: %s" % (stats['metadata']['name'], stats['usage']['cpu'], stats['usage']['memory']))