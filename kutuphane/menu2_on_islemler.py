import numpy as np
import sys
import os
from kutuphane.melih_kutuphane import sinirla,boya
from kutuphane.menu1_dosya_islemleri import goruntu_oku,goruntu_bastir

def __rgb_gray_yontem(rgb):
    return sinirla(int((int(rgb[0])+int(rgb[1])+int(rgb[2]))/3.0))

def rgb2gray(goruntu):
    e,b,k=goruntu.shape
    yeni=np.zeros((e,b),dtype="uint8")

    for i in range(e):
        for j in range(b):
            yeni[i][j]=__rgb_gray_yontem(goruntu[i][j])

    return yeni

def gri_histogram_hesaplama(goruntu):
    grt = goruntu.copy()
    e, b = grt.shape
    histogram = {}
    for i in range(256):
        histogram[i] = 0
    for i in range(e):
        for j in range(b):
            histogram[grt[i][j]] += 1
    return histogram

def gri_histogram_esitleme(goruntu):
    grt = goruntu.copy()
    e, b = grt.shape
    histogram = gri_histogram_hesaplama(grt)
    kumulatif_toplam = {}
    ara_toplam = 0
    for i in range(len(histogram)):
        ara_toplam = histogram[i] + ara_toplam
        kumulatif_toplam[i] = ara_toplam
    for i in range(len(kumulatif_toplam)):
        kumulatif_toplam[i] = sinirla(int((kumulatif_toplam[i] / kumulatif_toplam[255]) * 255))

    return boya(grt, list(kumulatif_toplam.values()))

def kes(goruntu,x):
    x1, y1, x2, y2=x
    boyut=goruntu.shape
    e=boyut[0]
    b=boyut[1]

    if (y1!=y2 or x1!=x2) and (x1<e and x2 <e and x1>=0 and x2>=0 and y1<b and y2 <b and y1>=0 and y2>=0):
        return goruntu[x1:x2+1,y1:y2+1]

    return goruntu

def goruntu_boyutlandirma(goruntu,yeni_boyut):#en yakin komsu
    boyut=goruntu.shape
    e = boyut[0]
    b = boyut[1]
    e2,b2=yeni_boyut

    if len(boyut)==2:#gri
        yeni=np.zeros(yeni_boyut,dtype="uint8")
        for i in range(e2):
            for j in range(b2):
                yeni[i][j]=goruntu[int(i*e/e2)][int(j*b/b2)]

    else:#renkli
        yeni = np.zeros((e2,b2,3), dtype="uint8")
        for i in range(e2):
            for j in range(b2):
                yeni[i][j][0] = goruntu[int(i * e / e2)][int(j * b / b2)][0]
                yeni[i][j][1] = goruntu[int(i * e / e2)][int(j * b / b2)][1]
                yeni[i][j][2] = goruntu[int(i * e / e2)][int(j * b / b2)][2]

    return yeni