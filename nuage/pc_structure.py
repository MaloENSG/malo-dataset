# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 10:32:42 2024

@author: malo de lacour
"""

import numpy as np
import matplotlib.pyplot as plt
import laspy
from laspy import lasappender
import pyCloudCompare as cc
import open3d as o3d
import glob

# path_las1 = 'D:\\DL\\31_1.las'
# path_las2 = 'D:\\DL\\31_2.las'

# output_las_path = 'D:\\DL\\31_test2.las'

# path_80 = 'D:\\DL\\81.las'
# outlas = 'D:\\DL\\tiled\\'

###################
###################

# las = laspy.read(path_las1)
# las2 = laspy.read(path_las2)

# # with laspy.open(path_las1) as f:
# #     for points in f.chunk_iterator(1_000_000):
# #         las2.


# name = las.point_format.dimension_names
# for n in name:
#     print(n)


# outlas = laspy.LasData(las.header)

# las = laspy.read(path_las1)
# las2 = laspy.read(path_las2)

#################### Fonctions de bases ####################

def view_features(las):
    
    name = las.point_format.dimension_names
    for n in name:
        print(n)

def merge(inlas_lst, outlas):
    """
    Fusion de nuage de points.
    Perte du géoréférencement ->> à revoir

    """
    
    # Creation d'un las vide
    las1 = laspy.read(inlas_lst[0])
    new_las = laspy.create(point_format=las1.point_format)
    new_las.write(outlas)
    
    # Ouverture de ce las vide en mode appending
    with laspy.open(outlas, mode='a') as out:
        for inlas_file in inlas_lst:
            
            # Test du las à ajouter par rapport au premier de la liste
            las_to_add = laspy.read(inlas_file)
            if las1.point_format != las_to_add.point_format:
                print(inlas_file)
                raise ValueError("Les formats de point des deux fichiers LAS ne sont pas compatibles.")
            
            # Ajout du las au las créé
            with laspy.open(inlas_file) as inlas:
                for points in inlas.chunk_iterator(2_000_000):
                    out.append_points(points)

def add_tag(las, value):
    """
    Ajoute une nouvelle dimension "ground_truth" à un fichier LAS/LAZ avec une valeur constante.

    Cette fonction prend un objet LAS (ou LAZ) et ajoute une nouvelle dimension nommée "ground_truth".
    Elle remplit cette dimension avec la même valeur pour tous les points du fichier.

    Parameters
    ----------
    las : laspy.LasData
        L'objet LAS/LAZ représentant un nuage de points.
    value : int
        La valeur à associer à la nouvelle dimension "ground_truth" pour chaque point du nuage.

    Returns
    -------
    las : laspy.LasData
        L'objet LAS modifié avec la nouvelle dimension "ground_truth" ajoutée.

    """
    
    new_dimension_name = 'ground_truth'
    nb_pts = len(las.points)
    new_feature_values = np.full((nb_pts,), value)
    las.add_extra_dim(laspy.ExtraBytesParams(name=new_dimension_name, type=np.int32))
    las[new_dimension_name] = new_feature_values 
    
    return las
    
def las2np(las):
    """
    Convertit un objet LAS/LAZ en un tableau NumPy contenant des caractéristiques sélectionnées du nuage de points.

    Cette fonction extrait les caractéristiques spécifiques du fichier LAS/LAZ et les stocke dans un tableau NumPy. 
    Les p caractéristiques actuellement extraites sont définit par features.


    Parameters
    ----------
    las : laspy.LasData
        L'objet LAS/LAZ représentant un nuage de points.

    Returns
    -------
    np.ndarray
        Un tableau NumPy de forme (n, 7) où n est le nombre de points dans le nuage et p le nombre de feature pour chaque point.

    """
    # features = ['x', 'y', 'z', 'intensity', 'return_number', 'number_of_returns', 
    #             'scan_angle_rank', 'red', 'green', 'blue', 'ground_truth']
    
    features = ['x', 'y', 'z', 'red', 'green', 'blue', 'ground_truth']
    
    n = len(las.points)
    np_pc = np.zeros((n, 1))
    
    for feature in  features:
        pc_feature = np.array(las[feature]).reshape((n, 1))
        np_pc = np.hstack((np_pc, pc_feature))
        
    return np_pc[:, 1:]

def las_stat(las):
    """
    Calcule la répartition des points dans un nuage de points LAS/LAZ en fonction des valeurs de "ground_truth".

    Cette fonction analyse la dimension "ground_truth" d'un fichier LAS/LAZ et compte le nombre de points 
    associés à chaque tag prédéfini. Elle renvoie un tableau NumPy contenant les décomptes de points pour chaque 
    tag.

    Parameters
    ----------
    las : laspy.LasData
        L'objet LAS/LAZ contenant les points et la dimension "ground_truth".

    Returns
    -------
    np.ndarray
        Un tableau NumPy où chaque élément représente le nombre de points correspondant à un 
        tag de la liste `tags`..
        
    Notes:
        - La fonction utilise une liste prédéfinie de `tags` à adapter selon la nomenclature.
        - Assurez-vous que la dimension "ground_truth" existe dans l'objet LAS avant d'appeler cette fonction.
    """
    
    tags = [1, 11, 12, 13, 14, 21, 22, 23, 31, 32, 33, 34, 41, 51, 52, 53, 61, 62, 70, 80, 90, 91, 92, 93, 99]
    pt_count = []
    
    for tag in tags:
        tag_count = np.sum(las.ground_truth==tag)
        pt_count.append(tag_count)
        
    return np.array(pt_count)

#################### Découpage en tuiles ####################

# 10 à 15 m ??
tilesize = 10
treshold = 1000

def split_las(las, outpath, tilesize, treshold):
    
    x_min, y_min = las.x.min(), las.y.min()
    x_max, y_max = las.x.max(), las.y.max()
    
    i = x_min
    while i < x_max :
        j = y_min
        while j < y_max :
            
            # Création de la tuile
            new_las = laspy.LasData(las.header)
            mask_x = (las.x >= i) & (las.x < i+tilesize)
            mask_y = (las.y >= j) & (las.y < j+tilesize)
            new_las.points = las.points[mask_x&mask_y]
            
            # Sauvegarde des las assez grands
            if len(new_las.points) > treshold :
                new_las.write(outpath + str(int(i))[2:] + '_' + str(int(j))[3:] + '.las')
                
            j += tilesize
        i += tilesize
        
##########
        
def split_n_convert(las, outpath, tilesize, treshold):
    
    x_min, y_min = las.x.min(), las.y.min()
    x_max, y_max = las.x.max(), las.y.max()
    
    i = x_min
    while i < x_max :
        j = y_min
        while j < y_max :
            
            # Création de la tuile
            new_las = laspy.LasData(las.header)
            mask_x = (las.x >= i) & (las.x < i+tilesize)
            mask_y = (las.y >= j) & (las.y < j+tilesize)
            new_las.points = las.points[mask_x&mask_y]
            
            # Sauvegarde des las assez grands
            if len(new_las.points) > treshold :
                
                new_np = las2np(new_las)
                np.savez_compressed(outpath + str(int(i))[2:] + '_' + str(int(j))[3:] + '.npz', new_np)
                
                
                # new_las.write(outpath + str(int(i))[2:] + '_' + str(int(j))[3:] + '.las')
                
            j += tilesize
        i += tilesize    
    
##########

def split_n_convert2(las, outpath, tilesize, treshold, name_dataset):
    
    arrays_dict = {}
    name = 0
    
    x_min, y_min = las.x.min(), las.y.min()
    x_max, y_max = las.x.max(), las.y.max()
    
    i = x_min
    while i < x_max :
        j = y_min
        while j < y_max :
            
            # Création de la tuile
            new_las = laspy.LasData(las.header)
            mask_x = (las.x >= i) & (las.x < i+tilesize)
            mask_y = (las.y >= j) & (las.y < j+tilesize)
            new_las.points = las.points[mask_x&mask_y]
            
            # Sauvegarde des las assez grands
            if len(new_las.points) > treshold :
                
                array_name = f"array_{name}"
                name += 1
                arrays_dict[array_name] = las2np(new_las)
                print(name)
                stats = las_stat(new_las)
                with open(outpath + 'arrays_info_' + name_dataset +'.txt', 'a') as file:
                    count = ';'.join(map(str, stats))
                    file.write(count + "\n")
                    # file.write(f"{stats}\n")
                
                # np.savez_compressed(outpath + str(int(i))[2:] + '_' + str(int(j))[3:] + '.npz', new_np)
                # new_las.write(outpath + str(int(i))[2:] + '_' + str(int(j))[3:] + '.las')
                
            j += tilesize
        i += tilesize    
        
    np.savez_compressed(outpath+'ds_zone8_' + name_dataset + '.npz', **arrays_dict)

#################### Traitement de nuages ####################


###
idir = 'D:\\data\\superpoint _T\\pred\VT\\'

# oodir = 'D:\\data\\arolla_dataset\\label\\T1zone5A\\t1z5a.las'

def set_subcloud_gt(idir) :
    """
    Ajouter l'attribut ground truth aux sous nuages de points

    Parameters
    ----------
    idir : str
        Chemin du dossier contenant les sous nuages

    Returns
    -------
    None.

    """

    files = sorted(glob.glob(f'{idir}*.las'))
    for file in files:
        
        # Récupération de l'id classe
        tag_nb = int(file[len(idir):len(idir)+2])
        print(tag_nb)
        
        # Vérification format et taille
        las = laspy.read(file)
        print(' __ ', las.point_format.size, las.point_format)
        
        # Ajout de l'attribut et réécriture du fichier
        las = add_tag(las, tag_nb)
        las.write(file)


###

# in_dir = 'D:\\data\\arolla_dataset\\label\\T1zone4\\t1z4.las'
# out_dir = 'D:\\data\\arolla_dataset\\label\\T1zone4\\'

# las = laspy.read(in_dir)
# split_n_convert2(las, out_dir, 10, 2000, 'T1Zone4')




# num = 6
for num in range(7, 15):
    anno = 'Annotations'
    subarea = f'subarea_{num}'
    area = 'Area_2'
    
    in_dir = f'D:\\data\\arolla_dataset\\tranches_las\\t1zone4\\p{num}.las'
    out_dir = 'D:\\data\\maloDataset\\'
    
    # tags = [1, 11, 12, 13, 14, 21, 22, 23, 31, 32, 33, 34, 41, 51, 52, 53, 61, 62, 70, 80, 90, 91, 92, 93]
    tags = [21, 22, 23, 51, 52, 53, 61, 62, 70, 80, 90]
    fmt = ['%.2f', '%.2f', '%.2f', '%d', '%d', '%d']
    
    las = laspy.read(in_dir)
    lasnp = las2np(las)
    lasnp = lasnp[lasnp[:, -1] != 99]
    
    ####################
    # Centrage des coordonnées et mappage des couleurs
    xmean, ymean = lasnp[:, 0].mean(), lasnp[:, 1].mean()
    zmin = lasnp[:, 2].min()
    
    lasnp[:, 0] = (lasnp[:, 0] - xmean) #x
    lasnp[:, 1] = (lasnp[:, 1] - ymean) #y
    lasnp[:, 2] = (lasnp[:, 2] - zmin) #z zmin and not zmean!
    
    lasnp[:, 3] = (lasnp[:, 3] / 65280 * 255).astype(np.int32) #R
    lasnp[:, 4] = (lasnp[:, 4] / 65280 * 255).astype(np.int32) #V
    lasnp[:, 5] = (lasnp[:, 5] / 65280 * 255).astype(np.int32) #B
    #######################
    
    np.savetxt(out_dir + area + '\\' + subarea + '\\' + subarea + '.txt' , lasnp[:, :6], fmt=fmt, delimiter=' ')
    
    my_pylone = lasnp[(lasnp[:, -1] == 1) &(lasnp[:, -1] == 11) &(lasnp[:, -1] == 12) &(lasnp[:, -1] == 13) &(lasnp[:, -1] == 14)]
    my_iso = lasnp[(lasnp[:, -1] == 31) &(lasnp[:, -1] == 32) &(lasnp[:, -1] == 33) &(lasnp[:, -1] == 34)]
    
    if my_pylone.shape[0] > 0:
        np.savetxt(out_dir + area + '\\' + subarea + '\\' + anno + '\\' + 'obj10_1.txt', my_pylone[:, :6], fmt=fmt, delimiter=' ')
    if my_iso.shape[0] > 0:
        np.savetxt(out_dir + area + '\\' + subarea + '\\' + anno + '\\' + 'obj30_1.txt', my_iso[:, :6], fmt=fmt, delimiter=' ')
    
    for tag in tags:
        
        my_obj = lasnp[lasnp[:, -1] == tag]
        if my_obj.shape[0] > 0:
            np.savetxt(out_dir + area + '\\' + subarea + '\\' + anno + '\\' + f'obj{tag}_1.txt' , my_obj[:, :6], fmt=fmt, delimiter=' ')
            
























