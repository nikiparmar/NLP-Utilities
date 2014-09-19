
file_reader = open('test_data.txt','w')
fp = open('alltest.txt','r')
count =0
for line in fp:
	for word in line.replace('\n','').replace('#','').split(" "):
		if word == "Subject:" or word == "" or word == " " or word == "\n":
			continue
		if word == "SPAM":
			#file_reader.write("SPAM ")
			continue
		if word == "HAM":
			#file_reader.write("HAM ")
			continue
		#word = word.lower()
		file_reader.write(word + " ")
	file_reader.write("\n")


fp.close()
file_reader.close()	
