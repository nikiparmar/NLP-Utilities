#! /usr/bin/env python

#Perceptron CLassifier
#Input : Line to classify
#Output Label for the input

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


while 1:
	line = sys.stdin.readline()
	if not line:
		break
	weight_vector = dict()
	for label in label_tree:
		weight_vector[label] = 0
	for word in line.replace('\n',' ').split(" "):
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
	print(cal_label)
	sys.stdout.flush()	
