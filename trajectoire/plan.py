# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as plt
import geojson
from pyproj import Proj, transform, Transformer
from mpl_toolkits.mplot3d import Axes3D
import requests

def get_elevation(latitude, longitude):
    url = 'https://api.open-elevation.com/api/v1/lookup'
    params = {
        'locations': f'{latitude},{longitude}'
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Erreur API : Alti par defaut = 100")
        return 100
    if response.status_code == 200:
        results = response.json()['results']
        if results:
            return results[0]['elevation']
    return None

#################################

def get_altitude(latitude, longitude):
    
    # Conversion WGS84 en LV95
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:2056")
    easting, northing = transformer.transform(latitude, longitude)
    
    # URL de l'API Swisstopo pour obtenir l'altitude
    url = "https://api3.geo.admin.ch/rest/services/height"
    
    # Paramètres de la requête
    params = {
        'easting': easting,
        'northing': northing,
        'sr': 2056,
        'format': 'json'
    }
    
    try:
        # Envoyer la requête GET
        response = requests.get(url, params=params)
        
        # Vérifier si la requête a réussi
        if response.status_code == 200:
            data = response.json()
            altitude = data['height']
            return float(altitude)
        else:
            print(f"Erreur : {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Exception : {e}")
        return None

# alti = get_elevation(46.7811930547308, 6.66299981893201)
# print('alti point : ', alti)

# Convertir les coordonnées géographiques WGS84 en planaires WGS84 UTM zone 32N
def geo2plan(lon, lat):
    
    wgs84 = Proj(init='epsg:4326')  # WGS84
    utm32n = Proj(init='epsg:32632')  # UTM zone 32N
    
    E, N = transform(wgs84, utm32n, lon, lat)
    
    return E, N

def plan2geo(E, N):
    
    wgs84 = Proj(init='epsg:4326')  # WGS84
    utm32n = Proj(init='epsg:32632')  # UTM zone 32N
    
    lon, lat = transform(utm32n, wgs84, E, N)
    
    return lon, lat

# Créer un point dans l'alignement de deux points
def inter_pt(x1, y1, h1, x2, y2, h2, t):
    xp = x1 + t * (x2 - x1)
    yp = y1 + t * (y2 - y1)
    hp = h1 + t * (h2 - h1)
    return xp, yp, hp

def open_gjson(path):
    pass

# # Exemple de points A et B
# lon1, lat1 = 6.675499209565924, 46.752140816904948
# lon2, lat2 = 6.692410577623107, 46.750218488096777

# # Fraction
# t = -0.5


# path = 'pilonne_gj.geojson'


# with open(path, 'r') as file:
#     geojson_data = geojson.load(file)

# print(len(geojson_data["features"]))



####################################
####################################


def u_turn(Ep, Np, hp, Ec, Nc, hc, R, nb_pt, full=True):  
    
    omega = 0.3
    H = max(hp, hc)
    a = 2*np.pi/nb_pt # angle entre chaque point en rd
    
    
    # orientation initial du cercle
    beta = np.arctan2(Np-Nc, Ep-Ec)
    
    list_pt = []
    
    # création des points
    for i in range(nb_pt):
        
        gamma = a*i + a/2 + beta
        
        pti = [Ec + R*np.cos(gamma), Nc + R*np.sin(gamma), H]
        list_pt.append(pti)
        
    if full :
        
        pt1 = [Ec + R*np.cos(omega + beta), Nc + R*np.sin(omega + beta), H]
        ptn = [Ec + R*np.cos(-(omega - beta)), Nc + R*np.sin(-(omega - beta)), H]
        
        list_pt.insert(0, pt1)
        list_pt.append(ptn)
        
    return np.array(list_pt)


# Ep, Np, hp, Ec, Nc, hc = 3, 3, 8, 1, 2, 9
# R = 1 
# nb_pt = 4
# circle = u_turn(Ep, Np, hp, Ec, Nc, hc, R, nb_pt, full=True)

# plt.plot([3, 1], [3, 2])
# plt.plot(circle[:, 0], circle[:, 1])

####################################
####################################

def wp_u_turn(points, R, nb_pt, is_left=True):
    
    dist = 1.5*R
    
    # gestion d'une extrémité
    if is_left :
        
        pt0 = points[0]
        pt1 = points[1]
        
    else :
        
        pt0 = points[-1]
        pt1 = points[-2]
    
    x1, y1, h1 = pt0
    x2, y2, h2 = pt1
    
    # conversion de dist en facteur t
    dist_pt = np.sqrt((x1-x2)**2 + (y1-y2)**2)
    t = dist/dist_pt
    
    # projection du centre
    xc, yc, hc = inter_pt(x1, y1, h1, x2, y2, h2, -t)
    
    # calcul des points sur le cercle de demi tour
    list_u_turn = u_turn(x1, y1, h1, xc, yc, hc, R, nb_pt, full=False)
    
    # # Display
    # plt.plot(points[:, 0], points[:, 1])
    # plt.scatter(xc, yc)
    # plt.plot(list_u_turn[:, 0], list_u_turn[:, 1])
    
    return list_u_turn
    
    
# # Exemple de points de la polyligne initiale
# points = np.array([[0, 0, 8], [1, 2, 9], [3, 3, 7], [5, 1, 8.9]])


# R = 1 
# nb_pt = 6
# dist = 0.5
# list_u_turn = wp_u_turn(points, R, nb_pt, is_left=True)

####################################
####################################
        
def line_order(list_pt):
    
    list_pt.sort(key=lambda x: (x[1], x[0]))
    return list_pt

def line_angle(x1, y1, x2, y2, x3, y3):
    
    # Convertir les points en tableaux numpy
    A = np.array([x1, y1])
    B = np.array([x2, y2])
    C = np.array([x3, y3])
    
    # Vecteurs BA et BC
    BA = A - B
    BC = C - B
    
    # Produit scalaire de BA et BC
    dot_product = np.dot(BA, BC)
    
    # Longueur des vecteurs BA et BC
    magnitude_BA = np.linalg.norm(BA)
    magnitude_BC = np.linalg.norm(BC)
    
    # Cosinus de l'angle
    cos_angle = dot_product / (magnitude_BA * magnitude_BC)
    
    # Angle en radians
    angle = np.arccos(cos_angle)
    
    # Convertir l'angle en degrés
    angle_degrees = np.degrees(angle)
    
    return angle_degrees
    



####################################
####################################

def perp_vec(v):
    return np.array([-v[1], v[0]])

def norm_vec(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
        return v
    return v / norm

def offset_lines(points, offset_distance):
    """
    Crée deux polylignes parallèles à la polyligne donnée.
    """
    points = np.array(points)
    nb_pts = len(points)
    
    # Liste des points pour les polylignes décalées
    line_left = []
    line_right = []
    
    for i in range(nb_pts - 1):
        
        pts0 = np.array([points[i, 0], points[i, 1]])
        pts1 = np.array([points[i + 1, 0], points[i + 1, 1]])

        # Vecteur de direction du segment
        direction = pts1 - pts0
        norm_dir = norm_vec(direction)
        
        # Vecteur perpendiculaire normalisé
        perp_vector = perp_vec(norm_dir)
        
        # Points décalés pour ce segment
        left_point = pts0 + perp_vector * offset_distance
        right_point = pts0 - perp_vector * offset_distance
        
        # Ajouter les points décalés aux listes de polylignes
        line_left.append(left_point)
        line_right.append(right_point)
        
        if i == nb_pts - 2:  # Ajouter le dernier point du segment final
            
            left_point = pts1 + perp_vector * offset_distance
            right_point = pts1 - perp_vector * offset_distance
            
            line_left.append(left_point)
            line_right.append(right_point)
    
    return np.array(line_left), np.array(line_right)


def wp_lines(points, offset_distance):
    
    n, p = points.shape
    H = points[:, 2].reshape(n,1)
    P = points[:, 3].reshape(n,1)
    
    # Calculer les polylignes décalées
    polyline_left, polyline_right = offset_lines(points, offset_distance)
    
    polyline_left = np.hstack((polyline_left, H, P))
    polyline_right = np.hstack((polyline_right, H, P))
    
    return polyline_left, polyline_right


def ext_line(points, dist):
    
    # Ajout d'un point au début
    pt0 = points[0]
    pt1 = points[1]
    
    x1, y1, h1, p1 = pt0
    x2, y2, h2, p2 = pt1
    
    # conversion de dist en facteur t
    dist_pt = np.sqrt((x1-x2)**2 + (y1-y2)**2)
    t = dist/dist_pt
    
    xl, yl, hl = inter_pt(x1, y1, h1, x2, y2, h2, -t)
    
    pt_l = np.array([xl, yl, hl, p1])
    
    ###########################
    # Ajout d'un point au début
    pt0 = points[-1]
    pt1 = points[-2]
    
    x1, y1, h1, p1 = pt0
    x2, y2, h2, p2 = pt1
    
    # conversion de dist en facteur t
    dist_pt = np.sqrt((x1-x2)**2 + (y1-y2)**2)
    t = dist/dist_pt
    
    xr, yr, hr = inter_pt(x1, y1, h1, x2, y2, h2, -t)
    
    pt_r = np.array([xr, yr, hr, p1])
    
    # ajout de ces points à la ligne
    points = np.vstack((pt_l, points))
    points = np.vstack((points, pt_r))
    
    return points

##################################

# path = 'D:\plan_vol\Data\HT_pomy\pilonne_gj.geojson'

def import_json(path):

    with open(path, 'r') as file:
        geojson_data = geojson.load(file)
    
    elements = geojson_data["features"]
    points = []
    
    # wgs84 = Proj(init='epsg:4326')  # WGS84
    # utm32n = Proj(init='epsg:32632')  # UTM zone 32N
    p = Proj(proj='utm',zone=32,ellps='WGS84', preserve_units=False)
    
    for el in elements:
        lon = el["geometry"]["coordinates"][0]
        lat = el["geometry"]["coordinates"][1]
        h = el["properties"]["hauteur"]
        
        # E, N = p(lon, lat)
        # ht = get_altitude(lat, lon)
        
        E, N = lon, lat
        # ht = el["properties"]["Z (m)"]
        
        lon, lat = p(E, N, inverse=True)
        ht = get_altitude(lat, lon)
        
        points.append([E, N, ht+h, h])
        
    return np.array(points)
    

def wp_speed_master(line_offset, Vmin, Vmax, teta, margin):
    
    n, p = line_offset.shape
    teta = np.radians(teta)
    
    line_out = []
    
    for i in range(n-2):
        
        x1, y1, h1, p1 = line_offset[i]
        x2, y2, h2, p2 = line_offset[i+1]
        
        dp = p2/np.tan(teta) + margin + 5
        
        # conversion de dist en facteur t
        dist_pt = np.sqrt((x1-x2)**2 + (y1-y2)**2)
        t = (dist_pt-dp)/dist_pt
        
        x_, y_, h_ = inter_pt(x1, y1, h1, x2, y2, h2, t)
        
        ###
        # conversion de dist en facteur t
        te = (dist_pt-10)/dist_pt
        
        x_e, y_e, h_e = inter_pt(x1, y1, h1, x2, y2, h2, te)
        
        line_out.append([x1, y1, h1, Vmax])
        line_out.append([x_, y_, h_, Vmin])
        line_out.append([x_e, y_e, h_e, Vmax])
        # line_out.append([x2, y2, h2, Vmax])
    
    xn, yn, hn, pn = line_offset[-2]
    line_out.append([xn, yn, hn, Vmax])
    xn, yn, hn, pn = line_offset[-1]
    line_out.append([xn, yn, hn, Vmax])
    return np.array((line_out))



def report(trajectory, flyname, path_out):
    
    n = len(trajectory)
    dist = []
    deniv = []
    pente = []
    tps = []
    
    for i in range(n-1):
        
        x1, y1, z1, v1, a1 = trajectory[i]
        x2, y2, z2, v2, a2 = trajectory[i+1]
        
        p_dist = np.sqrt((x1-x2)**2 + (y1-y2)**2)
        p_deniv = z2-z1
        p_pente = np.arctan(p_deniv/p_dist)
        p_tps = p_dist/v1
        
        dist.append(p_dist)
        deniv.append(p_deniv)
        pente.append(np.degrees(p_pente))
        tps.append(p_tps)
        
    dist = np.array((dist))
    deniv = np.array((deniv))
    pente = np.array((pente))
    tps = np.array((tps))
    
    infos = (
        f'Plan de vol : {flyname}\n'
        f'Distance totale : {np.sum(dist)}\n'
        f'Temps total : {np.sum(tps)}\n'
        f'Dénivelé total : {deniv[deniv > 0].sum()}\n'
        f'Altitude max : {np.max(trajectory[:, 2])}\n'
        f'Altitude min : {np.min(trajectory[:, 2])}\n'
        f'pente max : {np.max(pente)}'
    )
    
    with open(path_out + "/report_" + flyname + ".txt", 'w', encoding='utf-8') as file:
        file.write(infos)
        
    print("Infos trajectoire généré avec succès")




def make_trajecto2(path):

    points = import_json(path)
    print(points)
    
    offset = 2
    R = 5
    nb_pt = 6
    Vmax = 8
    Vmin = 3
    hauteur_survol = 22
    
    teta = 50
    margin = 22
    start_pt = 8
    
    #######################
    # Zone d'acquisition
    ext_points = ext_line(points, dist=60)
    ext_points[:, 2] += hauteur_survol
    
    #######################
    # WayPoint acquisition
    polyline_left, polyline_right = wp_lines(ext_points, offset)
    polyline_left = wp_speed_master(polyline_left[::-1], Vmin, Vmax, teta, margin)
    polyline_right = wp_speed_master(polyline_right, Vmin, Vmax, teta, margin)
    
    # Ajout des actions
    n, p = polyline_left.shape
    act_line = np.full((n, 1), 99)
    act_line[0, 0], act_line[-1, 0] = 2, 1
    
    polyline_left = np.hstack((polyline_left, act_line))
    polyline_right = np.hstack((polyline_right, act_line))
    
    #######################
    # WayPoint demi-tour
    turn_left = wp_u_turn(ext_points[:, :3], R, nb_pt, is_left=True)
    turn_right = wp_u_turn(ext_points[:, :3], R, nb_pt, is_left=False)
    
    # Ajout des vitesses sur le virage
    a, b = turn_left.shape
    v_vir = np.full((a, 1), Vmin)
    v_vir[-1, 0] = Vmax
    act_vir = np.full((a, 1), 99)
    
    turn_left = np.hstack((turn_left, v_vir, act_vir))
    turn_right = np.hstack((turn_right, v_vir, act_vir))
    
    #######################
    # Concatenation de la trajectoire
    trajectory = np.vstack((polyline_right, turn_right))
    trajectory = np.vstack((trajectory, polyline_left))
    trajectory = np.vstack((trajectory, turn_left))
    
    #######################
    # Mise en place du START
    trajectory = np.roll(trajectory, shift=-start_pt, axis=0)
    trajectory = np.vstack((trajectory[-1, :], trajectory))
    trajectory[0, 4] = 0
    
    return ext_points, trajectory


def display_traj2D(trajectory, ext_points, wp_info, flyname, path_out):
    
    plt.figure(figsize=(50, 30))
    
    plt.plot(trajectory[:, 0], trajectory[:, 1], label='Trajectoire')
    plt.scatter(trajectory[:, 0], trajectory[:, 1], linewidths=1, label='Waypoints')
    plt.scatter(ext_points[:, 0], ext_points[:, 1], linewidths=2, label='Pylones')
    
    if wp_info == 'alti':
        wpi = 2
    if wp_info == 'speed':
        wpi = 3
    if wp_info == 'action':
        wpi = 4
    
    for i, (x_coord, y_coord) in enumerate(zip(trajectory[:, 0], trajectory[:, 1])):
        plt.text(x_coord, y_coord, str(i) + '_' + str(trajectory[i, wpi]), fontsize=3, ha='right')
    
    plt.title('Plan de vol : ' + flyname)
    plt.xlabel('Easting')
    plt.ylabel('Northing')
    plt.legend()
    plt.axis('equal')
    plt.savefig(path_out, dpi=300)
    plt.show()
    
    


# ext_points, trajectory = make_trajecto2(path)

# display_traj2D(trajectory, ext_points, 'speed', 'flyname', 'name.png')


def densif_traj(trajectory, density, filename):
    
    dense_traj = []
    utm32_proj = "EPSG:32632"
    mn95_proj = "EPSG:2056"
    utm32TOmn95 = Transformer.from_crs(utm32_proj, mn95_proj)
    
    for i in range(len(trajectory)-1):
        
        x1, y1, z1, v1, a1 = trajectory[i, :]
        x2, y2, z2, v2, a2 = trajectory[i+1, :]
        
        dist = np.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
        pas = 1/(density*dist)
        list_p = np.arange(0.01,1,pas)
        
        for p in list_p:
            xp, yp, zp = inter_pt(x1, y1, z1, x2, y2, z2, p)
            E_mn95, N_mn95 = utm32TOmn95.transform(xp, yp)
            dense_traj.append([E_mn95, N_mn95, zp, trajectory[i, 3]])
            
    dense_traj = np.array((dense_traj))
    
    with open(filename, 'w') as file:
        # Parcourir chaque ligne du tableau
        for row in dense_traj:
            # Joindre les éléments de la ligne avec des tabulations et écrire dans le fichier
            file.write('\t'.join(map(str, row)) + '\n')
        
      
def traj84toWGS84(trajectory):
    
    p = Proj(proj='utm',zone=32,ellps='WGS84', preserve_units=False)
    
    for i in range(len(trajectory)):
        
        E, N = trajectory[i, 0], trajectory[i, 1]
        lon, lat = p(E, N, inverse=True)
        trajectory[i, 0], trajectory[i, 1] = lon, lat
        
    return trajectory




# #######################
# # Ajout des vitesses sur la ligne
# n, p = polyline_left.shape
# v_line = np.full((n, 1), Vmax)
# v_line[-1, 0] = Vmin
# act_line = np.full((n, 1), 99)
# act_line[0, 0], act_line[-1, 0] = 2, 1

# polyline_left = np.hstack((polyline_left[::-1], v_line, act_line))
# polyline_right = np.hstack((polyline_right, v_line, act_line))

# #######################
# # Ajout des vitesses sur le virage
# a, b = turn_left.shape
# v_vir = np.full((a, 1), Vmin)
# v_vir[-1, 0] = Vmax
# act_vir = np.full((a, 1), 99)

# turn_left = np.hstack((turn_left, v_vir, act_vir))
# turn_right = np.hstack((turn_right, v_vir, act_vir))




# #######################
# # Mise en place du START
# trajectory = np.roll(trajectory, shift=-3, axis=0)
# trajectory = np.vstack((trajectory[-1, :], trajectory))
# trajectory[0, 4] = 0

# # plt.plot(trajectory[:, 0], trajectory[:, 1])
# # plt.scatter(trajectory[1, 0], trajectory[1, 1])
































    
    
def make_trajectory(path):
    
    points = import_json(path)
        
    
    
    # # Exemple de points de la polyligne initiale
    # points = np.array([[0, 0, 8], [1, 2, 9], [3, 3, 7], [5, 1, 8.9]])
    
    # # Décalage de la polyligne
    # offset_distance = 0.5
    
    # # Calculer les polylignes décalées
    # polyline_left, polyline_right = wp_lines(points, offset_distance)
    
    # plt.plot(points[:, 0], points[:, 1])
    # plt.plot(polyline_left[:, 0], polyline_left[:, 1])
    # plt.plot(polyline_right[:, 0], polyline_right[:, 1])
    
    
    offset = 2
    R = 5
    nb_pt = 6
    Vmax = 5
    Vmin = 3
    hauteur_survol = 20
    
    # Exemple coord pilonne
    #points = np.array([[0, 0, 8], [1, 2, 9], [3, 3, 7], [5, 1, 7.9]])
    
    
    # Zone d'acquisition
    ext_points = ext_line(points, dist=2)
    ext_points[:, 2] += hauteur_survol
    
    #######################
    # WayPoint acquisition
    polyline_left, polyline_right = wp_lines(ext_points, offset)
    
    # WayPoint demi-tour
    turn_left = wp_u_turn(ext_points, R, nb_pt, is_left=True)
    turn_right = wp_u_turn(ext_points, R, nb_pt, is_left=False)
    
    #######################
    # Ajout des vitesses sur la ligne
    n, p = polyline_left.shape
    v_line = np.full((n, 1), Vmax)
    v_line[-1, 0] = Vmin
    act_line = np.full((n, 1), 99)
    act_line[0, 0], act_line[-1, 0] = 2, 1
    
    polyline_left = np.hstack((polyline_left[::-1], v_line, act_line))
    polyline_right = np.hstack((polyline_right, v_line, act_line))
    
    #######################
    # Ajout des vitesses sur le virage
    a, b = turn_left.shape
    v_vir = np.full((a, 1), Vmin)
    v_vir[-1, 0] = Vmax
    act_vir = np.full((a, 1), 99)
    
    turn_left = np.hstack((turn_left, v_vir, act_vir))
    turn_right = np.hstack((turn_right, v_vir, act_vir))
    
    #######################
    # Concatenation de la trajectoire
    trajectory = np.vstack((polyline_right, turn_right))
    trajectory = np.vstack((trajectory, polyline_left))
    trajectory = np.vstack((trajectory, turn_left))
    
    
    #######################
    # Mise en place du START
    trajectory = np.roll(trajectory, shift=-3, axis=0)
    trajectory = np.vstack((trajectory[-1, :], trajectory))
    trajectory[0, 4] = 0
    
    # plt.plot(trajectory[:, 0], trajectory[:, 1])
    # plt.scatter(trajectory[1, 0], trajectory[1, 1])
    
    # Passage en coordonnées géo WGS84
    for i in range(len(trajectory)):
        
        E, N = trajectory[i, 0], trajectory[i, 1]
        lon, lat = plan2geo(E, N)
        trajectory[i, 0], trajectory[i, 1] = lon, lat
        
    return trajectory

# trajectory = make_trajectory(path)

### Affichage 2D
# plt.scatter(points[:, 0], points[:, 1])
# plt.plot(ext_points[:, 0], ext_points[:, 1])

# plt.plot(polyline_left[:, 0], polyline_left[:, 1], color='red')
# plt.plot(polyline_right[:, 0], polyline_right[:, 1], color='red')

# plt.plot(turn_left[:, 0], turn_left[:, 1], color='green')
# plt.plot(turn_right[:, 0], turn_right[:, 1], color='green')







# # Créer une figure et un axe 3D
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# # Tracer la courbe
# ax.plot(polyline_left[:, 0], polyline_left[:, 1], polyline_left[:, 2], color='red', label="Zone d'acquisition")
# ax.plot(polyline_right[:, 0], polyline_right[:, 1], polyline_right[:, 2], color='red')

# ax.plot(turn_left[:, 0], turn_left[:, 1], turn_left[:, 2], color='green', label="Zone demi-tour")
# ax.plot(turn_right[:, 0], turn_right[:, 1], turn_right[:, 2], color='green')

# ax.scatter(points[:, 0], points[:, 1], points[:, 2]-1, label='Sommet pilonne')


# ax.set_aspect('equal', 'box')
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# ax.legend()
# plt.show()





#####################################################
#####################################################
#####################################################














    
    
    
    
    