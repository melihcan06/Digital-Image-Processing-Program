import numpy as np
from kutuphane.melih_kutuphane import sinirla, SB_BEYAZ, SB_SIYAH, gri_sb_cevir, sb_griye_olcekle, \
    boya, \
    YAPISAL_ELEMAN_ARTI, griyi_renkliye_boya
import math
from kutuphane.menu2_on_islemler import gri_histogram_hesaplama


# kabul=beyaz nesne siyah arka plan

def dolas(goruntu, yeni, nesne_id, i, j):
    e, b = goruntu.shape
    if i > 0 and goruntu[i - 1][j] == SB_BEYAZ and yeni[i - 1][j] == SB_SIYAH:  # sol
        yeni[i - 1][j] = nesne_id
        yeni = dolas(goruntu, yeni, nesne_id, i - 1, j)
    if i < e - 1 and goruntu[i + 1][j] == SB_BEYAZ and yeni[i + 1][j] == SB_SIYAH:  # sag
        yeni[i + 1][j] = nesne_id
        yeni = dolas(goruntu, yeni, nesne_id, i + 1, j)
    if j > 0 and goruntu[i][j - 1] == SB_BEYAZ and yeni[i][j - 1] == SB_SIYAH:  # yukari
        yeni[i][j - 1] = nesne_id
        yeni = dolas(goruntu, yeni, nesne_id, i, j - 1)
    if j < b - 1 and goruntu[i][j + 1] == SB_BEYAZ and yeni[i][j + 1] == SB_SIYAH:  # asagi
        yeni[i][j + 1] = nesne_id
        yeni = dolas(goruntu, yeni, nesne_id, i, j + 1)

    return yeni


def sb_dortlu_komsuluk2(goruntu):  # nesne id lerine boyaniyorlar, buyuk resimlerde calismiyordu, ilk yaptigim
    grt = goruntu.copy()
    e, b = grt.shape
    yeni = np.zeros((e, b), dtype="uint8")
    nesne_id = 1

    # her nesne bir id adresine atanir 1,2,3... dolayisiyla resim sb olmaktan cikar
    for i in range(e):
        for j in range(b):
            if grt[i][j] == SB_BEYAZ and yeni[i][j] == SB_SIYAH:
                yeni[i][j] = nesne_id
                yeni = dolas(grt, yeni, nesne_id, i, j)
                nesne_id += 1

    # kendimce olcekleme yapiyorum
    if nesne_id == 1:  # 256/0 i engellemek icin
        bolum_miktari = 1
    else:
        bolum_miktari = (nesne_id - 1)
    artis_miktari = int(256 / bolum_miktari)
    renkler = [0 for i in range(256)]
    for i in range(nesne_id + 1):
        renkler[i] = i * artis_miktari
    yeni = boya(yeni, renkler)

    return yeni


