import pandas as pd
import numpy as np
import os
from PIL import Image

filename = "airplanes"

testkey = pd.read_csv('./data/archive/test.csv')
trainkey = pd.read_csv('./data/archive/train.csv')
validkey = pd.read_csv('./data/archive/val.csv')
key = pd.concat([testkey, trainkey, validkey])
key = key.sample(frac = 1)
print(key.nunique(dropna=True))

#modelList = ['737' '747' 'F-16']
modelList = ('707', '737','747', 'F-16', '727', '737', '747', '757', '767', '777', 'A300',
             'A310', 'A318', 'A319', 'A320', 'A321', 'A330', 'A340', 'A380', 'ATR', 'An',
             'BAE 146', 'BAE-125', 'Beechcraft 1900', 'Boeing 717', 'C-130', 'C-47', 'CRJ',
             'Cessna', 'Challenger', 'DC-3', 'DC-6', 'DC-8', 'DC-9', 'DH-82', 'DHC-1',
             'DHC-6', 'DHC-8', 'DR-400', 'Dornier 328', 'EMB-120', 'ERJ', 'Embraer Legacy',
             'Eurofighter Typhoon', 'F-16', 'F/A-18', 'Falcon', 'Fokker', 'Global Express',
             'Gulfstream', 'Hawk T1', 'II-76', 'L-1011', 'MD-11', 'MD-', 'Metroliner',
             'Model B200', 'PA-28', 'SR-20', 'Saab', 'Spitfire', 'Tornado', 'Tu-134', 'Tu-154',
             'Yak-42')
print(len(modelList))
tempkey = []
modelkey =[]
for i in range(len(key)): #CH-47, DC-3
  for j in range(len(modelList)):
    if modelList[j] in key.iloc[i]["Classes"]:
      if key.iloc[i]["Classes"] != 'MD-95':
        tempkey.append(list(key.iloc[i]))
        modelkey.append(modelList[j])
      else:
          tempkey.append(list(key.iloc[i]))
          modelkey.append('Boeing 717')
      break

key = pd.DataFrame(np.array(tempkey), columns = ['filename', 'Classes', 'Labels'])
key["model"] = modelkey




print(key)


newWidth = 300
newHeight = 300
outDir = './data/'+filename+'/'
for i in range(len(key)):
    srcFile = './data/archive/fgvc-aircraft-2013b/fgvc-aircraft-2013b/data/images/' + key.iloc[i]["filename"]
    img = Image.open(srcFile)
    img = img.resize((newWidth, newHeight), Image.Resampling.LANCZOS)

    destFile = outDir + key.iloc[i]["model"]
    destFile = destFile + '/'
    destFile = destFile + key.iloc[i]["filename"]
    os.makedirs(os.path.dirname(destFile), exist_ok=True)
    if os.path.exists(destFile):
        os.remove(destFile)
    img.save(destFile)

import os
import tarfile
tarFileName = './data/'+filename+'.tar'

def tardirectory(path,name):
   with tarfile.open(name, "w:gz") as tarhandle:
      for root, dirs, files in os.walk(path):
         for f in files:
            tarhandle.add(os.path.join(root, f))

tardirectory(outDir,tarFileName)