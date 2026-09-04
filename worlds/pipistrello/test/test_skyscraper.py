from options import Difficulty

from ..constants import Moves as M
from .test_base import LogicTestMixinBase, TestCase, TestExpertLogic, TestHardLogic, TestNormalLogic

test_cases = [
    TestCase(  # Room with 2 key blocks
        room_name="SlimeCorp Skyscraper (X+3, Y-4) - lor97 (Main)",
        location_map_name=None,
        possible_items={Difficulty.option_normal: [[M.OFF], [M.UFO], [M.RIDE]]},
    ),
    TestCase(
        room_name="SlimeCorp Skyscraper (X+4, Y-1) - lor54",
        location_map_name="Badge (Stun)",
        possible_items={Difficulty.option_normal: [[M.OFF]], Difficulty.option_expert: [[M.DASH, M.RIDE]]},
    ),
    TestCase(
        room_name="SlimeCorp Skyscraper (X+3, Y-4) - lor97 (Southeast)",
        location_map_name="BP Shard 1",
        possible_items={Difficulty.option_normal: [[M.OFF], [M.UFO]], Difficulty.option_hard: [[M.DASH, M.RIDE]]},
    ),
    TestCase(
        room_name="SlimeCorp Skyscraper (X+0, Y-4) - lor187",
        location_map_name="Staff ID",
        possible_items={Difficulty.option_normal: [[M.OFF], [M.UFO], [M.RIDE]]},
    ),
]


class SkyscraperLogicTestMixin(LogicTestMixinBase):
    origin_room_label = "SlimeCorp Skyscraper (X+0, Y-2) - lor2 (West)"
    test_cases = test_cases


class TestSkyscraperNormalLogic(SkyscraperLogicTestMixin, TestNormalLogic):
    pass


class TestSkyscraperHardLogic(SkyscraperLogicTestMixin, TestHardLogic):
    pass


class TestSkyscraperExpertLogic(SkyscraperLogicTestMixin, TestExpertLogic):
    pass


# class TestSkyscraperCustomLogic(TestNormalLogic):
#     run_default_tests = False
#
#     def test_starting_room(self) -> None:
#         self._set_origin_region()
#         start_room_east = self.world.get_region("Skyscraper (X+0, Y-2) (East)")
#
#         with self.subTest("Test east side of starting room is reachable with vanilla logic"):
#             self.assertTrue(start_room_east.can_reach(self.multiworld.state))
#
#         with self.subTest("Test east side of starting room is reachable with alternate route"):
#             entrance = self.world.get_entrance("Skyscraper (X+0, Y-2) (West) -> Skyscraper (X+0, Y-2) (East)")
#             self.world.set_rule(entrance, False_())
#             possible_items = {
#                 "Wall-Ride + Wall-Dash": [M.RIDE, M.DASH],
#                 "UFO Throw": [M.UFO],
#             }
#             self.assert_access_dependency([start_room_east], possible_items.values())
#
#     def _set_origin_region(self) -> None:
#         self.world.origin_region_name = "Skyscraper (X+0, Y-2) (West)"
