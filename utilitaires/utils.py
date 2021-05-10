"""Fonctions ou classes utiles à plusieurs packages."""

from pathlib import Path
import datetime as dt
from typing import Optional, Union
import pandas as pd
import geopandas as gpd
from pandas import DataFrame, Series
from pandas.api.types import is_categorical
from openpyxl.utils.cell import get_column_letter
from .conf import chemins

jours = pd.CategoricalDtype(
    categories=["L", "Ma", "Me", "J", "V", "S", "D"], ordered=True
)
pd.options.io.excel.xlsx.writer = "openpyxl"  # pour xlsx_write_adjust


def get_file(path: Path, geo: bool = False) -> Optional[DataFrame]:
    """Lit une table dans un fichier en fonction de son extension.
    
    Formats pris en compte: parquet ou csv.
    """
    suffix = path.suffix
    try:
        if suffix == ".parquet":
            if not geo:
                return pd.read_parquet(path)
            else:
                return gpd.read_parquet(path)
        elif suffix == ".csv":
            return pd.read_csv(path)
        else:
            raise NotImplementedError(f"{suffix} est un type de fichier non implémenté.")
    except FileNotFoundError:
        print(f"{path.name} n'existe pas.")
        return None


def save_file(df: DataFrame, path: Path) -> None:
    """Sauvegarde la table en fonction de l'extension de son fichier.
    
    Formats pris en compte: parquet ou csv.
    """
    suffix = path.suffix
    if suffix == ".parquet":
        df.to_parquet(path)
    elif suffix == ".csv":
        df.to_csv(path)
    else:
        raise NotImplementedError(f"{suffix} est un type de fichier non implémenté.")


class Donnée:
    """Classe abstraite pour conteneur de données transformées.

    Attributs:
        filename: Union[str, list[str, ...]] nom(s) du ou des fichiers de sauvegarde des données
        paths: list, chemins de sauvegarde
        d: Union[DataFrame, tuple[DataFrame, ...]] table(s) de données

    Si filename est une liste, cstr_base() doit renvoyer un tuple qui est dans le même ordre.
    """

    filename = ""
    save_path = chemins["transformed"]

    def __init__(self, geo: bool = False) -> None:
        self.multiple = isinstance(self.filename, list)
        if not self.multiple:
            self.paths = [self.save_path / self.filename]
        else:
            self.paths = [self.save_path / f for f in self.filename]
        dfs = [get_file(path=p, geo=geo) for p in self.paths]
        if any(el is None for el in dfs):
            b = "des bases" if self.multiple else "de la base"
            print(f"Construction et sauvegarde {b}.")
            self.d = self.cstr_base()
            dfs = self.d if self.multiple else [self.d]
            for df, p in zip(dfs, self.paths):
                save_file(df=df, path=p)
        else:
            self.d = dfs if self.multiple else dfs[0]

    def cstr_base(self) -> Union[DataFrame, tuple[DataFrame, ...]]:
        """Construit la ou les base(s)."""
        pass


def dates_en_jours(s: Series) -> Series:
    """Transforme une série de dates en jours de la semaine."""
    return pd.Categorical.from_codes(s.dt.weekday.fillna(-1).astype(int), dtype=jours)


def nbr_jours_an(an: int) -> int:
    """Nombre de jour dans l'année."""
    return (dt.date(an, 12, 31) - dt.date(an, 1, 1)).days + 1


def xlsx_write_adjust(
    writer: pd.ExcelWriter, df: DataFrame, sheet_name: str, debug: bool = False
) -> None:
    """Écrit le dataFrame sur le fichier Excel en ajustant la largeur de colonnes et en figeant les volets.

    L'utilisation de BestFit pour la largeur des colonnes ne fonctionne pas pour tous les types de données.
    Arguments:
        writer: doit utiliser l'engine openpyxl
            l'import de ce module doit le définir comme engine par défaut dans les options

    Exemple:
    with pd.ExcelWriter("test.xslx") as xl:
        xlsx_write_adjust(xl, df, sheet_name="feuille1")
    """
    df.to_excel(writer, sheet_name=sheet_name)
    worksheet = writer.sheets[sheet_name]
    is_multi = df.columns.nlevels > 1
    try:
        df = df.reset_index()
    except TypeError:  # on essaie d'enlever les catégories
        if is_multi:
            for lev, c in enumerate(df.columns.levels):
                if is_categorical(c):
                    df.columns.set_levels(c.astype(str), level=lev, inplace=True)
        else:
            df.columns = df.columns.astype(str)
        df = df.reset_index()
    for idx, col in enumerate(df):  # loop through all columns
        series = df[col]
        len_name = (
            max(len(str(c)) for c in series.name) if is_multi else len(str(series.name))
        )
        p = (series.astype(str).map(len).max(), len_name)  # len of largest item
        if debug:
            print(series.name, p)
        max_len = max(p) + 1  # adding a little extra space
        worksheet.column_dimensions[get_column_letter(idx + 1)].width = max_len
        # worksheet.set_column(idx, idx, max_len)  # version xlsxwriter
    worksheet.freeze_panes = get_column_letter(df.columns.nlevels + 1) + str(
        df.index.nlevels + 1
    )
    # version xlsxwriter
    # worksheet.freeze_panes(df.columns.nlevels, df.index.nlevels)
