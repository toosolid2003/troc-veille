#!/usr/bin/python3.2
# -*-coding:utf-8 -*

from bs4 import BeautifulSoup
import requests
import smtplib
#from email.MIMEMultipart import MIMEMultipart
#from email.MIMEText import MIMEText
import datetime
import argparse


#
#def envoiMail(billets, vd, va, dd):
#        '''Envoi d'un mail avec les billets spécifiés. Prend en paramètre 
#        d'entrée une liste de billets, la ville de départ, celle d'arrivée
#         la date de départ'''
#        
#        expediteur = 'toosolid2003@yahoo.fr'
#        destinataire = 'thibaut.segura@yahoo.fr'
#        msg = MIMEMultipart()
#        msg['From'] = expediteur
#        msg['To'] = destinataire
#        msg['Subject'] = 'Requete Troc des trains {} - {} - depart le '.format(vd, va, dd)
#        corps = 'Il y a {} billet(s) disponibles pour le '.format(len(billets))+ dd
#        for bil in billets:
#            corps = corps + bil.date_depart.strftime("%d %B %Y") + ' '+ bil.heure_depart.encode('utf-8') +' '+ bil.prix.encode('utf-8') + ' E '+ bil.lien + '\n'
#            
#        msg.attach(MIMEText(corps, 'plain'))
#
#        server = smtplib.SMTP_SSL('smtp.mail.yahoo.com',465)
#        server.connect('smtp.mail.yahoo.com',465)
#        server.login('toosolid2003','brutasse2003')
#        text = msg.as_string()
#
#        server.sendmail(expediteur, destinataire, text)

################################################################################################

def recupData(bil):
    '''Entrée: un billet au format soup. En sortie: un dictionnaire qui porte les données du billet. Les données 
    sont récupérées en chaînes de caractère unicode. La fonction en convertit certaines en str ou int.'''
    
    
###Structure d'un objet billet
######
#billetsHtml[0] Racine
#   contents[1] = données billet
#      content[1] = <div style="position: relative">   Conteneur

#          contents[1] = <span class="col-gares">      Gares
#              contents[1] = <span class="gare-rech">      Gare d'origine
#              contents[5] = <span class="gare-interm">    Gare intermédiaire
#              contents[7] = <span class="gare-rech">      Gare de destination

#          contents[3] = <span class="col-heures">     Heures
#              contents[1] = <span class="heure-rech">     Heure Départ
#              contents[3] = <span class="heure-rech">     Heure d'arrivée

#          contents[5] = <span class="col-date">       Dates
#              contents[1] = <span class="date">           Date départ
#              contents[3] = <span class="train">          N° du train
#              contents[5] = <span style="font-size:14px;">Places dispo
#              contents[7] = <span class="train">          Prix
    
    dataBillet = {}
    
    dataBillet['gareOrigine'] = str(bil.contents[1].contents[1].contents[1].contents[1].get_text().strip())
    dataBillet['gareDest'] = str(bil.contents[1].contents[1].contents[1].contents[7].get_text().strip())

    dataBillet['dateDep'] = bil.contents[1].contents[1].contents[5].contents[1].get_text().strip()
    dataBillet['heureDep'] = bil.contents[1].contents[1].contents[3].contents[1].get_text().strip()

    nbPlaces = bil.contents[1].contents[1].contents[5].contents[5].get_text().strip()
    dataBillet['nbPlaces'] = int(nbPlaces[0:1])
    
    
    #Pour le prix, seuls les 2 premiers caractères nous intéressent. Nota: que se passe-t-il pour un prix à virgule?
    prix = bil.contents[1].contents[1].contents[5].contents[7].get_text().strip()
    prix = prix[0:2].strip()
    dataBillet['prix'] = int(prix)
    
    #Captage du lien
    dataBillet['lien'] = bil['href']

    return dataBillet

################################################################################################
        
#def afficheConsole(billets, vd, va, dd):
#    '''Affiche les billets renvoyés par la requête. Prend en paramètres d\'entrée 
#    une liste de billets, la ville de départ, la ville d'arrivée et la date du
#    départ.'''
#    
#    print "Trajet "+ vd + " - " + va +\
#    " pour le " + dd
#    print "{} résultat(s) trouvés".format(len(billets))
#
#    #Nota: on a spécifié l'encodage utf-8 por les attributs date_depart et prix afin d'éviter des erreurs d'impression dans la console.
#    for bil in billets:
#        print "Départ le {} à {} pour {} euros. Nb contacts: {}".format(bil.date_depart.encode('utf-8'), bil.heure_depart,
#                                                                            bil.prix.encode('utf-8'), bil.contacts)

        
################################################################################################





def main():
    
    #### Parsing de la ligne de commande
    parser = argparse.ArgumentParser(description='Requete de veille automatisee sur trocdestrains.com')
    
    parser.add_argument('-varr', action='store', dest='ville_arrivee', help='ville d\'arrivée')
    parser.add_argument('-c', action='store', dest='contacts', help='nombre de contacts max reçu(s) par billet (facultatif). Defaut = 1',\
                        default=1, type=int)
    
    resultats = parser.parse_args()
    
    va = resultats.ville_arrivee
    ct = resultats.contacts

    
    #### Ouverture de la page 'Billets déposés aujourd'hui'
    print("[+] Ouverture de la page")
    header={'User-agent':'Mozilla 5.10'}
    req = requests.get('http://www.trocdestrains.com/?choix=rech_recents&tri_col=date_depot&tri_sens=DESC',headers=header)

    #Création d'un objet soup à partir du fichier
    soup = BeautifulSoup(req.content)

    
    # Parsing de la réponse
    soup = BeautifulSoup(req.content)
    print('[+] Parsing de la réponse')
    billetsHtml = soup.findAll("a", class_="bulle-billet")


    #Lancement de la fonction recupData pour capter les données des objets 'billetsHtml'
    print("[+] Constitution des billets")
    listeBillets = []

    for bil in billetsHtml:
        listeBillets.append(recupData(bil))

    
    #Tri des billets: la liste billetsValide contient uniquement les billets avec la destination spécifiée en entrée
    billetsValide = []
    for billet in listeBillets:
        if billet['gareOrigine'] == 'Paris' and billet['gareDest'] == va:
            billetsValide.append(billet)
    
    for bil in billetsValide:
        print("Départ le {} à {} pour {}. Prix: {}€".format(bil['dateDep'], bil['heureDep'], bil['gareDest'],bil['prix']))
    
    
    #Affichage des résultats dans la console
    #afficheConsole(bContact, vd, va, dd)
    
    #Envoi d'un mail
    #envoiMail(bContact, vd, va, dd)

    
    
if __name__ == "__main__":
    main()