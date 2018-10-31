import cv2
import numpy as np
import matplotlib.pyplot as plt
import pydicom as pdicom
import os
import scipy.ndimage
#&matplotlib inline
import scipy.ndimage
import random
import csv

def load_scan2(path, name):
    lstFilesDCM = []
    for dirName, subdirList, fileList in os.walk(path, topdown=True):
        for filename in fileList:
            if '.dcm' in filename.lower() and name in os.path.join(dirName, filename):
                #print(os.path.join(dirName, filename))
                lstFilesDCM.append(os.path.join(dirName, filename))

    return lstFilesDCM


def get_curr_dicom_arr(dirname, standardPixelDim):
    name = "setra"  # type of MRI image to be included
    curr_patient = load_scan2(dirname, name)  # get list of DICOM file names + dir
    # print("No of DICOM files for curr patient: " + str(len(curr_patient)))

    # ds = pdicom.read_file(curr_patient[0])
    # CurrPixelDim = ds.Rows, ds.Columns, max_slice  # get pixel dimension using first file as reference
    # The Array is sized based on 'CurrPixelDim'
    ArrayDicom = np.zeros(standardPixelDim)

    # get image pixels into ArrayDicom
    for filenameDCM in curr_patient:
        # read file
        ds = pdicom.read_file(filenameDCM)
        # store the raw image data
        if ds.Rows != 384:
            im = ds.pixel_array
            scale = 384 / im.shape[0]
            ArrayDicom[:, :, curr_patient.index(filenameDCM)] = scipy.ndimage.interpolation.zoom(im, [scale, scale])
        else:
            ArrayDicom[:, :, curr_patient.index(filenameDCM)] = ds.pixel_array
    #print(ArrayDicom.shape)

    if len(curr_patient) < standardPixelDim[2]:
        # print("filling in slice number " + str(len(curr_patient)) + " to " + str(standardPixelDim[2]-1))
        for j in range(len(curr_patient), standardPixelDim[2]-1):
            num = random.randint(0, len(curr_patient))
            ArrayDicom[:, :, j] = ArrayDicom[:, :, num]


    # print("Shape of DICOM Array for curr patient: " + str(ArrayDicom.shape))
    # print("\n")

    return ArrayDicom


def disp_pic(ArrayDicom, ConstPixelDim, ConstPixelSpacing):
    x = np.arange(0.0, (ConstPixelDim[0]+1)*ConstPixelSpacing[0], ConstPixelSpacing[0])
    y = np.arange(0.0, (ConstPixelDim[1]+1)*ConstPixelSpacing[1], ConstPixelSpacing[1])
    z = np.arange(0.0, (ConstPixelDim[2]+1)*ConstPixelSpacing[2], ConstPixelSpacing[2])
    plt.figure(dpi=1600)
    plt.axes().set_aspect('equal', 'datalim')
    plt.set_cmap(plt.gray())
    plt.pcolormesh(x, y, np.flipud(ArrayDicom[:, :, 22, 98]))
    plt.show()


def getY(path):
    with open(path, 'r') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        data_train = {}
        data_test = {}
        idx = 0

        for row in readCSV:
            if row[0] == 'ProxID':
                continue
            else:
                if idx < 80:
                    if row[0] in data_train:
                        idx -=1
                        if (row[4]) > data_train[row[0]]:
                            data_train[row[0]] = row[4]
                    else:
                        data_train[row[0]] = row[4]
                else:
                    if row[0] in data_test:
                        idx -= 1
                        if (row[4]) > data_test[row[0]]:
                            data_test[row[0]] = row[4]
                    else:
                        data_test[row[0]] = row[4]
            idx += 1

        print(data_train)
        print(data_test)

        Y_Train = np.fromiter(data_train.values(), dtype=int)
        Y_Test = np.fromiter(data_test.values(), dtype=int)
        print("size of Y_Train: " + str(len(Y_Train)) + ", size of Y_Test: " + str(len(Y_Test)))
        # print(Y_Train)
        # print(Y_Test)

        return Y_Train, Y_Test

def load_dataset():
    INPUT_FOLDER = 'C:/Users/Windrich/MRI_Data/PROSTATEx/'
    patients = os.listdir(INPUT_FOLDER)
    patients.sort()
    #print(len(patients))

    first_patient = load_scan2(INPUT_FOLDER + "ProstateX-0000/", name="setra")
    # get reference file
    RefDs = pdicom.read_file(first_patient[0])
    #print(RefDs)
    # Load dimensions based on the number of rows, columns, and slices
    ConstPixelDim = (int(RefDs.Rows), int(RefDs.Columns), 26)
    #print(ConstPixelDim)
    # Load spacing values in mm
    ConstPixelSpacing = (float(RefDs.PixelSpacing[0]), float(RefDs.PixelSpacing[1]), float(RefDs.SliceThickness))
    # print(ConstPixelSpacing)


    max_slice = 26
    TrainPixelDim = (int(RefDs.Rows), int(RefDs.Columns), max_slice, len(patients)-19)
    TestPixelDim = (int(RefDs.Rows), int(RefDs.Columns), max_slice, 19)
    X_Train = np.zeros(TrainPixelDim)
    X_Test = np.zeros(TestPixelDim)

    patient_dir = 'C:/Users/Windrich/MRI_Data/PROSTATEx/'
    index = 0
    for i in range(0, 204):  # bcs there patient IDs go up to 203
        if i < 10:
            idx = "ProstateX-000" + str(i)
        elif i < 100:
            idx = "ProstateX-00" + str(i)
        else:
            idx = "ProstateX-0" + str(i)

        if idx in patients:  # check if current patient ID exists
            curr_dir = patient_dir + idx
            # call function to get dicom array for current patient
            # print("Patient ID: " + id + " index: " + str(index))
            curr_dicom_arr = get_curr_dicom_arr(curr_dir, ConstPixelDim)

            if index < 80:
                X_Train[:, :, :, index] = curr_dicom_arr
            else:
                index = 0
                X_Test[:, :, :, index] = curr_dicom_arr
            index += 1

    print("Final Shape of X_Train: " + str(X_Train.shape))
    print("Final Shape of X_Test: " + str(X_Test.shape))
    #disp_pic(all_dicom_arr, ConstPixelDim, ConstPixelSpacing)

    path = "C:/Users/Windrich/MRI_Data/ProstateX-2-Findings-Train.csv"
    # max = np.amax(X_Train)
    # print("MAX: " + str(max))
    # print("Mean: " + str(np.mean(X_Train)))
    # print("Median: " + str(np.median(X_Train)))
    # print("Min: " + str(np.min(X_Train)))

    Y_Train, Y_Test = getY(path)
    Y_Train = Y_Train.reshape(1, Y_Train.shape[0])
    Y_Test = Y_Test.reshape(1, Y_Test.shape[0])
    # print("Y_Train: " + str(Y_Train))
    print("Final shape of Y: " + str(Y_Train.shape))
    # print("Y_Test: " + str(Y_Test))
    print("Final shape of Y: " + str(Y_Test.shape))

    return X_Train, X_Test, Y_Train, Y_Test


# X_Train, X_Test, Y_Train, Y_Test = load_dataset()