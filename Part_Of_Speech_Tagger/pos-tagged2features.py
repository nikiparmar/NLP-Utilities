#! /usr/bin/env python
import sys

training = []
count = 0
previous1 = ""
previous2 = ""
current = ""
current_pos = ""
prev_pos1 = ""
prev_pos2 = ""
pos = ""
file_reader = open(sys.argv[1],'r')
for  line in file_reader:
	previous1 = ""
	previous2 = ""
	current = ""
	current_pos = ""
	prev_pos1 = ""
	prev_pos2 = ""
	pos = ""
	feature = ""
	for word in line.replace('\n',' ').split(" "):	
		count =0
		for label in word.split("/"):
			if count ==0:
				feature = label
					
			else:
				pos = label
			count +=1
		if current_pos != "":
			print(current_pos + " " + "prevtag1:" + prev_pos1 + " " + "prevword1:" + previous1 +  " " + "prevpref1:" + previous1[:2] + " " + "prevsuff1:" + previous1[-2:] + " " +  "prevtag2:" + prev_pos2 + " " + "prevword2:" + previous2 +  " " + "prevpref2:" + previous2[:2] + " " + "prevsuff2:" + previous2[-2:] + " "+  "currword:" + current + " " + "currpref:" + current[:2] + " " + "currsuff:" + current[-2:] + " " +  "nextword:"+ feature + " " + "nextpref:" + feature[:2] + " " + "nextsuff:" + feature[-2:])
		previous1 = previous2
		previous2 = current
		current = feature
		prev_pos1 = prev_pos2
		prev_pos2 = current_pos
		current_pos = pos
file_reader.close()
