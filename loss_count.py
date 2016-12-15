#!/usr/bin/python

import numpy as np

src = open("../traces/out.tr","r")

pertes = []
nb_pertes = 0
for i in range(25):
	pertes.append([i] * 25)

for line in src:
	event = line.rstrip('\n\r').split(" ")

	if event[0] == 'd':
		pertes[int(event[2])][int(event[3])]+=1
		nb_pertes++

imax = 0
jmax = 0
valmax = 0

for i in range(25):
	for j in range(25):
		if pertes[i][j] > valmax:
			valmax = pertes[i][j]
			imax = i
			jmax = j

dst  = open("info.txt", "w")

dst.write("Pertes totales %s\n" %(nb_pertes))
dst.write("Le lien le plus faible est %s %s avec %s pertes\n" %(imax,jmax,valmax))

src.close()
dst.close()