from math import sqrt 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import psutil,time,random
from scipy.spatial import KDTree
from scipy.optimize import curve_fit

#6194813
#146.83.128.60
random.seed(1)

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

def get_distance(x2,x1,y2,y1):
  return sqrt((x2-x1)**2+(y2-y1)**2)

def get_velocity(row,df):
    id = int(row["PersID"])
    frame = int(row["Frame"])
    group_data = df[df["PersID"] == id]
    
    if group_data["Frame"].min() == frame:
        return 0
    
    prev_data = group_data[group_data["Frame"] == frame - 1]
    prev_x = prev_data["X"].iloc[0]
    prev_y = prev_data["Y"].iloc[0]
    distancia = get_distance(row["X"],prev_x,row["Y"],prev_y)
    return distancia/0.04
    
def read_file(filename):
    dataFrame = pd.read_csv("src/data/"+filename,skiprows=3,sep="\t")
    dataFrame = dataFrame.rename(columns={
        "# PersID": "PersID"
    })
    return dataFrame

def read_modified_file(filename):
    modified_filename = filename.rstrip(".txt")+"_modified.txt"
    dataFrame = pd.read_csv("src/results/"+modified_filename,sep="\t")
    return dataFrame
    
def compare_histograms(df1, df2,fileName1,fileName2):
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    axes[0].hist2d(x=df1["Frame"], y=df1["Velocity"], bins=len(df1["Frame"].unique())//10)
    axes[0].set_xlabel("Frame")
    axes[0].set_ylabel("Velocity")
    axes[0].set_title(fileName1)
    
    axes[1].hist2d(x=df2["Frame"], y=df2["Velocity"], bins=len(df2["Frame"].unique())//10)
    axes[1].set_xlabel("Frame")
    axes[1].set_ylabel("Velocity")
    axes[1].set_title(fileName2)
    plt.savefig("images/"+"histogram_velocity_comparisson.png")
    plt.show()

def process_data(fileName):
    dataFrame = read_file(fileName)
    dataFrame["Velocity"] = dataFrame.apply(get_velocity, df=dataFrame, axis=1)
    dataFrame.to_csv("src/results/"+fileName.rstrip(".txt")+"_modified.txt",index=False,sep="\t")
    return dataFrame
    
def calculate_sk(fileName, dataframe, k):
    dataframe["Sk_Value"] = 0

    for i in dataframe["Frame"].unique():
        df = dataframe[dataframe["Frame"] == i].copy()
        coordenates = df[["X", "Y"]].values
        df["indexes"] = np.arange(len(df))

        for id in df["indexes"]:
            query_point = coordenates[id]

            tree = KDTree(coordenates)
            neighborsIndex = tree.query_ball_point(query_point, k)
            neighborsIndex = [index for index in neighborsIndex if index != id]
            neighborsFrame = coordenates[neighborsIndex]

            mean_sk = 0
            if len(neighborsIndex) > 0:
                distances = np.linalg.norm(neighborsFrame - query_point, axis=1)
                mean_sk = np.sum(distances) / len(neighborsIndex)

            filtered_index = df.index[df["indexes"] == id].values
            dataframe.at[int(filtered_index), "Sk_Value"] = mean_sk

    dataframe.to_csv("src/results/" + fileName.rstrip(".txt") + "_modified.txt", index=False, sep="\t")
    return dataframe
    
def main():
    files = {
        # Right to Left
        1:"UNI_CORR_500_01.txt", 
        2:"UNI_CORR_500_02.txt", 
        4:"UNI_CORR_500_04.txt", 
        6:"UNI_CORR_500_06.txt", 
        8:"UNI_CORR_500_08.txt",
        # Left to Right
        3:"UNI_CORR_500_03.txt",
        5:"UNI_CORR_500_05.txt",
        7:"UNI_CORR_500_07.txt",
        9:"UNI_CORR_500_09.txt"
    }
    
    fileName1 = files[1]
    fileName2 = files[5]
    
    dataFrame1 = read_modified_file(fileName1)
    dataFrame2 = read_modified_file(fileName2)

    dataFrame1 = calculate_sk(fileName1,dataFrame1,k=5)        

get_resource_info(main)