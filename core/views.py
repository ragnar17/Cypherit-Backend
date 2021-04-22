from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from core.paillier import paillier as pai
class CaeserCypherView(APIView):
    def post(self,request,*args,**kwargs):
        plainText = request.data.get('plainText')
        shift = request.data.get('shift')
        plainText = str(plainText)
        shift = int(shift)
        cipher = ""
        pFreq = [0]*26
        cFreq = [0]*26
        mxP = mxC = 1
        for i in plainText:
            if(ord(i) >= ord('a') and ord(i) <=ord('z')):
                tmp = (shift + ord(i)-ord('a'))%26
                tmp = (tmp+26)%26
                c = chr(ord('a')+tmp)
            elif(ord(i) >= ord('A') and ord(i) <=ord('Z')):
                tmp = (shift + ord(i)-ord('A'))%26
                tmp = (tmp+26)%26
                c = chr(ord('A')+tmp)
            else:
                cipher += i
                continue
            cipher += c
            c = chr(ord('a')+tmp)
            cur = i.lower()
            pFreq[ord(cur)-ord('a')]+=1
            cFreq[ord(c)-ord('a')]+=1
            mxC = max(mxC,cFreq[ord(c)-ord('a')])
            mxP = max(mxP,pFreq[ord(cur)-ord('a')])
        d = []
        for i in range(26):
            pFreq[i]/=mxP
            cFreq[i]/=mxC
            d.append({'name' : chr(ord('a')+i),'pFreq':pFreq[i],'cFreq':cFreq[i]})
        data = {
            'plainText' : plainText,
            'shift' : shift,
            'cipher' : cipher,
            'graphdata' : d
        }
        # data = {'n':'n'}
        return Response(data)
class PA0View(APIView):
    def post(self,request,*args,**kwargs):
        plainText = request.data.get('plainText')
        plainText = str(plainText)
        cipher = ""
        pFreq = [0]*26
        cFreq = [0]*26
        mxP = mxC = 1
        for i in plainText:

            if(ord(i) >= ord('a') and ord(i) <=ord('z')):
                tmp = (25 - ord(i)+ord('a'))%26
                tmp = (tmp+26)%26
                c = chr(ord('a')+tmp)
            elif(ord(i) >= ord('A') and ord(i) <=ord('Z')):
                tmp = (25 - ord(i)+ord('A'))%26
                tmp = (tmp+26)%26
                c = chr(ord('A')+tmp)
            else:
                cipher += i
                continue
            cipher += c
            c = chr(ord('a')+tmp)
            cur = i.lower()
            pFreq[ord(cur)-ord('a')]+=1
            cFreq[ord(c)-ord('a')]+=1
            mxC = max(mxC,cFreq[ord(c)-ord('a')])
            mxP = max(mxP,pFreq[ord(cur)-ord('a')])
        d = []
        for i in range(26):
            pFreq[i]/=mxP
            cFreq[i]/=mxC
            d.append({'name' : chr(ord('a')+i),'pFreq':pFreq[i],'cFreq':cFreq[i]})
        data = {
            'plainText' : plainText,
            'cipher' : cipher,
            'graphdata' : d
        }
        return Response(data)

class KeyGeneratorView(APIView):
    def post(self,request,*args,**kwargs):
        bits = request.data.get('bits')
        bits = int(bits)
        pr,pb = pai.generateKeypair(bits)
        data = {
            'pbn' : str(pb.n),
            'pbg' : str(pb.g),
            'prl' : str(pr.l),
            'prmu' : str(pr.mu)
        }
        return Response(data)

import cv2
import numpy as np
from core.paillier import encryptImage
from core.paillier import paillier
from core.paillier import floating_point as fp
class EncryptImageView(APIView):
    def post(self,request,*args,**kwargs):
        image = np.asarray(bytearray(request.data['myFile'].read()), dtype="uint8")
        image = cv2.imdecode(image,0)
        pbn = int(request.data['pbn'])
        pbg = int(request.data['pbg'])
        enc_img = encryptImage.encrypt(image,pbn,pbg)
        enc_json = encryptImage.toJson(enc_img)
        data = {
            "cipher" : enc_json
        }
        return Response(data)
import json
from django.http import HttpResponse
from core.paillier import decryptImage as dc
from django.http import FileResponse
from core.paillier import ImageOperations as ig
import base64
def get_data(request):
    data = json.loads(request.data['data'])
    data = data['cipher']
    enc_img = []
    n,m = len(data),len(data[0])
    for i in range(n):
        tmp = [0]*m
        for j in range(m):
            val = json.loads(data[i][j])
            tmp[j] = fp.FloatingPoint(int(val['mantissa']),int(val['exponent']))
        enc_img.append(tmp)
    pb = paillier.PublicKey(int(request.data['pbn']),int(request.data['pbg']))
    pr = paillier.PrivateKey(int(request.data['prl']),int(request.data['prmu']))

    return pr,pb,enc_img
