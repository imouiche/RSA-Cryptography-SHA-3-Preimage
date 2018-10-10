

def Matrix():
	L = list(open("theta.txt", "r"))
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

def Theta():
	M = Matrix()
	print M
	for y in range(5):
		for x in range(5):
			HexToBin1 = Sha3Hex(M[x][y])
			HexToBin2 = Sha3Hex(M[(x+1)%5][y])
			HexToBin3 = Sha3Hex(M[(x+2)%5][y])
			
	return M














