''''
plot the data from plotter.txt
'''

import matplotlib.pyplot as plt
import sys
from os import path

# Check the command line arguments
if len(sys.argv) < 2:
    sys.exit('Usage: %s [plotter.txt location]\nexample: %s ~/plotter.txt' % (sys.argv[0], sys.argv[0]))

if not path.exists(sys.argv[1]):
    sys.exit('ERROR: plotter.txt file %s was not found.' % sys.argv[1])

pred_cpu_list = []
actual_cpu_list = []
x_axis = []
y = 0

# Open the file and read out all the info
with open(sys.argv[1]) as f:
    try:
        for line in f:
            pred_cpu, actual_cpu = line.split(" ")
            pred_cpu_list.append(pred_cpu)
            actual_cpu_list.append(actual_cpu)
            x_axis.append(y)
            y+=1
    except:
        sys.exit('ERROR: plotter.txt format not correct')



# plot the data
plt.plot(x_axis, actual_cpu_list, x_axis, pred_cpu_list, "r--")
plt.show()
