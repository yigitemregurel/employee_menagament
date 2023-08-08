#!/usr/bin/env python
# coding: utf-8

# In[2]:

#   Kendi yazdığım program, çalışanların performansını ölçmeyi kolaylaştırıyor. 
#   Hedefler belirlemelerine yardımcı olmanın yanı sıra ilerlemeyi anlık olarak takip etme imkanı sunuyor. 


#   The program I've developed makes it easier to measure employees' performance.
#   In addition to assisting in setting goals, it provides the opportunity to track progress in real-time.


import tkinter as tk
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session



Base = declarative_base()


class Calisan(Base):
    __tablename__ = 'calisanlar'
    id = Column(Integer, primary_key=True)
    isim = Column(String(100), nullable=False)
    is_saati_uyum = Column(Integer)
    task_puani = Column(Integer)
    iletisim = Column(Integer)
    proje_uyum = Column(Integer)
    toplam_puan = Column(Float)


host = 'localhost'
port = '5432'
database = 'performans'
user = 'postgres'
password = 'admin'


engine = create_engine(f'postgresql://postgres:admin@localhost:5432/performans')



def create_table():
    Base.metadata.create_all(engine)


Session = scoped_session(sessionmaker(bind=engine))



#----------------------------------------------------
def kullanici_giris_al():
    isim = input("Çalışanın İsim ve Soyisim: ")
    is_saati_uyum = int(input("İş Saatlerine Uyum Puanı (0-100): "))
    task_puani = int(input("Task Puanı (0-100): "))
    iletisim = int(input("İletişim Puanı (0-100): "))
    proje_uyum = int(input("Proje Bitiş Tarihine Uyum Puanı (0-100): "))
    return isim, is_saati_uyum, task_puani, iletisim, proje_uyum

def performans_puanlama(is_saati_uyum, task_puani, iletisim, proje_uyum,):
 
    katsayilar = [0.6, 0.4, 0.2, 0.1]

   
    baslik_puanlar = [is_saati_uyum, task_puani, iletisim, proje_uyum]

   
    toplam_puan = sum([baslik_puan * katsayi for baslik_puan, katsayi in zip(baslik_puanlar, katsayilar)])
    return toplam_puan

def performans_siniflandirma(toplam_puan):
    if toplam_puan < 25:
        return "Kötü"
    elif toplam_puan < 50:
        return "Orta"
    elif toplam_puan < 75:
        return "İyi"
    else:
        return "Çok İyi"

def calisan_ekle(isim, is_saati_uyum, task_puani, iletisim, proje_uyum, toplam_puan):
    calisan = Calisan(isim=isim, is_saati_uyum=is_saati_uyum, task_puani=task_puani,
                      iletisim=iletisim, proje_uyum=proje_uyum, toplam_puan=toplam_puan)
    try:
        session = Session()
        session.add(calisan)
        session.commit()
        print("Çalışan başarıyla eklendi.")
    except Exception as e:
        print("Hata:", str(e))
    finally:
        session.close()

def calisan_sil(calisan_id):
    try:
        session = Session()
        calisan = session.query(Calisan).filter_by(id=calisan_id).first()
        if calisan:
            session.delete(calisan)
            session.commit()
            print(f"Çalışan (ID: {calisan_id}) başarıyla silindi.")
        else:
            print(f"Çalışan (ID: {calisan_id}) bulunamadı.")
    except Exception as e:
        print("Hata:", str(e))
    finally:
        session.close()
        
def calisanlari_listele():
    try:
        session = Session()
        calisanlar = session.query(Calisan).all()
        return calisanlar
    except Exception as e:
        print("Hata:", str(e))
        return []  
    finally:
        session.close()


def calisanlari_goruntuleme():
    calisanlari_listele()

def calisanlari_silme():
    while True:
        calisan_id = input("Silmek istediğiniz çalışanın ID'sini girin (Çıkmak için 'q' tuşuna basın): ")
        if calisan_id.lower() == 'q':
            break
        if not calisan_id.isdigit():
            print("Geçersiz giriş. Lütfen bir sayı girin.")
            continue
        calisan_id = int(calisan_id)
        calisan_sil(calisan_id)

def calisan_ekleme():
    while True:
        print("\n--- Çalışan Ekleme ---")
        isim, is_saati_uyum, task_puani, iletisim, proje_uyum = kullanici_giris_al()
        toplam_puan = performans_puanlama(is_saati_uyum, task_puani, iletisim, proje_uyum)
        calisan_ekle(isim, is_saati_uyum, task_puani, iletisim, proje_uyum, toplam_puan)

        performans_sinif = performans_siniflandirma(toplam_puan)

        
        root = tk.Tk()
        root.title("Çalışan Performans Değerlendirme")

        label = tk.Label(root, text=f"{isim} adlı çalışanın puanı: {toplam_puan}", padx=20, pady=10)
        label.pack()

        siniflandirma_label = tk.Label(root, text=f"{isim} adlı çalışanın performansı: {performans_sinif}", padx=20, pady=10)
        siniflandirma_label.pack()

        root.mainloop()

        devam_et = input("Yeni bir çalışan eklemek istiyor musunuz? (E/H): ")
        if devam_et.lower() != 'e':
            calisanlari_listele()
            break

    silme_istegi = input("Bir çalışan silmek istiyor musunuz? (E/H): ")
    if silme_istegi.lower() == 'e':
        calisanlari_silme()
#-----------------------------------------        

def main():
    create_table()
    calisan_ekleme()


# In[3]:


if __name__ == '__main__':
    main()


# In[ ]:




