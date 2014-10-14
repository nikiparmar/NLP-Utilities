import sys
from decimal import *

train = open(sys.argv[1])
number_iters = int(sys.argv[2])
output = open(sys.argv[3],'w')
channel = open(sys.argv[4], 'w')


record = []
count = 0
align = dict()
length = 0
words  = []
epron = dict()
engl = dict()
prialig = []
records = []
c =0 

for line in train:
	line = line.strip("\r\n")
	#print line
	record.append(line)
	if line == "":
		eword = record[0]
		records.append(eword)
		english = record[0].split(" ")
		for e in english:
			if e not in epron:
				epron[e] = dict()
		align[eword] = dict()
		engl[eword] = english
		if(c < 5):
			prialig.append(eword)
		for r in record[1:-1]:
			align[eword][r] = 1
			count = 0
			for j in r.split(" "):
				if j not in epron[english[count]]:
					epron[english[count]][j] = 0
				epron[english[count]][j] +=1
				count +=1
		c +=1	
		record = []
train.close()

count = dict()

for e in epron:
	count[e] = dict()
	for j in epron[e]:
		count[e][j] =0


i = 0
for i in range(0, number_iters):
	for eword in align:
		n = len(align[eword])
		if i==0:
			for a in align[eword]:
				align[eword][a] = Decimal(1)/Decimal(n)
		else:
			for a in align[eword]:
				ei = engl[eword]
				ai = align[eword][a]
				ji = a.split(" ")
				ai = 1
				c = 0
			
				for jseq in ji:
					ai *= Decimal(epron[ei[c]][jseq])/Decimal(len(epron[ei[c]]))
					c +=1
				align[eword][a] = ai
			total = 0
			for a in align[eword]:
				total += align[eword][a]
			#max_val = 0
			#max_align = ""
			for a in align[eword]:
				align[eword][a] = Decimal(align[eword][a])/Decimal(total)
			#	if eword in prialig:
			#		if align[eword][a] > max_val:
			#			max_val = align[eword][a]
			#			max_align = a
			#if eword in prialig:
			#	print eword + " "
			#	print max_align + " " + str(max_val) +"\n"
		for a in align[eword]:
			ei = engl[eword]
			ji = a.split(" ")
			c = 0
			for jseq in ji:
				count[ei[c]][jseq] += align[eword][a]	
				c +=1
					
	
	for ei in epron:
		total = 0
		for ji in epron[ei]:
			total += count[ei][ji]
		for ji in epron[ei]:
			epron[ei][ji] = Decimal(count[ei][ji])/Decimal(total) 
	for ei in epron:
		for ji in epron[ei]:
			count[ei][ji] =0

	i += 1

#print align

for eword in records:
	max_val = 0
	max_align = ""
	for a in align[eword]:
		if align[eword][a] > max_val:
                	max_val = align[eword][a]
                       	max_align = a
	output.write(eword+"\n")
	string = ""
	seq = ""
	count =1
        for a in max_align.split(" "):
		for ji in a.split(":"):
			seq += str(count) + " "
			string += ji + " "
		count +=1
	output.write(string + "\n" + str(seq) + "\n")
	output.flush()
output.close()

channel.write("0\n")	
state = 1
for ei in epron:
	for ji in epron[ei]:
		if epron[ei][ji] > 0.01:
			j = ji.split(":")
        	        l = len(j)
			
       	         	if len(j) == 1:
	        		channel.write("(0 (0 " + ei + " " + j[0] + " " + str(epron[ei][ji]) + " ))\n")
  	              	else:
                		channel.write("(0 ( "  + str(state) + " " + ei + " " + j[0] + " " + str(epron[ei][ji]) + " ))\n")
                        	for i in range(1,l -1):
                        		channel.write("( " + str(state) + " ( " +  str(state +1) + " *e* " + j[i] + " 1 ))\n")
                                	state += 1
                        	channel.write("( " + str(state ) + " (0 *e* " + j[l-1] + " 1 ))\n")
                       		state +=1
               		channel.flush()
channel.close()
