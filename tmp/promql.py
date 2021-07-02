import requests
import time
import sys

# Prometheus api endpoint for query 
URL = "http://localhost:51083/api/v1/query"

# CPU Query
PROMQL1 = {'query':'container_cpu_usage_seconds_total'}

print("row,instance,memory,cpu")

line_no = 1

#Query every 15 seconds 100 times
for seq in range(0 , 100):
    rows = []
    row = 0

    r1 = requests.get(url = URL, params = PROMQL1)

    r1_json = r1.json()['data']['result']

    for result in r1_json:
        l = []
        l.append(result['metric'].get('instance', ''))
        l.append(result['value'][1])
        rows.append(l)

    for ro in rows:
        line = str(line_no)
        line = line + "," + ro[0] + "," + ro[1]
        print(str(line))
        line_no = line_no + 1
    sys.stdout.flush()
    time.sleep(15)