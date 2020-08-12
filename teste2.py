import os
import subprocess
output = subprocess.check_output("dir", stderr=subprocess.STDOUT, shell=True)

print(output.decode('ISO-8859-1'))
