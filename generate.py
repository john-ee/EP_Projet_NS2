#!/usr/bin/python

from scipy.stats import zipf
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
		dst.write("set monitor_queue(%s,%s) [$ns monitor-queue $n(%s) $n(%s) queue(%s,%s) 1]\n" %(topo[0], topo[1], topo[0], topo[1], topo[0], topo[1]))
		dst.write("$ns at 0 \"record %s %s\"\n" %(topo[0], topo[1]))
		dst.write("\n")


def multiple10(x):
	mult = 10
	cond = True
	if x < mult:
		return 1
	while cond:
		if x > mult and x < mult*10:
			cond = False
		else:
			mult = mult * 10
	return mult/10


def trafic( src, dst, sim_time, burst, idle, shape, nb_flux):

	debut = math.floor(sim_time * 0.10)
	fin = sim_time - debut

	dst.write("Agent/TCP set packetSize_ 1500\n")
	dst.write("Agent/TCP set windowSize_ 536\n")
	dst.write("Agent/UDP set packetSize_ 1500\n")

	for line in src:
		
		traf = line.rstrip('\n\r').split(" ")
		data = int(traf[2])

		pareto_traf = int(math.floor(0.85 * data)) 
		ftp_traf = int( data - pareto_traf)

		nb_cycle = (burst + idle) / sim_time
		rate = ( pareto_traf * 2 ) / sim_time
		#rate = int ( ( pareto_traf / nb_cycle ) / burst ) 

		if rate == 0:
			print "\nValeur nulle %s avec pareto*2 : %s sim_time: %s" %(rate, pareto_traf*2, sim_time)
			rate = 1
			print "New rate %s\n" %(rate)		

		dst.write("set sink_udp(%s,%s) [new Agent/UDP]\n" %(traf[0], traf[1]))
		dst.write("$ns attach-agent $n(%s) $sink_udp(%s,%s)\n" %(traf[1], traf[0], traf[1]))
		dst.write("set udp(%s,%s) [new Agent/UDP]\n" %(traf[0], traf[1]))
		dst.write("$ns attach-agent $n(%s) $udp(%s,%s)\n" %(traf[0], traf[0], traf[1]))
		dst.write("$ns connect $udp(%s,%s) $sink_udp(%s,%s)\n" %(traf[0], traf[1], traf[0], traf[1]))

		dst.write("set p(%s,%s) [new Application/Traffic/Pareto]\n" %(traf[0], traf[1]))
		dst.write("$p(%s,%s) set packetSize_ 1500\n" %(traf[0], traf[1]))
		dst.write("$p(%s,%s) set burst_time_ %s\n" %(traf[0], traf[1], burst))
		dst.write("$p(%s,%s) set idle_time_ %s\n" %(traf[0], traf[1], idle))
		dst.write("$p(%s,%s) set shape_ %s\n" %(traf[0], traf[1], shape))
		dst.write("$p(%s,%s) set rate_ %sG\n" %(traf[0], traf[1], rate))
		dst.write("$p(%s,%s) attach-agent $udp(%s,%s)\n" %(traf[0], traf[1], traf[0], traf[1]))
		dst.write("$ns at %s \"$p(%s,%s) start\"\n" %(debut, traf[0], traf[1]))
		dst.write("$ns at %s \"$p(%s,%s) stop\"\n\n" %(fin, traf[0], traf[1]))

		random_traf = 0
		i = 0

		print "%s %s" %(pareto_traf, ftp_traf)
		offset = multiple10(ftp_traf)

		while random_traf < ftp_traf:

			sent = zipf.rvs(shape) * offset
			instant = int(rand.uniform(debut,fin))
			if sent == 0:
				print "\nValeur null%s\n\n" %(sent)

			if sent < ftp_traf:
				if i > nb_flux-1:
					dst.write("$ns at %s \"$tcp(%s,%s,%s) send %sG\"\n\n" %(instant, traf[0], traf[1], i%nb_flux, sent))

				else:
					dst.write("set tcp(%s,%s,%s) [new Agent/TCP]\n" %(traf[0], traf[1], i))
					dst.write("$ns attach-agent $n(%s) $tcp(%s,%s,%s)\n" %(traf[0], traf[0], traf[1], i))

					dst.write("set sink(%s,%s,%s) [new Agent/TCPSink]\n" %(traf[0], traf[1], i))
					dst.write("$ns attach-agent $n(%s) $sink(%s,%s,%s)\n" %(traf[1], traf[0], traf[1], i))
					dst.write("$ns connect $tcp(%s,%s,%s) $sink(%s,%s,%s)\n" %(traf[0], traf[1], i, traf[0], traf[1], i))
					dst.write("$ns at %s \"$tcp(%s,%s,%s) send %sG\"\n\n" %(instant, traf[0], traf[1], i, sent))

				random_traf += sent
				i+=1


src_topo = open("topo.top","r")
src_traf = open("traff.traf","r")
dest = open("simulation.tcl","w")

dest.write("set ns [new Simulator]\n")
dest.write("set loss_monitor [open loss.tr w]\n\n")

dest.write("proc finish {} {\n")
dest.write("    global ns loss_monitor\n")
dest.write("    $ns flush-trace\n")
dest.write("    close $loss_monitor\n")
dest.write("    exit 0\n")
dest.write("}\n\n")

dest.write("Node instproc getidnode {} {\n")
dest.write("	$self instvar id_\n    return \"$id_\"\n}\n\n")

dest.write("proc record {i j} {\n")
dest.write("	global ns n monitor_queue loss_monitor\n")
dest.write("	set now [$ns now]\n")
dest.write("	set next 3\n")
dest.write("	set from_node [$n($i) getidnode]\n")
dest.write("	set to_node [$n($j) getidnode]\n")
dest.write("	$monitor_queue($i,$j) instvar size_ pkts_ barrivals_ bdepartures_ parrivals_ pdepartures_ bdrops_ pdrops_\n")
dest.write("	puts $loss_monitor \"$now $from_node $to_node $pdrops_ $pdepartures_\"\n")
dest.write("	$ns after $next \"record $i $j\"\n")
dest.write("}\n\n")

topologie(src_topo, dest)

trafic(src_traf, dest, 300, 0.05, 0.05, 1.2, 41)

dest.write("$ns at 300 \"finish\"\n")
dest.write("puts \"Starting Simulation...\"\n$ns run\n")

src_topo.close()
src_traf.close()
dest.close()