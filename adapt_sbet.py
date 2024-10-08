# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 10:50:56 2024

@author: malo de lacour
"""

import numpy as np
from pyproj import Proj, transform

# Trajectoir SBET
path = 'D:\CC\zone5B\DJI_20240705104028_0002_L_sbet.txt'

# Trajectoir Planair
filename = 'D:/CC/zone5B/traj_planair_5B.txt'

def trag_geo2plan(infile, outfile):
    """
    Convertit des coordonnées géographiques (latitude, longitude) en coordonnées projetées (planaire) et écrit le résultat dans un fichier.
    WGS84 -> WGS84 UTM 32

    Parameters
    ----------
    infile : str
        Le chemin vers le fichier d'entrée contenant les données trajectoire sbet en format texte.
    outfile : TYPE
        Le chemin vers le fichier de sortie où les données converties seront enregistrées.

    Returns
    -------
    None.

    """
    
    # Ouverture du sbet au format txt
    # lat (rd), lon (rd), alti (m), tps gps (SOW)
    traj = np.genfromtxt(infile, skip_header=2, usecols=(1, 2, 3, 0))
    
    # Définition du changement de coordonnées
    wgs84 = Proj(init='epsg:4326')  # WGS84
    utm32n = Proj(init='epsg:32632')  # UTM zone 32N
    p = Proj(proj='utm',zone=32,ellps='WGS84', preserve_units=False)
    
    # Boucle a opti avec numpy
    # Conversion en degré puis transfo en planaire
    for pt in traj:
        
        lon = np.degrees(pt[1])
        lat = np.degrees(pt[0])
        
        E, N = p(lon, lat)
        
        pt[0] = N
        pt[1] = E
        
    # Ecriture de la traj planaire
    with open(outfile, 'w') as file:
        # Parcourir chaque ligne du tableau
        for row in traj:
            # Joindre les éléments de la ligne avec des tabulations et écrire dans le fichier
            file.write('\t'.join(map(str, row)) + '\n')
            
            
            
            