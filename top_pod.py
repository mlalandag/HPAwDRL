import subprocess

# subprocess.check_output(['kubectl', 'top', 'pod', '-n', 'php-apache', '--sort-by=cpu'])

result = subprocess.run(['kubectl', 'top', 'pod', '-n', 'php-apache', '--sort-by=cpu'], stdout=subprocess.PIPE)
print(result.stdout.decode('utf-8'))