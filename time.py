from timeit import default_timer as timer

L = [1,0,1,0,1]
T = []

for i in xrange(5):
	start = timer()
	if L[i]==1:
		x = i*i 
	end = timer()
	T.append(end - start)
print T