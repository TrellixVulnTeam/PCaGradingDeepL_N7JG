import cv2
import numpy as np
import matplotlib.pyplot as plt
import pydicom as pdicom
import os
import glob
import csv

path = "C:/Users/Windrich/MRI_Data/ProstateX-2-Findings-Train.csv"

with open(path, 'r') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    ids = []
    data = {}

    for row in readCSV:
        if row[0] == 'ProxID':
            continue
        else:
            if row[0] in data:
                if (row[4]) > data[row[0]]:
                    data[row[0]] = row[4]
            else:
                data[row[0]] = row[4]

    print(data)

    Y = list(data.values())
    print(Y)