#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  utilisation.py
#  
#  Copyright 2025 Jean Dalbrut
#  

#
def main(args):
    return 0

import webbrowser
from pathlib import Path
from creapass import FoncCom

com = FoncCom(None)

def get_freq_util():
    """Lit le statut de l'utilisation dans user_data.json."""
    prefs = com.gestion_fichiers("user_data.json", {}, "r")
    return prefs.get("freq_util")

def set_freq_util(compt):
    """Écrit le statut appliqué dans user_data.json."""
    prefs = com.gestion_fichiers("user_data.json", {}, "r")
    prefs["freq_util"] = compt
    return com.gestion_fichiers("user_data.json", prefs, "w")

def get_utilisation():
    """Lit le statut de l'utilisation dans user_data.json."""
    prefs = com.gestion_fichiers("user_data.json", {}, "r")
    return prefs.get("utilisation")

def set_utilisation(compt):
    """Écrit le statut appliqué dans user_data.json."""
    prefs = com.gestion_fichiers("user_data.json", {}, "r")
    prefs["utilisation"] = compt
    return com.gestion_fichiers("user_data.json", prefs, "w")

freq_util = get_freq_util()
utilisation = get_utilisation()
utilisation += 1
set_utilisation(utilisation)
if utilisation > freq_util :
    html_path = Path("active_html/don.html")
    webbrowser.open(html_path.resolve().as_uri()) 
    set_utilisation(0)
    freq_util -= 1
    set_freq_util(freq_util)
    if freq_util == 4:
        set_freq_util(20)
    exit()    
else :
    exit()
   
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))  

