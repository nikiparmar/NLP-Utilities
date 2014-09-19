#! /usr/bin/env python

import sys

training = []
count = 0
previous1 = ""
previous2 = ""
current = ""
previous_pos = ""
pos = ""
tag = ""
previous_tag1 = ""
previous_tag2 = ""
current_tag = ""
prev_bio1 = ""
prev_bio2 = ""
file_reader = open(sys.argv[1],'r')
for  line in file_reader:
	previous1 = ""
	previous2 = ""
	current = ""
	previous_pos = ""
	pos = ""
	tag = ""
	previous_tag1 = ""
	previous_tag2 = ""
	current_tag = ""
	prev_bio1 = ""
	prev_bio2 = ""

	for word in line.replace('\n',' ').split(" "):	
		count =0
		for label in word.split("/"):
			if count ==0:
				feature = label
			else:	
					
				if count == 2:
					pos = label
				else:
					tag = label				
			count +=1
		if previous_pos != "":
			print(previous_pos + " " + "prevbio1:" + prev_bio1 + " " + "prevtag1:" + previous_tag1 + " " + "prevword1:" + previous1 +  " " + "prevpref1:" + previous1[:3] + " " + "prevsuff1:" + previous1[-3:] + " " + "prevbio2:" + prev_bio2 + " " + "prevtag2:" + previous_tag2 + " " + "prevword2:" + previous2 +  " " + "prevpref2:" + previous2[:3] + " " + "prevsuff2:" + previous2[-3:] + " " + "currtag:" +  current_tag + " " + "currword:" + current + " " + "currpref:" + current[:3] + " " + "currsuff:" + current[-3:] + " " + "nexttag:" + tag+  " " +  "nextword:"+ feature + " " + "nextpref:" + feature[:3] + " " + "nextsuff:" + feature[-3:])
		previous1 = previous2
		previous2 = current
		current = feature
		prev_bio1 = prev_bio2
		prev_bio2 = previous_pos
		previous_pos = pos
		previous_tag1 = previous_tag2
		previous_tag2 = current_tag
		current_tag = tag
file_reader.close()
