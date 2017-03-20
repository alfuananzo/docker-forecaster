# docker-forecaster
A docker container resource predictor written in python

This program can be used for monitoring and predicting a docker resource usage. it can then be used to limit the docker container to a certain limit of its resources. We recommend you read the paper here <link to paper> where you can find out more about the research done by this. The research is done by students of the Security and Network engineering degree at the University of Amsterdam < link os3 >.

Curently is only monitors CPU, but we plan to upgrade this to memmory, Disk I/O and Network usage.

## How to use this

First, run docker_logger.py for a couple of minutes (10 atleast) to allow it to gather data. Then run nostradamus.py to create the predictions. We strongly recommend you run these things in the background. If you want to show a plot of how your predictions are going you can use the docker_plotter.py. You do need the matplotlib python package to make this work.

### Summary

1. Run docker_logger.py (10 minutes)
2. run nostradamus.py
3. After letting nostradamus.py run for a certain time (n days, hours etc) plot your results and see how the resource prediction is going
