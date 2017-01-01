#!/usr/bin/python

import numpy as np

src = open("loss.tr","r")

pertes = []
total = []
for i in range(25):
	pertes.append([i] * 25)
	recus.append([i] * 25)

for line in src:
	event = line.rstrip('\n\r').split(" ")

	pertes[int(event[1])][int(event[2])]+= int(event[3])
	total[int(event[1])][int(event[2])]+= int(event[4])

imax = [0]*3
jmax = [0]*3
valmax = [0]*3

for i in range(len(pertes)):
	for j in range(len(pertes[i])):
		if pertes[i][j] / total[i][j] > valmax[0]:
			valmax[0] = pertes[i][j] / total[i][j]
			imax[0] = i
			jmax[0] = j
		elif pertes[i][j] / total[i][j] > valmax[1]:
			valmax[1] = pertes[i][j] / total[i][j]
			imax[1] = i
			jmax[1] = j
		elif pertes[i][j] / total[i][j] > valmax[2]:
			valmax[2] = pertes[i][j] / total[i][j]
			imax[2] = i
			jmax[2] = j


dst  = open("info.txt", "a")

dst.write("Les liens les plus faibles sont:\n")
dst.write("\t%s-%s avec %s %% de pertes\n" %(imax[0], jmax[0], valmax[0]))
dst.write("\t%s-%s avec %s %% de pertes\n" %(imax[1], jmax[1], valmax[1]))
dst.write("\t%s-%s avec %s %% de pertes\n" %(imax[2], jmax[2], valmax[2]))

src.close()
dst.close()