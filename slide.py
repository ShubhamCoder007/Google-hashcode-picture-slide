
file = open("a.txt",'r+')
content = file.read()
content = content.splitlines()
file.close()

N = int(content[0])
content = [con+" photo"+str(i) for i,con in zip(range(0,N),content[1:]) ]

V = [i for i in content if i.startswith('V')]
H = [i for i in content if i.startswith('H')]

slide = []
taken = []
V_new = []

def generateV(V):
	V1 = []
	for i in range(0,len(V)):
		if i in taken:
			continue
		for j in range(1,len(V)):
			if j in taken:
				continue
			sr = similarity_ratio(V[i],V[j])
			if sr <= 0.7 and sr >= 0.2: 
				taken.append(i)
				taken.append(j)
				V1.append(fuseV(V[i],V[j]))
				
	return V1
			

def similarity_ratio(A, B):
	A = A.split()
	a = A[1]
	A = A[2:]
	B = B.split()
	b = B[1]
	B = B[2:]
	union = 0 
	inter = 0
	for i in A:
		if i in B:
			inter = inter + 1
		#if i not in B:
		#	union = union + 1
	union = int(a) + int(b) - int(inter)
	return inter/union
	
	
def combineV():
	for i in range(0,len(V)):
		for j in generateV(V):
			if j not in V_new:
				V_new.append(j)
		
	'''	
def fuse(v):
	for i in v:
		set = []
		a = i[0]
		b = i[1]
		a = a.split()
		b = b.split()
		for j in a:
			if j not in b:
				b.append(j)'''
				
		
def fuseV(A, B):
	A = A.split()
	B = B.split()
	b = B[2:-1]
	for i in A[2:-1]:
		if i not in b:
			b.append(i)
	count = len(b)
	s = "V "+str(count)
	for i in b:
		s = s + " "+ i 
	s = s + " " + A[-1] + " " + B[-1][5:]
	return s
		
		
		
def mergeSlides(H,V_new):
	return H + V_new
	
#V_new = [i for i in V_new if i != []]


def slide_generate(A, A_id, pics):
	t = [(0,0)]				# stores (min,id) pair; compare for min values if the coming is greater include
	A = A.split()
	Aset = A[2:int(A[1])+1]
	for i in range(0,len(pics)-1):
		if i is A_id:
			i = i + 1
		union = 0
		m = 0
		B = pics[i]
		B = B.split()
		Bset = B[2:int(B[1])+1]
		for j in Bset:
			if j in Aset:
				union = union + 1
		m = min(int(A[1]),int(B[1]),union)
		if t[-1][0] < m:
			t.append((m,i))
			
	print(t)
	B = pics[t[-1][1]]
	B = B.split()
	if len(t) > 1:
		if A[-1].startswith('photo'):
			slide.append(A[-1][5:])
		else:
			slide.append(A[-2][5:])
			slide.append(A[-1])
			
		if B[-1].startswith('photo'):
			slide.append(B[-1][5:])
		else:
			slide.append(B[-2][5:])
			slide.append(B[-1])
	
	else:
		#removing the used picture
		pics.remove(pics[A_id])
		pics.remove(pics[t[-1][1]])
		

def create_slides(pics):
	for i in range(0,len(pics)-1):
		slide_generate(pics[i],i,pics)
			
		


print(content)
print("\n")
print("\n")
combineV()
print("\n")
print(H,V,V_new,taken)
print("\n")

pics = mergeSlides(H,V_new)
create_slides(pics)
print("\n")

print(slide)
