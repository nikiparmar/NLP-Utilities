import sys,math
from decimal import *

train = open(sys.argv[1])
test = open(sys.argv[2])
tag_word = dict()
tags_bigram =  dict()
tag_number = dict()
total_tags = 0
tag_count =1
prev = ""
word_dict = dict()

 
for line in train:
	words = line.strip("\r\n").split("/")
	# Word to tag
	if (words[1] not in tag_word):
		tag_word[words[1]] = dict()
	if words[0] not in tag_word[words[1]]:
		tag_word[words[1]][words[0]] = 0
	if words[0] not in word_dict:
		word_dict[words[0]] = 1
	tag_word[words[1]][words[0]] +=1
	#tag dict
	if words[1] not in tag_number:
		tag_number[words[1]] = tag_count
		tag_count +=1
	if prev != "":
		if prev not in tags_bigram:
			tags_bigram[prev] = dict()
		if words[1] not in tags_bigram[prev]:
			tags_bigram[prev][words[1]] = 0
		tags_bigram[prev][words[1]] +=1
	else:
		if "." not in tags_bigram:
			tags_bigram["."] = dict()
		if words[1] not in tags_bigram["."]:
			tags_bigram["."][words[1]] = 0
		tags_bigram["."][words[1]] += 1 
	total_tags +=1
	prev = words[1]

total_count = 0
for tag in tag_word:
	total_count = 0
	for word in tag_word[tag]:
		total_count += tag_word[tag][word]
	for word in word_dict:
		if word in tag_word[tag]:
			tag_word[tag][word] = Decimal(tag_word[tag][word] + 1)/Decimal(total_count + len(word_dict))
		else:
			tag_word[tag][word] = Decimal(1)/Decimal(total_count + len(word_dict))

bigram_count = len(tag_number)

for tag in tags_bigram:
	start = tag_number[tag]
	total_count = 0
	for prev_tag in tags_bigram[tag]:
		total_count += tags_bigram[tag][prev_tag]
	for prev_tag in tag_number:
		if prev_tag in tags_bigram[tag]:
			tags_bigram[tag][prev_tag] = Decimal(tags_bigram[tag][prev_tag] + 1)/Decimal(total_count + bigram_count)
		else:
			tags_bigram[tag][prev_tag] = Decimal(1)/Decimal(total_count + bigram_count)

best_pred = dict()
Q = dict()
training = []


for line in test:
	word =line.strip('\r\n').replace("\"","").split(" ")
	training.append(word)
	Q[0] = dict()
	best_pred[0] = dict()
	best_score = -1000000000
	start = "."
	sys.stdout.write(word[0] + " ")
	for tag in tag_number:
		Q[0][tag_number[tag]] = math.log(tags_bigram["."][tag]) + math.log(tag_word[tag][word[0]])
		best_pred[0][tag_number[tag]] = tag
	for i in range(1, len(word)):
		sys.stdout.write(word[i] + " ")
		Q[i] = dict()
		best_pred[i] = dict()
		for tag in tag_number:
			no = tag_number[tag]
			Q[i][no] = -1000000000000.00
			best_pred[i][no] = 0
			best_score = -1000000000000.00
			pword = tag_word[tag][word[i]]
			for t in tag_number:
				k = tag_number[t]
				r = math.log(tags_bigram[t][tag]) + math.log(pword) + (Q[i-1][k])
				if r> best_score:
					best_score = r
					best_pred[i][no] = t
					Q[i][no] = r

	sys.stdout.write("\n")	
	final_best = 0
	final_score = -10000000000
	n = len(word) - 1
	for tag in tag_number:
		j = tag_number[tag]
		if Q[n][j] > final_score:
			final_score = Q[n][j]
			final_best = tag
	result = []
	result.append(final_best)
	current = final_best
	for i in range(n-1, 0, -1):
		current = best_pred[i+1][tag_number[current]]
		result.append(current)
	result.append(best_pred[1][tag_number[current]])
	for i in reversed(result):
		sys.stdout.write(i + " ")
	sys.stdout.write("\n")
