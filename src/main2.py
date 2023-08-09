import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import psutil

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
  file = pd.read_csv("src/"+filename,skiprows=3,sep="\t")
  file = file.rename(columns={
    "# PersID": "PersID",
  })
  return file

def load_data():
  file_name1 = "UNI_CORR_500_01.txt"
  file_name2 = "UNI_CORR_500_02.txt"
  file1 = read_file(file_name1)
  file2 = read_file(file_name2)
  return pd.concat([file1, file2],ignore_index=True)

def conversion(x, y):
    px = 320 + 35.5 * float(x)
    py = 96 * float(y)
    return pd.Series({"X": int(px), "Y": int(py)})

def write_matrix(matrix):
  file = open("src/frequency_matrix.txt","w")
  count = 0
  for line in matrix:
    file.write(str(count)+str(line)+"\n")
    count+=1
  file.close()

def main():
  data = load_data()
  data[["X", "Y"]] = data.apply(lambda row: conversion(row["X"], row["Y"]), axis=1)
  fig, ax = plt.subplots(figsize=(9, 6))
  freq_matrix, x_edges, y_edges = np.histogram2d(data["X"], data["Y"], bins=80)
  freq_matrix = freq_matrix.transpose()
  write_matrix(freq_matrix)
  im = ax.imshow(freq_matrix, origin="lower", cmap="plasma", extent=[x_edges[0], x_edges[-1], y_edges[0], y_edges[-1]], interpolation="nearest", aspect="auto")
  plt.colorbar(im, label="Frecuencia")
  plt.xlabel("X")
  plt.ylabel("Y")
  plt.title("Matriz de Frecuencias")
  plt.show()
  
get_resource_info(main)
  





