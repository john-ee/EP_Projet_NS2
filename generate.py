#!/usr/bin/python

import scipy.special as sps
import numpy as np
import math
import random as rand

def topologie(src,dst):

	nodes = []

	for line in src:
		topo = line.rstrip('\n\r').split(" ")

		if topo[0] not in nodes:
			nodes.append(topo[0])
			dst.write("set n(%s) [$ns node]\n" %(topo[0]))

		if topo[1] not in nodes:
			nodes.append(topo[1])
			dst.write("set n(%s) [$ns node]\n" %(topo[1]))

		dst.write("$ns duplex-link $n(%s) $n(%s) %sGb %sms DropTail\n" %(topo[0], topo[1], topo[2], topo[3]))
		dst.write("$ns queue-limit $n(%s) $n(%s) 10\n" %(topo[0],topo[1]))
		dst.write("\n")


def trafic( src, dst, sim_time, burst, idle, shape):

	debut = math.floor(sim_time * 0.10)
	fin = sim_time - debut

	dst.write("Agent/TCP packetSize_ set 1500\n")
	dst.write("Agent/UDP packetSize_ set 1500\n")
	dst.write("Agent/Traffic/Pareto set packetSize_ 1500\n")
	dst.write("Agent/Traffic/Pareto set burst_time_ %s\n" %(burst))
	dst.write("Agent/Traffic/Pareto set idle_time_ %s\n" %(idle))
	dst.write("Agent/Traffic/Pareto set shape_ %s\n" %(shape))
	dst.write("Application/FTP set type_ FTP\n\n")

	for line in src:
		
		traf = line.rstrip('\n\r').split(" ")
		data = int(traf[2])

		pareto_traf = int(math.floor(0.85 * data)) 
		ftp_traf = int( data - pareto_traf)

		nb_cycle = (burst + idle) / sim_time
		rate = int( math.floor( ( pareto_traf / nb_cycle ) / burst ) )

		dst.write("set sink_udp(%s,%s) [new Agent/UDP]\n" %(traf[0], traf[1]))
		dst.write("$ns attach-agent $n(%s) $sink_udp(%s,%s)\n" %(traf[1], traf[0], traf[1]))
		dst.write("set udp(%s,%s) [new Agent/UDP]\n" %(traf[0], traf[1]))
		dst.write("$ns attach-agent $n($%s) $udp(%s,%s)\n" %(traf[0], traf[0], traf[1]))
		dst.write("$ns connect $udp($%s,$%s) $sink_udp(%s,%s)\n" %(traf[0], traf[1], traf[0], traf[1]))

		dst.write("set p(%s,%s) [new Application/Traffic/Pareto]\n" %(traf[0], traf[1]))
		dst.write("$p(%s,%s) set rate_ %s G\n" %(traf[0], traf[1], rate))
		dst.write("$p(%s,%s) attach-agent $udp(%s,%s)\n" %(traf[0], traf[1], traf[0], traf[1]))
		dst.write("$ns at %s \"$p(%s,%s) start\"\n\n" %(debut, traf[0], traf[1]))
		dst.write("$ns at %s \"$p(%s,%s) stop\"\n\n" %(fin, traf[0], traf[1]))

		dst.write("set tcp(%s,%s) [new Agent/TCP]\n" %(traf[0], traf[1]))
		dst.write("$ns attach-agent $n%s $tcp(%s,%s)\n" %(traf[0], traf[0], traf[1]))

		dst.write("set sink(%s,%s) [new Agent/TCPSink]\n" %(traf[0], traf[1]))
		dst.write("$ns attach-agent $n%s $sink(%s,%s)\n" %(traf[1], traf[0], traf[1]))
		dst.write("$ns connect $tcp(%s,%s) $sink(%s,%s)\n" %(traf[0], traf[1], traf[0], traf[1]))

		dst.write("set ftp(%s,%s) [$tcp(%s,%s) attach_app FTP]\n" %(traf[0], traf[1], traf[0], traf[1]))

		random_traf = 0
		i = 0
		offset = int(math.floor(ftp_traf / 1000))

		print "%s %s %s" %(pareto_traf, ftp_traf, offset)

		while random_traf < ftp_traf:

			zipf = np.random.zipf(shape) 
			instant = rand.random() * (fin - debut) + debut
			dst.write("$ns at %s \"$ftp(%s,%s) send %s G\"\n\n" %(instant, traf[0], traf[1], zipf))
			random_traf += zipf 
			i+=1


src_topo = open("topo.top","r")
src_traf = open("traff.traf","r")
dest = open("simulation.tcl","w")

dest.write("set ns [new Simulator]\n\n")
dest.write("proc finish {} {\n")
dest.write("    exit 0\n")
dest.write("}\n\n")

topologie(src_topo, dest)

trafic(src_traf, dest, 300, 0.05, 0.05, 2)

dest.write("$ns at 300 \"finish\"\n")
dest.write("puts \"Starting Simulation...\"\n$ns run\n")

src_topo.close()
src_traf.close()
dest.close()