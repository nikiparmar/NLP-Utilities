import sys

#print(sys.argv[1])

pspam = dict()
word_count = dict()
label_count =0
spam_tree = dict()
distinct_words =0
no_labels =  0
file_reader = open(sys.argv[1])
for line in file_reader:
	count =0
	for word in line.replace('\n',' ').split(" "):
		#print(word)
		if word == "Subject:" or word == "" or word == " ":
			continue
		if count ==0:
			label = word
			if word in pspam.keys():
				pspam[word] +=1	
			else:
				pspam[word] = 1
				no_labels +=1
			if word not in spam_tree:
				spam_tree[label] = dict()
						
			label_count +=1
		else:	
			word = word.lower()
			if word in spam_tree[label]: 
				spam_tree[label][word] +=1
			else:
				flag = 0
				for l in spam_tree:
					if word in spam_tree[l]:
						flag =1
						break
				if flag ==0:
					distinct_words+=1
				spam_tree[label][word]=1
			if label in word_count.keys():
				word_count[label] += 1
			else:
				word_count[label] =1
		count +=1
	#spam_tree[label].update(spam_words)

print(pspam)
#print(spam_tree)
print(word_count)
print(no_labels)
print(label_count)
print(distinct_words)
file_reader.close()


f1 = open(sys.argv[2],'w')
f1.write(str(no_labels) + "\n")
f1.write( str(spam_tree) + "\n")
f1.write(str(pspam) + "\n")
#f1.write(str(distinct_words) + "\n")
f1.write(str(word_count) + "\n")
f1.write(str(label_count) + "\n")
f1.write(str(distinct_words))
f1.close()

print(distinct_words)