class k_means:  # centroid calisiyor medoid degil

    def __baslangic_kume_merkezi_ata(self, resim_turu, k, atama_turu):
        if atama_turu == 'bolerek':
            if resim_turu == 'gri':
                birim = int(256 / (k + 1))
                return [i * birim for i in range(1, k + 1)]
            if resim_turu == 'renkli':
                birim = int(256 / (k + 1))
                r = np.array([i * birim for i in range(1, k + 1)])
                g = np.array([i * birim for i in range(1, k + 1)])
                b = np.array([i * birim for i in range(1, k + 1)])
                merkezler = []
                for i in range(k):
                    merkezler.append([r[i], g[i], b[i]])
                return merkezler

        if atama_turu == 'rastgele':
            if resim_turu == 'gri':
                merkezler = []
                x = np.random.randint(0, 255, k)
                for i in x:
                    merkezler.append(x)
                return merkezler
            if resim_turu == 'renkli':
                merkezler = []
                for i in range(k):
                    x = np.random.randint(0, 255, 3)
                    merkezler.append([x[0], x[1], x[2]])
                return merkezler

        return None

    def __renkleri_tespit_et_renkli(self, goruntu):
        renkler = []
        e, b, k = goruntu.shape
        for i in range(e):
            for j in range(b):
                if renkler.count([goruntu[i][j][0], goruntu[i][j][1], goruntu[i][j][2]]) == 0:
                    renkler.append([goruntu[i][j][0], goruntu[i][j][1], goruntu[i][j][2]])

        return np.array(renkler)

    def __rgb2str(self, rgb):
        x = str(rgb[0]) + "," + str(rgb[1]) + "," + str(rgb[2])
        return x

    def __str2rgb(self, etiket):
        bolunmus = etiket.split(",")
        return [int(bolunmus[0]), int(bolunmus[1]), int(bolunmus[2])]

    def __oklid_uzaklik(self, renkler, merkezler):
        uzakliklar = {}
        for j in merkezler:
            uzakliklar[self.__rgb2str(j)] = []
        for i in renkler:
            for j in merkezler:
                uzakliklar[self.__rgb2str(j)].append(
                    int(math.sqrt(((i[0] - j[0]) ** 2) + ((i[1] - j[1]) ** 2) + ((i[2] - j[2]) ** 2))))

        return uzakliklar

    def __uzakliklara_gore_kumelere_ata_renkli(self, renkler, uzakliklar, merkezler):
        kumeler = {}
        for j in merkezler:
            kumeler[self.__rgb2str(j)] = []
        for i in range(len(renkler)):
            ek = uzakliklar[self.__rgb2str(merkezler[0])][i]
            ek_sinif = self.__rgb2str(merkezler[0])
            for j in merkezler:
                if uzakliklar[self.__rgb2str(j)][i] < ek:
                    ek = uzakliklar[self.__rgb2str(j)][i]
                    ek_sinif = self.__rgb2str(j)
            kumeler[ek_sinif].append([renkler[i][0], renkler[i][1], renkler[i][2]])

        return kumeler

    def __yeni_merkezleri_hesapla_renkli(self, kumeler):
        # 0=r, 1=g, 2=b ortalama ve toplam etiketleri icin
        yeni_merkezler = []
        ortalama = {}
        for i in kumeler:
            toplam = {0: 0, 1: 0, 2: 0}
            for j in kumeler[i]:
                toplam[0] += j[0]
                toplam[1] += j[1]
                toplam[2] += j[2]
            y = len(kumeler[i])
            if y == 0:
                y = 1
            ortalama[0] = int(toplam[0] / y)
            ortalama[1] = int(toplam[1] / y)
            ortalama[2] = int(toplam[2] / y)
            yeni_merkezler.append([ortalama[0], ortalama[1], ortalama[2]])

        return yeni_merkezler

    def __boya_renkli(self, goruntu, kumeler):
        grt = goruntu.copy()
        e, b, k = grt.shape

        for i in range(e):
            for j in range(b):
                for m in kumeler:
                    if kumeler[m].count([grt[i][j][0], grt[i][j][1], grt[i][j][2]]) == 1:
                        grt[i][j] = self.__str2rgb(m)

        return grt

    def __renkli_kmeans(self, goruntu, k, baslangic_merkezleri_atama='bolerek'):
        merkezler = self.__baslangic_kume_merkezi_ata('renkli', k, baslangic_merkezleri_atama)
        eski_merkezler = [[-1, -1, -1] for i in range(k)]
        renkler = self.__renkleri_tespit_et_renkli(goruntu)
        kumeler = {}

        while (True):
            if merkezler == eski_merkezler:  # fazladan islem yapiyoruz aslinda kume ici kontrol edilse daha iyi olur
                break
            uzakliklar = self.__oklid_uzaklik(renkler, merkezler)
            kumeler = self.__uzakliklara_gore_kumelere_ata_renkli(renkler, uzakliklar, merkezler)
            eski_merkezler = merkezler.copy()
            merkezler = self.__yeni_merkezleri_hesapla_renkli(kumeler)

            # adim basi gosterme#
            """rsm=self.__boya_renkli(goruntu, kumeler)
            cv2.imshow("rsm", rsm)
            cv2.waitKey(0)"""
            # -#

        return self.__boya_renkli(goruntu, kumeler)

    def __renkleri_tespit_et_gri(self, goruntu):
        renkler = []
        e, b = goruntu.shape
        for i in range(e):
            for j in range(b):
                if renkler.count(goruntu[i][j]) == 0:
                    renkler.append(goruntu[i][j])

        return np.array(renkler)

    def __manhattan_uzaklik(self, renkler, merkezler):
        uzakliklar = {}
        for j in merkezler:
            uzakliklar[j] = []
        for i in renkler:
            for j in merkezler:
                uzakliklar[j].append(math.fabs(i - j))

        return uzakliklar

    def __uzakliklara_gore_kumelere_ata_gri(self, renkler, uzakliklar, merkezler):
        kumeler = {}
        for j in merkezler:
            kumeler[j] = []
        for i in range(len(renkler)):
            ek = uzakliklar[merkezler[0]][i]
            ek_sinif = merkezler[0]
            for j in merkezler:
                if uzakliklar[j][i] < ek:
                    ek = uzakliklar[j][i]
                    ek_sinif = j
            kumeler[ek_sinif].append(renkler[i])
        return kumeler

    def __yeni_merkezleri_hesapla_gri(self, kumeler):
        yeni_merkezler = []
        for i in kumeler:
            toplam = 0
            for j in kumeler[i]:
                toplam += j
            y = len(kumeler[i])
            if y == 0:
                y = 1
            ortalama = int(toplam / y)
            yeni_merkezler.append(ortalama)

        return yeni_merkezler

    def __boya_gri(self, goruntu, kumeler):
        grt = goruntu.copy()
        e, b = grt.shape

        for i in range(e):
            for j in range(b):
                for m in kumeler:
                    if kumeler[m].count(grt[i][j]) == 1:
                        grt[i][j] = m

        return grt

    def __gri_kmeans(self, goruntu, k, baslangic_merkezleri_atama='bolerek'):
        merkezler = self.__baslangic_kume_merkezi_ata('gri', k, baslangic_merkezleri_atama)
        eski_merkezler = [-1 for i in range(k)]
        renkler = self.__renkleri_tespit_et_gri(goruntu)
        kumeler = {}
        while (True):
            if merkezler == eski_merkezler:  # fazladan islem yapiyoruz aslinda kume ici kontrol edilse daha iyi olur
                break
            uzakliklar = self.__manhattan_uzaklik(renkler, merkezler)
            kumeler = self.__uzakliklara_gore_kumelere_ata_gri(renkler, uzakliklar, merkezler)
            eski_merkezler = merkezler.copy()
            merkezler = self.__yeni_merkezleri_hesapla_gri(kumeler)

        return self.__boya_gri(goruntu, kumeler)

    def k_means_kumeleme(self, goruntu, k=2, baslangic_merkezleri_atama=0):
        if baslangic_merkezleri_atama == 0:
            baslangic_merkezleri_atama = 'bolerek'
        else:
            baslangic_merkezleri_atama = 'rastgele'

        if len(goruntu.shape) == 3:
            return self.__renkli_kmeans(goruntu, k, baslangic_merkezleri_atama)
        if len(goruntu.shape) == 2:
            return self.__gri_kmeans(goruntu, k, baslangic_merkezleri_atama)
        return None


