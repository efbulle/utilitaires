"""Manipulation des pk."""

import re
from pandas import Series

REGEX_LIG_RG_PK = r"(?P<lig_rg>\d+-\d+)-(?P<pk_dec>-?\d+)"
REGEX_PK_DEC = r"(?P<add1>\d+|\D)(?P<op>[+-])(?P<add2>\d+)"
RER_C = {  # pk particuliers pour lignes 983000 et 984000 (Invalides à Austerlitz)
    "D": 0,
    "E": 1,
    "F": 2,
    "G": 3,
    "H": 4,
}


def lit_to_dec(pk_lit: Series) -> Series:
    """Convertit une série pk littéraux en pk entiers."""
    dec = pk_lit.str.extract(REGEX_PK_DEC).astype({"add2": float})
    dec["add1"] = dec["add1"].replace(RER_C).astype(float)
    dec2 = (dec["add1"] * 1000).add(dec["add2"].where(dec["op"] == "+", -dec["add2"]))
    try:  # à changer avec le nouveau type Int64 quand il sera stabilisé
        return dec2.astype(int)
    except ValueError:
        return dec2.astype(float)


def interne_to_dec(pk_internes: Series) -> Series:
    """Convertit une série de pk internes en pk métriques."""
    milliers_avec_zéros, unités = pk_internes.divmod(1000)
    milliers, correction = milliers_avec_zéros.divmod(100)
    return ((milliers + correction).mul(1000) + unités).where(
        pk_internes >= 0, pk_internes
    )


def sépare_lig_rg(lig_rg_pk: str) -> tuple[str, int]:
    """Décompose une chaîne de lig_rg_pk en (lig_rg, pk_dec)."""
    match = re.match(REGEX_LIG_RG_PK, lig_rg_pk)
    return match[1], int(match[2])
