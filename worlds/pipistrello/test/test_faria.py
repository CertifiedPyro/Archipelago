from options import Difficulty

from ..constants import Badges as B
from ..constants import Moves as M
from ..constants import OtherItems as OI
from ..constants import Upgrades as U
from .bases import PipTestBase


class TestFariaNormalLogic(PipTestBase):
    run_default_tests = False
    options = {
        "difficulty": Difficulty.option_normal,
    }

    def test_vanilla_logic(self) -> None:
        with self.subTest("Test skyscraper is reachable with vanilla logic"):
            skyscraper_region = self.world.get_region("Faria (X+4, Y-3) (North)")
            self.assertFalse(skyscraper_region.can_reach(self.multiworld.state))

            possible_items = {
                "Offstring Throw": [M.OFF],
                "Walk-the-Dog": [M.DOG],
                "Wall-Dash": [M.DASH],
                "UFO Throw": [M.UFO],
                "Wall-Ride": [M.RIDE],
                "SS + BP Shards": [B.SS] + [OI.BP] * 4,
                "SS + Upgrades": [B.SS, U.BAT_POUCH, U.BAT_BACKPACK],
                "SS + BP Shards + Bat Pouch": [B.SS, U.BAT_POUCH] + [OI.BP] * 2,
                "SS + BP Shards + Bat Backpack": [B.SS, U.BAT_BACKPACK] + [OI.BP] * 2,
                "SS+ + BP Shards": [B.SS] * 2 + [OI.BP] * 2,
                "SS+ + Bat Pouch": [B.SS] * 2 + [U.BAT_POUCH],
                "SS+ + Bat Backpack": [B.SS] * 2 + [U.BAT_BACKPACK],
            }
            self.assert_access_dependency([skyscraper_region], possible_items.values())

        with self.subTest("Test dungeon is reachable with vanilla logic"):
            dungeon_region = self.world.get_region("Faria (X+8, Y-3) (Main)")
            staff_id = self.get_item_by_name("Staff ID").name

            self.assert_access_dependency([dungeon_region], [[M.DASH], [M.UFO], [M.RIDE], [staff_id]])

    def test_water_section(self) -> None:
        self.world.origin_region_name = "Faria (X+10, Y+2) (Main)"
        golden_badge = self.world.get_location("S Plaza (X-1, Y+4): Badge")
        self.assert_access_dependency([golden_badge], [["Walk-the-Dog"]])


class TestFariaHardLogic(PipTestBase):
    run_default_tests = False
    options = {
        "difficulty": Difficulty.option_hard,
    }

    def test_vanilla_logic(self) -> None:
        with self.subTest("Test skyscraper is reachable without abilities on hard logic"):
            key = self.world.get_location("Faria (X+6, Y-4): Key")
            skyscraper_region = self.world.get_region("Faria (X+4, Y-3) (North)")
            self.assertTrue(key.can_reach(self.multiworld.state))
            self.assertFalse(skyscraper_region.can_reach(self.multiworld.state))

            self.collect(key.item)
            self.assertTrue(skyscraper_region.can_reach(self.multiworld.state))

    def test_water_section(self) -> None:
        self.world.origin_region_name = "Faria (X+10, Y+2) (Main)"
        golden_badge = self.world.get_location("S Plaza (X-1, Y+4): Badge")

        possible_items = {
            "Walk-the-Dog": [M.DOG],
            "Wall-Ride + Wall-Dash + SS + BP Shards": [M.DASH, M.RIDE, B.SS] + [OI.BP] * 4,
            "Wall-Ride + Wall-Dash + SS + Upgrades": [M.DASH, M.RIDE, B.SS, U.BAT_POUCH, U.BAT_BACKPACK],
            "Wall-Ride + Wall-Dash + SS + BP Shards + Bat Pouch": [M.DASH, M.RIDE, B.SS, U.BAT_POUCH] + [OI.BP] * 2,
            "Wall-Ride + Wall-Dash + SS + BP Shards + Bat Backpack": [M.DASH, M.RIDE, B.SS, U.BAT_BACKPACK]
            + [OI.BP] * 2,
            "Wall-Ride + SS+ + BP Shards": [M.RIDE] + [B.SS] * 2 + [OI.BP] * 2,
            "Wall-Ride + SS+ + Bat Pouch": [M.RIDE] + [B.SS] * 2 + [U.BAT_POUCH],
            "Wall-Ride + SS+ + Bat Backpack": [M.RIDE] + [B.SS] * 2 + [U.BAT_BACKPACK],
        }
        self.assert_access_dependency(
            [golden_badge],
            possible_items.values(),
        )


class TestFariaExpertLogic(PipTestBase):
    run_default_tests = False
    options = {
        "difficulty": Difficulty.option_expert,
    }

    def test_water_section(self) -> None:
        self.world.origin_region_name = "Faria (X+10, Y+2) (Main)"
        golden_badge = self.world.get_location("S Plaza (X-1, Y+4): Badge")

        possible_items = {
            "Walk-the-Dog": [M.DOG],
            "Wall-Ride + Wall-Dash": [M.RIDE, M.DASH],
        }
        self.assert_access_dependency(
            [golden_badge],
            possible_items.values(),
        )
