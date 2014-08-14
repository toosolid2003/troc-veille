# -*- coding: utf-8 -*-
import re

def recup_dates(contenu):
    '''Prend entrée un objet de type "soup" et renvoie une liste
    de dates de départ'''
    
    soup_dates = contenu.find_all("span", attrs={"class": "date"})
    liste_resultats = []

    for d in soup_dates:
            liste_resultats.append(d.contents[0].strip())

    return liste_resultats

    #La même chose avec des regex
    ##regex_dates =  re.compile('[a-z]{3} [0-9][0-9] [a-z]{3}')
    ##liste_dates = re.findall(regex_dates, str(soup_dates))

def recup_prix(contenu):
    '''Prend entrée un objet de type "soup" et renvoie une liste
    de prix pour chacun des billets renvoyés par la requête'''

    soup_prix = contenu.find_all("span", attrs={"class": "prix"})
    regex_prix = re.compile('[0-9]{2}')
    liste_resultats = re.findall(regex_prix, str(soup_prix))

    return liste_resultats

def recup_heures(contenu):
    '''Prend entrée un objet de type "soup" et renvoie une liste
    d'heures pour chacun des billets renvoyés par la requête'''
    
    soup_heures = contenu.find_all("span", attrs={"class": "heure-rech"})
    liste_resultats = []
    for h in soup_heures:
        liste_resultats.append(h.contents[0].strip())

    return liste_resultats

def recup_contacts(contenu):
    '''Prend entrée un objet de type "soup" et renvoie une liste
    de contacts reçus pour chacun des billets renvoyés par la requête'''
    
    
    soup_contacts = contenu.find_all("span", attrs={"class": "contacts"})
    regex_contacts = re.compile('<strong>([0-9]*)</strong>')
    liste_resultats = re.findall(regex_contacts, str(soup_contacts))

    return liste_resultats

def recup_ddepot(contenu):
    '''Prend entrée un objet de type "soup" et renvoie une liste
    de contacts reçus pour chacun des billets renvoyés par la requête'''
    
    soup_ddepot = contenu.find_all("span", attrs={"class": "contacts"})
    regex_dates_depot = re.compile('([0-9][0-9]/[0-9][0-9])')
    liste_resultats = re.findall(regex_dates_depot, str(soup_ddepot))

    return liste_resultats

def recup_liens(contenu):

    liens_tag = []
    for link in contenu.find_all('a'):
            liens_tag.append((link.get('href')))
    liens_tag = str(liens_tag)                                  #Conversion en chaîne de caractère pour rendre la liste exploitable par une regex

    regex_lien = re.compile('http://www.trocdestrains.com/billet-de-train\S*') #Regex à revoir: bug quand il y a un S majuscule à la fin du lien
    liste_resultats = re.findall(regex_lien, liens_tag)

    return liste_resultats

