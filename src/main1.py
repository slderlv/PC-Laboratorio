import numpy as np
import matplotlib.pyplot as plt
import psutil
import time

def get_resource_info(code_to_measure):
    resources_save_data = get_resource_usage(code_to_measure=code_to_measure)
    print(f"Tiempo de CPU: {resources_save_data['tiempo_cpu']} segundos")
    print(f"Uso de memoria virtual: {resources_save_data['memoria_virtual']} MB")
    print(f"Uso de memoria residente: {resources_save_data['memoria_residente']} MB")
    print(f"Porcentaje de uso de CPU: {resources_save_data['%_cpu']} %")

# Función que devuelve el tiempo de CPU y el uso de memoria para un código dado
def get_resource_usage(code_to_measure):
    process = psutil.Process()
    #get cpu status before running the code
    cpu_percent = psutil.cpu_percent()
    start_time = time.time()
    code_to_measure()
    end_time = time.time()
    end_cpu_percent = psutil.cpu_percent() 
    cpu_percent = end_cpu_percent - cpu_percent
    cpu_percent = cpu_percent / psutil.cpu_count()
    
    return {
        'tiempo_cpu': end_time - start_time,
        'memoria_virtual': process.memory_info().vms / (1024 * 1024),  # Convertir a MB
        'memoria_residente': process.memory_info().rss / (1024 * 1024),  # Convertir a MB
        '%_cpu': cpu_percent # Porcentaje de uso de CPU
    }


def read_file(filename):
    file = open("src/"+filename,"r")
    coordenates = [coord.strip("\n").split("\t")[2:] for coord in file.readlines()[4:]]
    return coordenates

def conversion(X,Y):
    newX = int(35.5*float(X)+320)
    newY = int(-96*float(Y))
    return newX,newY

def divide_coordenates(coordenates):
    XList = []
    YList = []
    ZList = []
    XYList = []
    for coor in coordenates:
      X,Y = conversion(coor[0],coor[1])
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

def visualize_data_frames(frequency_matrix1, frequency_matrix2):
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Histograma para el primer conjunto de datos
    im1 = axes[0].imshow(frequency_matrix1, origin="lower", cmap="plasma", interpolation="nearest", aspect="auto")
    axes[0].set_title("Matriz de Frecuencias - Data 1")
    axes[0].set_xlabel("X")
    axes[0].set_ylabel("Y")
    plt.colorbar(im1, ax=axes[0], label="Frecuencia")
    
    # Histograma para el segundo conjunto de datos
    im2 = axes[1].imshow(frequency_matrix2, origin="lower", cmap="plasma", interpolation="nearest", aspect="auto")
    axes[1].set_title("Matriz de Frecuencias - Data 2")
    axes[1].set_xlabel("X")
    axes[1].set_ylabel("Y")
    plt.colorbar(im2, ax=axes[1], label="Frecuencia")
    plt.tight_layout()
    plt.savefig("images/" + "double_hist2d_main1.png")
    plt.show()

def visualize_frequency_matrix(frequency_matrix):
    fig, ax = plt.subplots(figsize=(9, 6))
    x_edges = np.arange(0, frequency_matrix.shape[1] + 1)
    y_edges = np.arange(0, frequency_matrix.shape[0] + 1)
    im = ax.imshow(frequency_matrix, origin="lower", cmap="plasma", extent=[x_edges[0], x_edges[-1], y_edges[0], y_edges[-1]], interpolation="nearest", aspect="auto")
    plt.colorbar(im, label="Frecuencia")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Matriz de Frecuencias")
    plt.savefig("images/" + "hist2d_main1.png")
    plt.show()

def main():
    file_name1 = "UNI_CORR_500_01.txt"
    file_name2 = "UNI_CORR_500_02.txt"
    data_frame1 = read_file(file_name1)
    data_frame2 = read_file(file_name2)
    XPixels1, YPixels1, ZList1, XYList1 = divide_coordenates(data_frame1)
    XPixels2, YPixels2, ZList2, XYList2 = divide_coordenates(data_frame2)
    # identify_highest_frequency(XPixels,YPixels,ZList)
    
    XYDictionary1 = make_dictionary(XYList1)
    XYDictionary2 = make_dictionary(XYList2)
    
    # highest_frequencies1 = get_highest_frequency(XYDictionary1)
    # highest_frequencies2 = get_highest_frequency(XYDictionary2)
    # print(*highest_frequencies1.items(), sep="\n")
    # print(*highest_frequencies2.items(), sep="\n")
    
    frequency_matrix1 = make_frequency_matrix(XYDictionary1)
    frequency_matrix2 = make_frequency_matrix(XYDictionary2)
    frequency_matrix1 = np.rot90(frequency_matrix1)
    frequency_matrix2 = np.rot90(frequency_matrix2)
    combined_matrix = np.maximum(frequency_matrix1, frequency_matrix2)
      
    # write_matrix(frequency_matrix)
    visualize_data_frames(frequency_matrix1, frequency_matrix2)
    visualize_frequency_matrix(combined_matrix)
  
get_resource_info(main)
  




