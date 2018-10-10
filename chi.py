import numpy as np

def Matrix():	L = list(open("chiImage.txt", "r"))
	#L = list(open("Pi.txt1", "r"))
	L = list(row.strip().split() for row in L) #remove all odd characters.
	M= [[0 for x in range(5)] for y in range(5)]
	j = 0
	for y in range(5):
		for x in range(5):
			M[x][y] = L[0][j]
			j +=1
	return M
def Sha3Hex(n):
	num_of_bits = 8
	H = bin(int(n, 16))[2:].zfill(num_of_bits)
	#H = shift(N, 7)
	#H = H[::-1]
	return H
def BinTohex(n):
	num_of_bits = 8
	Bh = hex(int(n, 2))[2:]
	return Bh
def shift(l, n):
    return l[n:] + l[:n]

def flipbit(n):
	if n =='1':
		return '0'
	else:
		return '1'
def Preimage(w):
	R = ''
	for k in range(5):
		s = shift(w, k)
		print s
		A = s[0]; B = s[1]; C = s[2]; D=s[3]; E=s[4]
		A1 = flipbit(A); B1 = flipbit(B); C1 = flipbit(C); D1 = flipbit(D); E1 = flipbit(E)
		A = int(A); A1 = int(A1); B = int(B); B1 = int(B1); C = int(C); C1 = int(C1); D= int(D)
		D1= int(D1); E = int(E); E1 = int(E1)
		R = R + str(A*B | A*C1*E1 | A*C1*D | A1*B1*C*E1 | A1*B1*C*D | A*C*D1*E | A1*B1*C1*D1*E)
	return R
def Chi():
	M = Matrix()
	M = np.array(M)
	for i in range(5):
		N = M[:,i]
		prnt N
		N0 = Sha3Hex(N[0]); N1 = Sha3Hex(N[1]); N2 = Sha3Hex(N[2])
		N3 = Sha3Hex(N[3]); N4 = Sha3Hex(N[4])
		A0 = ''; A1 = ''; A2 = ''; A3 = ''; A4 = '';
		#S = ' '
		#s = N0[0]+N1[0]+N2[0]+N3[0]+N4[0]
		for j in range(8):
			s = N0[j]+N1[j]+N2[j]+N3[j]+N4[j]
			S = Preimage(s)
			A0 = A0+S[0]; A1=A1+S[1]; A2=A2+S[2]; A3=A3+S[3]; A4=A4+S[4] 
		#print A0
		m0 = BinTohex(A0); m1 = BinTohex(A1); m2 = BinTohex(A2)
		m3 = BinTohex(A3); m4 = BinTohex(A4)
		print  m0, m1, m2, m3,m4
	return m0, m1, m2, m3,m4













