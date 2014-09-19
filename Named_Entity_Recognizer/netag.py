#! /usr/bin/env python

import sys

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


training = ""
count = 0
current = ""
previous_pos = ""
pos = ""
tag = ""
previous_tag = ""
current_tag = ""
while 1:
	line = sys.stdin.readline()
	if not line:
		break
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
       	output = ""
	for word_test in line.replace('\n',' ').split(" "):	
		count =0
		for label in word_test.split("/"):
			if count ==0:
				feature = label
			else:	
				tag = label				
			count +=1
		if current != "":
			training = previous_pos + " " + "prevbio1:" + prev_bio1 + " " + "prevtag1:" + previous_tag1 + " " + "prevword1:" + previous1 +  " " + "prevpref1:" + previous1[:3] + " " + "prevsuff1:" + previous1[-3:] + " " + "prevbio2:" + prev_bio2 + " " + "prevtag2:" + previous_tag2 + " " + "prevword2:" + previous2 +  " " + "prevpref2:" + previous2[:3] + " " + "prevsuff2:" + previous2[-3:] + " " + "currtag:" +  current_tag + " " + "currword:" + current + " " + "currpref:" + current[:3] + " " + "currsuff:" + current[-3:] + " " + "nexttag:" + tag+  " " +  "nextword:"+ feature + " " + "nextpref:" + feature[:3] + " " + "nextsuff:" + feature[-3:]
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

                        output += current + "/" + current_tag + "/" + cal_label + " "
			pos = cal_label
			#print(cal_label)
		previous1 = previous2
		previous2 = current
		current = feature
		prev_bio1 = prev_bio2
		prev_bio2 = pos
		previous_tag1 = previous_tag2
		previous_tag2 = current_tag
		current_tag = tag

	print(output)
        sys.stdout.flush()

