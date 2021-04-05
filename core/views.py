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
            if(i == " "):
                cipher += i
                continue
            if(ord(i) >= ord('a') and ord(i) <=ord('z')):
                tmp = (shift + ord(i)-ord('a'))%26
                tmp = (tmp+26)%26
                c = chr(ord('a')+tmp)
            else:
                tmp = (shift + ord(i)-ord('A'))%26
                tmp = (tmp+26)%26
                c = chr(ord('A')+tmp)
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
        shift = request.data.get('shift')
        plainText = str(plainText)
        shift = int(shift)
        cipher = ""
        pFreq = [0]*26
        cFreq = [0]*26
        mxP = mxC = 1
        for i in plainText:
            if(i == " "):
                cipher += i
                continue
            if(ord(i) >= ord('a') and ord(i) <=ord('z')):
                tmp = (shift - ord(i)+ord('a'))%26
                tmp = (tmp+26)%26
                c = chr(ord('a')+tmp)
            else:
                tmp = (shift - ord(i)+ord('A'))%26
                tmp = (tmp+26)%26
                c = chr(ord('A')+tmp)
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
# def test_view(request):
#     print(request)
#     data = {
#         'name':'Amit'
#     }
#     return JsonResponse(data)
