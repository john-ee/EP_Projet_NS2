#!/usr/bin/python

import time
import os

timer = open("info.txt", "a")
start = time.time()
os.system("ns simulation.tcl")
timer.write("Temps d'execution de la simulation : %s h\n" %(time.time() - start) / 3600)
timer.close()