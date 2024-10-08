# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 11:39:23 2024

@author: malo.delacour
"""

from lxml import etree
import zipfile
import numpy as np


def actionGroue_KML(my_placemark,i_action, i_start ,i_end , sensor, state):
    
    action_Actuator_Func = ""
    
    if sensor == "lidar":
        action_Trigger_Type = "reachPoint"
        action_Actuator_Func = "recordPointCloud"
        action_Group_Start_Index, action_Group_End_Index = i_start ,i_end
        if state == 0 :
            record_Point_Cloud_Operate = "startRecord"
        if state == 1 :
            record_Point_Cloud_Operate = "pauseRecord"
        if state == 2 :
            record_Point_Cloud_Operate = "resumeRecord"
    if sensor == "camera":
        action_Trigger_Type = "multipleTiming"
        action_Actuator_Func = "takePhoto"
        action_Group_Start_Index, action_Group_End_Index = i_start, i_end
    
    
    actionGroup = etree.SubElement(my_placemark, '{http://www.dji.com/wpmz/1.0.2}actionGroup')
    
    actionGroupId = etree.SubElement(actionGroup, '{http://www.dji.com/wpmz/1.0.2}actionGroupId')
    actionGroupId.text = i_action
    
    actionGroupStartIndex = etree.SubElement(actionGroup, '{http://www.dji.com/wpmz/1.0.2}actionGroupStartIndex')
    actionGroupStartIndex.text = action_Group_Start_Index
    
    actionGroupEndIndex = etree.SubElement(actionGroup, '{http://www.dji.com/wpmz/1.0.2}actionGroupEndIndex')
    actionGroupEndIndex.text = action_Group_End_Index
    
    actionGroupMode = etree.SubElement(actionGroup, '{http://www.dji.com/wpmz/1.0.2}actionGroupMode')
    actionGroupMode.text = "sequence"
    
    actionTrigger = etree.SubElement(actionGroup, '{http://www.dji.com/wpmz/1.0.2}actionTrigger')
    
    actionTriggerType = etree.SubElement(actionTrigger, '{http://www.dji.com/wpmz/1.0.2}actionTriggerType')
    actionTriggerType.text = action_Trigger_Type
    
    if sensor == "camera":
        
        actionTriggerParam = etree.SubElement(actionTrigger, '{http://www.dji.com/wpmz/1.0.2}actionTriggerParam')
        actionTriggerParam.text = "2"
    
    action = etree.SubElement(actionGroup, '{http://www.dji.com/wpmz/1.0.2}action')
    
    actionId = etree.SubElement(action, '{http://www.dji.com/wpmz/1.0.2}actionId')
    actionId.text = "0"
    
    actionActuatorFunc = etree.SubElement(action, '{http://www.dji.com/wpmz/1.0.2}actionActuatorFunc')
    actionActuatorFunc.text = action_Actuator_Func
    
    actionActuatorFuncParam = etree.SubElement(action, '{http://www.dji.com/wpmz/1.0.2}actionActuatorFuncParam')
    
    if sensor == "lidar":
    
        recordPointCloudOperate = etree.SubElement(actionActuatorFuncParam, '{http://www.dji.com/wpmz/1.0.2}recordPointCloudOperate')
        recordPointCloudOperate.text = record_Point_Cloud_Operate
        
        payloadPositionIndex = etree.SubElement(actionActuatorFuncParam, '{http://www.dji.com/wpmz/1.0.2}payloadPositionIndex')
        payloadPositionIndex.text = "0"

    if sensor == "camera":
        
        payloadPositionIndex = etree.SubElement(actionActuatorFuncParam, '{http://www.dji.com/wpmz/1.0.2}payloadPositionIndex')
        payloadPositionIndex.text = "0"
        
        useGlobalPayloadLensIndex = etree.SubElement(actionActuatorFuncParam, '{http://www.dji.com/wpmz/1.0.2}useGlobalPayloadLensIndex')
        useGlobalPayloadLensIndex.text = "0"



def payload_KML(folder):
    
    payloadParam = etree.SubElement(folder, '{http://www.dji.com/wpmz/1.0.2}payloadParam')
    
    payloadPositionIndex = etree.SubElement(payloadParam, '{http://www.dji.com/wpmz/1.0.2}payloadPositionIndex')
    payloadPositionIndex.text = "0"
    
    meteringMode = etree.SubElement(payloadParam, '{http://www.dji.com/wpmz/1.0.2}meteringMode')
    meteringMode.text = "average"
    
    dewarpingEnable = etree.SubElement(payloadParam, '{http://www.dji.com/wpmz/1.0.2}dewarpingEnable')
    dewarpingEnable.text = "0"
    
    returnMode = etree.SubElement(payloadParam, '{http://www.dji.com/wpmz/1.0.2}returnMode')
    returnMode.text = "tripleReturn"
    
    samplingRate = etree.SubElement(payloadParam, '{http://www.dji.com/wpmz/1.0.2}samplingRate')
    samplingRate.text = "240000"
    
    scanningMode = etree.SubElement(payloadParam, '{http://www.dji.com/wpmz/1.0.2}scanningMode')
    scanningMode.text = "repetitive"
    
    modelColoringEnable = etree.SubElement(payloadParam, '{http://www.dji.com/wpmz/1.0.2}modelColoringEnable')
    modelColoringEnable.text = "1"








# points = np.array([[6.66299981893201, 46.7811930547308, 640, 3, 0],
#                     [6.66287955075114, 46.781435000256,  650, 3, 99],
#                     [6.66350753399317, 46.781146753127,  645, 5, 1],
#                     [6.6630888784733,  46.7811451950246, 640, 5, 2],
#                     [6.66280739492916, 46.7809291801647, 645, 2, 99]])

def make_kml(points):
    
    # Création de l'élément racine KML avec les espaces de noms nécessaires
    kml = etree.Element('kml', nsmap={None: 'http://www.opengis.net/kml/2.2', 'wpml': 'http://www.dji.com/wpmz/1.0.2'})
    
    # Création du document
    document = etree.SubElement(kml, 'Document')
    
    #####################################################
    #####################################################
    
    # Informations de création de fichier
    author = etree.SubElement(document, '{http://www.dji.com/wpmz/1.0.2}author')
    author.text = "Name"
    
    createTime = etree.SubElement(document, '{http://www.dji.com/wpmz/1.0.2}createTime')
    createTime.text = "1637600807044"
    
    updateTime = etree.SubElement(document, '{http://www.dji.com/wpmz/1.0.2}updateTime')
    updateTime.text = "1637600875837"
    
    #####################################################
    #####################################################
    
    take_Off_Security_Height = "80"
    
    
    # Configuration de la mission
    missionConfig = etree.SubElement(document, '{http://www.dji.com/wpmz/1.0.2}missionConfig')
    
    flyToWaylineMode = etree.SubElement(missionConfig, '{http://www.dji.com/wpmz/1.0.2}flyToWaylineMode')
    flyToWaylineMode.text = "safely"
    
    finishAction = etree.SubElement(missionConfig, '{http://www.dji.com/wpmz/1.0.2}finishAction')
    finishAction.text = "goHome"
    
    exitOnRCLost = etree.SubElement(missionConfig, '{http://www.dji.com/wpmz/1.0.2}exitOnRCLost')
    exitOnRCLost.text = "goContinue"
    
    executeRCLostAction = etree.SubElement(missionConfig, '{http://www.dji.com/wpmz/1.0.2}executeRCLostAction')
    executeRCLostAction.text = "hover"
    
    takeOffSecurityHeight = etree.SubElement(missionConfig, '{http://www.dji.com/wpmz/1.0.2}takeOffSecurityHeight')
    takeOffSecurityHeight.text = take_Off_Security_Height
    
    # takeOffRefPoint = etree.SubElement(missionConfig, '{http://www.dji.com/wpmz/1.0.2}takeOffRefPoint')
    # takeOffRefPoint.text = "23.98057,115.987663,100"
    
    # takeOffRefPointAGLHeight = etree.SubElement(missionConfig, '{http://www.dji.com/wpmz/1.0.2}takeOffRefPointAGLHeight')
    # takeOffRefPointAGLHeight.text = "35"
    
    globalTransitionalSpeed = etree.SubElement(missionConfig, '{http://www.dji.com/wpmz/1.0.2}globalTransitionalSpeed')
    globalTransitionalSpeed.text = "15"
    
    droneInfo = etree.SubElement(missionConfig, '{http://www.dji.com/wpmz/1.0.2}droneInfo')
    
    droneEnumValue = etree.SubElement(droneInfo, '{http://www.dji.com/wpmz/1.0.2}droneEnumValue')
    droneEnumValue.text = "89"
    
    droneSubEnumValue = etree.SubElement(droneInfo, '{http://www.dji.com/wpmz/1.0.2}droneSubEnumValue')
    droneSubEnumValue.text = "0"
    
    payloadInfo = etree.SubElement(missionConfig, '{http://www.dji.com/wpmz/1.0.2}payloadInfo')
    
    payloadEnumValue = etree.SubElement(payloadInfo, '{http://www.dji.com/wpmz/1.0.2}payloadEnumValue')
    payloadEnumValue.text = "84"
    
    payloadSubEnumValue = etree.SubElement(payloadInfo, '{http://www.dji.com/wpmz/1.0.2}payloadSubEnumValue')
    payloadSubEnumValue.text = "0"
    
    payloadPositionIndex = etree.SubElement(payloadInfo, '{http://www.dji.com/wpmz/1.0.2}payloadPositionIndex')
    payloadPositionIndex.text = "0"
    
    #####################################################
    # FOLDER
    #####################################################
    
    # Configuration du modèle de waypoint
    folder = etree.SubElement(document, 'Folder')
    
    templateType = etree.SubElement(folder, '{http://www.dji.com/wpmz/1.0.2}templateType')
    templateType.text = "waypoint"
    
    templateId = etree.SubElement(folder, '{http://www.dji.com/wpmz/1.0.2}templateId')
    templateId.text = "0"
    
    ######### waylineCoordinateSysParam ##########
    waylineCoordinateSysParam = etree.SubElement(folder, '{http://www.dji.com/wpmz/1.0.2}waylineCoordinateSysParam')
    
    coordinateMode = etree.SubElement(waylineCoordinateSysParam, '{http://www.dji.com/wpmz/1.0.2}coordinateMode')
    coordinateMode.text = "WGS84"
    
    heightMode = etree.SubElement(waylineCoordinateSysParam, '{http://www.dji.com/wpmz/1.0.2}heightMode')
    heightMode.text = "EGM96"
    
    positioningType = etree.SubElement(waylineCoordinateSysParam, '{http://www.dji.com/wpmz/1.0.2}positioningType')
    positioningType.text = "GPS"
    ##############################################
    
    
    autoFlightSpeed = etree.SubElement(folder, '{http://www.dji.com/wpmz/1.0.2}autoFlightSpeed')
    autoFlightSpeed.text = "8"
    
    globalHeight = etree.SubElement(folder, '{http://www.dji.com/wpmz/1.0.2}globalHeight')
    globalHeight.text = "660"
    
    caliFlightEnable = etree.SubElement(folder, '{http://www.dji.com/wpmz/1.0.2}caliFlightEnable')
    caliFlightEnable.text = "1"
    
    gimbalPitchMode = etree.SubElement(folder, '{http://www.dji.com/wpmz/1.0.2}gimbalPitchMode')
    gimbalPitchMode.text = "usePointSetting"
    
    globalWaypointHeadingParam = etree.SubElement(folder, '{http://www.dji.com/wpmz/1.0.2}globalWaypointHeadingParam')
    
    waypointHeadingMode = etree.SubElement(globalWaypointHeadingParam, '{http://www.dji.com/wpmz/1.0.2}waypointHeadingMode')
    waypointHeadingMode.text = "followWayline"
    
    waypointHeadingAngle = etree.SubElement(globalWaypointHeadingParam, '{http://www.dji.com/wpmz/1.0.2}waypointHeadingAngle')
    waypointHeadingAngle.text = "0"
    
    waypointPoiPoint = etree.SubElement(globalWaypointHeadingParam, '{http://www.dji.com/wpmz/1.0.2}waypointPoiPoint')
    waypointPoiPoint.text = "0.000000,0.000000,0.000000"
    
    waypointHeadingPoiIndex = etree.SubElement(globalWaypointHeadingParam, '{http://www.dji.com/wpmz/1.0.2}waypointHeadingPoiIndex')
    waypointHeadingPoiIndex.text = "0"
    
    globalWaypointTurnMode = etree.SubElement(folder, '{http://www.dji.com/wpmz/1.0.2}globalWaypointTurnMode')
    globalWaypointTurnMode.text = "toPointAndPassWithContinuityCurvature"
    
    globalUseStraightLine = etree.SubElement(folder, '{http://www.dji.com/wpmz/1.0.2}globalUseStraightLine')
    globalUseStraightLine.text = "0"
    
    #####################################################
    #####################################################
    
    i = 0
    action_groupe_i = 0
    i_max = len(points)-1
    gimbal_Pitch_Angle = "-50"
    
    for myPoint in points :
        
        lon, lat, h, V_point, act = myPoint
    
        # Ajout d'un placemark avec point
        placemark = etree.SubElement(folder, 'Placemark')
        
        point = etree.SubElement(placemark, 'Point')
        
        coordinates = etree.SubElement(point, 'coordinates')
        coordinates.text = str(lon) + "," + str(lat)
        
        index = etree.SubElement(placemark, '{http://www.dji.com/wpmz/1.0.2}index')
        index.text = str(i)
        
        ellipsoidHeight = etree.SubElement(placemark, '{http://www.dji.com/wpmz/1.0.2}ellipsoidHeight')
        ellipsoidHeight.text = "709.826232910156"
        
        height = etree.SubElement(placemark, '{http://www.dji.com/wpmz/1.0.2}height')
        height.text = str(h)
        
        waypointSpeed = etree.SubElement(placemark, '{http://www.dji.com/wpmz/1.0.2}waypointSpeed')
        waypointSpeed.text = str(V_point)
        
        useGlobalHeadingParam = etree.SubElement(placemark, '{http://www.dji.com/wpmz/1.0.2}useGlobalHeadingParam')
        useGlobalHeadingParam.text = "1"
        
        useGlobalTurnParam = etree.SubElement(placemark, '{http://www.dji.com/wpmz/1.0.2}useGlobalTurnParam')
        useGlobalTurnParam.text = "1"
        
        gimbalPitchAngle = etree.SubElement(placemark, '{http://www.dji.com/wpmz/1.0.2}gimbalPitchAngle')
        gimbalPitchAngle.text = gimbal_Pitch_Angle
        
        useStraightLine = etree.SubElement(placemark, '{http://www.dji.com/wpmz/1.0.2}useStraightLine')
        useStraightLine.text = "0"
        
        isRisky = etree.SubElement(placemark, '{http://www.dji.com/wpmz/1.0.2}isRisky')
        isRisky.text = "0"
        
        # Ajout des actions
        # Démarage de l'acquisition
        if i == 0:
            actionGroue_KML(placemark,str(action_groupe_i) ,str(i) ,str(i) , "lidar", state=0)
            action_groupe_i += 1
            actionGroue_KML(placemark,str(action_groupe_i) ,str(i) ,str(i_max) , "camera", state=0)
            action_groupe_i += 1
            
        # Mise en pause du Lidar
        if act == 1:
            actionGroue_KML(placemark,str(action_groupe_i) ,str(i) ,str(i) , "lidar", state=1)
            action_groupe_i += 1
            
        # Reprise du Lidar
        if act == 2:
            actionGroue_KML(placemark,str(action_groupe_i) ,str(i) ,str(i) , "lidar", state=2)
            action_groupe_i += 1
        
        i += 1
    
    payload_KML(folder)
    
    
    
    # Convertir l'élément KML en chaîne XML avec la déclaration XML
    kml_str = etree.tostring(kml, pretty_print=True, xml_declaration=True, encoding='UTF-8')
    

    # Sauvegarder le fichier KML
    with open('template.kml', 'wb') as file:
        file.write(kml_str)
        
    print("KML généré avec succès")



# make_kml(points)





# kml_file = 'custom_tags.kml'

# with zipfile.ZipFile('kmz_file.kmz', 'w', zipfile.ZIP_DEFLATED) as kmz:
#     kmz.write(kml_file, arcname='doc.kml')

# print("Fichier KML avec balises personnalisées créé avec succès : custom_tags.kml")