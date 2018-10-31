import cv2
import numpy as np
import matplotlib.pyplot as plt
import pydicom as pdicom
import os
import glob
import scipy.ndimage

def disp_pic(ArrayDicom, ConstPixelDim, ConstPixelSpacing):
    x = np.arange(0.0, (ConstPixelDim[0]+1)*ConstPixelSpacing[0], ConstPixelSpacing[0])
    y = np.arange(0.0, (ConstPixelDim[1]+1)*ConstPixelSpacing[1], ConstPixelSpacing[1])
    z = np.arange(0.0, (ConstPixelDim[2]+1)*ConstPixelSpacing[2], ConstPixelSpacing[2])
    #print(ArrayDicom.shape)
    plt.figure(dpi=1600)
    plt.axes().set_aspect('equal', 'datalim')
    plt.set_cmap(plt.gray())
    plt.pcolormesh(x, y, np.flipud(ArrayDicom[:, :, 0]))
    plt.show()

def load_scan2(path, name):
    lstFilesDCM = []
    for dirName, subdirList, fileList in os.walk(path, topdown=True):
        for filename in fileList:
            if '.dcm' in filename.lower() and name in os.path.join(dirName, filename):
                #print(os.path.join(dirName, filename))
                lstFilesDCM.append(os.path.join(dirName, filename))

    return lstFilesDCM

path = 'C:/Users/Windrich/MRI_Data/PROSTATEx/ProstateX-0199'

listFilesDCM = load_scan2(path, name="setra")  # get list of DCM files dir

# get reference file
RefDs = pdicom.read_file(listFilesDCM[0])
# Load dimensions based on the number of rows, columns, and slices
ConstPixelDim = (int(RefDs.Rows), int(RefDs.Columns), len(listFilesDCM)+1)
print(ConstPixelDim)
# Load spacing values in mm
ConstPixelSpacing = (float(RefDs.PixelSpacing[0]), float(RefDs.PixelSpacing[1]), float(RefDs.SliceThickness))

standardPixelDim = (384, 384, 26)
ArrayDicom = np.zeros(standardPixelDim, dtype=RefDs.pixel_array.dtype)
#ArrayDicom[:, :, 0] = RefDs.pixel_array
im = RefDs.pixel_array
im2 = np.zeros(ConstPixelDim)
im2[:, :, 0]= RefDs.pixel_array
print(ArrayDicom.shape)

if im.shape[0] != 384:  # downsample arraydicom if it's > 384 (usually 620)
    #ArrayDicom_downsample = ArrayDicom[::2, ::2, :]

    scale = 384/im.shape[0]
    ArrayDicom[:, :, 0] = scipy.ndimage.interpolation.zoom(im, [scale, scale])
    ArrayDicom_Orig = ArrayDicom
    disp_pic(ArrayDicom_Orig, standardPixelDim, ConstPixelSpacing)
    print("Array shape: " + str(ArrayDicom.shape))
    print(np.amax(ArrayDicom))
    #ArrayDicom[ArrayDicom>255] = 255
    ArrayDicom = ArrayDicom/1740*255
    print(np.amax(ArrayDicom))
    #print(ArrayDicom_downsample.shape)
    #print(ArrayDicom_downsample[:,:,0])

    # RefDs.PixelData = ArrayDicom_downsample.tobytes()
    # RefDs.Rows, RefDs.Columns, slices = ArrayDicom_downsample.shape
    # ConstPixelDim = (int(RefDs.Rows), int(RefDs.Columns), len(listFilesDCM)+1)
    # print(ConstPixelDim)
#
# print(ArrayDicom_downsample.shape)
# downsamplePixelDim = (ArrayDicom_downsample.shape[0], ArrayDicom_downsample.shape[1], ArrayDicom_downsample.shape[2])
#
# FinalArrayDicom = np.zeros(standardPixelDim, dtype=ArrayDicom_downsample.dtype)
# print(FinalArrayDicom.shape)
# FinalArrayDicom[:ArrayDicom_downsample.shape[0], :ArrayDicom_downsample.shape[1], :ArrayDicom_downsample.shape[2]] = ArrayDicom_downsample
# #print(FinalArrayDicom)
#
disp_pic(ArrayDicom, standardPixelDim, ConstPixelSpacing)
# #print(RefDs)


