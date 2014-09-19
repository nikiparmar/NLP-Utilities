
spam_words = dict()
ham_words = dict()
pspam =0
pham =0
spam_word_count =0
ham_word_count =0
distinct_words =0
file_reader = open('allspam.txt')
for line in file_reader:
	count =0
	for word in line.replace('\n',' ').split(" "):
		if word == "Subject:" or word == "" or word == " ":
			continue;
		if count ==0:
			if word not in spam_words[word]:
				spam[word] = []
		spam_word_count +=1
		if word in spam_words: 
			spam_words[word] +=1
		else:
			spam_words[word]=1
			distinct_words+=1
	pspam +=1
		count +=1
print(spam_word_count)
print(pspam)
print(spam_words)
file_reader.close()

file_reader = open('allham.txt')
for line in file_reader:
	count = 0
	for word in line.replace('\n','').split(" "):
		if word == "Subject:" or word == "HAM" or word == "" or word == " ":
			continue;
		ham_word_count +=1
		if word in ham_words: 
			ham_words[word] +=1
		else:
			ham_words[word]=1
			if word not in spam_words:
				distinct_words+=1
	pham +=1
print(ham_word_count)
print(pham)
print(ham_words)
file_reader.close()

f1 = open('learn.nb','w')
f1.write(str(spam_words))
f1.write("\n")
f1.write(str(ham_words) + "\n")
f1.write(str(pspam) + "\n")
f1.write(str(pham) + "\n")
f1.write(str(distinct_words) + "\n")
f1.write(str(spam_word_count) + "\n")
f1.write(str(ham_word_count) + "\n")
f1.close()

print(distinct_words)
