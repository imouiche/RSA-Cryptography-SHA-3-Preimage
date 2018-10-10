
""" Cryptography using RSK (Rivest Shamir and Adleman)"""
import  time

def rap_expo(x, r):
    
	if r==1:
		return x
	elif r%2==0:
		return rap_expo(x**2,r/2)
	else:
		return x*rap_expo(x**2,(r-1)/2)

# extended euclid algorithm

def egcd(x,y):
    u, v = 0, 1
    m, n = 1, 0
    while x !=0:
        quotient, res = y//x, y%x # paralell assignment
        m1= u-m*quotient
        n1= v-n*quotient
        y, x = x,res
        u, v = m,n
        m, n = m1,n1
    return y, u, v           # y=gcd(x,y) and u, v are eucludian coefs

# Check if y=1
def modular_inv(x,l):
	d, u, v = egcd(x,l)
	if d!=1:
		return "the inverse of x modulo l does not exist"
	else:
		return u       # public key
#p=8191,q=127

def encrypt(p,q):
	n = p*q
	phin = (p-1)*(q-1)
	f = open('Plaintext_phone.txt','r')
	msg = f.readlines()             # read the msg to encrypt line by line
	alphabet = 'abcdefghijklmnopqrstuvwxyz'   # alph list
	Alphabet = alphabet.upper()
	out = open('cyphertext_phone1.txt','w')  # open file text in writing mode
	i, j, code1, code2 =0,0,{},{}
	for j in xrange(n):
		if egcd(j,n)[0]==1:    # select only j coprime with n to ensure the inverse exists
			if i<26:
				code1.update({alphabet[i]:j})  # load alph in code1 dict n assign the corresp value j
				code2.update({Alphabet[i]:j})   # for the upper case
				i+=1
			else:
				code1.update({alphabet[i%26]+str(divmod(i,26)[0]):j}) # increase the alph list by adding number
				code2.update({Alphabet[i%26]+str(divmod(i,26)[0]):j}) 
				i+=1
			
	#e = 11
	e = 31
	#e = 23
	for sentence in msg:    # choose a sentence in the list of msg
		cypher =''
		i = 0				# Initialize of the ith letter 
		while i < len(sentence):
			if (sentence[i] not in alphabet) and (sentence[i] not in Alphabet):
				cypher += sentence[i]      # conserve this character if it is not in alph
				i +=1
			elif sentence[i] in alphabet:
				k=(rap_expo(code1[sentence[i]],e))%n   # compute the exp of the ith value in code1
				cypher += code1.keys()[code1.values().index(k)]  #  add keys alph corresp to the index of value k
				i +=1
			else :
				k=(rap_expo(code2[sentence[i]],e))%n    # compute the exp of the ith value in code2
				cypher +=  code2.keys()[code2.values().index(k)] # keys whose value index = k
				i +=1
		out.write(cypher)     # write in the created cypher text
	out.close()
	#p=8191,q=127

def decrypt(p,q):      # decryption function
	T_init = time.clock()
	n = p*q
	phin = (p-1)*(q-1)
	f = open('cyphertext_phone1.txt','r') # open encrypted msg
	msg = f.readlines()                             # read it line by line
	alphabet = 'abcdefghijklmnopqrstuvwxyz'     # alph
	Alphabet = alphabet.upper()
	out = open('Phone1.txt','w')   # open empty file named plaintsrk in writing mode
	i, j, code1, code2 =0,0,{},{}     # initialize dict1 n dict2
	for j in xrange(n):
		if egcd(j,n)[0]==1:           # select only j coprime with n to ensure the inverse exists
			if i<26:
				code1.update({alphabet[i]:j}) # load alph in code1 dict n assign the corresp value j
				code2.update({Alphabet[i]:j}) 
				i+=1
			else:
				code1.update({alphabet[i%26]+str(divmod(i,26)[0]):j}) # extend the alph list for large n
				code2.update({Alphabet[i%26]+str(divmod(i,26)[0]):j}) 
				i+=1
	e = 31
	#e = 23
	#e = 11                         # public key
	d =modular_inv(e,phin)%n      # private key
	for m in msg:                 #  select message by line
		s,al,i,j ='', [],0,0      # s is the string
		while j<len(m):
			k = j+1                # is the next variable a letter or a number
			try:                  # 
				int(m[k])
				s += m[j]
				j += 1
			except: 
				s += m[j]
				al.append(s)      # append if s is a letter n initialise s again
				j +=1 
				s = ''
		plaint,t ='', 0   # here y have al as a list contain alph by block 
		while t < len(al):       # while loop to decrypt each block letter
			if al[t] not in code1 and al[t] not in code2:
				plaint += al[t]
				t +=1
			elif al[t] in code1:
				k=(rap_expo(code1[al[t]],d))%n  # compute exp power d
				plaint += code1.keys()[code1.values().index(k)]   # take the keys in dict corresp to value index k
				t +=1
			else: 
				k=(rap_expo(code2[al[t]],d))%n    ## compute exp power d
				plaint += code2.keys()[code2.values().index(k)]
				t +=1
		out.write(plaint)
	out.close()
	
	Elapse_time = (time.clock()-T_init)
	print Elapse_time