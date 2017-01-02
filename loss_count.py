#!/usr/bin/python

src = open("loss.tr","r")

pertes = []
total = []
for i in range(26):
	pertes.append([i] * 26)
	total.append([i] * 26)
	for j in range (0,26):
		total[i][j] = 0


for line in src:
	event = line.rstrip('\n\r').split(" ")

	pertes[int(event[0])][int(event[1])] = int(event[2])
	total[int(event[0])][int(event[1])] = int(event[3])

dst  = open("loss_results.txt", "w")

dst.write("Pourcentage de pertes par liens dans les deux sens :\n")
for i in range(26):
	for j in range(i+1,26):
		if ( total[i][j] + total[j][i] != 0 ) :
			pourcent = (pertes[i][j]+pertes[j][i]) / (total[i][j]+total[j][i])
			dst.write("\tLien %s-%s : %s\n" %(i,j,pourcent))
src.close()
dst.close()
