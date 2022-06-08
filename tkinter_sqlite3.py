# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 12:45:05 2022

@author: Ahmet
"""

# tkinter sqlite3
from tkinter import *
import hashlib
import sqlite3

baglanti=sqlite3.connect("veri.db")
imlec=baglanti.cursor()
pencere=Tk()
pencere.geometry("720x480")
title=Label(text="Ana Ekran")
title.place(relx=.1, rely=.05)

# tablo oluştur
tablo="CREATE TABLE IF NOT EXISTS Tablom (kullanici VARCHAR(32),sifre VARCHAR(32), id INTEGER PRIMARY KEY AUTOINCREMENT )"
imlec.execute(tablo)
# veritabanındaki değişiklikleri kaydet
baglanti.commit()

def kayitEkle(kullanici, sifre):
    tabloKullanici=kullanici.encode("UTF-8")
    hashedtabloSifre=hashlib.md5(sifre.encode("UTF-8")).hexdigest()
    #hashedtabloSifre=kullanici.encode("UTF-8")
    imlec.execute("INSERT INTO Tablom (kullanici,sifre) VALUES(?,?)",(tabloKullanici,hashedtabloSifre))
    baglanti.commit()
    print("Kullanıcı Olusturuldu")
    resultStr.set("Kullanıcı oluşturuldu")

    
    imlec.execute("SELECT kullanici,sifre, id FROM Tablom")
    liste=imlec.fetchall()
    for i in liste:
        print(i)
    
    baglanti.close()

def ekle():
    global resultStr
    eklemeSayfasi=Frame(pencere)   #pencere üstüne açılan çerçeve
    eklemeSayfasi.place(relwidth=.9, relheight=.9, relx=.05, rely=.03)
    etiketKullanici=Label(eklemeSayfasi, text="Kullanıcı Adı :")
    entryKullanici=Entry(eklemeSayfasi, width=30)
    etiketKullanici.place(relx=.20, rely=.1)
    entryKullanici.place(relx=.37,rely=.1,)
    
    etiketSifre=Label(eklemeSayfasi, text="Sifre :")
    entrySifre=Entry(eklemeSayfasi, width=30)
    etiketSifre.place(relx=.20, rely=.2)
    entrySifre.place(relx=.37,rely=.2)
    # lamda ile her işlemde içeriğin değişmesini/güncellenmesini sağlıyor
    butonGiris=Button(eklemeSayfasi,text="Kaydet",bg="blue",fg="white",command=lambda:kayitEkle(entryKullanici.get(),entrySifre.get()))
    butonGiris.place(relx=.45,rely=.3)
    
    butonIptal=Button(eklemeSayfasi,text="İptal",command=lambda: eklemeSayfasi.place_forget())
    butonIptal.place(relx=.60,rely=.3)
    
    resultStr = StringVar()
    result = Label(yeniKullanici, textvariable=resultStr)
    result.place(relx=.45, rely=.7)

def kontrol(username,password):
    loginDurum=StringVar()
    etiketSonuc=Label(win,textvariable=loginDurum)
    etiketSonuc.place(relx=.45,rely=.7)
    imlec.execute("SELECT COUNT(*) FROM Tablom")
    sayi=imlec.fetchall()
    if sayi[0][0]==0:
        print("Kullanici kaydı yok")
        loginDurum.set("Kullanıcı yok")
        return
    else:
        eslesenKullanici=False
        eslesenSifre=False
        kullaniciId=0
        userKullanici=username.encode("UTF-8")
        hasliSifre=hashlib.md5(password.encode("UTF-8")).hexdigest()
        #imlec.execute("SELECT kullanici FROM Tablom WHERE kullanici=?", (username))
        #imlec.execute("SELECT kullanici FROM Tablom")
        imlec.execute("SELECT * FROM Tablom WHERE kullanici=?", (userKullanici,))
       
        sorgula=imlec.fetchone()
        boyut=len(sorgula)
        print(boyut)
        if boyut >0:
            eslesenKullanici=True
            idnum=sorgula[2]
            if sorgula[1]==hasliSifre:
                print("Şifre Eşleşti")
                loginDurum.set("Kullanıcı Girişi Başarılı")
                izinliSayfa(idnum)
            else:
                loginDurum.set("Hatalı Bilgi")
           
def izinliSayfa(userId):
    win.place_forget()
    etiketKullaniciBilgileri=Label(pencere,text="Kullanıcı ID : # {}".format(userId))
    etiketKullaniciBilgileri.place(relx=.4,rely=.4)
    
win=Frame(pencere)
win.place(relwidth=.9, relheight=.9, relx=.05, rely=.03)

etiketKullanici=Label(win, text="Kullanıcı Adı :")
entryKullanici=Entry(win, width=30)
etiketKullanici.place(relx=.20, rely=.1)
entryKullanici.place(relx=.37,rely=.1,)

etiketSifre=Label(win, text="Sifre :")
entrySifre=Entry(win, width=30)
etiketSifre.place(relx=.20, rely=.2)
entrySifre.place(relx=.37,rely=.2)

butonGiris=Button(win,text="Giriş",fg="blue",command=lambda:kontrol(entryKullanici.get(),entrySifre.get()))
butonGiris.place(relx=.45,rely=.3)

butonKayit=Button(win,text="Kayit Ol",command=ekle)
butonKayit.place(relx=.60, rely=.3)
win.mainloop()