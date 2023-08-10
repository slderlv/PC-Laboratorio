import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import psutil
from math import sqrt

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
  return file1,file2

def visualize_data_frames(data1, data2):
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Histograma para el primer DataFrame
    freq_matrix1, x_edges1, y_edges1 = np.histogram2d(data1["X"], data1["Y"], bins=80)
    freq_matrix1 = freq_matrix1.transpose()
    im1 = axes[0].imshow(freq_matrix1, origin="lower", cmap="plasma", extent=[x_edges1[0], x_edges1[-1], y_edges1[0], y_edges1[-1]], interpolation="nearest", aspect="auto")
    axes[0].set_title("Matriz de Frecuencias - Data 1")
    axes[0].set_xlabel("X")
    axes[0].set_ylabel("Y")
    plt.colorbar(im1, ax=axes[0], label="Frecuencia")
    
    # Histograma para el segundo DataFrame
    freq_matrix2, x_edges2, y_edges2 = np.histogram2d(data2["X"], data2["Y"], bins=80)
    freq_matrix2 = freq_matrix2.transpose()
    im2 = axes[1].imshow(freq_matrix2, origin="lower", cmap="plasma", extent=[x_edges2[0], x_edges2[-1], y_edges2[0], y_edges2[-1]], interpolation="nearest", aspect="auto")
    axes[1].set_title("Matriz de Frecuencias - Data 2")
    axes[1].set_xlabel("X")
    axes[1].set_ylabel("Y")
    plt.colorbar(im2, ax=axes[1], label="Frecuencia")
    plt.tight_layout()
    plt.savefig("images/" + "double_hist2d_main2.png")
    plt.show()

def visualize_frequency_matrix(data):
    fig, ax = plt.subplots(figsize=(9, 6))
    freq_matrix, x_edges, y_edges = np.histogram2d(data["X"], data["Y"], bins=80)
    freq_matrix = freq_matrix.transpose()
    im = ax.imshow(freq_matrix, origin="lower", cmap="plasma", extent=[x_edges[0], x_edges[-1], y_edges[0], y_edges[-1]], interpolation="nearest", aspect="auto")
    plt.colorbar(im, label="Frecuencia")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Matriz de Frecuencias")
    plt.savefig("images/" + "hist2d_main2.png")
    plt.show()  

def conversion(x, y):
    px = 320 + 35.5 * float(x)
    py = 96 * float(y)
    return int(px), int(py)

def get_distance(x1, y1, x2, y2):
    return sqrt((x2-x1)**2 + (y2-y1)**2)

def get_velocity(row, data):
    if row["Frame"] == data.loc[data["PersID"] == row["PersID"], "Frame"].min():
        return 0
    prev_row = data[(data["PersID"] == row["PersID"]) & (data["Frame"] == row["Frame"] - 1)]
    if not prev_row.empty:
        x_distance = row["X"] - prev_row["X"].iloc[0]
        y_distance = row["Y"] - prev_row["Y"].iloc[0]
        distance = sqrt(x_distance**2 + y_distance**2)
        velocity = distance / 0.01
    else:
        velocity = 0
    return velocity


def generate_frame_points(data):
    unique_frames = data['Frame'].unique()
    frame_points = []

    for frame_number in unique_frames:
        frame_data = data[data['Frame'] == frame_number]
        frame_points.append((frame_number, frame_data[['X', 'Y']].values))

    return frame_points

def show_by_frame(data):
    fig, ax = plt.subplots()
    ax.set_xlim(100, 500)
    ax.set_ylim(0, 500)
    
    x_ticks = np.arange(100, 501, 50)
    y_ticks = np.arange(0, 501, 50)
    
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)
    
    frame_points = generate_frame_points(data)
    
    for frame_number, points in frame_points:
        ax.clear()
        ax.set_title(f"Frame: {frame_number}")
        
        ax.scatter(points[:, 0], points[:, 1], c='blue', label='Coordenada')
        
        ax.set_xticks(x_ticks)
        ax.set_yticks(y_ticks)
        
        plt.pause(1/25)


def main():  
    data_frame1, data_frame2 = load_data()
    data_frame1[["X", "Y"]] = data_frame1.apply(lambda row: conversion(row["X"], row["Y"]), axis=1).tolist()
    data_frame2[["X", "Y"]] = data_frame2.apply(lambda row: conversion(row["X"], row["Y"]), axis=1).tolist()
    data = pd.concat([data_frame1, data_frame2])
    show_by_frame(data)
    # visualize_data_frames(data_frame1, data_frame2)
    # visualize_frequency_matrix(data)
    # data.sort_values(by=["PersID", "Frame"])
    # data["Velocity"] = data.apply(lambda row: get_velocity(row, data), axis=1)
    
get_resource_info(main)