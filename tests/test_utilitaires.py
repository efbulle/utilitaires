"""Tests."""

from pathlib import Path
import unittest
from unittest.mock import mock_open, patch
from pandas import DataFrame
import utilitaires.conf as conf
import utilitaires.utils as utils


class DonnéesTest(utils.Donnée):
    filename = "test.parquet"

    def cstr_base(self):
        return DataFrame({"a": [2], "b": [4]})

    def fichier_brut(self) -> DataFrame:
        return 1


class TestUtils(unittest.TestCase):
    def test_données(self):
        d = DonnéesTest().data
        self.assertEqual(d["a"].iloc[0], 2)
        (DonnéesTest.save_path_parent / DonnéesTest.filename).unlink()


class TestConf(unittest.TestCase):
    def test_fichier_manquant(self):
        chemins = conf.lit_config(["fichier_manquant"])
        self.assertEqual(chemins, {"transformed": Path(".")})

    def test_section_manquante(self):
        with patch("builtins.open", mock_open(read_data="[test]")):
            chemins = conf.lit_config(["mock"])
            self.assertEqual(chemins, {"transformed": Path(".")})

    def test_valeurs(self):
        d = {"transformed": "test", "output": "test2"}
        read_data = "[paths]\n"
        for k, v in d.items():
            read_data += f"{k}={v}\n"
        with patch("builtins.open", mock_open(read_data=read_data)):
            chemins = conf.lit_config(["mock"])
            self.assertEqual(chemins, {k: Path(v) for k, v in d.items()})

    def test_transformed_default(self):
        read_data = "[paths]\noutput=test"
        with patch("builtins.open", mock_open(read_data=read_data)):
            chemins = conf.lit_config(["mock"])
            self.assertEqual(chemins["transformed"], Path("."))


if __name__ == "__main__":
    unittest.main()
