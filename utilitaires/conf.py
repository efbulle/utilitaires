"""Module de lecture d'un fichier de configuration.

Nommé `projects.ini` et situé dans le répertoire personnel.
La syntaxe est celle des fichiers .ini :
https://docs.python.org/3/library/configparser.html#supported-ini-file-structure

Crée un dict 'chemins' contenant les répertoires utiles aux modules sous forme de pathlib.Path.
"""

from pathlib import Path
import configparser

CONFIG_FILENAME = "projects.ini"
CONFIG_PATH = Path.home()
PATH_SECTION_NAME = "paths"
DEFAULT_PATHS = {PATH_SECTION_NAME: {"transformed": "."}}

config = configparser.ConfigParser()
config.read_dict(DEFAULT_PATHS)
config.read([CONFIG_PATH / CONFIG_FILENAME])
p = config[PATH_SECTION_NAME]
chemins = {c: Path(p[c]) for c in p}
for c in chemins.values():
    if not c.exists():
        print(f"Le chemin {c} n'existe pas.")
