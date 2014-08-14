#!/usr/bin/python
# -*-coding:utf-8 -*

from fonctions import *
import mechanize
from bs4 import BeautifulSoup
import re
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import datetime
import argparse


##Définition d'une classe Billet
#######################################################

class Billet:

    '''Billet de train'''

    def __init__(self, date_dep, heure_dep, prix, date_depot, contacts, lien):
        self.date_depart = date_dep
        self.heure_depart = heure_dep
        self.prix = prix
        self.contacts = contacts
        self.lien = lien
        self.date_depot = date_depot
        self.nouveau = False

    def __repr__(self):
        """Affichage sexy du billet"""
        return "Train partant le {} à {} pour un prix de {} euros. Billet déposé le {}.".format(self.date_depart, self.heure_depart,
                                                                                                self.prix, self.date_depot)
    def conver_date(self):
        '''Méthode convertissant l'attribut date_depart de l'objet billet en objet date, plus facilement
        manipulable. Prend un objet Billet en paramètre d'entrée.'''

        #Récupération du jour, en 5e position de la chaîne de caractère retirée du site trocdestrains

        j = int(self.date_depart[4:6])
        annee = 2013
        ms = 0
        #Récupération du mois
        
        dico = {"jan":1,"fév":2, "mar":3, "avr":4, "mai":5,"jun":6,"jui":7,"aou":8,
                "sep":9,"oct":10,"nov":11,"déc":12}
        ms = dico.get(self.date_depart[7:])
                
        self.date_depart = datetime.date(2013, ms, j)    

##Lancement de la requête
########################################################

def requete(vd, va, dd):
    #Constitution du browser

    browser = mechanize.Browser(factory=mechanize.RobustFactory())
    browser.set_handle_robots(False)
    #Simulation d'un agent humain en faisant semblant d'utiliser firefox - grâce aux headers
    browser.addheaders = [('User-agent', 'Mozilla 5.10')]

    #Ouverture du site et sélection du formulaire des trains

    req = mechanize.Request('http://www.trocdestrains.com')
    reponse = browser.open(req)
    browser.select_form(name="recherche_prems")

    #Entrée des données du formulaire

    browser['ville_dep'] = [vd]
    browser['ville_arr'] = [va]
    browser['L_jour_dep'] = [dd[0:2]]
    browser['L_mois_annee_dep'] = [dd[6:10] + '-'+ dd[3:5]]

    reponse = browser.submit(name="choix_rech_billet")
    return reponse

##Parsing de la réponse
########################################################
def parserReponse(soup):
    '''Parsing de la réponse obtenue par la requête, préalablement
    passée au format soup. Renvoie une liste de listes'''
    
    liste_dates = recup_dates(soup)
    liste_prix = recup_prix(soup)

    liste_heures = recup_heures(soup)
    liste_nb_contacts = recup_contacts(soup)
    
    liste_dates_depot = recup_ddepot(soup)
    liste_liens = recup_liens(soup)
    
    liste_resultats = [liste_dates, liste_prix, liste_heures, liste_nb_contacts, liste_dates_depot, liste_liens]
    
    return liste_resultats

##Création des objets billets au sein d'une liste
########################################################

def creaBillets(liste_resultats):
    '''Création des objets billets. Renvoie une liste d'objets.'''
    i = 0
    j = 0                               #Le cpteur j sert à itérer la liste des heures. On ne veut retenir que les heures de départ, soit une entrée sur deux.
    billets = []                        #On stocke les billets dans une liste
    for px in liste_resultats[1]:
        billets.append(Billet(liste_resultats[0][i], liste_resultats[2][j], liste_resultats[1][i], liste_resultats[4][i],
                              int(liste_resultats[3][i]), liste_resultats[5][i]))
        i+=1
        j+=2
    return billets


def envoiMail(billets, vd, va, dd):
        '''Envoi d'un mail avec les billets spécifiés. Prend en paramètre 
        d'entrée une liste de billets, la ville de départ, celle d'arrivée
         la date de départ'''
        
        expediteur = 'toosolid2003@yahoo.fr'
        destinataire = 'thibaut.segura@yahoo.fr'
        msg = MIMEMultipart()
        msg['From'] = expediteur
        msg['To'] = destinataire
        msg['Subject'] = 'Requete Troc des trains {} - {} - depart le '.format(vd, va, dd)
        corps = 'Il y a {} billet(s) disponibles pour le '.format(len(billets))+ dd
        for bil in billets:
            corps = corps + bil.date_depart.strftime("%d %B %Y") + ' '+ bil.heure_depart.encode('utf-8') +' '+ bil.prix.encode('utf-8') + ' E '+ bil.lien + '\n'
            
        msg.attach(MIMEText(corps, 'plain'))

        server = smtplib.SMTP_SSL('smtp.mail.yahoo.com',465)
        server.connect('smtp.mail.yahoo.com',465)
        server.login('toosolid2003','brutasse2003')
        text = msg.as_string()

        server.sendmail(expediteur, destinataire, text)
        
