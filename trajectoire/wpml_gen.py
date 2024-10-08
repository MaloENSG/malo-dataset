# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 09:58:25 2024

@author: malo.delacour
"""

from lxml import etree
import zipfile
import numpy as np


def make_wpml():

    take_Off_Security_Height = "80"
    
    
    # Création de l'élément racine KML avec les espaces de noms nécessaires
    kml = etree.Element('kml', nsmap={None: 'http://www.opengis.net/kml/2.2', 'wpml': 'http://www.dji.com/wpmz/1.0.2'})
    
    # Création du document
    document = etree.SubElement(kml, 'Document')
    
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
    
    
    
    
    # Convertir l'élément KML en chaîne XML avec la déclaration XML
    kml_str = etree.tostring(kml, pretty_print=True, xml_declaration=True, encoding='UTF-8')
    
    # Sauvegarder le fichier KML
    with open('waylines.wpml', 'wb') as file:
        file.write(kml_str)

    print("WPML généré avec succès")

















