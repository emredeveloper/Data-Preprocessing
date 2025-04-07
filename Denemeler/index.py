import pandas as pd
import numpy as np

data = np.random.randn(3,3)
print(data)

dataframe = pd.DataFrame(data)
print(dataframe)

yenidataframe = pd.DataFrame(data,index=["Emre","Ahmet","Mehmet"],columns=["Maas","yas","calisma saati"])
print(yenidataframe)

print(yenidataframe["yas"])

print(yenidataframe.loc["Emre"]) # emreye ait bilgileri getiriyoruz.

yenidataframe["Emeklilik Yasi"] = yenidataframe["yas"] + yenidataframe["yas"]
 # print(yenidataframe)
print(yenidataframe.drop("Emeklilik Yasi",axis=1)) #axis yaptığımızda sütunu düşürüyor.
print(yenidataframe.drop("Mehmet"))
print(yenidataframe)
print(yenidataframe.drop("Emeklilik Yasi",axis=1,inplace = True)) # inplace yaptığımızda kalıcı olarak tablodan siliyor 
print(yenidataframe)

print(yenidataframe.loc["Emre","yas"]) # emrenin yas bilgisini almış oluyoruz

print(yenidataframe < 0) # 0'dan küçük olan sayıları true diğerleri false oluyor.

boolenframe = yenidataframe <0

print(yenidataframe[boolenframe]) # böylece sadece sıfırdan küçük olanların sayısını görmüş olduk diğerleri nan

print(yenidataframe[yenidataframe["yas"]> 0]) # yas bilgisi sıfırdan büyük olanları ekrana getir sadece

#print(yenidataframe.reset_index()) # index resetleme

#yeniindexlistesi = ["A","B","C",  "D"]
#yenidataframe["Yeni Index"] = yeniindexlistesi # yeni sütun ekledik üstteki değerlerle beraber
#print(yenidataframe)
 
 
