from __future__ import division
import numpy as np
from math import log


def Matrix():
	L = list(open("lotaimage.txt", "r"))
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
	H = H[::-1]
	return H
def BinTohex(n):
	num_of_bits = 8
	Bh = hex(int(n, 2))[2:]
	return Bh

def rc(t):
	if t%255==0:
		return 1
	else:
		R = list('10000000')
		for i in range(1, t%255 + 1):
			R = list('0')+ R
			
			R[0] = bin(int(R[0],2) ^ int(R[8],2))[2:].zfill(len(R[0]))
			R[4] = bin(int(R[4],2) ^ int(R[8],2))[2:].zfill(len(R[4]))
			R[5] = bin(int(R[5],2) ^ int(R[8],2))[2:].zfill(len(R[5]))
			R[6] = bin(int(R[6],2) ^ int(R[8],2))[2:].zfill(len(R[6]))
			R = R[0:8]
			#print R
		return R[0]
def lo(ir):
	out = open('lotapreimage.txt','w') 
	M = Matrix()
	print M
	RC = list('00000000')
	l = int(log(8,2))
	for j in range(l+1):
		RC[(2**j) - 1] = rc(j+7*ir)

	m = Sha3Hex(M[0][0])
	#print RC, m
	s = ' '
	for z in range(8):
		print s, m[z]
		#m = Sha3Hex(M[0][0])
			#m1 = bin(int(m,2) ^ int(RC[z]))[2:].zfill(len(M[0][0]))
		m1 = bin(int(m[z],2) ^ int(RC[z],2))[2:]
		#m1 = bin(int(m1,2) ^ int(RC[z],2))[2:]
		#print s, m1
		s = s + m1
	print RC,m, s

	#print s, RC
		
	M[0][0] = BinTohex(s[::-1])
	A = np.array(M)
	for i in range(5):
		for j in range(5):
			s = A[j][i] + ' '
			out.write('{}'.format(s))
	out.write('{}'.format(s))
	out.close()
	return M

