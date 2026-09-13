import unittest

from world.regions import REGIONS


class RegionsTest(unittest.TestCase):
    def test_regions_is_a_dict_of_lists(self) -> None:
        self.assertIsInstance(REGIONS, dict)
        for countries in REGIONS.values():
            self.assertIsInstance(countries, list)

    def test_every_region_has_countries(self) -> None:
        for countries in REGIONS.values():
            self.assertTrue(countries)
