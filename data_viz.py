# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 15:39:12 2024

@author: malo.delacour
"""

import matplotlib. pyplot as plt
import numpy as np
from matplotlib import colors
import glob

# ifile = "arrays_info_large.txt"
# ifile2 = "arrays_info_rvb.txt"
idir = ''

labels = ['Fondation', 'Pylone chat', 'Pylone à triangle', 'Pylone nappe', 'Pylone autre', 
          'Conducteur', 'Cable de garde', 'Cable de fixation', 'Isolateur V blanc', 
          'Isolateur H blanc', 'Isolateur V rouge', 'Isolateur H rouge', 'Signalisation', 
          'Végétation haute', 'Végétation basse', 'Pelouse', 'Roches', 
          'Terre et graviers', 'Routes', 'Eau', 'Batiment', 'Nid oiseaux', 'Entretoise', 
          'Disjoncteur', 'Non labéllisé']

labels_colors = ['#ffe599', '#a4c2f4', '#a4c2f4', '#a4c2f4', '#a4c2f4', '#f9cb9c', '#f9cb9c', 
          '#f9cb9c', '#ea9999', '#ea9999', '#ea9999', '#ea9999', '#b4a7d6', '#538b53', 
          '#6ea158', '#b6d7a8', '#efefef', '#b6b6b6', '#e6b8af', '#9fc5e8', '#a56262', 
          '#f107e5', '#f107e5', '#f107e5', '#000000']



# labels = ['pylone', 'conducteur', 'cdg', 'isolateur', 'vegetation', 'rochers', 'sol']
# labels_colors = ['tab:blue', 'gray', 'lightblue', 'orange', 'green', 'yellow', 'black']


file_list =  sorted(glob.glob(f'{idir}*.txt'))

data = np.genfromtxt(file_list[0], delimiter=';')


for file in file_list[1:]:
    add_data = np.genfromtxt(file, delimiter=';')
    data = np.vstack((data, add_data))


freq_oc = np.where(data==0, data, 1)


total_class = np.sum(data, axis=0)
total_tiles = np.sum(freq_oc, axis=0)

tot_pt_per_tile = np.sum(data, axis=1)

nb_class_per_tile = np.sum(freq_oc, axis=1)


def plot_hist_class(labels, values, colors, title='My title', logscale=True):

    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.bar(labels, values, color=colors)
    ax.set_title(title)
    ax.set_ylabel('Number of points')
    if logscale:
        ax.set_yscale('log')
    
    for label in ax.get_xticklabels(which='major'):
        label.set(rotation=40, horizontalalignment='right')

    plt.show()




def plot_scatter_class(val_class, val_tiles, labels, colors, title='My title', logscale=True):

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(val_class, val_tiles, linewidths=10, c=colors)
    
    # for i, txt in enumerate(labels):
    #     ax.annotate(txt, (val_class[i], val_tiles[i]+2), horizontalalignment='center')
        
    if logscale:
        ax.set_xscale('log')
    ax.set_title(title)
    ax.set_xlabel('Nombre de points')
    ax.set_ylabel('Nombre de tuile contenant la classe')
    
    plt.show()
    
def plot_hist_nb(values, n_bins, title='My title'):
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.hist(values, bins=n_bins)
    ax.set_title(title)
    ax.set_xlabel('Number of points')
    ax.set_ylabel('Number of tiles')
    
    plt.show()



    
    
# plot_hist_class(labels, total_class, labels_colors, title='Total number of points per class')
# plot_scatter_class(total_class, total_tiles, labels, labels_colors, title='Number of tiles containing each class depending on the number of points belonging to that class')
# plot_hist_nb(tot_pt_per_tile, 50, title='Number of points per tiles')
# plot_hist_nb(nb_class_per_tile, 11, title='Number of class per tiles')



##########################


new_labels = ['Pylone', 'Conducteur', 'Cable de garde', 'Cable de fixation', 'Isolateur',  
          'Végétation haute', 'Végétation basse', 'Pelouse', 'Roches', 
          'Terre et graviers', 'Routes', 'Eau', 'Batiment', 'Non labéllisé']

new_labels_colors = ['#a4c2f4', '#f9cb9c', '#f9cb9c', 
          '#f9cb9c', '#ea9999', '#538b53', 
          '#6ea158', '#b6d7a8', '#efefef', '#b6b6b6', '#e6b8af', '#9fc5e8', '#a56262', '#000000']

pylone = data[:, 0] + data[:, 1] + data[:, 2] + data[:, 3] + data[:, 4]
isolateur = data[:, 8] + data[:, 9] + data[:, 10] + data[:, 11]

new_data = np.hstack((pylone[:, np.newaxis], data[:, 5:8], isolateur[:, np.newaxis], data[:, 13:21], data[:, 24][:, np.newaxis]))


freq_oc = np.where(new_data==0, new_data, 1)
total_class = np.sum(new_data, axis=0)
total_tiles = np.sum(freq_oc, axis=0)
tot_pt_per_tile = np.sum(new_data, axis=1)
nb_class_per_tile = np.sum(freq_oc, axis=1)


plot_hist_class(new_labels, total_class, new_labels_colors, title='Total number of points per class')
plot_scatter_class(total_class, total_tiles, new_labels, new_labels_colors, title='Répartition spatiale des classe')
plot_hist_nb(tot_pt_per_tile, 50, title='Number of points per tiles')
plot_hist_nb(nb_class_per_tile, 10, title='Number of class per tiles')


































