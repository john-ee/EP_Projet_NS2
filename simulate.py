#!/usr/bin/python

import time
import os

timer = open("info.txt", "w")
start = time.time()
os.system("ns simulation.tcl")
timer.write("Temps d'execution de la simulation : %s\n" %(time.time() - start))
timer.close()