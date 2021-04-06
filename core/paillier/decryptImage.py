import numpy as np
from core.paillier import floating_point as fp
from core.paillier import paillier as pai
import cv2

def decrypt(pr,pb,enc_img):
    n,m = len(enc_img),len(enc_img[0])
    img = np.zeros([n,m],dtype=np.uint8)
    for i in range(n):
        for j in range(m):
            img[i][j] = max(0,min(255,fp.getValue(pr,pb,enc_img[i][j])))
    # cv2.imwrite("hello.png", img)
    return img

def convertToByte(img):
    success, encoded_image = cv2.imencode('.png', img)
    content = encoded_image.tobytes()
    return content
