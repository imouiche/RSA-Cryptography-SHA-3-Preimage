""" Preimage of the Rho fuction in SHA-3"""

from __future__ import division
import numpy as np

def shift(l, n):
    return l[n:] + l[:n]
def Sha3Hex(n):
	num_of_bits = 8
	N = bin(int(n, 16))[2:].zfill(num_of_bits)
	#H = shift(N, 7)
	H = N[::-1]
	return H
def BinTohex(n):
	num_of_bits = 8
	Bh = hex(int(n, 2))[2:]
	return Bh


def Ro(w):

	M = [[0,36,3,105,210],[1,300,10,45,66],[190,6,171,15,253],[28,55,153,21,120],[91,276,231,136,78]]
	for i in range(5):
		for j in range(5):
			#print j
			M[i][j] = M[i][j]%w
			#M[i][j] = M[i][j]%w

	L = list(open("roout.txt", "r"))
	L = list(row.strip().split() for row in L) #remove all odd characters.
	out = open('Ropreimage1.txt','w') 
	j = 0
	s = ' '
	M = np.array(M)
	for y in range(5):
		for x in range(5):
			#print  M[x, y], M[x][y], L[0][j]
			el =L[0][j]
			HexToBin = Sha3Hex(el)
			Shift = shift(HexToBin, M[x][y])
			BintoHex1 = BinTohex(Shift[::-1])
			if len(BintoHex1)==1:
				BintoHex1 = '0'+ BintoHex1
				s = BintoHex1 + ' '
				out.write('{}'.format(s))
				print el,BintoHex1
				j +=1
			else:
			#BintoHex = BinTohex(Shift)

				s = BintoHex1 + ' '
				print el, BintoHex1
				out.write('{}'.format(s))
				j +=1
	out.close()

	return M
