import sys
import os

print('Number of Replicas: {}'.format(str(sys.argv)))
# os.system('kubectl scale deployment php-apache --replicas=3')
command = "kubectl scale deployment php-apache --replicas=" + str(sys.argv[1]) + " -n php-apache"
print(command)
os.system(command)