from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import psutil
import time
import random
from scipy.spatial import KDTree
from scipy.optimize import curve_fit

# 6194813
# 146.83.128.60
random.seed(1)

# def get_resource_info(code_to_measure):
#     resources_save_data = get_resource_usage(code_to_measure=code_to_measure)
#     print(f"Tiempo de CPU: {resources_save_data['tiempo_cpu']} segundos")
#     print(f"Uso de memoria virtual: {resources_save_data['memoria_virtual']} MB")
#     print(f"Uso de memoria residente: {resources_save_data['memoria_residente']} MB")
#     print(f"Porcentaje de uso de CPU: {resources_save_data['%_cpu']} %")

# # Función que devuelve el tiempo de CPU y el uso de memoria para un código dado
# def get_resource_usage(code_to_measure):
#     process = psutil.Process()
#     #get cpu status before running the code
#     cpu_percent = psutil.cpu_percent()
#     start_time = time.time()
#     code_to_measure()
#     end_time = time.time()
#     end_cpu_percent = psutil.cpu_percent()
#     cpu_percent = end_cpu_percent - cpu_percent
#     cpu_percent = cpu_percent / psutil.cpu_count()

#     return {
#         'tiempo_cpu': end_time - start_time,
#         'memoria_virtual': process.memory_info().vms / (1024 * 1024),  # Convertir a MB
#         'memoria_residente': process.memory_info().rss / (1024 * 1024),  # Convertir a MB
#         '%_cpu': cpu_percent # Porcentaje de uso de CPU
#     }


def compare_histograms(df1, df2, fileName1, fileName2):
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    axes[0].hist2d(x=df1["Frame"], y=df1["Velocity"],
                   bins=len(df1["Frame"].unique())//10)
    axes[0].set_xlabel("Frame")
    axes[0].set_ylabel("Velocity")
    axes[0].set_title(fileName1)

    axes[1].hist2d(x=df2["Frame"], y=df2["Velocity"],
                   bins=len(df2["Frame"].unique())//10)
    axes[1].set_xlabel("Frame")
    axes[1].set_ylabel("Velocity")
    axes[1].set_title(fileName2)
    plt.savefig("../images/"+"histogram_velocity_comparisson.png")
    plt.show()


def get_distance(x2, x1, y2, y1):
    return sqrt((x2-x1)**2+(y2-y1)**2)


def get_velocity(row, df):
    id = int(row["PersID"])
    frame = int(row["Frame"])
    group_data = df[df["PersID"] == id]

    if group_data["Frame"].min() == frame:
        return 0

    prev_data = group_data[group_data["Frame"] == frame - 1]
    prev_x = prev_data["X"].iloc[0]
    prev_y = prev_data["Y"].iloc[0]
    distancia = get_distance(row["X"], prev_x, row["Y"], prev_y)
    return distancia/0.04


def read_file(filename):
    dataFrame = pd.read_csv("./data/"+filename, skiprows=3, sep="\t")
    dataFrame = dataFrame.rename(columns={
        "# PersID": "PersID"
    })
    return dataFrame


def read_modified_file(filename):
    modified_filename = filename.rstrip(".txt")+"_modified.txt"
    dataFrame = pd.read_csv("./results/"+modified_filename, sep="\t")
    return dataFrame


def process_data(fileName):
    dataFrame = read_file(fileName)
    dataFrame["Velocity"] = dataFrame.apply(get_velocity, df=dataFrame, axis=1)
    dataFrame.to_csv("./results/"+fileName.rstrip(".txt") +
                     "_modified.txt", index=False, sep="\t")
    return dataFrame


def calculate_sk(fileName, dataframe, k):
    # Crear una copia del DataFrame para las modificaciones
    updated_dataframe = dataframe.copy()
    updated_dataframe["Sk_Value"] = 0

    for i in updated_dataframe["Frame"].unique():
        df = updated_dataframe[updated_dataframe["Frame"] == i].copy()
        coordenates = df[["X", "Y"]].values
        df["indexes"] = np.arange(len(df))

        tree = KDTree(coordenates)

        for id in df["indexes"]:
            query_point = coordenates[id]

            neighborsIndex = tree.query_ball_point(query_point, k)
            neighborsIndex = [index for index in neighborsIndex if index != id]
            neighborsFrame = coordenates[neighborsIndex]

            mean_sk = 0
            if len(neighborsIndex) > 0:
                distances = np.linalg.norm(
                    neighborsFrame - query_point, axis=1)
                mean_sk = np.sum(distances) / len(neighborsIndex)

            filtered_index = df[df["indexes"] == id].index
            if len(filtered_index) > 0:
                index_to_update = filtered_index[0]
                updated_dataframe.loc[index_to_update, "Sk_Value"] = mean_sk

    output_filename = "./data/" + fileName.rstrip(".txt") + "_modified.txt"
    updated_dataframe.to_csv(output_filename, index=False, sep="\t")
    return updated_dataframe


def show_sk_vel_graph(df, id_person):

    df = df[df["PersID"] == id_person]
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(df["Velocity"], df["Sk_Value"], marker='^')
    ax.set_xlabel("Velocity")
    ax.set_ylabel("Sk_Value")
    ax.set_title("Correlación entre Velocity y Sk_Value")
    plt.savefig("../images/"+"sk_vel_graph.png")
    plt.show()


def get_most_repited(df):
    ids = df['PersID']

    idss, frecuency = np.unique(ids, return_counts=True)
    indice_valor_max = np.argmax(frecuency)
    return idss[indice_valor_max]


def main():
    files = {
        # Right to Left
        1: "UNI_CORR_500_01.txt",
        2: "UNI_CORR_500_02.txt",
        4: "UNI_CORR_500_04.txt",
        6: "UNI_CORR_500_06.txt",
        8: "UNI_CORR_500_08.txt",
        # Left to Right
        3: "UNI_CORR_500_03.txt",
        5: "UNI_CORR_500_05.txt",
        7: "UNI_CORR_500_07.txt",
        9: "UNI_CORR_500_09.txt"
    }

    fileName1 = files[1]
    fileName2 = files[2]
    fileName3 = files[3]
    fileName4 = files[4]
    fileName5 = files[5]
    fileName6 = files[6]
    fileName7 = files[7]
    fileName8 = files[8]
    fileName9 = files[9]
    df = read_modified_file(fileName5)

    id_person = get_most_repited(df)

    show_sk_vel_graph(df, id_person)


main()
