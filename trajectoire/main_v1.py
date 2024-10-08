# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 15:04:49 2024

@author: malo.delacour
"""

import numpy as np
import matplotlib.pyplot as plt
import geojson
from pyproj import Proj, transform
from mpl_toolkits.mplot3d import Axes3D
import requests
from datetime import datetime

from lxml import etree
import zipfile
import os
import shutil


import plan
import kml_gen
import wpml_gen

def create_kmz_from_folder(folder_path, output_kmz_path):
    
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Le dossier {folder_path} n'existe pas.")
    
    # Crée un fichier zip (KMZ)
    with zipfile.ZipFile(output_kmz_path, 'w', zipfile.ZIP_DEFLATED) as kmz:
        # Parcourt tous les fichiers dans le dossier spécifié
        for root, _, files in os.walk(folder_path):
            for file in files:
                # Ajoute chaque fichier au fichier zip
                file_path = os.path.join(root, file)
                kmz.write(file_path, os.path.relpath(file_path, folder_path))

def make_wpml_folder(folder, files_to_move):
    
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Dossier créé: {folder}")
    
    for file in files_to_move:
        if os.path.exists(file):
            # Obtient le nom de base du fichier
            base_name = os.path.basename(file)
            # Construit le chemin de destination
            dest_path = os.path.join(folder, base_name)
            # Déplace le fichier
            shutil.move(file, dest_path)
            print(f"Fichier déplacé: {file} -> {dest_path}")
        else:
            print(f"Fichier non trouvé: {file}")




path = 'T3zone6.geojson'
flyname = 'T3zone6'




wp_info = 'speed'
now = datetime.now()
datefile = now.strftime("%Y-%m-%d_%H-%M")
fold_mission = flyname + "_" + datefile

if not os.path.exists(fold_mission):
    os.makedirs(fold_mission)
    print(f"Dossier créé: {fold_mission}")

pil_points, trajectory = plan.make_trajecto2(path)
plan.display_traj2D(trajectory, pil_points, wp_info, flyname, fold_mission + "/IMG_UTM32_" + flyname + ".png")
plan.report(trajectory, flyname, fold_mission)
plan.densif_traj(trajectory, 50, fold_mission + "/CC_MN95_" + flyname + ".txt")

###############
trajectory = plan.traj84toWGS84(trajectory)
kml_gen.make_kml(trajectory)
wpml_gen.make_wpml()

folder = 'wpmz'
files_to_move = ['template.kml', 'waylines.wpml']
output_kmz = fold_mission + "/" + flyname + '.kmz'

make_wpml_folder(fold_mission + "/" + folder, files_to_move)
create_kmz_from_folder(fold_mission + "/" + folder, output_kmz)







