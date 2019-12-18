import numpy as np

SB_BEYAZ = 1#255 ten 1 e aldim
SB_SIYAH = 0

PREWITT_DIKEY = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
PREWITT_YATAY = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])

ORTALAMA_FILTRE = np.ones((3, 3)) / 9.0
ORTALAMA_FILTRE2 = np.ones((9, 9)) / 81.0
AGIRLIKLI_ORTALAMA_FILTRE = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]]) / 16.0

LAPLAS_FILTRE1 = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
LAPLAS_FILTRE2 = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])
LAPLAS_FILTRE3 = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])
LAPLAS_FILTRE4 = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])

YAPISAL_ELEMAN_ARTI = np.array([[0, SB_BEYAZ, 0], [SB_BEYAZ, SB_BEYAZ, SB_BEYAZ], [0, SB_BEYAZ, 0]], dtype="uint8")
YAPISAL_ELEMAN_KARE = np.array([[SB_BEYAZ,SB_BEYAZ, SB_BEYAZ], [SB_BEYAZ, SB_BEYAZ, SB_BEYAZ], [SB_BEYAZ, SB_BEYAZ, SB_BEYAZ]], dtype="uint8")

def sinirla_matris(grt):
    e,b=grt.shape
    yeni=np.zeros((e,b),dtype="uint8")

    for i in range(e):
        for j in range(b):
            yeni[i][j]=sinirla(grt[i][j])

    return yeni

def sinirla_dizi(grt):
    yeni = []
    for i in range(len(grt)):
        x = grt[i]
        if x > 255:
            x = 255
        elif x < 0:
            x = 0
        yeni.append(np.uint8(x))
    yeni = np.array(yeni, dtype=np.uint8)
    return yeni

def sinirla(x):
    if x > 255:
        x = 255
    elif x < 0:
        x = 0
    return np.uint8(x)

def boya(grt2, renkler):#gri resimler icin
    grt = grt2.copy()
    for i in range(grt.shape[0]):
        for j in range(grt.shape[1]):
            grt[i][j] = sinirla(renkler[grt[i][j]])

    return grt

import matplotlib.pyplot as plt
def histogram_cizdir(histogram):
    histo=[]
    for i in histogram.values():
        histo.append(i)
    plt.plot(range(0,256),histo)
    plt.show()

def griyi_renkliye_boya(grt2,renkler):
    grt = grt2.copy()
    e,b=grt.shape
    yeni=np.zeros((e,b,3),dtype="uint8")
    for i in range(e):
        for j in range(b):
            yeni[i][j][0] = sinirla(renkler[grt[i][j]][0])
            yeni[i][j][1] = sinirla(renkler[grt[i][j]][1])
            yeni[i][j][2] = sinirla(renkler[grt[i][j]][2])

    return yeni

def ortalama_filtre_olustur(boyut):
    x = np.ones(boyut) / (boyut[0]*boyut[1])
    return x

def sb_ters_alma(goruntu):
    grt = goruntu.copy()
    e, b = grt.shape
    for i in range(e):
        for j in range(b):
            if grt[i][j] == SB_BEYAZ:
                grt[i][j] = SB_SIYAH
            else:
                grt[i][j] = SB_BEYAZ
    return grt

def gri_ters_alma(goruntu):
    grt = goruntu.copy()

    for i in range(grt.shape[0]):
        for j in range(grt.shape[1]):
            grt[i][j] = 255 - grt[i][j]
    return grt

def gri_sb_cevir(goruntu, esik=127):
    grt = goruntu.copy()
    e, b = grt.shape
    for i in range(e):
        for j in range(b):
            if grt[i][j] <= esik:
                grt[i][j] = SB_SIYAH
            else:
                grt[i][j] = SB_BEYAZ
    return grt

def gri_sb_cevir_2esik(goruntu, esik1=80, esik2=160):
    grt = goruntu.copy()
    e, b = grt.shape
    for i in range(e):
        for j in range(b):
            if grt[i][j] < esik1:
                grt[i][j] = SB_SIYAH
            elif grt[i][j] > esik2:
                grt[i][j] = SB_SIYAH
            else:
                grt[i][j] = SB_BEYAZ
    return grt

def sb_griye_olcekle(goruntu):
    grt=goruntu.copy()
    e,b=grt.shape
    for i in range(e):
        for j in range(b):
            if grt[i][j] == SB_SIYAH:
                grt[i][j] = 0
            elif grt[i][j] == SB_BEYAZ:
                grt[i][j] = 255
    return grt

def topla(goruntu1, goruntu2):
    e, b = goruntu1.shape
    yeni = np.zeros((e, b), dtype=np.float)

    for i in range(e):
        for j in range(b):
            yeni[i][j] = float(goruntu1[i][j]) + float(goruntu2[i][j])

    return yeni

def bitsel_ve(goruntu1, goruntu2):
    e, b = goruntu1.shape
    yeni = np.zeros((e, b), dtype="uint8")

    for i in range(e):
        for j in range(b):
            yeni[i][j] = goruntu1[i][j] & goruntu2[i][j]

    return yeni

def bitsel_veya(goruntu1, goruntu2):
    e,b=goruntu1.shape
    yeni=np.zeros((e,b),dtype="uint8")

    for i in range(e):
        for j in range(b):
            yeni[i][j]=goruntu1[i][j]|goruntu2[i][j]

    return yeni

def padding_sayisi_hesaplama(grt,filtre_boyutu,kaydirma=1):#grt nun boyutlarini alsam yeterliydi aslinda :(
    return (int((((grt.shape[0] - 1) * kaydirma) + filtre_boyutu[0] - grt.shape[0]) / 2),
                      int((((grt.shape[1] - 1) * kaydirma) + filtre_boyutu[1] - grt.shape[1]) / 2))

def padding_sayisi_hesaplama2(x,filtre_boyutu,kaydirma=1):
    en,boy=x
    return (int((((en - 1) * kaydirma) + filtre_boyutu[0] - en) / 2),
                      int((((boy - 1) * kaydirma) + filtre_boyutu[1] - boy) / 2))
def multiply(x,filtre):#gri goruntude
    e,b=x.shape
    yeni=np.zeros((e,b),dtype="uint8")
    for i in range(e):
        for j in range(b):
            yeni[i][j]=x[i][j]*filtre[i][j]
    return yeni

def sum(x):#gri goruntude
    e, b = x.shape
    yeni = 0
    for i in range(e):
        for j in range(b):
            yeni += x[i][j]
    return yeni

def median(x):#gri goruntude
    e, b = x.shape
    yeni = []

    for i in range(e):
        for j in range(b):
            yeni.append(x[i][j])

    for i in range(len(yeni)):
        for j in range(len(yeni)-1):
            if yeni[j]>yeni[j+1]:
                g=yeni[j+1]
                yeni[j+1]=yeni[j]
                yeni[j]=g

    return yeni[int(len(yeni)/2)]

def max(x):#gri goruntude
    e, b = x.shape
    eb=x[0][0]
    for i in range(e):
        for j in range(b):
            if x[i][j] > eb:
                eb=x[i][j]
    return eb

def min(x):#gri goruntude
    e, b = x.shape
    ek = x[0][0]
    for i in range(e):
        for j in range(b):
            if x[i][j] < ek:
                ek = x[i][j]
    return ek