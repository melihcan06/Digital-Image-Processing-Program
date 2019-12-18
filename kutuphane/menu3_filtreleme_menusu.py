import numpy as np
import matplotlib.pyplot as plt
from math import log10, sqrt
from kutuphane.melih_kutuphane import topla,sinirla,boya,PREWITT_DIKEY,PREWITT_YATAY,ORTALAMA_FILTRE,padding_sayisi_hesaplama,LAPLAS_FILTRE1,LAPLAS_FILTRE2,LAPLAS_FILTRE3,LAPLAS_FILTRE4,sinirla_matris
from kutuphane.menu2_on_islemler import gri_histogram_esitleme
import kutuphane.melih_kutuphane as mk
def zero_padding(grt, padding_sayisi=(1,1)):
    yeni = np.zeros((grt.shape[0] + padding_sayisi[0] * 2, grt.shape[1] + padding_sayisi[1] * 2), dtype=np.uint8)
    m = padding_sayisi[0]
    for i in range(grt.shape[0]):
        n = padding_sayisi[1]
        for j in range(grt.shape[1]):
            yeni[m][n] = grt[i][j]
            n += 1
        m += 1
    return yeni

def konvolusyon(goruntu, filtre, padding_sayisi=(0,0)):  # filtreler m = tek sayi mxm olmak zorundadir,stride kaydirma ekle
    grt = goruntu.copy()
    f_en, f_boy = filtre.shape
    kaydirma = 1  # stride

    yeni_en, yeni_boy = (int(((grt.shape[0] - f_en + (2 * padding_sayisi[0])) / kaydirma) + 1),
                         int(((grt.shape[1] - f_boy + (2 * padding_sayisi[1])) / kaydirma) + 1))
    if padding_sayisi != (0,0):#padding yapilacak
        grt = zero_padding(grt, padding_sayisi)

    e, b = grt.shape
    yeni = np.ones((yeni_en, yeni_boy), dtype="uint8")

    baslangic_x = int(f_en / 2)
    bitis_x = e - baslangic_x
    baslangic_y = int(f_boy / 2)
    bitis_y = b - baslangic_y

    i_y = 0
    for i in range(baslangic_x, bitis_x, kaydirma):  # merkez noktalardan ilerleniyor!
        j_y = 0
        for j in range(baslangic_y, bitis_y, kaydirma):
            x = grt[i - baslangic_x:i + baslangic_x + 1, j - baslangic_y:j + baslangic_y + 1]
            yeni[i_y][j_y] = sinirla(mk.sum(mk.multiply(x, filtre)))
            j_y += 1
        i_y += 1

    return yeni

def laplas_icin_konvolusyon(goruntu, filtre, padding_sayisi=(0,0)):  # laplas ta - li degerler lazim burda sinirlama yapmiyoruz
    grt = goruntu.copy()
    f_en, f_boy = filtre.shape
    kaydirma = 1  # stride

    yeni_en, yeni_boy = (int(((grt.shape[0] - f_en + (2 * padding_sayisi[0])) / kaydirma) + 1),
                         int(((grt.shape[1] - f_boy + (2 * padding_sayisi[1])) / kaydirma) + 1))
    if padding_sayisi != (0,0):#padding yapilacak
        grt = zero_padding(grt, padding_sayisi)

    e, b = grt.shape
    yeni = np.ones((yeni_en, yeni_boy), dtype=np.float)

    baslangic_x = int(f_en / 2)
    bitis_x = e - baslangic_x
    baslangic_y = int(f_boy / 2)
    bitis_y = b - baslangic_y

    i_y = 0
    for i in range(baslangic_x, bitis_x, kaydirma):  # merkez noktalardan ilerleniyor!
        j_y = 0
        for j in range(baslangic_y, bitis_y, kaydirma):
            x = grt[i - baslangic_x:i + baslangic_x + 1, j - baslangic_y:j + baslangic_y + 1]
            yeni[i_y][j_y] = mk.sum(mk.multiply(x, filtre))
            j_y += 1
        i_y += 1

    return yeni

def siralama_filtreleri(goruntu, filtre_boyutu, padding_sayisi=(0,0), tur="ortanca"):
    grt = goruntu.copy()
    f_en, f_boy = filtre_boyutu
    kaydirma = 1  # stride

    yeni_en, yeni_boy = (int(((grt.shape[0] - f_en + (2 * padding_sayisi[0])) / kaydirma) + 1),
                         int(((grt.shape[1] - f_boy + (2 * padding_sayisi[1])) / kaydirma) + 1))
    if padding_sayisi != (0,0):
        grt = zero_padding(grt, padding_sayisi)

    e, b = grt.shape
    yeni = np.ones((yeni_en, yeni_boy), dtype="uint8")

    baslangic_x = int(f_en / 2)
    bitis_x = e - baslangic_x
    baslangic_y = int(f_boy / 2)
    bitis_y = b - baslangic_y

    i_y = 0
    for i in range(baslangic_x, bitis_x, kaydirma):  # merkez noktalardan ilerleniyor!
        j_y = 0
        for j in range(baslangic_y, bitis_y, kaydirma):
            x = grt[i - baslangic_x:i + baslangic_x + 1, j - baslangic_y:j + baslangic_y + 1]
            if tur == "ortanca":
                yeni[i_y][j_y] = mk.median(x)
            elif tur == "max":
                yeni[i_y][j_y] = mk.max(x)
            elif tur == "min":
                yeni[i_y][j_y] = mk.min(x)
            j_y += 1
        i_y += 1

    return yeni

