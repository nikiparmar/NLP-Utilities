from math import log
from decimal import *
import glob
import collections, sys


spam_tree = dict()

word_count = dict()
file_reader = open(sys.argv[1])
no_labels = file_reader.readline()
spam_tree = eval(file_reader.readline())
pspam = eval(file_reader.readline())
print(str(pspam) + "\n")
word_count = eval(file_reader.readline())
label_count = int(file_reader.readline())
distinct_words = int(file_reader.readline())
file_reader.close()


otput = open('spam.out','w')
#list_of_files = glob.glob('./SPAM_dev/HAM.*.txt')
#for file_name in list_of_files:
file_reader = open(sys.argv[2],'r')
#print(file_name)
for line in file_reader:
	classify = dict()
	count = 0
	for word in line.replace('\n',' ').split(" "):
		if word == "Subject:" or word == "" or word == " ":
			continue
		word = word.lower()
		for label in spam_tree.keys():
			if word in spam_tree[label]:
				ps = Decimal(spam_tree[label][word] +1)/(Decimal(word_count[label]) + Decimal(distinct_words))
			else:
				ps = Decimal(1)/(Decimal(word_count[label]) + Decimal(distinct_words))
			#print(log(ps))
			if label in classify:
				classify[label] +=(log(ps))
			else: 
				classify[label] = log(ps)		
		count +=1
	#print(str(classify))
	for label in classify:
                classify[label] += log((Decimal(pspam[label])/Decimal(label_count)))	
	#classify[label] += log((Decimal(pspam[label])/Decimal(label_count)))

	#print(classify)
	
	value = -65536
	for i in classify:
		if classify[i] > value:
			value = classify[i]
			label = i
	print(label)		
	
	otput.write(label + "\n")


file_reader.close()

otput.close()
