"""Module de lecture d'un fichier de configuration.

Nommé `projects.ini` et situé dans le répertoire personnel.
La syntaxe est celle des fichiers .ini :
https://docs.python.org/3/library/configparser.html#supported-ini-file-structure

Doit contenir une section Paths. À défaut, les chemins seront fixés au répertoire courant.
"""
from pathlib import Path
import configparser

CONFIG_FILENAME = "projects.ini"
CONFIG_PATH = Path.home()

config = configparser.ConfigParser()
config.read([CONFIG_PATH / CONFIG_FILENAME])
p = config["Paths"]
chemins = {c: Path(p.get(c, ".")) for c in p}
for c in chemins.values():
    if not c.exists():
        print(f"{c} n'existe pas.")
