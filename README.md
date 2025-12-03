# Creapass 🔐🌐

**Creapass** est une application locale et multilingue conçue pour faciliter la gestion sécurisée des identifiants et mots de passe, tout en préservant strictement la confidentialité de l'utilisateur.

## 🧰 Fonctionnalités principales
- Génération automatique et temporaire des mots de passe (non conservés)
- Interface multilingue dynamique (français, anglais, espagnol, roumain)
- Stockage local des identifiants hachés (SHA-256)
- Organisation claire des fichiers et des préférences utilisateur
- Interface graphique (images, icônes, contenu adapté selon la langue)
- Aide html + aide contextuelle (clic droit)

## 📂 Structure du projet
```
Creapass/
├── creapass.py                # Code source principal
├── creapass.exe               # Version compilée (Nuitka)
|__ docs
   |_ Images_creapass           
      |_logo_3.webp            # images pour pages docs
   |_ index.html
   |_ index_EN.html
   |_ index_ES.html
   |_ telechargement.html
   |_ telechargement_EN.html
   |_ telechargement_ES.html
   |_ styles.css
├── langues/                   # HTML et traductions JSON
   |_ HTML_Anglais # dossier
      |_ danger.html           # information des risques liés à la réinitialisation
      |_ presentation.html     # comme son nom l'indique
      |_don.html               # appel à don Paypal
      |_ notice.html           # comme son nom l'indique
      |_ conseils_ini.html     # sous-notice
   |_ HLML_Espagnol
      |_ . . .                 # même contenu que ci-dessus selon la langue
   |_ HTML_Français
      |_ . . .                 # même contenu que ci-dessus selon la langue
   |_ HTML_Roumain
      |_ . . .                 # même contenu que ci-dessus selon la langue
   |_ Anglais.json             # textes de l'interface
   |_ Espagnol.json
   |_ Français.json
   |_ Roumain.json
├── images_creapass/           # Illustrations et icônes
   |_ creapass.png             # icône
   |_ creapass.ico             # icône
   |_ fig_1.webp
   |_ . . .                    # les images pour notice.html
   |_ fig_8.webp
   |_ logo.png # logo
├── active_html/               # HTML généré dynamiquement 
├── user_data/                 # Préférences locales de l'utilisateur
├── lang.json                  # Copie du fichier langue en cours (interface)
├── id.json                    # Identifiants hachés (SHA-256)
├── sites.json                 # Liste évolutive des sites utilisés
├── README.md                  # Présentation du projet
├── .gitignore                 # Fichiers et dossiers à exclure
|__ utilisation                # Appel Paypal
```

## 🔒 Sécurité & Respect de la vie privée

> **Creapass est une application entièrement locale.**  
> Toutes les opérations (gestion, affichage, stockage) s’effectuent sur l’ordinateur personnel de l’utilisateur.  
> **Aucune connexion Internet, aucun service externe, aucun cloud** ne sont utilisés.

### 🔑 Mots de passe et identifiants

> Creapass ne conserve **jamais les mots de passe**, ni en clair, ni chiffrés.  
> Lorsqu’un mot de passe est requis, il est **généré à la volée**, selon les préférences de l’utilisateur.  
> Les identifiants (logins) sont **hachés en SHA-256** et stockés uniquement localement.  
> Cela garantit une protection maximale, sans exposition ni dépendance extérieure.

## 🚀 Lancer l’application
```bash
python creapass.py
---
```


🧭 **Origine du projet**

*Je n'avais aucune formation informatique, débutant dans la pâtisserie à 15 ans avec un BEPC, à 21 ans je suis passé à la photographie où j'ai fait ma carrière. À 76 ans, pour occuper ma petite retraite et tenter de faire la pige à Alzheimer je me suis lancé dans l'étude de la programmation avec Python. Ce programme est le résultat de 14 mois d'autodidaxie*  
Développé et testé avec soin à Limoges, Nouvelle-Aquitaine 🇫🇷  
Parce que la confidentialité mérite une touche artisanale.


