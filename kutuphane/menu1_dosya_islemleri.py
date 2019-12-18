import cv2
import matplotlib.pyplot as plt
import numpy as np
import shutil
import os

def goruntu_oku(goruntu_yolu,grimi=False):
    if grimi==True:
        return cv2.imread(goruntu_yolu,0)
    return cv2.imread(goruntu_yolu)

def goruntu_kaydet_hazir(goruntu,yol_ve_ad,format):#3 farkli format secilip kendimiz kaydedecegiz cv2 kullanmayacagiz!!!!
    cv2.imwrite(yol_ve_ad+"."+format,goruntu)
    return 1

def goruntu_bastir(goruntuler,baslangic=0):
    j=0
    for i in range(baslangic,baslangic+len(goruntuler)):
        cv2.imshow("grt" + str(i + 1), goruntuler[j])
        j+=1

    cv2.waitKey(0)

def plt_ciz(goruntuler, satir=1, sutun=None):
    if sutun == None:
        sutun = len(goruntuler)
    for i in range(len(goruntuler)):
        plt.subplot(satir, sutun, i + 1)
        plt.imshow(goruntuler[i])
        plt.gray()
        plt.axis('off')

    plt.show()