def agirlik_hesabi(degerler, toplam_pixel_sayisi):
    toplam = 0
    for i in degerler:
        toplam += i
    if toplam_pixel_sayisi == 0:
        toplam_pixel_sayisi = 1
    return toplam / toplam_pixel_sayisi


def ortalama_hesabi(degerler):
    toplam = 0
    genel_toplam = 0
    for i in range(len(degerler)):
        toplam += i * degerler[i]
        genel_toplam += degerler[i]
    if genel_toplam == 0:
        genel_toplam = 1
    return toplam / genel_toplam


def varyans_hesabi(degerler):
    ortalama = ortalama_hesabi(degerler)
    toplam = 0
    genel_toplam = 0
    for i in range(len(degerler)):
        toplam += ((i - ortalama) ** 2) * degerler[i]
        genel_toplam += degerler[i]
    if genel_toplam == 0:
        genel_toplam = 1
    return toplam / genel_toplam


def dict_values2list(sozluk):
    liste = []
    for i in sozluk.values():
        liste.append(i)
    return liste


def otsu_esikleme(goruntu):
    e, b = goruntu.shape
    ps = e * b
    histogram = dict_values2list(gri_histogram_hesaplama(goruntu))
    genel_varyanslar = []
    for esik in range(1, 256):  # 1,256
        kisim1 = histogram[0:esik]
        kisim2 = histogram[esik:256]
        genel_varyanslar.append(
            varyans_hesabi(kisim1) * agirlik_hesabi(kisim1, ps) + varyans_hesabi(kisim2) * agirlik_hesabi(kisim2, ps))

    ek = 0
    for i in range(len(genel_varyanslar)):
        if genel_varyanslar[i] < genel_varyanslar[ek]:
            ek = i

    return ek


