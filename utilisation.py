#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  utilisation.py
#  
#  Copyright 2025 Jean Dalbrut
#  


def main(args):
    return 0

import json
import webbrowser
from pathlib import Path
from creapass import FoncCom
import time
com = FoncCom(None)

def get_utilisation():
    """Lit le statut de l'utilisation dans user_data.json."""
    prefs = com.gestion_fichiers("user_data.json", {}, "r")
    return prefs.get("utilisation")


def set_utilisation(compt):
    """Écrit le statut appliqué dans user_data.json."""
    prefs = com.gestion_fichiers("user_data.json", {}, "r")
    prefs["utilisation"] = compt
    return com.gestion_fichiers("user_data.json", prefs, "w")

utilisation = get_utilisation()
print ("debug_1 ",utilisation)
utilisation += 1    
print ("debug_2 ",utilisation)
set_utilisation(utilisation)
if utilisation > 5 :
    html_path = Path("active_html/don.html")
    webbrowser.open(html_path.resolve().as_uri()) 
    set_utilisation(0)
    time.sleep(5)
    print("attends 5 secondes")
    exit()    
else :
    time.sleep(3)
    print("attends 3 secondes")
    exit()
   
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))  

