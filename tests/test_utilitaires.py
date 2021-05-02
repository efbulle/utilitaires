import utilitaires.conf as conf
import unittest


class TestConf(unittest.TestCase):
    def test_paths(self):
        self.assertGreater(len(conf.chemins), 1)


if __name__ == "__main__":
    unittest.main()
