from options import Difficulty
from test.param import classvar_matrix

from ..constants import Badges as B
from ..constants import Moves as M
from ..constants import SpecialItems as SI
from .test_base import LogicTestMixinBase, TestCase, TestExpertLogic, TestHardLogic, TestNormalLogic

ORIGIN_ROOM_LABEL = "South Plaza (X-2, Y-3) - ren223 (Main)"
TEST_CASES = [
    TestCase(  # Mini-dungeon starting room
        room_label="SlimeCorp Skyscraper (X+0, Y-2) - lor2 (West)",
        location_map_name=None,
        possible_items={
            Difficulty.option_normal: [[M.OFF], [M.DOG], [M.DASH], [M.RIDE], [M.UFO], [B.SS]],
            Difficulty.option_hard: None,
        },
    ),
    TestCase(  # Dungeon starting room
        room_label="SlimeCorp Excavation Site (X+0, Y+0) - lor149 (Main)",
        location_map_name=None,
        possible_items={
            Difficulty.option_normal: [[SI.FARIA_STAFF_ID]],
        },
    ),
    TestCase(  # Water section start
        room_label="Faria Slimer Borough (X+10, Y+2) - lor2334 (Main)",
        location_map_name=None,
        possible_items={
            Difficulty.option_normal: [[M.DASH], [M.RIDE], [M.UFO]],
        },
    ),
    TestCase(  # Water section end
        room_label="South Plaza (X-1, Y+4) - lor2248 (Southeast)",
        location_map_name="Badge (Golden)",
        possible_items={
            Difficulty.option_normal: [[M.DOG, M.DASH], [M.DOG, M.RIDE], [M.DOG, M.UFO]],
            Difficulty.option_hard: [[M.DASH, M.RIDE, B.SS], [M.RIDE, B.SS, B.SS]],
        },
    ),
]


@classvar_matrix(test_case=TEST_CASES)
class TestFariaNormalLogic(LogicTestMixinBase, TestNormalLogic):
    origin_room_label = ORIGIN_ROOM_LABEL
    pass


@classvar_matrix(test_case=TEST_CASES)
class TestFariaHardLogic(LogicTestMixinBase, TestHardLogic):
    origin_room_label = ORIGIN_ROOM_LABEL
    pass


@classvar_matrix(test_case=TEST_CASES)
class TestFariaExpertLogic(LogicTestMixinBase, TestExpertLogic):
    origin_room_label = ORIGIN_ROOM_LABEL
    pass
