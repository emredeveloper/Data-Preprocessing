import pandas as pd
import numpy as np

ilkindex = ["Simpson","Simpson","South Park","South Park"]
icindex = ["Homer","Bart","Cartman","Kenny "]
birlesmisindex = list(zip(ilkindex,icindex)) # indexleri birleştirdik
print(birlesmisindex)
birlesmisindex = pd.MultiIndex.from_tuples(birlesmisindex) # multiindexe çevirdik
print(birlesmisindex)

benimcizgifilmlsitem = [[40,"A"], [30,"B"],[20,"C"],[10,"E"]]
cizgifilmnumpy = np.array(benimcizgifilmlsitem) # numpya çevirme
print(cizgifilmnumpy)
cizgifilmdataframe = pd.DataFrame(cizgifilmnumpy,index= birlesmisindex,columns= ["Yas","Meslek"])
print(cizgifilmdataframe)
print(cizgifilmdataframe.loc["Simpson"])
print(cizgifilmdataframe.loc["South Park"].loc["Cartman"])