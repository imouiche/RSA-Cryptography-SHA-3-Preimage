
"""RSA based Chinese Remainder Theorem using Montgomery Algorithm
    Python code
    Author: Inoussa Mouiche, 
    MTIS graduate student UVic: Hardware Security and Cryptography by Dr. Samer """
import time

def rap_expo(x, r):
    
    if r==1:
        return x
    elif r%2==0:
        return rap_expo(x**2,r/2)
    else:
        return x*rap_expo(x**2,(r-1)/2)

#print 'hello inoussa'
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



def Megcd(x,y):
    u, v = 0, 1
    x1, y1 = x, y
    y = -y
    m, n = 1, 0
    while x !=0:
        quotient, res = y//x, y%x # paralell assignment
        m1= u-m*quotient
        n1= v-n*quotient
        y, x = x,res
        u, v = m,n
        m, n = m1,n1
    return (y, (u%y1), (v%x1)%y1)            # y=gcd(x,y) and u, v are eucludian coefs

# Check if y=1, not necessary

def modular_inv(x,l):
    d, u, v = Megcd(x,l)
    if d!=1:
        return "the inverse of x modulo l does not exist"
    else:
        return u




def encrypt(p,q):
    n = p*q
    phin = (p-1)*(q-1)
    f = open('Cryptography.txt','r')
    msg = f.readlines()             # read the msg to encrypt line by line
    alphabet = 'abcdefghijklmnopqrstuvwxyz'   # alph list
    Alphabet = alphabet.upper()
    out = open('cypherrsk2.txt','w')  # open file text in writing mode
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
        i = 0               # Initialize of the ith letter 
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


#------------------- Montgomery product-----------------------

def MonProd(x,y,n,r):
    #r = 16
    #r = 256
    #n = 137
    n1 = Megcd(r,n)[2]
    # n1 = 11
    t = x*y
    m = (t*n1)%r
    u = (t+m*n)/r
    #print u, t, m
    if u >= n:
        return u-n
    else:
        #print u-n
        return u
#------------------ Montgomery Multiplication -----------------------

def ModMul(x,y,n):  # modular multiplication
    n1 = Megcd(r,n)
    a = (x*r)%n
    x = MonProd(a,y,n,r)
    return x
#------------------- Montgomery Exponentiation---------------------------


def ModExp(M,e,n,r):  # modular exponentiation
    #r = 2**(8)
    #r = 16
    e = bin(e)[2:]
    k = len(e)
    M1 = (M*r)%n
    x1 = r%n
    #print M1, x1
    for i in range(k):
        x1 = MonProd(x1,x1,n,r)
        #print x1
        if int(e[i])==1:
            x1 = MonProd(M1,x1,n,r)
     #   print x1
    x = MonProd(x1,1,n,r)
    return x

# -------------- RSA Ecryption based CRT -------------------------------------

def decryption_CRT(e,m,p,q,r):  # using Garner formula
    n = p*q
    #r = 2**7
    dp = modular_inv(e,p-1)
    dq = modular_inv(e,q-1)
    qinv=  modular_inv(q,p)  # inverse of q mod p

    # m1 = c^dp mod p and m2 = c^dq mod q
    m1 = ModExp(m,dp,p,r)
    m2 = ModExp(m,dq,q,r)
    h = qinv*(m1-m2)%p
    m = m2 + h*q
    return m1, m2, m
def MRC(e,m,p,q,r):
    n = p*q
    #r = 2**7
    dp = modular_inv(e,p-1) # inverse of e mod p-1
    dq = modular_inv(e,q-1)
    pinv=  modular_inv(p,q)

    # m1 = c^dp mod p and m2 = c^dq mod q
    m1 = ModExp(m,dp,p,r)
    m2 = ModExp(m,dq,q,r)
   
    m = m1 + (((m2-m1)*(pinv%q))%q)*p
    return m

def SRC(e,m,p,q,r):
    n = p*q
    #r = 2**7
    dp = modular_inv(e,p-1)
    dq = modular_inv(e,q-1) # inverse of e mod q-1
    pinv=  modular_inv(p,q)
    qinv=  modular_inv(q,p)

    # m1 = c^dp mod p and m2 = c^dq mod q
    m1 = ModExp(m,dp,p,r)
    m2 = ModExp(m,dq,q,r)
   
    m = (m1*(qinv%p)*q + m2*(pinv%q)*p)%n 
    return m

# 1013, 997
def decrypt_CRT(p,q,r):      # decryption function
    T_init = time.clock()
    n = p*q
    phin = (p-1)*(q-1)
    f = open('cyphertext_phone1.txt','r') # open encrypted msg
    msg = f.readlines()                             # read it line by line
    alphabet = 'abcdefghijklmnopqrstuvwxyz'     # alph
    Alphabet = alphabet.upper()
    out = open('Phone1_crt','w')   # open empty file named plaintsrk in writing mode
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
    #e = 11
    e = 31 
    #e = 23                        # public key
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
                m = code1[al[t]]
                #k=(rap_expo(code1[al[t]],d))%n  # compute exp power d
                #k= MRC(e,m,p,q,r) # Mixed radix conversion
                k= SRC(e,m,p,q,r) # single Radix Convertion
                plaint += code1.keys()[code1.values().index(k)]   # take the keys in dict corresp to value index k
                t +=1
            else: 
                #k=(rap_expo(code2[al[t]],d))%n    ## compute exp power d
                m = code2[al[t]]
                #k= MRC(e,m,p,q,r)
                k= SRC(e,m,p,q,r) # single Radix Convertion
                plaint += code2.keys()[code2.values().index(k)]
                t +=1
        out.write(plaint)
    out.close()


    Elapse_time = (time.clock()-T_init)

    print Elapse_time