def afficheConsole(billets, vd, va, dd):
    '''Affiche les billets renvoyés par la requête. Prend en paramètres d\'entrée 
    une liste de billets, la ville de départ, la ville d'arrivée et la date du
    départ.'''
    
    print "Trajet "+ vd + " - " + va +\
    " pour le " + dd
    print "{} résultat(s) trouvés".format(len(billets))

    #Nota: on a spécifié l'encodage utf-8 por les attributs date_depart et prix afin d'éviter des erreurs d'impression dans la console.
    for bil in billets:
        print "Départ le {} à {} pour {} euros. Nb contacts: {}".format(bil.date_depart.encode('utf-8'), bil.heure_depart,
                                                                            bil.prix.encode('utf-8'), bil.contacts)
########################################################





def main():
    
    parser = argparse.ArgumentParser(description='Requete automatisee sur trocdestrains.com')
    
    parser.add_argument('-vdep', action='store', dest='ville_depart', help='ville de départ')
    parser.add_argument('-varr', action='store', dest='ville_arrivee', help='ville d\'arrivée')
    parser.add_argument('-ddep', action='store', dest='date_depart', help='date de départ')
    parser.add_argument('-dret', action='store', dest='date_retour', help='date de retour (facultatif)', default='aller_simple')
    parser.add_argument('-c', action='store', dest='contacts', help='nombre de contacts max reçu(s) par billet (facultatif). Defaut = 1',\
                        default=1, type=int)
    
    resultats = parser.parse_args()
    
    vd = resultats.ville_depart
    va = resultats.ville_arrivee
    dd = resultats.date_depart
    dr = resultats.date_retour
    ct = resultats.contacts

    #Lancement de la requête
    reponse = requete(vd, va, dd)
    
    #Parsing de la réponse
    soup = BeautifulSoup(reponse.read())
    liste_allers = parserReponse(soup)
        
    #Création des objets billets
    billets = creaBillets(liste_allers)

    #Sélection des billets ne dépassant pas le max de contact spécifié par l'utilisateur
    bContact = [bil for bil in billets if bil.contacts <= ct]
    
    #Affichage des résultats dans la console
    afficheConsole(bContact, vd, va, dd)
    
    #Envoi d'un mail
    #envoiMail(bContact, vd, va, dd)
    
    #Si l'utilisateur a saisi une date de retour, on lance une nouvelle requête pour récupérer les billets retour
    if dr != 'aller_simple':
    
        reponse = requete(va, vd, dr)
    
        #Parsing de la réponse
        soup = BeautifulSoup(reponse.read())
        liste_retours = parserReponse(soup)
        
        #Création des objets billets
        billets = creaBillets(liste_retours)
     
        #Affichage des résultats
        print "Trajet "+ va + " - " + vd + " pour le " + dr
        print "{} résultat(s) trouvés".format(len(liste_retours[0]))

        #Nota: on a spécifié l'encodage utf-8 por les attributs date_depart et prix afin d'éviter des erreurs d'impression dans la console.
        for billet in billets:
            print "Retour le {} à {} pour {} euros. {} contact(s) pris.".format(billet.date_depart.encode('utf-8'), billet.heure_depart,
                                                                               billet.prix.encode('utf-8'), billet.contacts)
        print "\n"
    
    
    
    
    ## #Identification d'un nouveau billet éventuel (pour une même requête)
    ## ##########################################################
    ## for bil in billets:
        ## #Extraction du jour et du mois de dépôt
        ## jour = int(bil.date_depot[0:2])
        ## mois = int(bil.date_depot[3:])
        ## bil.date_depot = datetime.date(2013, mois, jour)

        ## #Convesrion de la date de départ du billet en objet datetime
        ## bil.conver_date()
        
        ## #Comparaison avec la date du jour
        ## auj = datetime.date.today()
        ## if bil.date_depot == auj:
            ## bil.nouveau = True

    ## #Création d'une liste de nouveaux billets avec deux conditions:
    ## # 1 - Avoir été déposé le jour même
    ## # 2 - Que la date de départ du train corrspondent à la date saisie dans la requête

    ## jour = int(req_troc.jour_dep[0:2])
    ## mois = int(req_troc.jour_dep[3:5])
    ## annee = int(req_troc.jour_dep[6:])

    ## req_troc.jour_dep = datetime.date(annee, mois, jour)

    ## billets_nouveaux = [bil for bil in billets if bil.nouveau == True and bil.date_depart == req_troc.jour_dep]

if __name__ == "__main__":
    main()