import numpy as np
import sys
import os

from PyQt5.QtGui import QIcon, QPixmap

import kutuphane.menu1_dosya_islemleri as m1
import kutuphane.menu2_on_islemler as m2
import kutuphane.menu3_filtreleme_menusu as m3
import kutuphane.menu4_morfolojik_islemler as m4
import kutuphane.menu5_segmentasyon as m5
import kutuphane.melih_kutuphane as mk

from PyQt5.QtWidgets import *
#from PyQt5.uic import loadUi
from kutuphane.tasarim_py import Ui_MainWindow

class deneme3(QMainWindow):
    def __init__(self):
        super().__init__()
        self.RESIM_YOK_ = "RESIM YOK!"
        self.GRI_DEGIL_ = "GRI DEGIL!"
        self.RENKLI_DEGIL_ = "RENKLI DEGIL!"
        self.SIYAH_BEYAZ_DEGIL_ = "SIYAH BEYAZ DEGIL!"
        self.HATA_YOK_="HATA YOK!"
        self.resim = None
        self.gecici = None
        self.esik=127
        self.ekran_numara=1

        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionResim_Ac.triggered.connect(self.resim_ac)
        self.ui.actionKaydet.triggered.connect(self.resim_kaydet)
        self.ui.actionbas.triggered.connect(self.resim_bastir)
        self.ui.actionGriye_Cevir.triggered.connect(self.griye_cevir)
        self.ui.actionBulaniklastirma.triggered.connect(self.bulaniklastirma)
        self.ui.actionKeskinlestirme.triggered.connect(self.keskinlestirme)
        self.ui.actionOrtanca_Filtresi.triggered.connect(self.ortanca)
        self.ui.actionLaplace_Filtresi.triggered.connect(self.laplacian)
        self.ui.actionPrewitt_Kenar_Bulma.triggered.connect(self.kenar_bulma)
        self.ui.actionsb_cevir.triggered.connect(self.sb_cevir)
        self.ui.actionGenisletme.triggered.connect(self.genislet)
        self.ui.actionAsindirma.triggered.connect(self.asindirma)
        self.ui.actionAcma.triggered.connect(self.acma)
        self.ui.actionKapama.triggered.connect(self.kapama)
        self.ui.actionOtsu_Esikleme.triggered.connect(self.otsu)
        self.ui.actionDortlu_Komsuluk.triggered.connect(self.dortlu_komsu)
        self.ui.actionK_Means_Gri.triggered.connect(self.k_means_gri)
        self.ui.actionK_Means_Renkli.triggered.connect(self.k_means_renkli)
        self.ui.actionHistogram_Ciz.triggered.connect(self.histogram_bas)
        self.ui.actionYeniden_Boyutlandir.triggered.connect(self.boyutlandir)
        self.ui.actionKes.triggered.connect(self.kes)
        self.ui.actionBuyuKucul.triggered.connect(self.buyu_kucul)
        self.ui.actionters_al.triggered.connect(self.ters_al)

    def tur_don(self):
        if self.sb_mi():
            return "Siyah Beyaz"
        elif self.gri_mi():
            return "Gri"
        return "Renkli"

    def HATA_YOK(self,yazi=""):
        self.ui.label.setText(yazi)#self.HATA_YOK_
        if self.sb_mi():#uint tuttugumuz icin 0 1 olursa siyah basiyor onu engellemek icin siyahi 255 tutuyoruz
            m1.goruntu_kaydet_hazir(mk.sb_griye_olcekle(self.resim), yol + "gecici", "png")
        else:
            m1.goruntu_kaydet_hazir(self.resim,yol+"gecici","png")
        self.ui.label_2.setPixmap(QPixmap(yol+"gecici.png"))
        self.ui.label_6.setText(str(self.resim.shape[0])+","+str(self.resim.shape[1]))
        self.gecici=self.resim.copy()
        self.ui.label_10.setText(self.tur_don())
        return 1
    def HATA_YOK2(self):#buyultme kucultme de ham resim degil gecici basmak icin
        self.ui.label.setText("")#self.HATA_YOK_
        if self.sb_mi():#uint tuttugumuz icin 0 1 olursa siyah basiyor onu engellemek icin siyahi 255 tutuyoruz
            m1.goruntu_kaydet_hazir(mk.sb_griye_olcekle(self.gecici), yol + "gecici2", "png")
        else:
            m1.goruntu_kaydet_hazir(self.gecici,yol+"gecici2","png")
        self.ui.label_2.setPixmap(QPixmap(yol+"gecici2.png"))
        self.ui.label_6.setText(str(self.gecici.shape[0])+","+str(self.gecici.shape[1]))
        self.ui.label_10.setText(self.tur_don())
        return 1
    def GRI_DEGIL(self):
        self.ui.label.setText(self.GRI_DEGIL_)
        return 1
    def RESIM_YOK(self):
        self.ui.label.setText(self.RESIM_YOK_)
        return 1
    def RENKLI_DEGIL(self):
        self.ui.label.setText(self.RENKLI_DEGIL_)
        return 1
    def SIYAH_BEYAZ_DEGIL(self):
        self.ui.label.setText(self.SIYAH_BEYAZ_DEGIL_)
        return 1
    def bos_fonk(self,aksiyon):
        if self.resim_var_mi():
            if self.gri_mi():
                #self.resim
                return self.HATA_YOK()
            else:
                return self.GRI_DEGIL()
        else:
            return self.RESIM_YOK()

    def ters_al(self,aksiyon):
        if self.resim_var_mi():
            if self.gri_mi():
                self.resim=mk.gri_ters_alma(self.resim)
                return self.HATA_YOK()
            elif self.sb_mi():
                self.resim=mk.sb_ters_alma(self.resim)
                return self.HATA_YOK()
        else:
            return self.RESIM_YOK()

    def buyu_kucul_oran_al(self):
        try:
            x=float(self.ui.lineEdit_5.text())
            return int(self.gecici.shape[0]*x),int(self.gecici.shape[1]*x)
        except:
            return self.gecici.shape

    def buyu_kucul(self,aksiyon):
        if self.resim_var_mi():
            boyut=self.buyu_kucul_oran_al()
            self.gecici=m2.goruntu_boyutlandirma(self.gecici,boyut)
            return self.HATA_YOK2()
        else:
            return self.RESIM_YOK()

    def kesilecek(self):
        x=self.ui.lineEdit_3.text().split(",")
        try:
            return (int(x[0]),int(x[1]),int(x[2]),int(x[3]))
        except:
            return (0,0,self.resim.shape[0],self.resim.shape[1])

    def kes(self,aksiyon):
        if self.resim_var_mi():
            self.resim=m2.kes(self.resim,self.kesilecek())
            return self.HATA_YOK()
        else:
            return self.RESIM_YOK()

    def boyut_al(self):
        e = self.resim.shape[0]
        b = self.resim.shape[1]
        try:
            boyut = self.ui.lineEdit.text().split(",")
            x = int(boyut[0])
            y = int(boyut[1])
            if x > 0 and y > 0:
                return (x, y)
            else:
                return (e, b)
        except:
            return (e, b)

    def boyutlandir(self,aksiyon):
        if self.resim_var_mi():
            self.resim=m2.goruntu_boyutlandirma(self.resim,self.boyut_al())
            return self.HATA_YOK()
        else:
            return self.RESIM_YOK()

    def histogram_bas(self,aksiyon):
        if self.resim_var_mi():
            if self.gri_mi():
                histo=m2.gri_histogram_hesaplama(self.resim)
                mk.histogram_cizdir(histo)
                return self.HATA_YOK()
            else:
                return self.GRI_DEGIL()
        else:
            return self.RESIM_YOK()

    def sb_mi(self):
        """if len(self.resim.shape) == 2 or len(self.resim.shape) == 3:
            if (np.max(self.resim)==1 or np.max(self.resim)==255) and np.min(self.resim)==mk.SB_SIYAH:
                return True"""
        x=self.resim.shape
        if len(self.resim.shape) == 2:
            for i in range(x[0]):
                for j in range(x[1]):
                    if self.resim[i][j]!=1 and self.resim[i][j]!=255 and self.resim[i][j]!=0:
                        return False
        elif len(self.resim.shape) == 3:
            for i in range(x[0]):
                for j in range(x[1]):
                    y=self.resim[i][j]
                    if y[0] != 1 and y[0] != 255 and y[0] != 0:
                        return False
                    if y[1] != 1 and y[1] != 255 and y[1] != 0:
                        return False
                    if y[2] != 1 and y[2] != 255 and y[2] != 0:
                        return False
        return True

    def gri_mi(self):
        if self.sb_mi()==False and len(self.resim.shape) == 2:
            return True
        return False

    def renkli_mi(self):
        if len(self.resim.shape)==3:
            return True
        return False

    def resim_var_mi(self):
        try:
            if self.resim==None:
                return False
        except:
            return True

    def kumeleme_k_al(self):
        try:
            x=int(self.ui.lineEdit_4.text())
            if x >10:
                x=9
            return x
        except:
            return 2

    def k_means_gri(self,aksiyon):
        if self.resim_var_mi():
            if self.gri_mi():
                km=m5.k_means()
                k=self.kumeleme_k_al()
                self.resim=km.k_means_kumeleme(self.resim,k)
                return self.HATA_YOK()
            else:
                return self.GRI_DEGIL()
        else:
            return self.RESIM_YOK()

    def k_means_renkli(self,aksiyon):
        if self.resim_var_mi():
            if self.renkli_mi():
                km = m5.k_means()
                k = self.kumeleme_k_al()
                self.resim = km.k_means_kumeleme(self.resim, k)
                return self.HATA_YOK()
            else:
                return self.RENKLI_DEGIL()
        else:
            return self.RESIM_YOK()

    def dortlu_komsu(self,aksiyon):
        if self.resim_var_mi():
            if self.sb_mi():
                self.resim=m5.sb_dortlu_komsuluk(self.resim)
                return self.HATA_YOK()
            else:
                return self.SIYAH_BEYAZ_DEGIL()
        else:
            return self.RESIM_YOK()

    def otsu(self,aksiyon):
        if self.resim_var_mi():
            if self.gri_mi():
                otsu_esik=m5.otsu_esikleme(self.resim)
                self.sb_cevir(aksiyon, otsu_esik)
                return self.HATA_YOK("Otsu Esik: " + str(otsu_esik))
            else:
                return self.GRI_DEGIL()
        else:
            return self.RESIM_YOK()

    def genislet(self,aksiyon):
        if self.resim_var_mi():
            if self.sb_mi():
                self.resim=m4.genisleme(self.resim,self.yapisal_e_al())
                return self.HATA_YOK()
            else:
                return self.SIYAH_BEYAZ_DEGIL()
        else:
            return self.RESIM_YOK()

    def asindirma(self,aksiyon):
        if self.resim_var_mi():
            if self.sb_mi():
                self.resim=m4.asindirma(self.resim,self.yapisal_e_al())
                return self.HATA_YOK()
            else:
                return self.SIYAH_BEYAZ_DEGIL()
        else:
            return self.RESIM_YOK()

    def acma(self,aksiyon):
        if self.resim_var_mi():
            if self.sb_mi():
                self.resim=m4.acma(self.resim,self.yapisal_e_al())
                return self.HATA_YOK()
            else:
                return self.SIYAH_BEYAZ_DEGIL()
        else:
            return self.RESIM_YOK()

    def yapisal_e_al(self):
        if self.ui.radioButton_6.isChecked():
            return mk.YAPISAL_ELEMAN_ARTI
        return mk.YAPISAL_ELEMAN_KARE

    def kapama(self,aksiyon):
        if self.resim_var_mi():
            if self.sb_mi():
                self.resim=m4.kapama(self.resim,self.yapisal_e_al())
                return self.HATA_YOK()
            else:
                return self.SIYAH_BEYAZ_DEGIL()
        else:
            return self.RESIM_YOK()

    def sb_cevir(self,aksiyon,esik_degeri=-1):
        if self.resim_var_mi():
            if self.gri_mi():
                if esik_degeri==-1:
                    self.resim = mk.gri_sb_cevir(self.resim,self.esik)
                else:
                    self.resim = mk.gri_sb_cevir(self.resim,esik_degeri)
                return self.HATA_YOK()
            else:
                return self.GRI_DEGIL()
        else:
            return self.RESIM_YOK()
    def laplacian(self,aksiyon):#padding kendi hesapliyor
        if self.resim_var_mi():
            if self.gri_mi():
                self.resim=m3.laplas_keskinlestirme(self.resim,yumusatma_filtre_boyutu=self.filtre_don())
                return self.HATA_YOK()
            else:
                return self.GRI_DEGIL()
        else:
            return self.RESIM_YOK()
    def kenar_bulma(self,aksiyon):#prewitt her zaman icin 3x3 luk filtre ile yapiliyor
        if self.resim_var_mi():
            if self.gri_mi():
                if self.ui.radioButton.isChecked():
                    self.resim =m3.prewitt_kenar_bul(self.resim,padding_sayisi=(1,1))
                else:
                    self.resim = m3.prewitt_kenar_bul(self.resim, padding_sayisi=(0,0))
                return self.HATA_YOK()
            else:
                return self.GRI_DEGIL()
        else:
            return self.RESIM_YOK()
    def ortanca(self,aksiyon):
        if self.resim_var_mi():
            if self.gri_mi():
                self.resim=m3.ortanca_maskeleme(self.resim,filtre_boyutu=self.filtre_don(),padding_sayisi=self.padding_don())
                return self.HATA_YOK()
            else:
                return self.GRI_DEGIL()
        else:
            return self.RESIM_YOK()
    def keskinlestirme(self,aksiyon):#keskin olmayan maskelemede padding kesinlikle vardır
        if self.resim_var_mi():
            if self.gri_mi():
                self.resim=m3.keskin_olmayan_maskeleme(self.resim,filtre_boyutu=self.filtre_don())
                return self.HATA_YOK()
            else:
                return self.GRI_DEGIL()
        else:
            return self.RESIM_YOK()

    def bulaniklastirma(self,aksiyon):
        if self.resim_var_mi():
            if self.gri_mi():
                x=self.filtre_don()
                self.resim = m3.ortalama_maskeleme(self.resim,filtre=mk.ortalama_filtre_olustur(x),padding_sayisi=self.padding_don())
                return self.HATA_YOK()
            else:
                return self.GRI_DEGIL()
        else:
            return self.RESIM_YOK()

    def padding_don(self):
        if self.ui.radioButton.isChecked():
            return mk.padding_sayisi_hesaplama2(self.resim.shape,self.filtre_don())
        else:
            return (0,0)

    def filtre_don(self):
        x=self.ui.lineEdit_2.text()
        try:
            bir=int(x[0])
            if bir%2==0:
                bir+=1
            return (bir,bir)
        except:
            return (5,5)

    def resim_bastir(self,aksiyon):
        if self.resim_var_mi():
            if self.sb_mi():
                m1.goruntu_bastir([mk.sb_griye_olcekle(self.resim)],self.ekran_numara)
                self.ekran_numara+=1
            else:
                m1.goruntu_bastir([self.resim])
            return self.HATA_YOK()
        else:
            return self.RESIM_YOK()

    def resim_ac(self,aksiyon):#dosyadan secme ekle,dosya turu desteklenmiyor hatasi ekle
        filename, _ = QFileDialog.getOpenFileName(self, "", "", "")
        self.resim = m1.goruntu_oku(filename)
        if self.resim_var_mi():
            if self.sb_mi():#belki gereksiz
                if self.renkli_mi():
                    self.resim=m2.rgb2gray(self.resim)
                self.resim=mk.gri_sb_cevir(self.resim)
            return self.HATA_YOK()
        else:
            return self.RESIM_YOK()

    def resim_kaydet(self,aksiyon):#dosyadan secme ekle,dosya turu desteklenmiyor hatasi ekle
        #filename, _ = QFileDialog.getSaveFileName(self, "", "", "")
        filename, _ = QFileDialog.getSaveFileName()
        format="jpg"
        if self.ui.radioButton_4.isChecked():
            format = "png"
        elif self.ui.radioButton_5.isChecked():
            format = "tiff"
        if self.resim_var_mi():
            if self.sb_mi():
                m1.goruntu_kaydet_hazir(mk.sb_griye_olcekle(self.resim), filename, format)
            else:
                m1.goruntu_kaydet_hazir(self.resim, filename, format)
            return self.HATA_YOK()
        else:
            return self.RESIM_YOK()

    def griye_cevir(self,aksiyon):
        if self.resim_var_mi():
            if self.renkli_mi():
                self.resim=m2.rgb2gray(self.resim)
                return self.HATA_YOK()
            else:
                return self.RENKLI_DEGIL()
        else:
            return self.RESIM_YOK()

yol=os.path.abspath("")+"\\"
uygulama=QApplication([])
pencere=deneme3()
pencere.show()
uygulama.exec_()