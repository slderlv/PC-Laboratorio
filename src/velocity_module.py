from math import sqrt 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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
    
def get_frame_mean(frame_data):
    promedio = frame_data["Velocidad"].mean()
    frame = str(int(frame_data["Frame"].iloc[0]))
    return pd.Series({"Frame": frame, "Promedio_Velocidad": promedio})
        
def read_file(filename):
    dataFrame = pd.read_csv("src/data/"+filename,skiprows=3,sep="\t")
    dataFrame = dataFrame.rename(columns={
        "# PersID": "PersID"
    })
    return dataFrame



def main():
    filenames_right_to_left = ["UNI_CORR_500_01.txt", "UNI_CORR_500_02.txt", "UNI_CORR_500_04.txt", "UNI_CORR_500_06.txt", "UNI_CORR_500_08.txt"]
    filenames_left_to_right = ["UNI_CORR_500_03.txt","UNI_CORR_500_05.txt","UNI_CORR_500_07.txt","UNI_CORR_500_09.txt"]
    dataFrame = read_file(filenames_right_to_left[0])
    dataFrame["Velocity"] = dataFrame.apply(get_velocity, df=dataFrame, axis=1)
    dataFrame.plot.scatter(x="Frame",y="Velocity",c="DarkBlue",s=0.5)
    plt.show()
    print(dataFrame)

main()