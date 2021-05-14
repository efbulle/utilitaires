"""Gestion d'un fichier de configuration pour les autres modules.

Pour l'instant, une seule section 'paths' est prise en compte.
Elle contient des chemins de répertoires.
Le fichier doit être nommé 'projects.ini' et situé dans le répertoire personnel.
La syntaxe est celle des fichiers .ini :
https://docs.python.org/3/library/configparser.html#supported-ini-file-structure

Attributs:
    chemins: dict avec les répertoires utiles aux autres modules.
"""

from pathlib import Path
import configparser


def lit_config(filenames: list[Path]) -> dict:
    """Lecture du fichier de configuration.

    Args:
        filenames: liste de répertoires où trouver le fichier de configuration.

    Returns: dict créé à partir de la section 'paths',
        contenant des répertoires et avec au moins une clé "transformed".
    """
    config = configparser.ConfigParser()
    config.read_dict({"paths": {"transformed": "."}})
    config.read(filenames=filenames)
    return {key: Path(value) for key, value in config["paths"].items()}


chemins = lit_config([Path.home() / "projects.ini"])
