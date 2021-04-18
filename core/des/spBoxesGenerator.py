import random

#Cryptographer Dhruv > > Cryptographer Bharat

def random_shuffle(iter,arr):
	sz = len(arr)
	for i in range(iter):
		x = random.randint(0,sz)%sz
		y = random.randint(0,sz)%sz
		arr[x],arr[y] = arr[y],arr[x]
	return arr

def create_array(n):
	return random_shuffle(50,[i+1 for i in range(n)])

def create_permutation(arr,dont_take):
	for i in dont_take:
		arr.remove(i)
	return arr

def inverse_permutation(arr):
	tmp = [0]*len(arr)
	for i in range(len(arr)):
		tmp[arr[i]-1] = i+1
	return tmp
class ESP_BOX_Generator:
	
	def __init__(self,block_size,seed):
		random.seed(seed)
		self.seed = seed
		self.block_size = block_size
		self.run()

	def run(self):
		ignored = self.block_size//8
		self.PC_1 = create_permutation(create_array(self.block_size),create_array(ignored))

		self.PC_2 = create_permutation(create_array(self.block_size-ignored),create_array(ignored))

		#Intial Permutation and Inverse Permuation
		self.IP = create_permutation(create_array(self.block_size),[])
	
		self.IP_dash = inverse_permutation(self.IP)

		self.S_BOX = []
		for i in range(self.block_size//8):
			tmp = [x for x in range(16)]
			s_tmp = []
			for j in range(4):
				s_tmp.append(random_shuffle(50,tmp))
			self.S_BOX.append(s_tmp)
		
		#P-Box which shuflles the 32bit block
		self.P = create_permutation(create_array(self.block_size//2),[])

		#Expansion Box
		E_tmp = [i+1 for i in range(self.block_size//2)]
		self.E = []
		for i in range(0,len(E_tmp),4):
			self.E.append(E_tmp[i-1])
			for j in range(i,i+4,1):
				self.E.append(E_tmp[j])
			self.E.append(E_tmp[(i+4)%len(E_tmp)])

		#Matrix that determine the shift for each round of keys
		self.SHIFT = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]


	def printBoxes(self):
		print("PC_1 =",self.PC_1)
		print("PC_2 =",self.PC_2)

		
		print("IP =",self.IP)

		
		print("IP_dash =",self.IP_dash)


		print("S_BOX =",self.S_BOX)

		
		print("P =",self.P)

		
		print("E =",self.E)

# e = ESP_BOX_Generator(16,20)
# e.run()
# e.printBoxes()