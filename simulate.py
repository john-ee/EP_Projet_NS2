import time
import os

timer = open("time.txt", "r")
start = time.time()
os.system("ns simulation.tcl")
timer.write("Temps d'execution de la simulation : %s" %(time.time() - start))
timer.close()