def min_filtresi(goruntu, filtre_boyutu=(3,3), padding_sayisi=(0,0)):
    return siralama_filtreleri(goruntu, filtre_boyutu, padding_sayisi, "min")

def max_filtresi(goruntu, filtre_boyutu=(3,3), padding_sayisi=(0,0)):
    return siralama_filtreleri(goruntu, filtre_boyutu, padding_sayisi, "max")

def ortanca_maskeleme(goruntu, filtre_boyutu=(3,3), padding_sayisi=(0,0)):
    return siralama_filtreleri(goruntu, filtre_boyutu, padding_sayisi, "ortanca")

def ortalama_maskeleme(goruntu, filtre=ORTALAMA_FILTRE, padding_sayisi=(0,0)):
    grt = goruntu.copy()
    return konvolusyon(grt, filtre, padding_sayisi)

"""def padding_sayisi_hesaplama(grt,filtre_boyutu,kaydirma=1):#melih kutuphanede var
    return (int((((grt.shape[0] - 1) * kaydirma) + filtre_boyutu[0] - grt.shape[0]) / 2),
                      int((((grt.shape[1] - 1) * kaydirma) + filtre_boyutu[1] - grt.shape[1]) / 2))"""

def keskin_olmayan_maskeleme(goruntu, bulaniklastirma_metodu='ortanca_filtresi', filtre_boyutu=(5,5),filtre=ORTALAMA_FILTRE,kaydirma=1):
    grt=goruntu.copy()

    if bulaniklastirma_metodu == "ortalama_filtresi":
        padding_sayisi = padding_sayisi_hesaplama(grt, filtre.shape)
        bulanik = ortalama_maskeleme(grt.copy(), filtre, padding_sayisi)

    elif bulaniklastirma_metodu == "ortanca_filtresi":
        padding_sayisi = padding_sayisi_hesaplama(grt, filtre_boyutu)
        bulanik = ortanca_maskeleme(grt.copy(), filtre_boyutu, padding_sayisi)

    k = 1
    yeni = np.zeros((grt.shape[0], grt.shape[1]), dtype=np.uint8)

    for i in range(grt.shape[0]):
        for j in range(grt.shape[1]):
            b = np.int64(grt[i][j]) - np.int64(bulanik[i][j])
            b *= k
            b += np.uint8(grt[i][j])
            yeni[i][j] = sinirla(b)

    return yeni

def prewitt_kenar_bul(goruntu, padding_sayisi=(1,1)):
    grt = goruntu.copy()
    dikey = konvolusyon(grt, PREWITT_DIKEY, padding_sayisi)
    yatay = konvolusyon(grt, PREWITT_YATAY, padding_sayisi)
    yeni = np.zeros(dikey.shape, dtype="uint8")
    e, b = yeni.shape

    x = 0.1
    for i in range(e):
        for j in range(b):
            x = (yatay[i][j] ** 2 + dikey[i][j] ** 2) ** (1 / 2)
            yeni[i][j] = sinirla(x)

    return yeni

def olcekleme(goruntu):
    grt = goruntu.copy()
    e, b = grt.shape

    ek=mk.min(grt)

    yeni=np.zeros((e,b),dtype="float32")

    for i in range(e):
        for j in range(b):
            yeni[i][j]=grt[i][j]-ek

    eb=mk.max(yeni)

    sc=255.0/eb
    for i in range(e):
        for j in range(b):
            yeni[i][j]*=sc

    x=sinirla_matris(yeni)
    return x

def laplas_keskinlestirme(goruntu, filtre=LAPLAS_FILTRE3, yumusatma_filtre_boyutu=(7,7)):
    grt=goruntu.copy()
    padding_sayisi = padding_sayisi_hesaplama(grt,yumusatma_filtre_boyutu)
    grt=ortanca_maskeleme(grt,yumusatma_filtre_boyutu,padding_sayisi)
    padding_sayisi = padding_sayisi_hesaplama(grt,filtre.shape)
    x=laplas_icin_konvolusyon(grt,filtre,padding_sayisi)
    y=olcekleme(x)
    y=topla(goruntu,y)
    return olcekleme(y)#60-200 arasi histg. esitleme yap