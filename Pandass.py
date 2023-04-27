from operator import index
import pandas as pd


#mydataset = {
#  'cars': ["BMW", "Volvo", "Ford"],
#  'passings': [3, 7, 2]
#}

#myvar = pd.DataFrame(mydataset)  # dataframe ile verileri okumuþ olduk.

#print(myvar)

 # print(pd.__version__)  # pandas versiyon kontrolü

#a = [1, 7, 2]

#myvar1 = pd.Series(a)  # Pandalar Serisi, tablodaki bir sütun gibidir.

#print(myvar1)
#print(myvar1[0]) # dizideki ilk veriye ulaþýyoruz


#b = [1, 7, 2]

#myvar2 = pd.Series(b, index = ["x", "y", "z"]) # verilerimizin indexini biz belirledik

#print(myvar2)

calories = {"day 1": 420, "day 2": 380, "day 3": 390}

myvar3 = pd.Series(calories)

print(myvar3)

#data = {
#  "calories": [420, 380, 390],
#  "duration": [50, 40, 45]
#}

##load data into a DataFrame object:
#df = pd.DataFrame(data,index = ["Day 1","Day 2", "Day 3"])

#print(df) 


#df = pd.read_csv('pythondata.csv')

#print(df.to_string()) 

#print(pd.options.display.max_rows) #maximum satýr sayýsýný gördük

#pd.options.display.max_rows = 9999

#rd = pd.read_csv('https://www.w3schools.com/python/pandas/data.csv.txt')

#print(rd.head(5)) #üstten aþaðýya doðru kaç veri getireceðimizi belirledik
#print(rd.shape) # Veri setimiz kaç satýr, kaç sütun yani boyutlarý nedir shape niteliðinden öðreniyoruz.
#print(rd.tail()) #son 5 satýr
#print(rd.info()) # veri hakkýnda bilgi


#data = {
#  "Duration":{
#    "0":60,
#    "1":60,
#    "2":60,
#    "3":45,
#    "4":45,
#    "5":60
#  },
#  "Pulse":{
#    "0":110,
#    "1":117,
#    "2":103,
#    "3":109,
#    "4":117,
#    "5":102
#  },
#  "Maxpulse":{
#    "0":130,
#    "1":145,
#    "2":135,
#    "3":175,
#    "4":148,
#    "5":127
#  },
#  "Calories":{
#    "0":409,
#    "1":479,
#    "2":340,
#    "3":282,
#    "4":406,
#    "5":300
#  }
#}

#df = pd.DataFrame(data)

#print(df) 


#rd = pd.read_csv('https://www.w3schools.com/python/pandas/data.csv.txt')
#new_df = rd.dropna() # boþ sütun varsa onu eleyerek yeniden gösterim
#print(new_df.to_string())


#rd = pd.read_csv('https://www.w3schools.com/python/pandas/data.csv.txt')
#rd.dropna(inplace = True) # NULL deðerleri olan tüm satýrlarý kaldýrýn:

#print(rd.to_string())

#df = pd.read_csv('https://www.w3schools.com/python/pandas/data.csv.txt')

#df.fillna(130, inplace = True)
#print(df.to_string())  # NULL deðerleri 130 sayýsýyla deðiþtirin:


#df = pd.read_csv('https://www.w3schools.com/python/pandas/data.csv.txt')
#df["Calories"].fillna(130, inplace = True)  # Kalori" sütunlarýndaki NULL deðerleri 
## 130 sayýsýyla deðiþtirin:
#print(df.to_string())


#df = pd.read_csv('https://www.w3schools.com/python/pandas/data.csv.txt')

#x = df["Calories"].mean()  # ORTALAMA'yý hesaplayýn ve boþ deðerleri onunla deðiþtirin
#y = df["Calories"].median() # Median'ý hesaplayýn ve boþ deðerleri onunla deðiþtirin
#z = df["Calories"].mode()[0] # Calculate the MODE, and replace any empty values with it
## mean ortalama demek 
#df["Calories"].fillna(x, inplace = True) 
