#! /usr/bin/env python

import collections, sys

label_tree = dict()
label= ""
file_reader = open(sys.argv[1])
count =0
for line in file_reader:
        if count ==0:
                label = line.replace("\n","")
                label_tree[label] = dict()
                count =1
        else:
                current_dict = eval(line)
                label_tree[label] = current_dict
                count =0
file_reader.close()


count = 0
previous1 = ""
previous2 = ""
current = ""
current_pos = ""
pos = ""
training = ""
output = ""
while 1:
	line = sys.stdin.readline()
	if not line:
		break
	output = ""
	previous1 = ""
        previous2 = ""
        current = ""
        current_pos = ""
        prev_pos1 = ""
        prev_pos2 = ""
        pos = ""
        feature = ""
	for feature in line.replace('\n',' ').split(" "):	
		if current != "":		
			training = "prevtag1:" + prev_pos1 + " " + "prevword1:" + previous1 +  " " + "prevpref1:" + previous1[:2] + " " + "prevsuff1:" + previous1[-2:] + " " +  "prevtag2:" + prev_pos2 + " " + "prevword2:" + previous2 +  " " + "prevpref2:" + previous2[:2] + " " + "prevsuff2:" + previous2[-2:] + " "+  "currword:" + current + " " + "currpref:" + current[:2] + " " + "currsuff:" + current[-2:] + " " +  "nextword:"+ feature + " " + "nextpref:" + feature[:2] + " " + "nextsuff:" + feature[-2:]
			#print(training)
			weight_vector = dict()
        		for label in label_tree:
                		weight_vector[label] = 0
        		for word in training.replace('\n',' ').split(" "):
                		if word == "" or word == " ":
                        		continue
               			for label in label_tree:
                        		if word in label_tree[label]:
                                		weight_vector[label] += int(label_tree[label][word])

       		 	max_label = -10000
        		for label in label_tree:
                		if weight_vector[label] > max_label:
                        		max_label = weight_vector[label]
                     		   	cal_label = label
        	
			output += current +"/" + cal_label + " "
			pos = cal_label
		previous1 = previous2
                previous2 = current
                current = feature
                prev_pos1 = prev_pos2
                prev_pos2 = pos
	print(output)
        sys.stdout.flush()

