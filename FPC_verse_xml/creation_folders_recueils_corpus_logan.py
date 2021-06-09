#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#Created on Wed september  1 13:21:20 2019
#
#@author: marionfechino
#@description: Pour chaque recueil contenant des poésies, permet de créér un dossier auteur puis un dossier de ce recueil particulier pour ensuite ajouter chaque poème dans un fichier propre
#https://docs.python.org/2/library/xml.etree.elementtree.html
#"""

#Attention, ne permet que de traiter les poèmes qui ont des titres
 
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os
import glob

def prettify(elem):
    """
    Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def sanitize_name(name):
    """Return a sanitized version string of inputed name"""
    
    if name[0] == ' ':
        name = name[1:]
    sanitized_name = name.replace('\n\n', ' ').replace('\n', '').replace(' ', '_').replace("\'", '_')
    sanitized_name = sanitized_name.lower()
    return sanitized_name

def create_folder(sanitized_folder_name):
    """
    Check if a sanitized version of folder_name exists, 
    if not create it and return sanitized_folder_name string
    """
    if not os.path.isdir(sanitized_folder_name):
        os.makedirs(sanitized_folder_name)
    return sanitized_folder_name

def get_xml_root(filename):
    """Open a xml file and return root tag"""
    xml_file = ET.parse(filename)
    root = xml_file.getroot()
    return root
  
def create_file(filename_path, content):
    
    if os.path.exists(filename_path):
        return

    with open(filename_path, 'w') as output:
        output.write(content)
        

def create_poem_hierarchy(root, poem_tag):
  
    # find author / create folder
    author = root.find("AUTEUR").text
    date = root.find("DATE").text
    sanitized_author = sanitize_name(author)
    create_folder(sanitized_author)
    
    # find collection title / create collection title folder in author folder
    collection_title = root.find("TITRE_RECUEIL").text
    sanitized_collection_title = sanitize_name(collection_title)
    collection_path = os.sep.join([sanitized_author, sanitized_collection_title])
    create_folder(collection_path)
    
    # find collection title / create collection title folder in author_folder/collection_folder/
    poem_title = poem_tag.find("TITRE").text
    sanitized_title = sanitize_name(poem_title)
    poem_file_path = os.sep.join([sanitized_author, sanitized_collection_title, sanitized_title])
    poem_content = prettify(poem_tag)
    create_file(poem_file_path + ".xml", poem_content)

    return
    
def main (filenames):

    for filename in filenames:        
        root = get_xml_root(filename)
        for poem_tag in root.findall("POEME"):
            try:
                create_poem_hierarchy(root, poem_tag)
            except:
                print ("Error, can't make file hierarchy for a poem_tag")
    return

##################################################

# liste tous les fichiers du dossier actuelle
filenames = glob.glob("*.xml")


main(filenames)

