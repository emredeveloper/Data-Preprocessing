import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('deneme.csv')

#df.dropna(inplace= True)
#df.fillna(45,inplace=True)
df["isim"].fillna(100,inplace= True)
print(df.to_string())



 # print(pd.__version__)

a = [1, 7, 2]

myvar = pd.Series(a)

print(myvar)
"""

  # wrong format fix
"""
df = pd.read_csv('data.csv')

df['Date'] = pd.to_datetime(df['Date'])

print(df.to_string())

# Remove rows with a NULL value in the "Date" column:

df.dropna(subset=['Date'], inplace = True)

# Wrong data fix

df.loc[7, 'Duration'] = 45 # 7.satırda olan duration sütunundaki yanlış veriyi 45 ile güncelledik

for x in df.index:
  if df.loc[x, "Duration"] > 120:
    df.loc[x, "Duration"] = 120 # indexler arasında dolaşıp 120den büyük olan sayıları 120 olarak ayarla

for x in df.index:
  if df.loc[x, "Duration"] > 120:
    df.drop(x, inplace = True) # 120den büyük olan duration satırlarını düşür
    
df.drop_duplicates(inplace = True) # aynı olan verileri düşür

df.corr() # Veri Korelasyonları  corr() yönteminin sonucu, iki sütun arasındaki ilişkinin ne kadar iyi olduğunu gösteren çok sayıda sayı içeren bir tablodur.

df = pd.read_csv('data.csv')

df.plot()

plt.show() # verileri çizdiriyoruz yani çizimini görüyoruz

# histogram şeklinde veriyi gösterme kindi ile mümkün



