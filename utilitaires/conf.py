"""Configuration pour les autres modules.

Pour l'instant, juste des chemins de repertoires.
Lit 'projects.ini' situé dans le répertoire personnel 
'chemins' contient un dict avec les répertoires utiles aux modules.
"""

from pathlib import Path
import configparser


class Config:
    """Lecture du fichier de configuration.

    La syntaxe est celle des fichiers .ini :
    https://docs.python.org/3/library/configparser.html#supported-ini-file-structure

    Attributs:
        chemins: dict, créé à partir de la section 'paths', contenant des répertoires
            avec au moins une clé "transformed".
    """

    def __init__(self, filenames: list[Path]) -> None:
        config = configparser.ConfigParser()
        config.read_dict({"paths": {"transformed": "."}})
        config.read(filenames=filenames)
        p = config["paths"]
        self.chemins = {c: Path(p[c]) for c in p}
        for c in self.chemins.values():
            if not c.exists():
                print(f"Le chemin {c} n'existe pas.")


chemins = Config([Path.home() / "projects.ini"]).chemins
