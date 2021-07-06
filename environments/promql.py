import requests
import time
import sys
import numpy as np

MAX_PODS = 11

# Prometheus api endpoint for query 
URL = "http://localhost:57261/api/v1/query"

# Number of Pods
PROMQL1 = {'query':'count(kube_pod_info{namespace="php-apache", pod!~".*load.*"}) by (namespace)'}

# CPU Query
PROMQL2 = {'query':'sum (rate (container_cpu_usage_seconds_total{namespace="php-apache", name!~".*prometheus.*", image!="", container!="POD", id!~".*/docker/.*"}[2m])) by (pod)'}

print("row,pods,pod,cpu")

line_no = 1

#Query every 15 seconds 100 times
for seq in range(0 , 100):
    rows = []
    row = 0
    m1 = []    
    m2 = []        

    r1 = requests.get(url = URL, params = PROMQL1)
    r2 = requests.get(url = URL, params = PROMQL2)    

    r1_json = r1.json()['data']['result']
    r2_json = r2.json()['data']['result']    

    m1 = []
    for result in r1_json:
        # l.append(result['metric'].get('instance', ''))
        m1.append(result['value'][1])
        # rows.append(l)

    m2 = []
    for result in r2_json:
        # l.append(result['metric'].get('instance', ''))
        m2.append(result['value'][1])
        # rows.append(l)     
 

    # for ro in rows:
    #     line = str(line_no)
    #     line = line + "," + ro[0] + "," + ro[1]
    #     print(str(line))
    #     line_no = line_no + 1

    state = (m1 + m2)
    state += [0] * (MAX_PODS - len(state))
    print(state)

    sys.stdout.flush()
    time.sleep(15)