'''
This file logs the cpu / mem / etc usage of docker to /var/log/docker_resource.log
This is lates used by nostradamus.py to predict the CPU usage of the docker
container. Correct usage is:
docker_logger.py [container ID]
This should prob use the python logging library, but we'll do that some time later.
'''

import datetime
import subprocess
import sys

# Check the command line arguments
if len(sys.argv) < 2:
    sys.exit('Usage: %s [container name]\nexample: %s 287fa53c36f6' % (sys.argv[0], sys.argv[0]))

# Assert that the docker container exists
proc = subprocess.Popen(["docker", "ps"], stdout=subprocess.PIPE)
out = proc.communicate()[0]
raw = str(out).split(" ")

container_exists = False
for entry in raw:
    try:
        var = entry.split("\\n")[-1]
        if sys.argv[1] == var:
            container_exists = True
    except:
        continue


if not container_exists:
    sys.exit('ERROR: Docker container %s was not found.' % sys.argv[1])

while True:
    proc = subprocess.Popen(["docker", "stats", "--no-stream", sys.argv[1]], stdout=subprocess.PIPE)
    out = proc.communicate()[0]
    raw = str(out).split(" ")

    trimmed_raw = []
    for item in raw:
        if item != "":
            trimmed_raw.append(item)

    time = str(datetime.datetime.now()).split(".")[:-1]
    with open("/var/log/docker_resource.log", "a") as f:
       f.write(str(time[0]) + ":    " + "CPU: " + trimmed_raw[14] + ", MEM: "
               + trimmed_raw[15] + ", MEM%: " + trimmed_raw[20] + "\n")

