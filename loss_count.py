#!/usr/bin/python

import numpy as np

src = open("loss.tr","r")

pertes = []
total = []
for i in range(25):
	pertes.append([i] * 25)
	total.append([i] * 25)

for line in src:
	event = line.rstrip('\n\r').split(" ")

	pertes[int(event[1])][int(event[2])]+= int(event[3])
	total[int(event[1])][int(event[2])]+= int(event[4])

dst  = open("info.txt", "a")

dst.write("Pourcentage de pertes par liens dans les deux sens :\n")
for i in [0,25]:
	for j in [i,25]:
		if total[i][j] + total[j][i] != 0:
			pourcent = (pertes[i][j]+pertes[j][i]) / (total[i][j]+total[j][i])
			dst.write("\tLien %s-%s : %s\n" %(i,j,pourcent))
src.close()
dst.close()
