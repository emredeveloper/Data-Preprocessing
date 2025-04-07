import pandas as pd
import numpy as np

#nan işlemleri ve düşürme
"""
sozlukVerisi = {"Istanbul" : [30,29,np.nan],"Ankara" : [20,np.nan,25],"Izmir" : [40,39,38]}
havaDurumuDataFrame = pd.DataFrame(sozlukVerisi)

print(havaDurumuDataFrame)
print(havaDurumuDataFrame.dropna(axis = 1)) # nan bulunan sütunları siliyor
"""
# doldurma ve nan yazan yerleri düşürme ayarlama
"""
yeniVeri = {"Istanbul" : [30,29,np.nan],"Ankara" : [20,np.nan,25],"Izmir" : [40,39,38],"Antalya":[45,np.nan,np.nan]}
yeniDataFrame = pd.DataFrame(yeniVeri)


print(yeniDataFrame.dropna(axis=1,thresh=2)) # 2den fazla nan bulunan sütunu siler
print(yeniDataFrame.fillna(20)) #nan yazan yerleri 20 ile doldurduk
"""

maasSozlugu = {"Departman" : ["Yazılım","Yazılım","Pazarlama","Pazarlama","Hukuk","Hukuk"],
              "Calisan Ismi" : ["Ahmet","Mehmet","Atil","Burak","Zeynep","Fatma"],
               "Maas" : [100,150,200,300,400,500]
              }

maasDataFrame = pd.DataFrame(maasSozlugu)
print(maasDataFrame)

grupObjesi = maasDataFrame.groupby("Departman") # verileri departmana göre grupluyoruz

print(grupObjesi.count()) # her bir departmanda ka çkişi çalışıyor
print(grupObjesi.mean()) # departmanlarda ortalama maaş
print(grupObjesi.describe()) # genel sayısal veriler elde ediyoruz