import numpy as np

def read_file(filename):
  file = open("src/"+filename,"r")
  coordenates = [coord.strip("\n").split("\t")[2:] for coord in file.readlines()[4:]]
  return coordenates

def apply_formula(X,Y):
  newX = int(35.5*float(X)+350)
  newY = int(-96*float(Y)+480)
  return newX,newY

def divide_coordenates(coordenates):
  XList = []
  YList = []
  ZList = []
  XYList = []
  for coor in coordenates:
    X,Y = apply_formula(coor[0],coor[1])
    XList.append(X)
    YList.append(Y)
    ZList.append(float(coor[2]))
    XYList.append((X,Y))
    
  return XList,YList,ZList,XYList

def identify_highest_frequency(XList,YList,ZList):
  uniqueX, Xfrequency = np.unique(XList,return_counts=True)
  uniqueY, Yfrequency = np.unique(YList,return_counts=True)
  uniqueZ, Zfrequency = np.unique(ZList,return_counts=True)

  print("Las coordenadas X que más se repiten:",uniqueX[Xfrequency==max(Xfrequency)],"con un recuento de",max(Xfrequency))
  print("Las coordenadas Y que más se repiten:",uniqueY[Yfrequency==max(Yfrequency)],"con un recuento de",max(Yfrequency))
  print("Las coordenadas Z que más se repiten:",uniqueZ[Zfrequency==max(Zfrequency)],"con un recuento de",max(Zfrequency))

def make_dictionary(array):
    dictionary = {}
    for xy in array:
      if xy not in dictionary:
        dictionary[xy] = 1
      else:
        dictionary[xy] += 1
    return dictionary
    
def get_highest_frequency(dictionary):
  sortedDictionary = dict(sorted(dictionary.items(), key=lambda x: x[1], reverse=True))

  highest_entries = dict(list(sortedDictionary.items())[:10])

  return highest_entries

def make_frequency_matrix(dictionary):
  frequency_matrix = np.zeros((640,480))
  for xy in dictionary.keys():
    x,y = xy
    frequency_matrix[x][y] = dictionary[xy]
  return frequency_matrix
    

def write_matrix(matrix):
  file = open("src/frequency_matrix.txt","w")
  count = 0
  for line in matrix:
    file.write(str(count)+str(line)+"\n")
    count+=1
  file.close()

def main():
  fileName = "UNI_CORR_500_01.txt"
  coordenates = read_file(fileName)
  XPixels, YPixels, ZList, XYList = divide_coordenates(coordenates)
  identify_highest_frequency(XPixels,YPixels,ZList)
  
  XYDictionary = make_dictionary(XYList)
  highest_frequencies = get_highest_frequency(XYDictionary)
  print(*highest_frequencies.items(), sep="\n")
  frequency_matrix = make_frequency_matrix(XYDictionary)
  
  write_matrix(frequency_matrix)
  
main()
  





