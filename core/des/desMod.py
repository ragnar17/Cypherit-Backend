class DES_M:

    def __init__(self,block_size,rounds,key,seed,mask = 0):
        self.block_size = block_size
        self.rounds = rounds
        self.seed = seed
        from core.des import spBoxesGenerator as gen
        self.boxes = gen.ESP_BOX_Generator(block_size,seed)
        self.mask = mask

        self.keys = self.generate_keys(key,rounds,block_size)

    def char_to_binary(self,x,sz):
        return self.num_to_binary(ord(x),sz)

    def num_to_binary(self,x,sz):
        res = bin(x)[2:]
        while len(res) < sz :
            res = '0' + res

        return res

    def string_to_binary(self,s,sz):
        res = ""
        for i in s:
            res += self.char_to_binary(i,sz)
        arr = [int(i) for i in res]
        return arr

    def bit_array_to_string(self,arr):
        #split into group of 8
        arr = self.split_array(arr,8)
        fin = ""
        for block in arr:
            block = [str(x) for x in block]
            block = ''.join(block)
            fin += chr(int(block,2))
        return fin

    def permutation(self,arr,box):
        return [arr[i-1] for i in box]

    def expand(self,arr,box):
        return [arr[i-1] for i in box]

    def split_array(self,arr,x):
        return [arr[i:i+x] for i in range(0,len(arr),x)]

    def left_shift(self,arr,x):
        return arr[x:] + arr[:x]

    def xor(self,arr1,arr2):
        return [(arr1[i]^arr2[i]) for i in range(len(arr1))]

    def substitution(self,arr):
        arr = self.split_array(arr,6)
        fin = []
        for i in range(len(arr)):
            row = int(str(arr[i][0])+str(arr[i][5]),2)
            col = int(''.join([str(i) for i in arr[i][1:5]]),2)

            s_ij = self.boxes.S_BOX[i][row][col]
            s_ij = self.num_to_binary(s_ij,4)

            s_ij = [int(i) for i in s_ij]

            fin.extend(s_ij)
        return fin

    def generate_keys(self,key,no_of_keys,key_size):
        keys = []
        if(len(key) < key_size//8):
            raise "Key length should be atleast "+str(key_size//8)
        key = key[:key_size//8]
        key_arr = self.string_to_binary(key,8)
        if self.mask:
            import random
            random.seed(self.seed)
            key_arr[random.randint(0,len(key_arr))] ^= 1

        key = self.permutation(key_arr,self.boxes.PC_1)
        tmp = self.split_array(key,(key_size-key_size//8)//2)
        c0,d0 = tmp[0], tmp[1]
        for i in range(no_of_keys):
            c0,d0 = self.left_shift(c0,self.boxes.SHIFT[i]) , self.left_shift(d0,self.boxes.SHIFT[i])
            keys.append(self.permutation(c0+d0,self.boxes.PC_2))
        return keys

    def DEA(self,text,keys):
        blocks = self.split_array(text,self.block_size//8)

        cryp = []

        #Stores the result after every round
        cryp_inter = [[] for i in range(self.rounds)]

        for block in blocks:
            block = self.string_to_binary(block,8)

            #Apply Intial Permuatation
            block = self.permutation(block,self.boxes.IP)

            #Split the block in two halves
            L,R = self.split_array(block,self.block_size//2)

            for i in range(self.rounds):
                #Expand the right half to 48 bits
                R_dash = self.expand(R,self.boxes.E)

                #Take Xor of block bits with key
                R_dash = self.xor(keys[i],R_dash)

                #S-box
                R_dash = self.substitution(R_dash)

                R_dash = self.permutation(R_dash,self.boxes.P)


                R_dash = self.xor(R_dash,L)

                L = R
                R = R_dash

                cryp_inter[i].extend(self.permutation(R+L,self.boxes.IP_dash))
            tmp = R + L

            tmp = self.permutation(tmp,self.boxes.IP_dash)
            cryp.extend(tmp)

        cryp = self.bit_array_to_string(cryp)
        return cryp , cryp_inter

    def encrypt(self,msg,padding = 1):
        #Add Padding
        if padding :
            pad_l = 8 - len(msg)%8
            pad = str(chr(ord('0')+pad_l))*pad_l
            msg = msg + pad

        return self.DEA(msg,self.keys)

    def decrypt(self,c,padding = 1):
        pad_l = 0
        m , m_inter = self.DEA(c,list(reversed(self.keys)))
        if padding :
            pad_l = int(m[-1])
        return m[:len(m)-pad_l], m_inter



#-------------Set Rounds and Block Size-----------------#

rounds = 16
block_size = 64
seed = 20
#-------------------------------------------------------#


#-------------Set Plaintext and Secret key-----------------#

msg = "Hell"
secret_key = "aecret_k"

#-------------------------------------------------------#

# des object
# des_o = DES_M(block_size,rounds,secret_key,seed)
# cypher , cypher_dash = des_o.encrypt(msg)

# print("Encrypt : %r" %cypher)

# m , _ = des_o.decrypt(cypher)
# print("Decrypt :",m)
