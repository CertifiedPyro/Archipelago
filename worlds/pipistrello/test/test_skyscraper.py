from options import Difficulty
from rule_builder.rules import False_

from ..constants import Moves as M
from .bases import PipTestBase


class TestSkyscraperExpertLogic(PipTestBase):
    run_default_tests = False
    options = {
        "difficulty": Difficulty.option_expert,
    }

    def test_staff_id(self) -> None:
        self._set_origin_region()
        staff_id = self.world.get_location("Skyscraper (X+0,Y-4): Staff ID")
        possible_items = {
            "Offstring Throw": [M.OFF],
            "UFO Throw": [M.UFO],
            "Wall-Ride": [M.RIDE],
        }
        self.assert_access_dependency([staff_id], possible_items.values())

    def test_starting_room(self) -> None:
        self._set_origin_region()
        start_room_east = self.world.get_region("Skyscraper (X+0,Y-2) (East)")

        with self.subTest("Test east side of starting room is reachable with vanilla logic"):
            self.assertTrue(start_room_east.can_reach(self.multiworld.state))

        with self.subTest("Test east side of starting room is reachable with alternate route"):
            entrance = self.world.get_entrance("Skyscraper (X+0,Y-2) (West) -> Skyscraper (X+0,Y-2) (East)")
            self.world.set_rule(entrance, False_())
            possible_items = {
                "Wall-Ride + Wall-Dash": [M.RIDE, M.DASH],
                "UFO Throw": [M.UFO],
            }
            self.assert_access_dependency([start_room_east], possible_items.values())

    def test_keys_room(self) -> None:
        self._set_origin_region()
        key_room = self.world.get_region("Skyscraper (X+3,Y-4) (Main)")
        possible_items = {
            "Offstring Throw": [M.OFF],
            "Wall-Ride + Wall-Dash": [M.RIDE, M.DASH],
            "UFO Throw": [M.UFO],
        }
        self.assert_access_dependency([key_room], possible_items.values())

    def _set_origin_region(self) -> None:
        self.world.origin_region_name = "Skyscraper (X+0,Y-2) (West)"
