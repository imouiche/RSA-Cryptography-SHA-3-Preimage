from __future__ import division
import numpy as np


def shift(l, n):
    return l[n:] + l[:n]

def Matrix():
	L = list(open("Pi-image.txt", "r"))
	#L = list(open("Pi.txt1", "r"))
	L = list(row.strip().split() for row in L) #remove all odd characters.
	M= [[0 for x in range(5)] for y in range(5)]
	j = 0
	for y in range(5):
		for x in range(5):
			M[x][y] = L[0][j]
			j +=1
	return M

def pi():
	A= [[0 for x in range(5)] for y in range(5)]
	out = open('Pipreimage.txt','w') 
	M = Matrix()
	for  y in range(5):
		for x in range(5):
			# s1 = (y-3*x)%5
			# s2 = y
			s1 = (y-3*x)%5
			s2 = y
			# print s1, s2
			# if s2!=0 and (s2 < 5) and (s1!=0) and (s1 <5):
			# 	s1 = modular_inv(s1,5)
			# 	s2 = modular_inv(s2,5)
			# 	A[x][y] = M[s1][s2]
			# else:

			# 	print s1, s2
			A[x][y] = M[s2][s1]
	A = np.array(A)
	for i in range(5):
		A[:,i] = shift(A[:,i].tolist(), i)
	for i in range(5):
		for j in range(5):
			s = A[j][i] + ' '
			out.write('{}'.format(s))

	out.close()
	return A
