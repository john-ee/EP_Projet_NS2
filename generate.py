#!/usr/bin/python

import scipy.special as sps
import numpy as np
import random as rand 

def topologie(src,dst):
	nodes = []
	for line in src:
		topo = line.rstrip('\n\r').split(" ")
		if topo[0] not in nodes:
			nodes.append(topo[0])
			dst.write("set n%s [$ns node]\n" %(topo[0]))
		if topo[1] not in nodes:
			nodes.append(topo[1])
			dst.write("set n%s [$ns node]\n" %(topo[1]))

		dst.write("$ns duplex-link $n%s $n%s %sMb %sms DropTail\n" %(topo[0], topo[1],topo[2],topo[3]))
		dst.write("$ns queue-limit $n%s $n%s 10\n" %(topo[0],topo[1]))
		dst.write("\n")


def trafic( src, dst, sim_time, burst, idle, shape):
	nb_cycles = sim_time / (burst + idle)
	for line in src:
		traf = line.rstrip('\n\r').split(" ")
		dst.write("set sink_%s_%s [new Agent/TCPSink]\n" %(traf[0], traf[1]))
		dst.write("$ns attach-agent $n%s $sink_%s_%s\n" %(traf[1], traf[0], traf[1]))
		dst.write("set tcp_%s_%s [new Agent/TCP]\n" %(traf[0], traf[1]))
		dst.write("$ns attach-agent $n%s $tcp_%s_%s\n" %(traf[0], traf[0], traf[1]))
		dst.write("$ns connect $tcp_%s_%s $sink_%s_%s\n" %(traf[0], traf[1], traf[0], traf[1]))

		dst.write("set p_%s_%s [new Application/Traffic/Pareto]\n" %(traf[0], traf[1]))
		rate = float(traf[2]) * 1024*1024*8 / (1500 * nb_cycles)
		dst.write("$p_%s_%s set burst_time_ %s\n" %(traf[0], traf[1], burst))
		dst.write("$p_%s_%s set idle_time_ %s\n" %(traf[0], traf[1], idle))
		dst.write("$p_%s_%s set rate_ %s\n" %(traf[0], traf[1], rate))
		dst.write("$p_%s_%s set packetSize_ 1500\n" %(traf[0], traf[1]))
		dst.write("$p_%s_%s set shape_ %s\n" %(traf[0], traf[1], shape))
		dst.write("$p_%s_%s attach-agent $tcp_%s_%s\n" %(traf[0], traf[1], traf[0], traf[1]))
		dst.write("$ns at 0.0 \"$p_%s_%s start\"\n\n" %(traf[0], traf[1]))

	dst.write("$ns at %s \"finish\"\n" %(sim_time))
	dst.write("puts \"Starting Simulation...\"\n$ns run\n")


src_topo = open("topo.top","r")
src_traf = open("traff.traf","r")
dest  = open("simulation.tcl","w")

dest.write("set ns [new Simulator]\n")
dest.write("set f [open out.tr w]\n$ns trace-all $f\n")
dest.write("proc finish {} {\n")
dest.write("    global ns f\n")
dest.write("    $ns flush-trace\n")
dest.write("    close $f\n")
dest.write("    exit 0\n")
dest.write("}\n\n")

topologie(src_topo, dest)

trafic(src_traf, dest, 300, 0.05, 0.05, 1.5)

src_topo.close()
src_traf.close()
dest.close()