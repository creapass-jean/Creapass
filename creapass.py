#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  creapass.py
#  
#  Copyright 2025 Jean Dalbrut
#  sauf logo et icône : Copyright 2025 Quentin Dalbrut 
#
# Merci aux différentes IA : chatgpt, chat.deepseek,  chat.mistral.ai, gemini.google, perplexity.ai et copilot.microsoft
# pour leurs conseils la plupart du temps judicieux et quelques corrections bienvenues

#   Licence
# Ce logiciel est libre, vous êtes autorisé à l’utiliser sans restriction,
# le partager voire l’améliorer sous certaines conditions, notamment citer
# le nom de l’auteur et de l’accompagner des textes et image originaux qui
# le composent.
# Les précisions sont résumées à cette adresse :
# https://creativecommons.org/licenses/by-nc-sa/4.0/deed.fr
# ou sous forme plus complète et plus juridique à cette adresse :
# https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.fr (traduction)
# ou https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.en (original
# en anglais)
# La page donne également accès à plus de 30 traductions


import ttkbootstrap as tkb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.tooltip import ToolTip
from pathlib import Path
from PIL import Image
import pystray
import threading
import stat
import os
import shutil
import json
import hashlib
import base64
import pyperclip
import webbrowser

#  #########################################################

class FoncCom :
    '''Fonctions communes à plusieurs class'''
    def __init__(self, main_mdp):
        self.lang = LanguageManager()  # Gestionnaire de langues
        self.aide = Help()
        self.main_mdp = main_mdp  #référence à MainMdp

### section : gestion fichiers (fonctions statiques)
    @staticmethod
    def gestion_fichiers(fichier, data=None, wr="r"):
        if wr == "r":
            try:
                with open(fichier, "r", encoding="utf-8") as fic:
                    return json.load(fic)
            except FileNotFoundError:
                return {} if data is None else data
        elif wr == "w":
            with open(fichier, "w", encoding="utf-8") as fic:
                json.dump(data, fic, indent=4, ensure_ascii=False)
            return data
        
    @staticmethod
    def get_theme_choisi(defaut="Clair"):
        """Lit le thème choisi dans user_data.json, ou retourne une valeur par défaut."""
        prefs = FoncCom.gestion_fichiers("user_data.json", {}, "r")
        return prefs.get("theme_choisi", defaut)

    @staticmethod
    def set_theme_choisi(theme):
        """Écrit le thème choisi dans user_data.json."""
        prefs = FoncCom.gestion_fichiers("user_data.json", {}, "r")
        prefs["theme_choisi"] = theme
        return FoncCom.gestion_fichiers("user_data.json", prefs, "w")

    @staticmethod
    def get_theme_applique(defaut="cosmo"):
        """Lit le thème appliqué dans user_data.json (thème réel de l'interface graphique)."""
        prefs = FoncCom.gestion_fichiers("user_data.json", {}, "r")
        return prefs.get("theme_applique", defaut)

    @staticmethod
    def set_theme_applique(theme_ap):
        """Écrit le thème appliqué dans user_data.json."""
        prefs = FoncCom.gestion_fichiers("user_data.json", {}, "r")
        prefs["theme_applique"] = theme_ap        
        return FoncCom.gestion_fichiers("user_data.json", prefs, "w")
    
    @staticmethod
    def set_miniinterface(statut):
        """Écrit le statut appliqué dans user_data.json."""
        prefs = FoncCom.gestion_fichiers("user_data.json", {}, "r")
        prefs["MiniInterface"] = statut
        return FoncCom.gestion_fichiers("user_data.json", prefs, "w")
    @staticmethod
    def get_miniinterface(defaut="non"):
        """Lit le statut de l'interface mini dans user_data.json."""
        prefs = FoncCom.gestion_fichiers("user_data.json", {}, "r")
        return prefs.get("MiniInterface", defaut)

### fin gestion fichiers

### section cryptage
    def empreinte(self, widget_val):
        """calcule l'empreinte numérique du mot (string) qui lui est envoyé et transforme l'affichage hexadécimal en chaine de caractères compréhensible par un Humain"""
        entree = hashlib.sha256(widget_val.encode("utf-8")).hexdigest()
        sortie = base64.b85encode (entree.encode("utf-8"))
        sortie_codee = sortie.decode ("utf-8")
        return sortie_codee
### fin cryptage

