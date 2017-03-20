'''
This script tries to predict the resources required by the container in the container
for the next 30 seconds. It first reads the historic data from docker_resource.log
and then utilizes this data to predict the future. Based on information from the last
minute it predicts wether it is going up or down. If it is going down it will set an
alpha a as 0.7, if its going up it will set an alpha a as -0.2. The prediction is then
set to the docker image using docker update. It is given an extra 10% cpu untop of the
prediction to allow for growth when usage increases. In order to trade off performance
vs resource allocation, the resource allocation can be changed by changing n
'''

from time import sleep
import subprocess
import os
import sys

# Check the command line arguments
if len(sys.argv) < 2:
    sys.exit('Usage: %s [container name]\nexample: %s 287fa53c36f6' % (sys.argv[0], sys.argv[0]))

proc = subprocess.Popen(["docker", "ps"], stdout=subprocess.PIPE)
out = proc.communicate()[0]
raw = str(out).split(" ")

container_exists = False
for entry in raw:
    try:
        var = entry.split("\\n")[-1]
        if sys.argv [1] == var:
            container_exists = True
    except:
        continue


if not container_exists:
    sys.exit('ERROR: Docker container %s was not found.' % sys.argv[1])


pred_cpu = ""

# Fetch the final n lines of a file
def tail(f, n):
    stdout = subprocess.Popen(["tail", "-n " + str(n), f], stdout=subprocess.PIPE)
    out = stdout.communicate()[0]
    return out

# Bootstrap the first prev min as the last observed value et
bootstrap = []

# Fetch the last 120 entries
prev_min = str(tail("/var/log/docker_resource.log", 120)).split("\\n")
for entry in prev_min:
    try:
        bootstrap.append(float(entry.split(" ")[6][:-2]))
    except IndexError:
        continue

# Bootstrap the et
et = (sum(bootstrap) / len(bootstrap)) * 0.7


while True:
    avg_cpu = []
    temp_actual_usage = []

    # Get the usage of the last 15 entries
    actual_usage = str(tail("/var/log/docker_resource.log", 15)).split("\\n")

    # Gather the CPU percentage of the last 15 entries ~0.5 minutes of data
    for entry in actual_usage:
        try:
            temp_actual_usage.append(float(entry.split(" ")[6][:-2]))
        except IndexError:
            continue
    prev_min = sum(temp_actual_usage) / len(temp_actual_usage)

    # Grab the last 120 entries ~4 minutes to calculate ot
    ot_vars = str(tail("/var/log/docker_resource.log", 120)).split("\\n")
    for entry in ot_vars:
        try:
            avg_cpu.append(float(entry.split(" ")[6][:-2]))
        except IndexError:
            continue

    # Calculate OT and write the last prediction + the actual usage to plotter.txt
    ot = sum(avg_cpu) / len(avg_cpu)
    os.system("echo '" + str(pred_cpu) + " " + str(prev_min) + "' >> plotter.txt")

    # Detect a upward trend
    if prev_min > ot:
        a = -0.2
        pred_cpu = ot + abs(a) * (ot - et)
        et = pred_cpu

    # Detect a downward trend
    else:
        a = 0.7
        pred_cpu = a * et + (1 - a) * ot
        et = pred_cpu

    # Set resource limitations (CPU) add 10% for room to grow. Chech that we atleast allocate a percent
    cpu_share = int(float(pred_cpu) * 1000) + 10000
    if cpu_share < 1000:
        cpu_share = 1000

    # Do the allocation
    os.system("docker update d48784302a38 --cpu-quota=" + str(cpu_share) + " --cpuset-cpus='0'")
    # Wait 30 seconds, then do the next prediction
    sleep(30)

