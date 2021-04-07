import numpy as np
from core.paillier import floating_point as fp
from core.paillier import paillier as pai
def encrypt(img,pbn,pbg):
	pb = pai.PublicKey(pbn,pbg)
	print(pb)
	enc_img = []
	n,m = len(img),len(img[0])

	for i in range(n):
		enc_img.append([0]*m)
		for j in range(m):
			enc_img[i][j] = fp.encryptFP(pb,int(img[i][j]))

	return enc_img

def toJson(img):
	n,m = len(img),len(img[0])
	data = []
	for i in range(n):
		data.append([0]*m)
		for j in range(m):
			data[i][j] = img[i][j].to_json()
	return data
