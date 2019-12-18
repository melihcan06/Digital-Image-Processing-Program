import numpy as np
from kutuphane.melih_kutuphane import SB_SIYAH, SB_BEYAZ, YAPISAL_ELEMAN_ARTI, YAPISAL_ELEMAN_KARE, \
    bitsel_veya


def ortusuyor_mu(x, y):  # x y boyutlari esit y=yapisal eleman
    e, b = x.shape

    for i in range(e):
        for j in range(b):
            if y[i][j] == SB_BEYAZ and x[i][j] != y[i][j]:
                return False

    return True


def asindirma(goruntu, yapisal_eleman=YAPISAL_ELEMAN_ARTI):
    grt = goruntu.copy()
    e, b = grt.shape
    f_en, f_boy = yapisal_eleman.shape
    yeni = np.zeros((e, b), dtype="uint8")

    baslangic_x = int(f_en / 2)
    bitis_x = e - baslangic_x
    baslangic_y = int(f_boy / 2)
    bitis_y = b - baslangic_y

    for i in range(baslangic_x, bitis_x):  # merkez noktalardan ilerleniyor!
        for j in range(baslangic_y, bitis_y):
            x = grt[i - baslangic_x:i + baslangic_x + 1, j - baslangic_y:j + baslangic_y + 1]
            if ortusuyor_mu(x, yapisal_eleman) == True:
                yeni[i][j] = SB_BEYAZ

    return yeni

def yerlestir(grt,eleman):
    e,b=eleman.shape
    yeni=eleman.copy()

    for i in range(e):
        for j in range(b):
            if grt[i][j]==SB_BEYAZ:
                yeni[i][j]=SB_BEYAZ

    return yeni

def genisleme(goruntu, yapisal_eleman=YAPISAL_ELEMAN_ARTI):
    grt = goruntu.copy()
    e, b = grt.shape
    f_en, f_boy = yapisal_eleman.shape
    yeni = grt.copy()
    bir=np.ones((yapisal_eleman.shape),dtype="uint8")*SB_BEYAZ

    baslangic_x = int(f_en / 2)
    bitis_x = e - baslangic_x
    baslangic_y = int(f_boy / 2)
    bitis_y = b - baslangic_y

    for i in range(baslangic_x, bitis_x):  # merkez noktalardan ilerleniyor!
        for j in range(baslangic_y, bitis_y):
            if grt[i][j] == SB_BEYAZ:
                yeni[i - baslangic_x:i + baslangic_x + 1, j - baslangic_y:j + baslangic_y + 1] = yerlestir(yeni[i - baslangic_x:i + baslangic_x + 1, j - baslangic_y:j + baslangic_y + 1] ,yerlestir(grt[i - baslangic_x:i + baslangic_x + 1, j - baslangic_y:j + baslangic_y + 1],yapisal_eleman))


    return bitsel_veya(yeni, grt)


def acma(goruntu, yapisal_eleman=YAPISAL_ELEMAN_ARTI):
    return genisleme(asindirma(goruntu, yapisal_eleman), yapisal_eleman)


def kapama(goruntu, yapisal_eleman=YAPISAL_ELEMAN_ARTI):
    return asindirma(genisleme(goruntu, yapisal_eleman), yapisal_eleman)