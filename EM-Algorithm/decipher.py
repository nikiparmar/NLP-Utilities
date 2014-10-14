import sys,math
from decimal import *

def log_add(val1, val2):
	if math.isinf(val1):
		return val2
	if math.isinf(val2):
		return val1
	if val1 - val2 > 16:
		return val1
	if val1 > val2:
		return val1 + math.log(1 + math.exp(val2 - val1))	
	if val2 - val1 > 16:
		return val2
	return val2 + math.log(1 + math.exp(val1 - val2))	

def run_forward():
	global eng_trigram, cipher_word, mapping, alpha, record, eng_bigram, eng_unigram
	count = 0
	alpha[count] =dict()
	for l in mapping:
		alpha[count][l] = eng_unigram[l] 
			#+ cipher_word[l][record[0]]
	c = record[0]
	count +=1
	alpha[count] = dict()
	for l1 in mapping:
		alpha[count][l1] = dict()
		for l2 in mapping:
			alpha[count][l1][l2] = eng_bigram[l2][l1] + math.log(cipher_word[l2][c]) + alpha[count-1][l2]
	count +=1
							
	for c in record[1:]:
		alpha[count] = dict()
		for l1 in mapping:
			alpha[count][l1] = dict()
			for l2 in mapping:
				for k in mapping:
					temp = eng_trigram[k][l2][l1] + math.log(cipher_word[l2][c]) + alpha[count-1][l2][k]
					if l2 not in alpha[count][l1]:
						alpha[count][l1][l2] = temp
					else:
						alpha[count][l1][l2] = 	log_add(alpha[count][l1][l2] , temp)
				
					
		count +=1

def run_backward():
	global eng_trigram, cipher_word, mapping, beta, record, eng_bigram, eng_unigram
	count = len(record) -1
	beta[count] = dict()	
	rev_record = record[::-1]
	#print rev_record
	for l in mapping:
		beta[count][l] =  math.log(1)
	count -=1

	beta[count] =dict()
	c = rev_record[0]
	for l2 in mapping:
		beta[count][l2] = dict()
		for l1 in mapping:
			beta[count][l2][l1] = eng_bigram[l2][l1] + math.log(cipher_word[l1][c]) + beta[count +1][l1]
	count -=1
	for c in rev_record[1:-1]:
		beta[count] = dict()
		for l2 in mapping:
			beta[count][l2] = dict()
			for l1 in mapping:
				for k in mapping:
					temp = eng_trigram[l1][l2][k] + math.log(cipher_word[k][c]) + beta[count+1][k][l2]
					if l1 not in beta[count][l2]:
						beta[count][l2][l1] = temp
					else:
						beta[count][l2][l1] = 	log_add(beta[count][l2][l1] , temp)
				
					
		count -=1

def update_counts():
	global eng_trigram, cipher_word, mapping, beta, record, no_words, cipher_dict, eng_bigram, eng_unigram
	alpha_final = float("-inf")
	
	for l1 in alpha[no_words]:
		for l2 in alpha[no_words][l1]:
			alpha_final = log_add(alpha_final , alpha[no_words][l1][l2])

	cipher_count = dict()
	count = 0
	
	print "alpha final " + str(alpha_final)

	for c in record:
		for l1 in mapping:
			if l1 not in cipher_count:
				cipher_count[l1] = dict()
			alp = float("-inf")
			bet = float("-inf")
			if count == 0:
				alp = log_add(alp ,alpha[count][l1])
			else:
				for l2 in alpha[count][l1]:
					#print l2
					alp = log_add(alp, alpha[count][l1][l2])
			if count == no_words-1:
				bet = log_add(bet,beta[count][l1])
			else:
				for l2 in beta[count][l1]:	
					bet = log_add(bet, beta[count][l1][l2])
			temp =  math.exp(alp + bet + math.log(cipher_word[l1][c])  - alpha_final)
			if c not in cipher_count[l1]:
				cipher_count[l1][c] = temp
			else:
				cipher_count[l1][c]  += temp
		count +=1
			
	#print cipher_count
	for l1 in mapping:
		total = sum(cipher_count[l1].values())
		for c in cipher_count[l1]:
			cipher_word[l1][c] = Decimal(cipher_count[l1][c])/Decimal(total)
			if cipher_word[l1][c] < 0:
				cipher_word[l1][c] = 0.00001
	#print cipher_word