def idleri_griye_olcekle(yeni, nesne_id):
    # nesne id sine renk atiyorum ama 256 dan fazla nesne bulunca cortluyor
    if nesne_id < 255:
        if nesne_id == 0:
            renkler = [0 for i in range(256)]
            return boya(yeni, renkler)

        if nesne_id == 1:  # 256/0 i engellemek icin
            bolum_miktari = 1
        else:
            bolum_miktari = (nesne_id)

        artis_miktari = int(256 / bolum_miktari)
        renkler = [0 for i in range(256)]
        for i in range(nesne_id + 1):
            renkler[i] = i * artis_miktari

        return boya(yeni, renkler)
    return None


def komsuluklari_doldur2(goruntu, yeni, nesne_id, i, j):
    e, b = goruntu.shape
    sozluk = {}  # merkezin komsusu yeni de bossa 0,yeni bir nesne vardir

    if i > 0 and goruntu[i - 1][j] == SB_BEYAZ:  # sol
        if yeni[i - 1][j] == SB_SIYAH:
            sozluk['sol'] = 0
        else:
            sozluk['sol'] = 1
            # nesne_id = yeni[i - 1][j]

    if i < e - 1 and goruntu[i + 1][j] == SB_BEYAZ:  # sag
        if yeni[i + 1][j] == SB_SIYAH:
            sozluk['sag'] = 0
        else:
            sozluk['sag'] = 1
            # nesne_id = yeni[i + 1][j]

    if j > 0 and goruntu[i][j - 1] == SB_BEYAZ:  # yukari
        if yeni[i][j - 1] == SB_SIYAH:
            sozluk['ust'] = 0
        else:
            sozluk['ust'] = 1
            # nesne_id = yeni[i][j - 1]

    if j < b - 1 and goruntu[i][j + 1] == SB_BEYAZ:  # asagi
        if yeni[i][j + 1] == SB_SIYAH:
            sozluk['alt'] = 0
        else:
            sozluk['alt'] = 1
            # nesne_id = yeni[i][j + 1]

    # komsularin hepsi 0 sa yeni id olsun
    degerler = []
    for m in sozluk.values():
        degerler.append(m)
    etiketler = []
    for m in sozluk.keys():
        etiketler.append(m)

    # nesne id belirleme
    arttir = True
    for m in degerler:
        if m == 1:
            arttir = False
            yon = etiketler[degerler.index(1)]
            if yon == 'sol':
                nesne_id = yeni[i - 1][j]
            if yon == 'sag':
                nesne_id = yeni[i + 1][j]
            if yon == 'ust':
                nesne_id = yeni[i][j - 1]
            if yon == 'alt':
                nesne_id = yeni[i][j + 1]

    if arttir == True:
        nesne_id += 1

    # atama
    for m in etiketler:
        if m == 'sol':
            yeni[i - 1][j] = nesne_id
        if m == 'sag':
            yeni[i + 1][j] = nesne_id
        if m == 'ust':
            yeni[i][j - 1] = nesne_id
        if m == 'alt':
            yeni[i][j + 1] = nesne_id
    yeni[i][j] = nesne_id

    return yeni, nesne_id


def atama(goruntu, yeniler):
    if yeniler == {}:
        return goruntu
    grt = goruntu.copy()
    e, b = grt.shape
    yeni = np.zeros((e, b), dtype=np.int)

    etiketler = []
    for m in yeniler.keys():
        etiketler.append(m)

    for i in range(e):
        for j in range(b):
            if etiketler.count(grt[i][j]) == 1:
                yeni[i][j] = yeniler[grt[i][j]]

    return yeni

def key_var_mi(yeniler,etiket):
    etiketler = []
    for m in yeniler.keys():
        etiketler.append(m)
    if etiketler.count(etiket)==1:
        return True
    return False

