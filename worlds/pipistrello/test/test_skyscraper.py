from options import Difficulty
from test.param import classvar_matrix

from ..constants import Moves as M
from .test_base import LogicTestMixinBase, TestCase, TestExpertLogic, TestHardLogic, TestNormalLogic

ORIGIN_ROOM_LABEL = "SlimeCorp Skyscraper (X+0, Y-2) - lor2 (West)"
TEST_CASES = [
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
        room_name="SlimeCorp Skyscraper (X+2, Y+0) - lor16 (East)",
        location_map_name="Moneybag 1",
        possible_items={Difficulty.option_normal: None},
    ),
    TestCase(
        room_name="SlimeCorp Skyscraper (X+1, Y-5) - lor133",
        location_map_name="Moneybag 2",
        possible_items={Difficulty.option_normal: [[M.OFF], [M.UFO], [M.RIDE]]},
    ),
    TestCase(
        room_name="SlimeCorp Skyscraper (X+4, Y-5) - lor104",
        location_map_name="Moneybag 3",
        possible_items={Difficulty.option_normal: [[M.OFF], [M.UFO], [M.RIDE]]},
    ),
    TestCase(
        room_name="SlimeCorp Skyscraper (X+0, Y-2) - lor2 (West)",
        location_map_name="Musical Notes 1",
        possible_items={Difficulty.option_normal: None},
    ),
    TestCase(
        room_name="SlimeCorp Skyscraper (X+3, Y-4) - lor97 (North)",
        location_map_name="Musical Notes 2",
        possible_items={Difficulty.option_normal: [[M.OFF], [M.UFO], [M.RIDE]]},
    ),
    TestCase(
        room_name="SlimeCorp Skyscraper (X+0, Y-5) - lor151",
        location_map_name="Petal Container 1",
        possible_items={Difficulty.option_normal: [[M.OFF], [M.UFO], [M.RIDE]]},
    ),
    TestCase(
        room_name="SlimeCorp Skyscraper (X+0, Y-4) - lor187",
        location_map_name="Staff ID",
        possible_items={Difficulty.option_normal: [[M.OFF], [M.UFO], [M.RIDE]]},
    ),
]


@classvar_matrix(test_case=TEST_CASES)
class TestSkyscraperNormalLogic(LogicTestMixinBase, TestNormalLogic):
    origin_room_label = ORIGIN_ROOM_LABEL
    pass


@classvar_matrix(test_case=TEST_CASES)
class TestSkyscraperHardLogic(LogicTestMixinBase, TestHardLogic):
    origin_room_label = ORIGIN_ROOM_LABEL
    pass


@classvar_matrix(test_case=TEST_CASES)
class TestSkyscraperExpertLogic(LogicTestMixinBase, TestExpertLogic):
    origin_room_label = ORIGIN_ROOM_LABEL
    pass
