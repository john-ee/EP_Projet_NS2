#!/usr/bin/python

import time
import os

timer = open("../traces/info.txt", "w")
start = time.time()
os.system("ns ../traces/simulation.tcl")
timer.write("Temps d'execution de la simulation : %s\n" %(time.time() - start))
timer.close()