### section thème
    def change_theme(self, theme_selection) :        
        '''calcule l'ensemble thème-indice'''
        theme_selection = theme_selection.strip()
        # enregistrer pour utilisation future
        FoncCom.set_theme_choisi(theme_selection)
        langue_to_theme = {
        "Clair": ["cosmo", 0],
        "Foncé": ["darkly", 1],
        "Doux": ["morph", 2],
        "Bleu-nuit": ["superhero", 3],
        "Claro": ["cosmo", 0],
        "Oscuro": ["darkly", 1],
        "Suave": ["morph", 2],
        "azul-noche": ["superhero", 3],
        "Clear": ["cosmo", 0],
        "Dark": ["darkly", 1],
        "Soft": ["morph", 2],
        "blue-night": ["superhero", 3],
        "Clar": ["cosmo", 0],
        "Întuneric": ["darkly", 1],
        "Dulce": ["morph", 2],
        "albastru-noapte": ["superhero", 3]
        }
        nom_theme = langue_to_theme.get(theme_selection)
        theme = nom_theme[0]
        #enregistrer sur le disque pour la prochaine utilisation
        FoncCom.set_theme_applique(theme)
        return nom_theme

    def affiche_notice(self, cible): 
        self.cible = cible
        if cible == "Notice d'emploi":
            html_path = Path("active_html/notice.html")
            webbrowser.open(html_path.resolve().as_uri())  

#todo : construire les autres fonctions liées au menu Aide
            
    def recup_site(self, site, name, event = None) :
        """récupère le nom du site demandeur et en vérifie la validité. Si le nom ne figure pas dans la liste, l'ajoute et l'enregistre sur le disque"""
        site = site.capitalize()    #1ère lettre en capitale
        if site =="" or " " in site :
            Messagebox.show_error(
                self.lang.translate("Messagebox.show_error_2")[0],
                self.lang.translate("Messagebox.show_error_2")[1],
                alert = True
                )
            self.main_mdp.combobox_site.delete(0, END)
            self.main_mdp.combobox_site.focus_set()
            return
        else :
            # charge la liste des sites depuis le fichier"sites.json"
            data = FoncCom.gestion_fichiers("sites.json",[],wr="r")
            # vérifie la présence ou non dans la liste ; si absent, l'ajouter    
            if not site in data:
                data.append(site)
                data.sort()    #classe la liste par ordre alphabétique
            # enregistre la nouvelle liste
            FoncCom.gestion_fichiers("sites.json", data, "w")
            if name == "site":
                self.main_mdp.quitsite()
            self.main_mdp.combobox_site.configure(values = FoncCom.gestion_fichiers("sites.json", [], "r"),)    
            return

### validation des données et calcul final du mot de passe "solide"
    def mot_de_passe(self, site, event = None):
        """ Récupère les données, puis calcule le mot de passe "solide" final basé sur les empreintes numériques des données et le copie dans le presse-papier"""
        # quelques variables utiles
        site = site.capitalize()
        site_code = self.empreinte(site)
        verif_id = FoncCom.gestion_fichiers('id.json',[], 'r')
        identvar = verif_id[0]
        motvar = verif_id[1]
        # partie calcul du mot de passe désiré
        # créer une longue chaine à partir des données
        base = identvar + motvar + site_code
        passfinal = self.empreinte(base)
        passdesire = passfinal [0 : 25]
        
        """Bien que la probabilité qu'il manque soit une minuscule ou une majuscule ou un signe ou un chiffre, souvent demandés par les sites, soit extrèmement faible, cette ligne ajoute de façon sûre ces 4 types de caractères (y!Y8)"""
        passdesire = passdesire[0:4] + "y" + passdesire[5:10] + "!" + passdesire[11:16] + "Y" + passdesire[17:20] + "8" + passdesire[21:]
        return passdesire
        # fin mot_de_passe désiré            

### fin du calculfinal

# ##########################################################