class DecryptImageView(APIView):
    def post(self,request,*args,**kwargs):
        pr,pb,enc_img = get_data(request)
        omg = dc.decrypt(pr,pb,enc_img)
        omg = dc.convertToByte(omg)
        base64EncodedStr = base64.b64encode(omg)
        # print(base64EncodedStr)

        data = {
            "b64" : base64EncodedStr
        }
        return Response(data)

import pickle
import requests
class ImageIncreaseBrightness(APIView):
    def post(self,request,*args,**kwargs):
        pr,pb,enc_img = get_data(request)
        v = int(request.data['brightness'])
        out_img = ig.Secure_Image_Adjustment_Brightness_Control(enc_img,v,pb)

        # data = {
        # 	'enc_img' : enc_img,
        # 	'v' : v,
        # 	'pb' : pb
        # }
        # data2 = pickle.dumps(data,protocol=2)
        # url = "http://pailliercryptosystem.pythonanywhere.com/brightness_control"
        #
        # r = requests.post(url,data=data2)
        # out_img = pickle.loads(r.content)

        dec_img = dc.decrypt(pr,pb,out_img)
        out_json = encryptImage.toJson(out_img)
        omg = dc.convertToByte(dec_img)
        base64EncodedStr = base64.b64encode(omg)
        # data = {
        #     "cipher" : out_json,
        #     "b64" : base64EncodedStr
        # }
        data = {
            "b64" : base64EncodedStr
        }
        return Response(data)
class ImageNegation(APIView):
    def post(self,request,*args,**kwargs):
        pr,pb,enc_img = get_data(request)
        v = int(request.data['negation'])
        if v:
            out_img = ig.Secure_Image_Adjustment_Image_negation(enc_img,255,pb)
        else:
            out_img = enc_img
        dec_img = dc.decrypt(pr,pb,out_img)
        omg = dc.convertToByte(dec_img)
        base64EncodedStr = base64.b64encode(omg)

        data = {
            "b64" : base64EncodedStr
        }
        return Response(data)
class ImageBlur(APIView):
    def post(self,request,*args,**kwargs):
        pr,pb,enc_img = get_data(request)
        v = int(request.data['blur'])
        out_img = ig.Secure_Noise_Reduction_LPF(enc_img,v,v,pb)

        dec_img = dc.decrypt(pr,pb,out_img)
        omg = dc.convertToByte(dec_img)
        base64EncodedStr = base64.b64encode(omg)

        data = {
            "b64" : base64EncodedStr
        }
        return Response(data)
import copy
import math
class ImageEdgeDetect(APIView):
    def post(self,request,*args,**kwargs):
        pr,pb,enc_img = get_data(request)
        kerX = [[1,0,-1],[2,0,-2],[1,0,-1]]
        kerY = [[1,2,1],[0,0,0],[-1,-2,-1]]

        out_img1 = ig.sobelOperator(enc_img,kerX,pb)
        out_img2 = ig.sobelOperator(enc_img,kerY,pb)

        dec_img1 = dc.decrypt(pr,pb,out_img1)
        dec_img2 = dc.decrypt(pr,pb,out_img2)
        dec_img = copy.deepcopy(dec_img1)
        n,m = len(dec_img),len(dec_img[0])
        for i in range(n):
            for j in range(n):
                dec_img[i][j] = max(0,min(255,int(math.sqrt(dec_img1[i][j]**2+dec_img2[i][j]**2))))

        omg = dc.convertToByte(dec_img)
        base64EncodedStr = base64.b64encode(omg)

        data = {
            "b64" : base64EncodedStr
        }
        return Response(data)

from core.des import desService as desService
class Des(APIView):
    def post(self,request,*args,**kwargs):
        rounds = int(request.data["rounds"])
        block_size = int(request.data["blockSize"])
        txt = request.data["txt"]
        key = request.data["key"]
        mode = request.data["mode"]
        seed = int(request.data["seed"])
        padding = int(request.data["padding"])
        res, res_ = desService.runDes(key,block_size,rounds,txt,mode,padding,seed)

        data = {
            "txt" : res
        }
        return Response(data)
class DesAvalanche(APIView):
    def post(self,request,*args,**kwargs):
        rounds = int(request.data["rounds"])
        block_size = int(request.data["blockSize"])
        txt = request.data["txt"]
        key = request.data["key"]
        mode = request.data["mode"]
        seed = int(request.data["seed"])
        padding = int(request.data["padding"])
        x,y = desService.getGraph(key,block_size,rounds,txt,mode,padding,seed)
        d = []

        for i in range(rounds):
            d.append({"name":i+1,
                        "For Change in Key with Block-Size 16":y[0][i],
                        "For Change in Key with Block-Size 32":y[1][i],
                        "For Change in Key with Block-Size 64":y[2][i],
                        "For Change in text with Block-Size 16":y[3][i],
                        "For Change in text with Block-Size 32":y[4][i],
                        "For Change in text with Block-Size 64":y[5][i],})

        data = {
            "graphdata" : d
        }

        return Response(data)
# def test_view(request):
#     print(request)
#     data = {
#         'name':'Amit'
#     }
#     return JsonResponse(data)
