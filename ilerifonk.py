
import pandas as pd
import numpy as np

maasSozluk = {"Isim" : ["Atıl","Zeynep","Mehmet","Ahmet"], 
             "Departman" : ["Yazılım","Satış","Pazarlama","Yazılım"],
              "Maas" : [200,300,400,500]
             }


maasDataFrame = pd.DataFrame(maasSozluk)
print(maasDataFrame["Departman"].unique()) # bir kere yazdırmış oluyoruz  
print(maasDataFrame["Departman"].nunique()) # sadece sayılar

"""
def bruttennete(maas):

    return maas * 0.66

print[maasDataFrame["Maas"].apply(bruttennete)]

"""

yeniBirVeri = {"Karakter Sınıfı" : ["South Park", "South Park", "Simpson", "Simpson","Simpson"],
              "Karakter Ismi" : ["Cartman", "Kenny", "Homer", "Bart","Bart"],
               "Karakter Yas" : [9,10,50,20,10]
              }

yenibirdataframe = pd.DataFrame(yeniBirVeri)
# print(yenibirdataframe.to_excel("deneme.xlsx"))

# print(yenibirdataframe.pivot_table(values= "Karakter Yas ",index=["Karakter Sınıfı","Karakter Ismi"],aggfunc= np.sum))


dataFrame = pd.read_excel("deneme.xlsx")
print(dataFrame)