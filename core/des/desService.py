from core.des import desMod as des_mod
def getDataPoints(key,msg,msg2,rounds,block_size,seed,mask,padding):
	des_o = des_mod.DES_M(block_size,rounds,key,seed,0&mask)
	cypher , cypher_dash = des_o.encrypt(msg,padding)

	m , _ = des_o.decrypt(cypher,padding)

	des_o2 = des_mod.DES_M(block_size,rounds,key,seed,1&mask)
	cypher2 , cypher_dash2 = des_o2.encrypt(msg2,padding)
	# #For Graph
	x_points = [(i+1) for i in range(rounds)]
	y_points = []
	for i in range(rounds):
	    y_points.append(sum(des_o2.xor(cypher_dash[i],cypher_dash2[i])))

	return x_points,y_points


def runDes(key,block_size,rounds,txt,mode,padding,seed = 7):
	des_o = des_mod.DES_M(block_size,rounds,key,seed,0)
	if mode :
		res, res_ = des_o.encrypt(txt,padding)
		#convert the output to Hexadecimal
		# bin_arr = des_o.string_to_binary(res,8)
		# fin_res = ""
		# for i in range(0,len(bin_arr),4):
		# 	tmp = ""
		# 	for j in range(i,i+4,1):
		# 		tmp += str(j)
		# 	tmp = int(j,2)
		# 	fin_res += tmp < 10 ? str(tmp) : chr(ord('a')-10)
		# return fin_res, res_
	else:
		res, res_ = des_o.decrypt(txt,padding)
	return res ,res_

def getGraph(key,block_size,rounds,txt,mode,padding,seed = 7):
	blocks = [16,32,64]
	x_points = []
	y_points = []
	msg = txt
	msg2 = chr((ord(msg[0])+1)%256)
	for i in range(1,len(msg)):
		msg2 += msg[i]
	#Change in Key
	for i in blocks:
		x,y = getDataPoints(key,msg,msg2,rounds,i,seed,1,padding)
		x_points.append(x)
		y_points.append(y)
	# Change in plaintext
	for i in blocks:
		x,y = getDataPoints(key,msg,msg2,rounds,i,seed,0,padding)
		x_points.append(x)
		y_points.append(y)
	return x_points,y_points
