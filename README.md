# Creapass 🔐🌐

**Creapass** est une application conçue pour faciliter la gestion sécurisée des identifiants et mots de passe, avec une interface multilingue et adaptable.
## 🔐Confidentialité et fonctionnement local
Creapass est une application 100 % locale.
Toutes les opérations, y compris la gestion des identifiants, la personnalisation de l’interface, et le stockage des données, s’effectuent exclusivement sur l’ordinateur personnel de l’utilisateur.
Aucune information n’est transmise à des serveurs externes, aucun service cloud n’est sollicité, et aucune connexion réseau n’est requise pour utiliser l’application.
Cette approche garantit une confidentialité maximale et une maîtrise complète de vos données.



## 🧰 Fonctionnalités principales
- Sélection automatique de la langue et du thème
- Sauvegarde locale sécurisée des identifiants (hash SHA-256)
- Génération dynamique de l’interface HTML selon la langue choisie
- Interface graphique conviviale (images et icônes incluses)

## 📁 Organisation des fichiers
- `creapass.py` : le cœur du programme
- `langues/` : contient les versions HTML multilingues + fichiers de traduction `.json`
- `active_html/` : version active générée à partir de `langues/`
- `images_creapass/` : icônes, logos, images d’illustration
- `user_data/` : préférences utilisateur (langue, thème…)
- `id.json` : données utilisateur (SHA des identifiants/mots de passe)
- `creapass.exe` : version compilée (Nuitka)
- `.gitignore` : exclut les fichiers sensibles ou temporaires

## 🚀 Lancer l’application
```bash
python creapass.py
