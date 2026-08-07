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
        with self.subTest("Test water section is passable with vanilla logic"):
            self.assertAccessDependency([golden_badge], [["Walk-the-Dog"]], only_check_listed=True)


class TestFariaHardLogic(PipTestBase):
    options = {
        "difficulty": Difficulty.option_hard,
    }

    def test_water_section(self) -> None:
        self.world.origin_region_name = "FSB (+10,+2) (Main)"
        golden_badge = "SP (-1,+4) (Southeast): Golden Badge"
        ride = self.get_item_by_name("Wall-Ride")
        dash = self.get_item_by_name("Wall-Dash")
        ss = self.get_item_by_name("Progressive Skipping Stone Badge")
        bp = self.get_item_by_name("BP Shard")

        move_configs = {
            "Wall-Ride + Wall-Dash + SS (not enough BP)": ([ride, dash, ss, bp, bp], False),
            "Wall-Ride + Wall-Dash + SS": ([ride, dash, ss, bp, bp, bp, bp], True),
            "Wall-Ride + Wall-Dash + SS+": ([ride, dash, ss, ss, bp, bp], True),
        }
        for name, config in move_configs.items():
            with self.subTest(f"Test water section with alternative moves: {name}"):
                self.collect(config[0])
                self.assertEqual(
                    self.world.get_location(golden_badge).can_reach(self.multiworld.state),
                    config[1],
                    f"Expected move config {name} to return {config[1]}",
                )
                self.remove(config[0])
