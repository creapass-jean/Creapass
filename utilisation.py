#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  utilisation.py
#  
#  Copyright 2025 Jean Dalbrut
#  

#

import webbrowser
from pathlib import Path
from creapass import FoncCom

com = FoncCom(None)

def maj_user(data):
    '''Met à jour user_data'''
    prefs = com.gestion_fichiers("user_data.json", {}, "r")
    prefs["donateur"] = data
    return com.gestion_fichiers("user_data.json", prefs, "w")

users_data = com.gestion_fichiers("user_data.json", {}, "r") #lecture_users()
donateur = users_data.get("donateur")
statut_donateur = donateur[0]
utilisation = donateur[1]
freq_don = donateur[2]
utilisation += 1
donateur[1] = utilisation
maj_user(donateur)

if utilisation == freq_don :
    html_path = Path("active_html/don.html")
    webbrowser.open(html_path.resolve().as_uri()) 
    donateur[1] = 0    
    donateur[2] -= 1
    if donateur[2] == 4:
        donateur[2] = 25
    maj_user(donateur)

    exit()    
else :
    exit()
