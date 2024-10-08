# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 16:57:59 2024

@author: malo.delacour
"""

import numpy as np
import matplotlib.pyplot as plt
import laspy
from laspy import lasappender
import pyCloudCompare as cc
import open3d as o3d
import glob
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

def las2np(las):
    
    n = len(las.points)
    # features = ['x', 'y', 'z', 'intensity', 'return_number', 'number_of_returns', 
    #             'scan_angle_rank', 'gps_time', 'red', 'green', 'blue', 'ground_truth']
    
    # features = ['x', 'y', 'z', 'intensity', 'return_number', 'number_of_returns', 
    #             'scan_angle_rank', 'red', 'green', 'blue', 'ground_truth']
    
    features = ['classification']
    
    np_pc = np.zeros((n, 1))
    
    for feature in  features:
        pc_feature = np.array(las[feature]).reshape((n, 1))
        np_pc = np.hstack((np_pc, pc_feature))
        
    return np_pc[:, 1:].reshape((1, n))



"""
idir = 'D:\\data\\superpoint _T\\pred\\PREDI\\'

files = sorted(glob.glob(f'{idir}*.las'))

for file in files:

    lablas = laspy.read(file)
    lablas = las2np(lablas)
    nb_list = []
    
    for i in range (13):
    
        nb = np.count_nonzero(lablas == i)
        nb_list.append(nb)
        
    print(nb_list)"""

# features = lablas.point_format.dimension_names

# # Afficher la liste des features
# print("Liste des features du nuage de points :")
# for feature in features:
#     print(feature)

cm_full = np.array([[24504, 0, 0, 0, 559, 5122, 17, 446, 0, 0, 0, 0, 269],
    [0, 29154, 0, 0, 41, 0, 0, 0, 0, 0, 0, 0, 0],
    [36, 0, 18876, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [12, 45, 0, 228, 35, 0, 0, 0, 0, 0, 0, 0, 0],
    [33, 7, 0, 0, 324, 0, 0, 0, 0, 0, 0, 0, 0],
    [59, 0, 0, 0, 0, 3899975, 977862, 185127, 0, 0, 0, 0, 0],
    [267, 0, 0, 0, 0, 292829, 1321937, 177650, 173, 0, 0, 0, 0],
    [301, 0, 0, 0, 0, 55041, 107128, 2577496, 21, 0, 0, 0, 3],
    [0, 0, 0, 0, 0, 0, 423, 5716, 494, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 65, 183021, 0, 0, 0, 0, 438],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [104, 0, 0, 0, 0, 6677, 0, 1957, 0, 0, 0, 0, 110],
    [87, 0, 0, 0, 0, 1057, 14460, 52376, 41, 0, 0, 0, 116]])

cm = cm_full[:13, :]

class_name = ['Pylône', 'Conducteur', 'Câble de garde', 'Fixation', 'Isolateur', 'Végé haute', 'Végé basse', 
              'Pelouse', 'Rochers', 'Gravier', 'Routes', 'Eau', 'Bâtiment']

# Normalize the confusion matrix
cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

# Plot the confusion matrix with percentages
fig, ax = plt.subplots()
im = ax.imshow(cm_normalized, interpolation='nearest', cmap=plt.cm.Blues)
ax.figure.colorbar(im, ax=ax)

# We want to show all ticks and label them with the respective list entries
ax.set(xticks=np.arange(cm.shape[1]),
       yticks=np.arange(cm.shape[0]),
       xticklabels=class_name, yticklabels=class_name,
       title='Matrice de confusion normalisée',
       ylabel='Vérité terrain',
       xlabel='Prédiction')

# Rotate the tick labels and set their alignment
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

# Loop over data dimensions and create text annotations
fmt = '.2f'
thresh = cm_normalized.max() / 2.
for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        ax.text(j, i, format(cm_normalized[i, j], fmt),
                ha="center", va="center",
                color="white" if cm_normalized[i, j] > thresh else "black")
fig.tight_layout()
plt.show()











# lablas = laspy.read(in_dir)
# lablas = las2np(lablas)
# lab_sorted = np.lexsort((lablas[:, 2], lablas[:, 1], lablas[:, 0]))
