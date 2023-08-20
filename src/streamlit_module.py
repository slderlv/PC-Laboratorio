import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
import numpy as np
from scipy.optimize import curve_fit 

fileName1 = "UNI_CORR_500_01_modified.txt"
fileName2 = "UNI_CORR_500_02_modified.txt"
df1 = pd.read_csv("C:/Users/vicen/OneDrive/Escritorio/Progra científica/Laboratorios/Lab01/src/results/UNI_CORR_500_01_modified.txt", sep="\t")
df2 = pd.read_csv("C:/Users/vicen/OneDrive/Escritorio/Progra científica/Laboratorios/Lab01/src/results/UNI_CORR_500_02_modified.txt", sep="\t")
st.write(f"""
# {fileName1}       
         """)
st.table(df1.head(5))
st.write(f"""
# {fileName2}         
         """)
st.table(df2.head(5))

def show_box_plot(df,fileName):
    random_ids = random.sample(list(df["PersID"]), 10)
    id_filter = df["PersID"].isin(random_ids)
    df = df.loc[id_filter]
    grouped_data = df.groupby("PersID")["Velocity"].apply(list)
    plt.boxplot(grouped_data)
    plt.xticks(range(1, len(grouped_data) + 1), grouped_data.index)
    plt.xlabel("PersID")
    plt.ylabel("Velocity")
    plt.title("Velocity by Frame ({})".format(fileName))
    #plt.savefig("C:/Users/vicen/OneDrive/Escritorio/Progra científica/Laboratorios/Lab01/images/velocity_boxplot.png")
    st.pyplot(plt)

def show_histogram(df):
    with st.sidebar:
        st.write("Opciones")
        div = st.slider("Número de bins (histograma):",20,250,20)
    plt.hist2d(x=df["Frame"],y=df["Velocity"],bins=div)
    plt.xlabel("Frame")
    plt.ylabel("Velocity")
    st.pyplot(plt)

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
        
        st.pyplot(fig)
        
        plt.pause(1/25)

def visualize_data_frames(data1, data2):
    with st.sidebar:
        st.write("Opciones")
        div = st.slider("Número de bins:",0,130,25)
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Histograma para el primer DataFrame
    freq_matrix1, x_edges1, y_edges1 = np.histogram2d(data1["X"], data1["Y"], bins=div)
    freq_matrix1 = freq_matrix1.transpose()
    im1 = axes[0].imshow(freq_matrix1, origin="lower", cmap="plasma", extent=[x_edges1[0], x_edges1[-1], y_edges1[0], y_edges1[-1]], interpolation="nearest", aspect="auto")
    axes[0].set_title("Matriz de Frecuencias - Data 1")
    axes[0].set_xlabel("X")
    axes[0].set_ylabel("Y")
    plt.colorbar(im1, ax=axes[0], label="Frecuencia")
    
    # Histograma para el segundo DataFrame
    freq_matrix2, x_edges2, y_edges2 = np.histogram2d(data2["X"], data2["Y"], bins=div)
    freq_matrix2 = freq_matrix2.transpose()
    im2 = axes[1].imshow(freq_matrix2, origin="lower", cmap="plasma", extent=[x_edges2[0], x_edges2[-1], y_edges2[0], y_edges2[-1]], interpolation="nearest", aspect="auto")
    axes[1].set_title("Matriz de Frecuencias - Data 2")
    axes[1].set_xlabel("X")
    axes[1].set_ylabel("Y")
    plt.colorbar(im2, ax=axes[1], label="Frecuencia")
    plt.tight_layout()
    #plt.savefig("images/" + "double_hist2d_main2.png")
    st.pyplot(plt)

def visualize_histogram(data):
    with st.sidebar:
        st.write("Opciones")
        div = st.slider("Número de bins:", 20, 200, 10)
    fig, ax = plt.subplots(figsize=(8, 6))
    
    freq_matrix, x_edges, y_edges = np.histogram2d(data["X"], data["Y"], bins=div)
    freq_matrix = freq_matrix.transpose()
    im = ax.imshow(freq_matrix, origin="lower", cmap="plasma", extent=[x_edges[0], x_edges[-1], y_edges[0], y_edges[-1]], interpolation="nearest", aspect="auto")
    ax.set_title("Matriz de Frecuencias")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    plt.colorbar(im, ax=ax, label="Frecuencia")
    plt.tight_layout()
    st.pyplot(plt)

def correlation(df1):
    fig, ax = plt.subplots()
    ax.scatter(df1["Velocity"], df1["Sk_Value"])
    ax.set_xlabel("Velocity")
    ax.set_ylabel("Sk_Value")
    ax.set_title("Correlación entre Velocity y Sk_Value")
    st.pyplot(fig)

def curve_func(x, a, b, c):
    return a * np.exp(-b * x) + c

def optimize_sk(df,fileName):
    x_data = df["Sk_Value"].values
    y_data = df["Velocity"].values

    params, covariance = curve_fit(curve_func, x_data, y_data)

    a_fit, b_fit, c_fit = params

    print(f"Parámetros ajustados: a={a_fit}, b={b_fit}, c={c_fit}")

    df["Velocity_Fitted"] = curve_func(x_data, a_fit, b_fit, c_fit)

    plt.scatter(x_data, y_data, label="Datos reales")
    plt.plot(x_data, df["Velocity_Fitted"], label="Valores ajustados", color="red")
    plt.xlabel("Sk_Value")
    plt.ylabel("Velocity")
    plt.legend()
    plt.title(f"Ajuste de curva para {fileName}")
    st.pyplot(plt)

show_box_plot(df1,fileName1)
show_histogram(df1)
correlation(df1)
optimize_sk(df1,fileName1)
#show_by_frame(df1)