def sb_dortlu_komsuluk3(goruntu):
    grt = goruntu.copy()
    e, b = grt.shape
    yeni = np.zeros((e, b), dtype=np.int)
    nesne_id = 0

    for i in range(e):  # buranin cikisinda arka plan a 0 kaliyor
        for j in range(b):
            if grt[i][j] == SB_BEYAZ:  # and yeni[i][j] == SB_SIYAH:
                yeni, nesne_id = komsuluklari_doldur2(grt, yeni, nesne_id, i, j)
    yeni = duzenle(yeni)

    # int 2 uint8
    yeni2 = np.zeros((e, b), dtype="uint8")
    for i in range(e):
        for j in range(b):
            yeni2[i][j] = sinirla(yeni[i][j])

    renkler = []
    for i in range(e):
        for j in range(b):
            if renkler.count(yeni2[i][j]) == 0:
                renkler.append(yeni2[i][j])

    renk_sayisi = len(renkler)
    # renklendirme
    renkler = []
    i = 0
    while i < renk_sayisi:  # arka plan siyah kalmiyor ona da bir rgb ataniyor
        rgb = np.random.randint(0, 256, 3)
        x = [rgb[0], rgb[1], rgb[2]]
        if renkler.count(x) == 0:
            renkler.append(x)
            i += 1

    return griyi_renkliye_boya(yeni2, renkler)

def duzenle(grt):
    e, b = grt.shape
    degisti = True

    while degisti:
        degisti = False
        for i in range(0, e - 1):  # dikeyde en kucugu alma
            for j in range(0, b - 1):
                if grt[i][j] != SB_SIYAH and grt[i + 1][j] != SB_SIYAH and grt[i][j] != grt[i + 1][j]:
                    degisti = True
                    if grt[i][j] < grt[i+ 1][j ]:
                        grt[i + 1][j]=grt[i][j]
                    else:
                        grt[i][j]=grt[i + 1][j]

        for i in range(0, e - 1):  # yatayda en kucugu alma
            for j in range(0, b - 1):
                if grt[i][j] != SB_SIYAH and grt[i][j + 1] != SB_SIYAH and grt[i][j] != grt[i][j + 1]:
                    degisti = True
                    if grt[i][j] < grt[i][j + 1]:
                        grt[i][j+1] = grt[i][j]
                    else:
                        grt[i][j] = grt[i][j + 1]

    return grt

def sb_dortlu_komsuluk(goruntu):
    grt = goruntu.copy()
    e, b = grt.shape
    yeni = np.zeros((e, b), dtype=np.int)
    nesne_id = 1

    """for i in range(0, e - 1):  # id atama    HATALI!
        for j in range(0, b - 1):
            if grt[i][j] != SB_SIYAH and grt[i][j + 1] != SB_SIYAH and grt[i][j] == grt[i][j + 1]:
                yeni[i][j]=nesne_id
            else:
                nesne_id+=1
        yeni[i][j]=nesne_id"""
    
    for i in range(0, e ):  # id atama
        for j in range(0, b - 1):
            if grt[i][j] != SB_SIYAH:
                yeni[i][j] = nesne_id
                if grt[i][j + 1] != SB_SIYAH and grt[i][j] == grt[i][j + 1]:
                    yeni[i][j+1] = nesne_id
            else:
                nesne_id+=1
        yeni[i][j]=nesne_id
        nesne_id += 1

    yeni = duzenle(yeni)

    renk_idler = []
    for i in range(e):
        for j in range(b):
            if renk_idler.count(yeni[i][j]) == 0:
                renk_idler.append(yeni[i][j])

    renk_sayisi = len(renk_idler)

    # renklendirme
    renkler = []
    i = 0
    while i < renk_sayisi:  # arka plan siyah kalmiyor ona da bir rgb ataniyor
        rgb = np.random.randint(0, 256, 3)
        x = [rgb[0], rgb[1], rgb[2]]
        if renkler.count(x) == 0:
            renkler.append(x)
            i += 1

    sozluk={}
    for i in range(len(renkler)):
        sozluk[renk_idler[i]]=renkler[i]

    renkli_grt=griyi_renkliye_boya(yeni, sozluk)
    return renkli_grt
