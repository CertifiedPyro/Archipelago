from options import Difficulty
from test.param import classvar_matrix

from ..constants import Badges as B
from ..constants import Moves as M
from ..constants import OtherItems as OI
from ..constants import Upgrades as U
from .test_base import LogicTestMixinBase, TestCase, TestExpertLogic, TestHardLogic, TestNormalLogic

ORIGIN_ROOM_LABEL = "SlimeCorp Excavation Site (X+0, Y+0) - lor149 (Main)"
TEST_CASES = [
    TestCase(  # Room on top-left w/ 2 cogs
        room_label="SlimeCorp Excavation Site (X-2, Y-1) - lor524 (Main)",
        location_map_name=None,
        possible_items={Difficulty.option_normal: [[M.OFF], [M.COINFLIP, U.PRODIGY], [M.DASH], [M.RIDE], [M.UFO]]},
    ),
    TestCase(  # Room before one-way path to dungeon
        room_label="SlimeCorp Excavation Site (X+1, Y+4) - lor755",
        location_map_name=None,
        possible_items={Difficulty.option_normal: [[M.DASH], [M.RIDE], [M.UFO]]},
    ),
    TestCase(
        room_label="SlimeCorp Excavation Site (X+5, Y-1) - lor1228",
        location_map_name="Badge (Wing)",
        possible_items={Difficulty.option_normal: [[M.OFF]]},
    ),
    TestCase(
        room_label="SlimeCorp Excavation Site (X+2, Y+4) - lor770",
        location_map_name="Badge (Berserker)",
        possible_items={Difficulty.option_normal: [[M.DASH], [M.RIDE], [M.UFO]]},
    ),
    TestCase(
        room_label="SlimeCorp Excavation Site (X+4, Y+3) - lor256",
        location_map_name="BP Shard 1",
        possible_items={
            Difficulty.option_normal: [
                [M.DASH],
                [M.RIDE],
                [M.UFO],
                [M.DOG, M.OFF],
                [M.DOG, M.COINFLIP, U.PRODIGY],
                [B.SS, M.OFF],
                [B.SS, M.COINFLIP, U.PRODIGY],
            ]
        },
    ),
    TestCase(
        room_label="SlimeCorp Excavation Site (X+0, Y+8) - lor1089",
        location_map_name="Mega-Battery",
        possible_items={Difficulty.option_normal: [[M.DASH] + [OI.PETAL] * 8], Difficulty.option_expert: [[M.DASH]]},
    ),
    # Only include notable money bags
    TestCase(
        room_label="SlimeCorp Excavation Site (X+4, Y-2) - lor179 (South Money Bag)",
        location_map_name="Moneybag 5",
        possible_items={Difficulty.option_normal: None},
    ),
    TestCase(
        room_label="SlimeCorp Excavation Site (X-3, Y-1) - lor534",
        location_map_name="Moneybag 17",
        possible_items={Difficulty.option_normal: [[M.OFF]], Difficulty.option_hard: [[M.DASH, M.UFO, M.RIDE]]},
    ),
    TestCase(
        room_label="SlimeCorp Excavation Site (X-4, Y-1) - lor1299",
        location_map_name="Moneybag 18",
        possible_items={
            Difficulty.option_normal: [
                [M.RIDE, M.OFF],
                [M.RIDE, M.COINFLIP, U.PRODIGY],
            ],
            Difficulty.option_hard: [[M.RIDE, M.DASH, M.UFO]],
        },
    ),
    TestCase(
        room_label="SlimeCorp Excavation Site (X-4, Y+7) - lor1309",
        location_map_name="Moneybag 28",
        possible_items={Difficulty.option_normal: [[M.DASH, M.RIDE]], Difficulty.option_hard: [[M.RIDE]]},
    ),
    # Skip Petal Container 1, which is (mostly) covered by room rule
    TestCase(
        room_label="SlimeCorp Excavation Site (X-4, Y+6) - yug3 (West)",
        location_map_name="Petal Container 2",
        possible_items={Difficulty.option_normal: [[M.DASH], [M.RIDE]]},
    ),
    TestCase(
        room_label="SlimeCorp Excavation Site (X+3, Y+5) - lor856",
        location_map_name="Petal Container 3",
        possible_items={Difficulty.option_normal: [[M.DASH], [M.RIDE], [M.UFO]]},
    ),
]


@classvar_matrix(test_case=TEST_CASES)
class TestExcavationNormalLogic(LogicTestMixinBase, TestNormalLogic):
    origin_room_label = ORIGIN_ROOM_LABEL
    pass


@classvar_matrix(test_case=TEST_CASES)
class TestExcavationHardLogic(LogicTestMixinBase, TestHardLogic):
    origin_room_label = ORIGIN_ROOM_LABEL
    pass


@classvar_matrix(test_case=TEST_CASES)
class TestExcavationExpertLogic(LogicTestMixinBase, TestExpertLogic):
    origin_room_label = ORIGIN_ROOM_LABEL
    pass
