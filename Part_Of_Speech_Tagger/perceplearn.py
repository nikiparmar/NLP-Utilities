#! /usr/bin/env python

## Code to train the classifier. uses a 2 level dict to store the word occurences for 
## different labels. Works in multiclass enviornment
## This perceptron run for 20 iterations

import sys, random

label_tree = dict()
training = []
number_of_rows =0
file_reader = open(sys.argv[1])
for line in file_reader:
	count =0
	training.append(line)
	for word in line.replace('\n',' ').split(" "):
		if word == " " or word == "":
			continue
		if count ==0:
			label = word
			if label not in label_tree:
				label_tree[label] = dict()
		else:	
			if word not in label_tree[label]: 
				label_tree[label][word] = 0
		count +=1
	number_of_rows +=1

file_reader.close()

# Put all word occurences in each label 
for l in label_tree:
	for word in label_tree[l]:
		for label in label_tree:
			if word not in label_tree[label]:
				label_tree[label][word]=0
#print(label_tree)
for i in range(1,20):
	training = random.sample(training, number_of_rows)
	for line in training:
		count =0
        	weight_vector = dict()
        	for l in label_tree:
                	weight_vector[l] = 0
        	for word in line.replace('\n',' ').split(" "):
			if word == " " or word == "":
				continue
                	if count ==0:
                        	label = word
                	else:
                                for l in label_tree:
                                        weight_vector[l] += label_tree[l][word]
                	count +=1
	

		max_label = -100000
		for l in weight_vector:
			if weight_vector[l] > max_label:
				max_label = weight_vector[l]
				cal_label = l
		
		if cal_label != label:
			for word in line.replace('\n',' ').split(" "):
				if word == label or word == cal_label or word == " " or word == "":
					continue
				label_tree[label][word] += 1
				label_tree[cal_label][word] -= 1


f1 = open(sys.argv[2],'w')
for label in label_tree:
	f1.write(label + "\n")
	f1.write(str(label_tree[label]) + "\n")
f1.close()