class LanguageManager:
    def __init__(self, lang_dir="langues", active_lang_file="lang.json"):
        """
        Initialise le gestionnaire de langues.
        :param lang_dir: Chemin vers le dossier contenant les fichiers de langues.
        :param active_lang_file: Nom du fichier actif (ex : "lang.json").
        """
        self.lang_dir = Path(lang_dir)
        self.active_lang_file = Path(active_lang_file)
        self.translations = self.load_translations()

    def load_translations(self):
        """Charge les traductions depuis le fichier actif."""
        try:
            with open(self.active_lang_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def translate(self, key):
        """Retourne la chaîne traduite pour la clé donnée."""
        return self.translations.get(key, f"[{key}]")  # Fallback : affiche la clé non trouvée

    def change_language(self, language_file):
        """
        Change la langue active en copiant un fichier de langue dans le fichier centralisé.
        :param language_file: Nom du fichier langue dans le dossier lang_dir (ex : "français.json").
        """
        source_path = self.lang_dir / language_file
        if source_path.exists():
            shutil.copy(source_path, self.active_lang_file)
            self.translations = self.load_translations()

    # écriture de la langue sur le disque en vue des prochains démarrages
    def save_language(self, language_file):
        """Sauve le nom de la langue dans user_data.json"""
        data = FoncCom.gestion_fichiers("user_data.json", {}, wr="r")
        data["langue"] = language_file
        FoncCom.gestion_fichiers("user_data.json", data, wr="w")

    def language_sorting(self, langage_file) :
        '''calcule l'ensemble langue-indice en fonction de la langue utilisée (ex : selon l'utilisateur, le fichier Français.)'''
        langue_to_fichier = {
            "Français": ["Français.json", 0],
            "Anglais": ["Anglais.json", 1],
            "Espagnol": ["Espagnol.json", 2],
            "Roumain": ["Roumain.json", 3],
            "French": ["Français.json", 0],
            "English": ["Anglais.json", 1],
            "Spanish": ["Espagnol.json", 2],
            "Romanian": ["Roumain.json", 3],
            "Francés": ["Français.json", 0],
            "Inglés": ["Anglais.json", 1],
            "Español": ["Espagnol.json", 2],
            "Rumano": ["Roumain.json", 3],
            "franceză": ["Français.json", 0],
            "Engleză": ["Anglais.json", 1],
            "spaniolă": ["Espagnol.json", 2],
            "română": ["Roumain.json", 3]
        }
        choix_langue = langue_to_fichier.get(langage_file)
        return choix_langue

    def change_html_lang(self, lang_file) :
        '''change la langue des fichiers HTML en copiant le dossier HTML_"langue" dans le dossier principal de l'application'''
        html_dir = Path('langues/HTML_'+lang_file)
        active_html_file = html_dir.with_suffix('')
        if os.path.exists("active_html") :
            shutil.rmtree("active_html", onerror = self.on_rm_error)
        shutil.copytree(active_html_file, "active_html")

    def on_rm_error(self, func, path, exc_info) :
        os.chmod(path, stat.S_IWRITE)
        func(path)

#  #########################################################       

class Help :
    '''Gestion de l'aide'''
    def __init__(self) :
        self.lang = LanguageManager()  # Gestionnaire de langues 
              
    def load_help_sections(self) :
        help_sections = self.lang.load_translations()
        return help_sections

    def show_help(self, widget_name):
        """ Fonction pour afficher la section d'aide correspondant au widget"""
        help_sections = self.load_help_sections()
        help_content = help_sections.get(widget_name)
        if help_content:
            Messagebox.show_info(help_content, help_sections["help"])
        else:
            Messagebox.show_warning(help_sections["Messagebox.show_warning"][0], help_sections["Messagebox.show_warning"][1])

    def on_f1(self, event):
        """Fonction appelée lors de l'appui sur F1"""
        widget = event.widget
        widget_name = widget.winfo_name()   # Récupère le nom du widget
        self.show_help(widget_name)

# ##########################################################

    
class App(tkb.Window):
    '''Gestion de l'application'''

    def __init__(self):
        super().__init__()
        self.lang = LanguageManager()  # Gestionnaire de langues
        self.aide = Help()             #gestion de l'aide
        self.com = FoncCom(self)
        theme = FoncCom.get_theme_applique()
        self.style.theme_use(theme)
        self.iconphoto(True, tkb.PhotoImage(file =  "images_creapass/creapass.png"))
        self.resizable(0,0)
        self.bind("<Control-q>", self.fermeture)
        self.bind("<Control-Q>", self.fermeture)
        self.current_frame = None

        mini = self.com.get_miniinterface()
        if mini == "Oui" :
            self.show_frame(IniMini)
        elif not os.path.exists("id.json"):
            self.show_frame(Ini)
        else:
            self.show_frame(MainMdp)

    def show_frame(self, frame_class):
        """Détruit l'ancien frame et affiche un nouveau"""
        if self.current_frame is not None:
            self.current_frame.destroy()  # Supprime l'ancien frame
        # Crée une nouvelle instance du frame et l'affiche
        self.current_frame = frame_class(self)
        self.current_frame.pack(fill="both", expand=True)  # Assure l'affichage correct

    def fermeture(self, event = None) :
        self.destroy()    

# ##########################################################

class Ini(tkb.Frame):
    '''Initialisation de l'application'''

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  # Stocke la référence au parent (App)
        self.lang = LanguageManager()  # Gestionnaire de langues
        self.aide = Help()
        self.com = FoncCom(self)
        self.parent.geometry("550x350+200+200")
        self.parent.title(self.lang.translate("ini_fen_ttk.Window_title"))
        self.create_widgets()

# création des widgets

    def create_widgets(self):
    # label info
        self.label_info = tkb.Label(self,
                               text = self.lang.translate("label_info_ini_text"),
                               font = ("arial", 15),
                               justify = "center",
                               foreground = "red",
                              )
        self.label_info.place(x= 60, y = 10, width = 510, height = 80)

    # label link_notice
        label_link_notice = tkb.Label(self,
                                      text = self.lang.translate("label_link_notice"),
                                      font = ("Times", 12, "underline"),
                                      cursor = "hand2",
                                      justify = "center"
                                      )
        label_link_notice.place(x = 210, y = 100, width = 150, height = 30)
        label_link_notice.bind("<Button-1>", lambda x: self.choisir_aide("Notice d'emploi"))
    # Ajouter un tooltip
        ToolTip(label_link_notice, text = self.lang.translate("ToolTip_label_link_notice"), alpha = 0.85)

    # label ini langue
        label_ini_langue = tkb.Label(self,
                                     text = self.lang.translate("label_ini_langue")
                                     )
        label_ini_langue.place(x = 20, y = 150, width = 120, height = 30)

    # combo langue
        #récupérer sur le disque la langue utilisée précédemment 
        data = FoncCom.gestion_fichiers("user_data.json", {}, wr="r")
        langue_choisie = data.get("langue", "Français")  # valeur par défaut
        # Récupérer toute la liste associée à la clé "combobox_ini_langue"
        combobox_langues_values = self.lang.translate("combobox_ini_langue")
        # Créer le Combobox avec les valeurs
        combobox_ini_langue = tkb.Combobox(self,
                                           values = combobox_langues_values,
                                           name = "ini_langue"
                                           )
        combobox_ini_langue.place(x=100, y=150, width=150, height=30)
        combobox_ini_langue.focus_set()
        index_langue_choisie = self.lang.language_sorting(langue_choisie)[1]
        combobox_ini_langue.current(index_langue_choisie)
        # Ajouter un événement pour gérer la sélection
        combobox_ini_langue.bind("<<ComboboxSelected>>", lambda event: self.change_langue(combobox_ini_langue.get()))
        combobox_ini_langue.bind("<F1>", self.aide.on_f1)
        combobox_ini_langue.bind("<Return>", self.quit_langue)
        # Ajouter un tooltip
        ToolTip(combobox_ini_langue, text=self.lang.translate("ToolTip_combobox_ini_langue"), alpha = 0.85)

    # label thème
        label_ini_theme = tkb.Label(self,
                                    text = self.lang.translate("label_ini_theme"))

        label_ini_theme.place(x = 270, y = 150, width = 120, height = 30)

    # combothème
        #récupérer sur le disque le thème choisi précédemment
        theme_choisi = FoncCom.get_theme_choisi()
        nom_theme = self.change_theme(theme_choisi)
        theme = nom_theme[0]
        index_theme_choisi = nom_theme[1]
        # Récupérer toute la liste associée à la clé "combobox_ini_theme"
        combobox_themes_values = self.lang.translate("combobox_ini_theme")
        # Créer le Combobox avec les valeurs
        self.combobox_ini_theme = tkb.Combobox(self,
                                          values = combobox_themes_values,
                                          name = "ini_theme",
                                          )
        self.combobox_ini_theme.place(x = 378, y = 150, width = 150, height = 30)
        self.combobox_ini_theme.current(index_theme_choisi)
        # Ajouter un événement pour gérer la sélection
        self.combobox_ini_theme.bind("<F1>", self.aide.on_f1)
        self.combobox_ini_theme.bind("<<ComboboxSelected>>", lambda event :self.change_theme(self.combobox_ini_theme.get()))
        self.combobox_ini_theme.bind("<Return>", self.quit_theme)
        # Ajouter un tooltip
        ToolTip(self.combobox_ini_theme, text = self.lang.translate("ToolTip_combobox_ini_theme"), alpha = 0.85)

    # label id
        label_id = tkb.Label(self,
                            text = self.lang.translate("label_id_ttk.Label_ini_fen_text"),
                            )
        label_id.place(x = 20, y = 200, width = 230, height = 30)

    # entry id
        self.entry_id = tkb.Entry(self,
                             name = "entry_id",
                             )
        self.entry_id.place(x = 270, y = 200, width = 260, height = 30)

        ToolTip(self.entry_id, text = self.lang.translate("ToolTip_entry_id_text"), alpha = 0.85)

        self.entry_id.bind('<F1>', self.aide.on_f1)
        self.entry_id.bind("<Return>", self.verif_entry_id)

    # label ini mdp
        label_ini_mdp = tkb.Label(self,
                                  text = self.lang.translate("label_ini_mdp_ttk.Label_ini_fen_text"),
                                  )
        label_ini_mdp.place(x = 20, y = 250, width = 230, height = 30)

    # entry ini mdp
        self.entry_ini_mdp = tkb.Entry(self,
                                  show = "*",
                                  name = "entry_ini_mdp",
                                  state = "disabled"
                                  )
        self.entry_ini_mdp.place(x = 270, y = 250, width = 260, height = 30)

        ToolTip(self.entry_ini_mdp, text = self.lang.translate("ToolTip_entry_ini_mdp_text"), alpha = 0.85)

        self.entry_ini_mdp.bind('<F1>', self.aide.on_f1)
        self.entry_ini_mdp.bind("<Return>", self.verif_entry_ini_mdp)

    # bouton validation
        self.button_valid_ini = tkb.Button(self,
                                      text = "=======",
                                      bootstyle = "success",
                                      command = self.validation,
                                      state = "disabled"
                                      )
        self.button_valid_ini.place(x = 228, y = 300, width = 84, height = 30)

        ToolTip(self.button_valid_ini, text =self.lang.translate("ToolTip_button_valid_ini_text"))

# fin widgets

### procédures actives
# choix de la langue de l'interface

    def change_langue(self, lang_file):
        """Change la langue de l'application."""
        # enregistrer pour utilisation future
        self.lang.save_language(lang_file)
        lang_file = self.lang.language_sorting(lang_file)[0]
        self.lang.change_language(lang_file)
        self.refresh_interface()
        self.lang.change_html_lang(lang_file)

    def refresh_interface(self):
        """Rafraîchit l'interface après un changement de langue."""
        for widget in self.winfo_children():
            widget.destroy()  # Supprime uniquement les widgets à l'intérieur
        self.create_widgets()  # Recrée tous les widgets

    def quit_langue(self, event = None) :
        self.combobox_ini_theme.focus_set()

    def choisir_aide(self, cible, event = None):
        self.com.affiche_notice(cible)

    def change_theme(self, theme_selection) :
        nom_theme = self.com.change_theme(theme_selection)
        theme = nom_theme[0]
        if theme == "darkly" or theme == "superhero":
            self.label_info.configure(foreground = "yellow")
            self.parent.style.theme_use(theme)
        else :
            self.label_info.configure(foreground = "red")
            self.parent.style.theme_use(theme)
        return nom_theme

    def quit_theme(self, event = None) :
        self.entry_id.configure(state = "enabled")
        self.entry_id.focus_set()

    def verif_entry_id(self, event = None) :
        '''vérification de l'identifiant'''
        ident = self.entry_id.get()
        if ident == "" or " " in ident :
            Messagebox.show_error(
            self.lang.translate("Messagebox.show_error_3")[0],
            self.lang.translate("Messagebox.show_error_3")[1],
            alert = True
            )
            self.entry_id.delete(0, END)
            self.entry_id.focus_set()
            return
        else :
            identifiant_code = self.com.empreinte(ident)
            self.quit_entry_id()
            return identifiant_code

    def quit_entry_id(self) :
        self.entry_ini_mdp.configure(state = "enabled")
        self.entry_ini_mdp.focus_set()

    def verif_entry_ini_mdp(self, event = None) :
        '''vérification du mot de passe'''
        mot = self.entry_ini_mdp.get()
        if mot == "" or " " in mot :
            Messagebox.show_error(self.lang.translate("Messagebox.show_error_4")[0], self.lang.translate("Messagebox.show_error_4")[1], alert = True)
            self.entry_ini_mdp.delete(0, END)
            self.entry_ini_mdp.focus_set()
            return
        else :
            mdp_code = self.com.empreinte(mot)
            self.quit_entry_ini_mdp()
            return mdp_code

    def quit_entry_ini_mdp(self) :
        self.button_valid_ini.configure(state = "enabled")
        self.button_valid_ini.configure(text = "Validez")
        self.button_valid_ini.focus_set()

    def validation(self, event = None) :
        '''enregistre les données d'initialisation sur le disqueet lance l'interface principale de l'application'''
        identifiant_code = self.verif_entry_id()
        mdp_code = self.verif_entry_ini_mdp()
        group_id = [identifiant_code, mdp_code]
        FoncCom.gestion_fichiers('id.json', group_id, 'w')
        os.system(f"attrib +h id.json")  # Cache le fichier

        self.parent.show_frame(MainMdp)

############################################################

class MainMdp(tkb.Frame):
    '''fenêtre principale'''
    def __init__(self, parent):
        super().__init__(parent)
        self.lang = LanguageManager()
        self.aide = Help()
        self.com = FoncCom(self)
        self.parent = parent  # Stocke la référence au parent (App)
        self.parent.geometry("600x340+200+200")
        self.parent.title("Creapass")
        self.compteur = 0
        self.create_widgets()

    def create_widgets(self) :
    # menu fichier
        bouton_fichier = tkb.Menubutton(self,
                                       text = self.lang.translate("file"),
                                       bootstyle = "primary-outline"
                                       )
        bouton_fichier.place(x= 2, y= 0, width = 148, height = 30)
        options_dispo = tkb.Menu(bouton_fichier)
        var_fichier = tkb.StringVar()
        for y in ["Quitter"] :
           options_dispo.add_radiobutton(label = y, variable = var_fichier, command= lambda y = y: self.fermeture())
        bouton_fichier['menu'] = options_dispo

    # menu thèmes
        bouton_theme = tkb.Menubutton(self,
                                       text = self.lang.translate("theme"),
                                       bootstyle = "primary-outline"
                                       )
        bouton_theme.place(x= 151, y= 0, width = 148, height = 30)
        themes_dispo = tkb.Menu(bouton_theme)        
        var_theme = tkb.StringVar()
        for y in ["Clair", "Foncé", "Doux", "Bleu-nuit"] :
           themes_dispo.add_radiobutton(label = y, variable = var_theme, command= lambda y = y : self.choisir_theme(y))
        bouton_theme['menu'] = themes_dispo

    # menu interface
        bouton_interface = tkb.Menubutton(self,
                                       text = self.lang.translate("interface"),
                                       bootstyle = "primary-outline"
                                       )
        bouton_interface.place(x= 300, y= 0, width = 148, height = 30)
        self.interface = tkb.Menu(bouton_interface)
        self.langues = tkb.Menu(self.interface)
        for y in ["Français", "Anglais", "Espagnol", "Roumain"] :
            self.langues.add_command(label = y,  command= lambda y = y : self.choisir_langue(y))
        self.interface.add_cascade(label = "Langue", menu = self.langues) 
        self.interface.add_command(label = "mini-interface", state= "disabled", command= self.mini_interface)
        bouton_interface['menu'] = self.interface

    # menu aide                                            
        bouton_aide = tkb.Menubutton(self,
                                       text = self.lang.translate("help"),
                                       bootstyle = "primary-outline"
                                       )
        bouton_aide.place(x= 449, y= 0, width = 148, height = 30)
        aide_dispo = tkb.Menu(bouton_aide)        
        var_aide = tkb.StringVar()
        for y in ["Notice d'emploi", "Vidéo", "À propos"] :
           aide_dispo.add_radiobutton(label = y, variable = var_aide, command= lambda y = y: self.choisir_aide(y))
        bouton_aide['menu'] = aide_dispo

    # label mdp
        label_mdp = tkb.Label(self,
                              text = self.lang.translate("label_mdp_text"),
                              )
        label_mdp.place(x = 20, y = 50, width = 269, height = 30)

    # entry mdp
        self.entry_mdp = tkb.Entry(self,
                              show = "*",
                              name = "mdp",
                              )
        self.entry_mdp.place(x = 300, y = 50, width = 266, height = 30)
        self.entry_mdp.focus_set()
        ToolTip(self.entry_mdp, text = self.lang.translate("ToolTip_entry_mdp_text"), alpha = 0.85)
        self.entry_mdp.bind('<F1>', self.aide.on_f1)
        self.entry_mdp.bind("<Return>", self.verif_entry_mdp)

    # label site
        label_site = tkb.Label(self,
                               text = self.lang.translate("label_site_text")
                               )
        label_site.place(x= 20, y = 100, width = 269, height = 30)

    #combo site
        self.combobox_site = tkb.Combobox(self,
                                     name = "site",
                                     values = FoncCom.gestion_fichiers("sites.json", [], "r"),
                                     state = "disabled"
                                     )
        self.combobox_site.place(x = 300, y = 100, width = 266, height = 30)
        ToolTip(self.combobox_site, text = self.lang.translate("ToolTip_combobox_site_text"), alpha = 0.85)

        self.combobox_site.bind('<F1>', self.aide.on_f1)
        self.combobox_site.bind("<Return>", self.recup_site)

    # bouton validation
        self.button_valid = tkb.Button(self,
                                  text = "     =======================================     ",
                                  command = self.mot_de_passe,
                                  state = "disabled"
                                  )
        self.button_valid.place(x = 113, y = 150, width = 374, height = 30)
        ToolTip(self.button_valid, text = self.lang.translate("ToolTip_button_valid_text"), alpha = 0.85)

    # label information sortie
        label_info_sortie = tkb.Label(self,
                                      text = self.lang.translate("label_info_sortie_text"),
                                      justify = "center",
                                      )
        label_info_sortie.place(x = 40, y = 200, width = 560, height = 60)

    # label sortie définitive
        self.label_sortie = tkb.Label(self,
                                 background = "lightgreen",
                                 font = ("", 20),
                                 text = "",
                                 foreground = "red",
                                 justify = "right",
                                 relief = "solid"
                                 )
        self.label_sortie.place(x = 70, y = 270, width = 440, height = 40)

        self.parent.bind("<Control-q>", self.fermeture)
        self.parent.bind("<Control-Q>", self.fermeture)

    def fermeture(self, event = None) :
        self.parent.destroy()

    def mini_interface(self) :
        reponse = Messagebox.show_question(
            self.lang.translate ("Messagebox.show_question")[0],
            self.lang.translate ("Messagebox.show_question")[1]
            )
        if reponse in ("Oui", "oui", "Yes", "yes", "Si", "si", "Da", "da") :
            self.com.set_miniinterface("Oui")
        self.parent.show_frame(MiniInterface)

    def choisir_theme(self, theme_selection) :
        nom_theme = self.com.change_theme(theme_selection)
        theme = nom_theme[0]
        self.parent.style.theme_use(theme)

    def choisir_langue(self, lang_file):
        """Change la langue de l'application."""
        # enregistrer pour utilisation future
        self.lang.save_language(lang_file)
        lang_file = self.lang.language_sorting(lang_file)[0]
        self.lang.change_language(lang_file)
        # Détruire tous les widgets existants et les réafficher dans la langue
        self.refresh_interface()
        self.lang.change_html_lang(lang_file)

    def choisir_aide(self, cible):
        self.com.affiche_notice(cible)

    def refresh_interface(self):
        """Rafraîchit l'interface après un changement de langue."""
        for widget in self.winfo_children():
            widget.destroy()  # Supprime uniquement les widgets à l'intérieur
        self.create_widgets()  # Recrée tous les widgets

### vérifications diverses
    # vérifie le mot de passe
    def verif_entry_mdp(self, event = None) :
        """Vérifie si le mot de passe est vide ou contient des espaces. Si correct, rend actif le menu mini-interface"""
        mot = self.entry_mdp.get()
        verif_id = FoncCom.gestion_fichiers('id.json',[], 'r')
        mdp_control = self.com.empreinte(mot)
        if mdp_control != verif_id[1] :
            Messagebox.show_error(
                self.lang.translate("Messagebox.show_error_1")[0],
                self.lang.translate("Messagebox.show_error_1")[1],
                alert = True
                )
            self.compteur += 1
            self.entry_mdp.delete(0, END)
            self.entry_mdp.focus_set()
            if self.compteur == 3 :
                self.parent.destroy()
            return
        else :
            self.interface.entryconfig("mini-interface", state = "normal")
            self.combobox_site.config(state = "enabled")
            self.combobox_site.focus_set()
    # fin vérification du mot de passe

    # récupération et vérification du nom du site
    def recup_site(self, event = None) :
        """récupère le nom du site demandeur et en vérifie la validité. Si le nom ne figure pas dans la liste, l'ajoute et l'enregistre sur le disque"""
        site = self.combobox_site.get()    #récupération du combo
        self.com.recup_site(site, "site")
    # fin traitement du nom du site
### fin vérifications

    def quitsite(self) :
        self.button_valid.configure(state = "enabled")
        self.button_valid.configure(text = self.lang.translate("button_valid.configure_text"))
        self.button_valid.configure(bootstyle = "success")
        self.label_sortie.config(text = "")
        self.button_valid.focus_set()

### validation des données et calcul final du mot de passe "solide"
    def mot_de_passe(self):
        """ Récupère les données, puis calcule le mot de passe "solide" final basé sur les empreintes numériques des données et le copie dans le presse-papier"""
        # quelques variables utiles
        site = self.combobox_site.get()
        passdesire = self.com.mot_de_passe(site)
        self.label_sortie.configure(text = passdesire)
        pressPap=pyperclip.copy(passdesire)
        self.button_valid.configure(text = "     =======================================     ")
        self.button_valid.configure(state = "disabled")
        self.combobox_site.delete(0, END)
        self.combobox_site.focus_set()
        return pressPap
        # fin mot_de_passe désiré            
### fin du calculfinal

# ##########################################################

class MiniInterface(tkb.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.lang = LanguageManager()
        self.aide = Help()
        self.com = FoncCom(self)
        self.parent = parent
        self.parent.overrideredirect(True) #windows
        x = 20
        y = 20
        self.parent.geometry(f"570x30+{x}+{y}")
        self.parent.title("Creapass")
        self.compte_retour = False
        self.sans_barre_sys = True #windows
        self.parent.bind("<Alt-m>", self.sans_barre_syst) #windows
        self.create_widgets()
        
#### projet systray ####

        # Interception de la fermeture par la croix
        self.parent.protocol("WM_DELETE_WINDOW", self.hide_window)
        # Icone personnalisée
        icon_path = "images_creapass/creapass.ico"
        self.image = Image.open(icon_path)
        # Configuration de l'icône système
        self.icon = pystray.Icon("Creapass")
        self.icon.icon = self.image
        self.icon.title = self.lang.translate("Systray_infobule")
        self.icon.menu = pystray.Menu(
            pystray.MenuItem(self.lang.translate("Minimenu")[0], self.show_window),
            pystray.MenuItem(self.lang.translate("Minimenu")[1], self.hide_window),
            pystray.MenuItem(self.lang.translate("Minimenu")[2], self.quit_app)
            )
        # Lancement du systray dans un thread séparé
        self.systray_thread = threading.Thread(target=self.icon.run, daemon=True)
        self.systray_thread.start()
        
    def hide_window(self):
        self.parent.withdraw()

    def show_window(self, icon=None, item=None):
        self.parent.deiconify()
        self.premier_plan()
        self.parent.update_idletasks()
        self.parent.after(700, lambda: self.combobox_site.focus_force())

    def premier_plan(self) :
        self.parent.lift()
        self.parent.attributes('-topmost', True)
        self.parent.after(300, lambda: self.parent.attributes('-topmost', False))  # pour redonner la main ensuite    

    def quit_app(self, icon=None, item=None):
        self.icon.stop()
        self.parent.after(0, self.parent.destroy)

#### fin projet systray ####

    def create_widgets(self) :
    
    # combobox sites
        self.combobox_site = tkb.Combobox(self,
                                     name = "site",
                                     values = self.com.gestion_fichiers("sites.json", [], "r")
                                     )
        self.combobox_site.place(x = 0, y = 0, width = 240, height = 30)
        self.combobox_site.focus_set()
        #ajouter un tooltype
        ToolTip(self.combobox_site, text = self.lang.translate("ToolTip_combobox_site_text"), alpha = 0.85)

        self.combobox_site.bind('<F1>', self.aide.on_f1)
        self.combobox_site.bind("<Return>", self.recup_site)

    # label sortie définitive
        self.label_sortie = tkb.Label(self,
                                 background = "lightgreen",
                                 font = ("", 15),
                                 text = "",
                                 foreground = "red",
                                 justify = "right",
                                 relief = "solid"
                                 )
        self.label_sortie.place(x = 241, y = 0, width = 330, height = 30)

    def sans_barre_syst(self, event = None):
        if self.sans_barre_sys == True:
            self.parent.overrideredirect(False)
        else:
            self.parent.overrideredirect(True)
        self.sans_barre_sys = not self.sans_barre_sys


    def recup_site(self, event = None) :
        if self.compte_retour == False:
            site = self.combobox_site.get()
            self.com.recup_site(site, "site_mini")
            
            if site == "" :
                return
            else :
                passdesire = self.com.mot_de_passe(site)
            
            self.label_sortie.configure(text = passdesire)
            pressPap = pyperclip.copy(passdesire)
            self.compte_retour = True
        else :
            self.combobox_site.delete(0, END)
            self.label_sortie.configure(text = "")
            self.combobox_site.focus_set()
            self.compte_retour = False
            return


# ##########################################################

class IniMini(tkb.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.lang = LanguageManager()
        self.aide = Help()
        self.com = FoncCom(self)
        self.parent = parent
        self.parent.overrideredirect(True) #windows 
        x = 20 
        y = 20 
        self.parent.geometry(f"570x30+{x}+{y}")
        self.parent.title("Creapass")
        self.parent.style.theme_use("cosmo")
        self.texte_entry = self.lang.translate("Mdp_inimini")
        self.compteur = 0
        self.create_widgets()

    def create_widgets(self) :

        self.entry_mdp_mini = tkb.Entry(self,
                                        bootstyle = "primary",
                                        foreground = "grey",
                                        width = 550,
                                        justify = "center"
                                        )
        self.entry_mdp_mini.insert(0, self.texte_entry)
        self.entry_mdp_mini.pack()
        self.entry_mdp_mini.bind("<FocusIn>", self.on_entry_click)
        self.entry_mdp_mini.bind("<Return>", self.verif_entry_mdp_mini)

    def verif_entry_mdp_mini(self, event = None) :
        """Vérifie si le mot de passe est vide ou contient des espaces."""
        mot = self.entry_mdp_mini.get()
        verif_id = FoncCom.gestion_fichiers('id.json',[], 'r')
        mdp_control = self.com.empreinte(mot)
        if mdp_control != verif_id[1] :
            Messagebox.show_error(
                self.lang.translate("Messagebox.show_error_1")[0],
                self.lang.translate("Messagebox.show_error_1")[1],
                alert = True
                )
            self.compteur += 1
            self.entry_mdp_mini.delete(0, END)
            self.entry_mdp_mini.focus_set()
            if self.compteur == 3 :
                self.parent.destroy()
            return
        else :
            self.parent.show_frame(MiniInterface)
            self.parent.withdraw(
            )

    def on_entry_click(self, event=None):
        if self.entry_mdp_mini.get() == self.texte_entry :
            self.entry_mdp_mini.delete(0, "end")
            self.entry_mdp_mini.config(foreground ='black', show='*')


# ##########################################################
    
if __name__ == "__main__":
    app = App()
    app.mainloop()
