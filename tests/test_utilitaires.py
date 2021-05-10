from pathlib import Path
import unittest
from unittest.mock import mock_open, patch
import utilitaires.conf as conf
import utilitaires.utils as utils
from pandas import DataFrame


class DonnéesTest(utils.Donnée):
    filename = "test.parquet"

    def cstr_base(self):
        return DataFrame({"a": [2], "b": [4]})


class TestUtils(unittest.TestCase):
    def test_données(self):
        d = DonnéesTest().d
        self.assertEqual(d["a"].iloc[0], 2)
        (DonnéesTest.save_path / DonnéesTest.filename).unlink()


class TestConf(unittest.TestCase):
    def test_fichier_manquant(self):
        c = conf.Config(["fichier_manquant"])
        self.assertEqual(c.chemins, {"transformed": Path(".")})

    def test_section_manquante(self):
        with patch("builtins.open", mock_open(read_data="[test]")):
            c = conf.Config(["mock"])
            self.assertEqual(c.chemins, {"transformed": Path(".")})

    def test_valeurs(self):
        d = {"transformed": "test", "output": "test2"}
        read_data = "[paths]\n"
        for k, v in d.items():
            read_data += f"{k}={v}\n"
        with patch("builtins.open", mock_open(read_data=read_data)):
            c = conf.Config(["mock"])
            self.assertEqual(c.chemins, {k: Path(v) for k, v in d.items()})

    def test_transformed_default(self):
        read_data = "[paths]\noutput=test"
        with patch("builtins.open", mock_open(read_data=read_data)):
            c = conf.Config(["mock"])
            self.assertEqual(c.chemins["transformed"], Path("."))


if __name__ == "__main__":
    unittest.main()