def run_viterbi():
	global record, mapping, eng_trigram, cipher_word, no_words
	Q = dict()
	best_pred = dict()	
	Q[0] = dict()
	best_pred[0] = dict()
	best_score = -1000000000
	word = record

	for tag in mapping:
		Q[0][mapping[tag]] = eng_unigram[tag] + math.log(cipher_word[tag][word[0]])
		best_pred[0][mapping[tag]] = tag
	
	Q[1] = dict()
	best_pred[1] = dict()
	for tag1 in mapping:
		j = mapping[tag1]
		best_pred[1][j] = dict()
		Q[1][j] = dict()
		for tag2 in mapping:
			j2 = mapping[tag2]
			Q[1][j][j2] = eng_bigram[tag1][tag2] + math.log(cipher_word[tag2][word[1]]) + Q[0][j]
			best_pred[1][j][j2] = tag2
			

	for i in range(2, no_words):
		#sys.stdout.write(word[i] + " ")
		Q[i] = dict()
		best_pred[i] = dict()
		for tag in mapping:
			no = mapping[tag]
			Q[i][no] = dict()
			best_pred[i][no] = dict()
			for tag2 in mapping:
				no2 = mapping[tag2]
				Q[i][no][no2] = -1000000000000.00
				best_pred[i][no][no2] = 0
				best_score = -1000000000000.00
				pword = cipher_word[tag2][word[i]]
				if pword < 0:
					pword = 0
				#print pword
				for t in mapping:
					k = mapping[t]
					r = eng_trigram[t][tag][tag2] + math.log(pword) + (Q[i-1][k][no])
					if r> best_score:
						best_score = r
						best_pred[i][no][no2] = t
						Q[i][no][no2] = r

	final_best = 0
	final_score = -10000000000
	n = len(word) - 1
	for tag in mapping:
		j = mapping[tag]
		for tag2 in mapping:
			j2 = mapping[tag2]
			if Q[n][j][j2] > final_score:
				final_score = Q[n][j][j2]
				final_best = tag2

	result = []
	result.append(final_best)
	current = final_best
	i = n-1
	while i >= 0:
		current_score = -1000000000
		next_best = 0
		c = mapping[current]
		for tag in mapping:
			j = mapping[tag]
			if best_pred[i+1][j][c] > current_score:
				next_best = tag
				current_score = best_pred[i+1][j][c]
		current =  next_best
		result.append(current)
		i -=1
	#result.append(best_pred[1][mapping[current]])
	decipher = ""
	for i in reversed(result):
		decipher += i
	print decipher
	return decipher
	
train = open(sys.argv[1])
source = open(sys.argv[2])
num_iters = int(sys.argv[3])

global eng_trigram, cipher_word, mapping, beta, record, no_words, eng_unigram, eng_bigram
record = []
count = 0
eng_trigram = dict()
eng_unigram = dict()
eng_bigram = dict()
cipher_word =dict()
mapping = dict()
total_map = 0

count = 0
prev2 = ""
prev1 = ""
for line in train:
	line = line.strip("\r\n")
	for l in line:
		if l not in mapping:
			mapping[l] = count
			eng_unigram[l] = 0
			count +=1
		eng_unigram[l] +=1
		if prev2 != "" and prev1 != "":
			if prev2 not in eng_trigram:
				eng_trigram[prev2] =dict()
			if prev1 not in eng_trigram[prev2]:
				eng_trigram[prev2][prev1] = dict()
			if l not in eng_trigram[prev2][prev1]:
				eng_trigram[prev2][prev1][l] = 1
			eng_trigram[prev2][prev1][l] +=1
			
		prev2 = prev1
		prev1 = l

train.close()


print mapping


for l1 in mapping:
	if l1 not in eng_trigram:
		eng_trigram[l1] = dict()
	for l2 in mapping:
		if l2 not in eng_trigram[l1]:
			eng_trigram[l1][l2] = dict()
		for l3 in mapping:
			if l3 not in eng_trigram[l1][l2]:
				eng_trigram[l1][l2][l3] = 1


eng_bigram = dict()
uni_total = sum(eng_unigram.values())
for l in mapping:
	eng_unigram[l] = math.log(Decimal(eng_unigram[l])/Decimal(uni_total))
	eng_bigram[l] = dict()
	for c in mapping:
		eng_bigram[l][c] = math.log(Decimal(1)/Decimal(27*27))
		
for prev2 in mapping:
	for prev1 in eng_trigram[prev2]:
		val = sum(eng_trigram[prev2][prev1].values())
		for l in eng_trigram[prev2][prev1]:
			eng_trigram[prev2][prev1][l] = math.log(Decimal(eng_trigram[prev2][prev1][l])/Decimal(val))

#print eng_trigram

for l in mapping:
	cipher_word[l] = dict()

cipher = []
record = ""
cipher_dict = dict()
for line in source:
	line = line.strip("\r\n")
	record += line
	for c in line:
		cipher.append(c)
		if c not in cipher_dict:
			cipher_dict[c] = 1

for c in cipher_dict:	
	for l in mapping:
		if l == ' ':
			if c == ' ':
				cipher_word[l][c] = 1000
			else:
				cipher_word[l][c] = 1
		else:
			cipher_word[l][c] = 1

for l in mapping:
	val = sum(cipher_word[l].values())
	for c in cipher_word[l]:
		cipher_word[l][c] = Decimal(cipher_word[l][c])/Decimal(val)

#print eng_trigram
#print cipher_word

no_words = len(record)

alpha = dict()
beta = dict()

for it in range( 0 , num_iters ):
	
	run_forward()
	run_backward()
	update_counts()
		
	result = run_viterbi()
	print result
