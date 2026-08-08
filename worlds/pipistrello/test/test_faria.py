from options import Difficulty

from .bases import PipTestBase


class TestFariaNormalLogic(PipTestBase):
    options = {
        "difficulty": Difficulty.option_normal,
    }

    def test_vanilla_logic(self) -> None:
        with self.subTest("Test skyscraper is reachable with vanilla logic"):
            skyscraper_region = self.world.get_region("FSB (+4,-3) (North)")
            self.assertFalse(skyscraper_region.can_reach(self.multiworld.state))

            self.collect_by_name("Offstring Throw")
            self.assertTrue(skyscraper_region.can_reach(self.multiworld.state))

    def test_water_section(self) -> None:
        self.world.origin_region_name = "FSB (+10,+2) (Main)"
        golden_badge = "SP (-1,+4) (Southeast): Golden Badge"
        self.assert_access_dependency([golden_badge], [["Walk-the-Dog"]])


class TestFariaHardLogic(PipTestBase):
    options = {
        "difficulty": Difficulty.option_hard,
    }

    def test_water_section(self) -> None:
        self.world.origin_region_name = "FSB (+10,+2) (Main)"
        golden_badge = "SP (-1,+4) (Southeast): Golden Badge"
        dog = self.get_item_by_name("Walk-the-Dog").name
        ride = self.get_item_by_name("Wall-Ride").name
        dash = self.get_item_by_name("Wall-Dash").name
        ss = self.get_item_by_name("Progressive Skipping Stone Badge").name
        bp = self.get_item_by_name("BP Shard").name

        possible_items = {
            "Walk-the-Dog": [dog],
            "Wall-Ride + Wall-Dash + SS": [ride, dash, ss, bp, bp, bp, bp],
            "Wall-Ride + SS+": [ride, ss, ss, bp, bp],
        }
        self.assert_access_dependency(
            [golden_badge],
            possible_items.values(),
        )
