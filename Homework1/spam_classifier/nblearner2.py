import collections

def tree():
	return collections.defaultdict(tree)

spam_words = dict()
pspam = dict()
word_count = dict()
label_count =0
spam_tree = tree()
distinct_words =0
no_labels =  0
file_reader = open('allspam1.txt')
for line in file_reader:
	count =0
	for word in line.replace('\n',' ').split(" "):
		print(word)
		if word == "Subject:" or word == "" or word == " ":
			continue
		if count ==0:
			label = word
			if word in pspam.keys():
				pspam[word] +=1	
			else:
				pspam[word] = 1
				no_labels +=1
			label_count +=1
		else:	
			if word in spam_tree[label]: 
				spam_tree[label][word] +=1
			else:
				spam_tree[label][word]=1
				distinct_words+=1
			if label in word_count.keys():
				word_count[label] += 1
			else:
				word_count[label] =1
		count +=1

print(pspam)
print(spam_tree)
print(word_count)
print(no_labels)
file_reader.close()


f1 = open('learn.nb','w')
f1.write(str(no_labels) + "\n")
f1.write( str(spam_tree) + "\n")
f1.write(str(pspam) + "\n")
#f1.write(str(distinct_words) + "\n")
f1.write(str(word_count) + "\n")
f1.write(str(label_count) + "\n")
f1.close()

print(distinct_words)
