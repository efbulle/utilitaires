"""Module de lecture d'un fichier de configuration.

Nommé `projects.ini` et situé dans le répertoire personnel.

Doit contenir une section Paths. À défaut, les chemins seront fixés au répertoire courant.
"""
from pathlib import Path
import configparser

config = configparser.ConfigParser()
config.read([Path.home() / "projects.ini"])
p = config["Paths"]
chemins = {c: Path(p.get(c, ".")) for c in p}
for c in chemins.values():
    if not c.exists():
        print(f"{c} n'existe pas.")