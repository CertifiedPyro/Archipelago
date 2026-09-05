from options import Difficulty
from test.param import classvar_matrix

from ..constants import Badges as B
from ..constants import Moves as M
from .test_base import LogicTestMixinBase, TestCase, TestExpertLogic, TestHardLogic, TestNormalLogic

ORIGIN_ROOM_LABEL = "South Plaza (X-2, Y-3) - ren223 (Main)"
TEST_CASES = [
    # Skip Golden Badge and Diamond 1, which should be bundled with Faria
    # Skip Hellhound Badge, which should be bundled with Gallineiros
    TestCase(
        room_label="Safe House (X+0, Y+0) - mig38",
        location_map_name="Badge (Eye)",
        possible_items={Difficulty.option_normal: None},
    ),
    TestCase(
        room_label="South Plaza (X-2, Y+4) - yug5210",
        location_map_name="Badge (Pitcher's)",
        possible_items={Difficulty.option_normal: [[M.DOG], [M.DASH], [M.UFO], [M.RIDE], [B.SS]]},
    ),
    TestCase(
        room_label="South Plaza (X+2, Y+4) - yug5154",
        location_map_name="BP Shard 1",
        possible_items={Difficulty.option_normal: [[M.UFO], [M.RIDE]]},
    ),
    TestCase(
        room_label="South Plaza (X-2, Y-3) - ren223 (Main)",
        location_map_name="Combat 1 (optional)",
        possible_items={Difficulty.option_normal: None},
    ),
    TestCase(
        room_label="South Plaza (X-3, Y+3) - ren4152",
        location_map_name="Combat 2",
        possible_items={Difficulty.option_normal: [[M.DOG], [M.UFO], [M.RIDE], [B.SS]]},
    ),
    # Skip trivial Moneybag 1-4
    TestCase(
        room_label="South Plaza (X-2, Y-3) - ren223 (Southwest)",
        location_map_name="Moneybag 5",
        possible_items={Difficulty.option_normal: [[M.DOG], [M.UFO], [M.RIDE], [B.SS]]},
    ),
    TestCase(
        room_label="South Plaza (X-2, Y-3) - ren223 (Main)",
        location_map_name="Moneybag 6",
        possible_items={Difficulty.option_normal: None},
    ),
    TestCase(
        room_label="South Plaza (X-1, Y-6) - ren355 (East)",
        location_map_name="Moneybag 7",
        possible_items={Difficulty.option_normal: [[M.RIDE], [M.UFO, M.DOG]]},
    ),
    # Skip trivial Moneybag 8
    TestCase(
        room_label="South Plaza (X-1, Y+4) - lor2248 (North)",
        location_map_name="Moneybag 9",
        possible_items={Difficulty.option_normal: [[M.DOG], [M.DASH], [M.UFO], [M.RIDE], [B.SS]]},
    ),
    TestCase(
        room_label="South Plaza (X+1, Y+4) - yug4939 (West)",
        location_map_name="Moneybag 10",
        possible_items={Difficulty.option_normal: [[M.DOG], [M.DASH], [M.UFO], [M.RIDE], [B.SS]]},
    ),
    TestCase(
        room_label="South Plaza (X+1, Y+4) - yug4939 (West)",
        location_map_name="Moneybag 11",
        possible_items={Difficulty.option_normal: [[M.DOG], [M.DASH], [M.UFO], [M.RIDE], [B.SS]]},
    ),
    TestCase(
        room_label="South Plaza (X+1, Y+4) - yug4939 (East)",
        location_map_name="Moneybag 12",
        possible_items={Difficulty.option_normal: [[M.DASH], [M.UFO], [M.RIDE]]},
    ),
    TestCase(
        room_label="South Plaza (X-2, Y-3) - ren223 (South)",
        location_map_name="Musical Notes 1",
        possible_items={
            Difficulty.option_normal: [
                [M.OFF, M.DOG],
                [M.OFF, M.DASH],
                [M.OFF, M.UFO],
                [M.OFF, M.RIDE],
                [M.OFF, B.SS],
            ]
        },
    ),
    TestCase(
        room_label="South Plaza (X-2, Y-3) - ren223 (South)",
        location_map_name="Musical Notes 2",
        possible_items={
            Difficulty.option_normal: [
                [M.OFF, M.DOG],
                [M.OFF, M.DASH],
                [M.OFF, M.UFO],
                [M.OFF, M.RIDE],
                [M.OFF, B.SS],
            ],
            Difficulty.option_expert: [
                [M.ATW, M.DOG],
                [M.ATW, M.DASH],
                [M.ATW, M.UFO],
                [M.RIDE],
                [M.ATW, B.SS],
            ],
        },
    ),
    TestCase(
        room_label="South Plaza (X-2, Y-3) - ren223 (Main)",
        location_map_name="Petal Container 1",
        possible_items={Difficulty.option_normal: None},
    ),
    TestCase(
        room_label="South Plaza (X-2, Y-3) - ren223 (Main)",
        location_map_name="Quest (Burger 1)",
        possible_items={Difficulty.option_normal: None},
    ),
    # Skip trivial Taxi Phone 1
    # Skip Sewers, since it depends on Faria water section.
    # TestCase(
    #     room_name="South Plaza (Sewers) (X-1, Y+5) - yug1700 (East)",
    #     location_map_name="Moneybag 1",
    #     possible_items={
    #         Difficulty.option_normal: [[M.OFF, M.DOG, M.UFO], [M.OFF, M.DOG, M.RIDE]],
    #     },
    # ),
    # TestCase(
    #     room_name="South Plaza (Sewers) (X-1, Y+5) - yug1700 (East)",
    #     location_map_name="Petal Container 1",
    #     possible_items={
    #         Difficulty.option_normal: [[M.OFF, M.DOG, M.UFO], [M.OFF, M.DOG, M.RIDE]],
    #     },
    # ),
]


@classvar_matrix(test_case=TEST_CASES)
class TestSouthPlazaNormalLogic(LogicTestMixinBase, TestNormalLogic):
    origin_room_label = ORIGIN_ROOM_LABEL
    pass


@classvar_matrix(test_case=TEST_CASES)
class TestSouthPlazaHardLogic(LogicTestMixinBase, TestHardLogic):
    origin_room_label = ORIGIN_ROOM_LABEL
    pass


@classvar_matrix(test_case=TEST_CASES)
class TestSouthPlazaExpertLogic(LogicTestMixinBase, TestExpertLogic):
    origin_room_label = ORIGIN_ROOM_LABEL
    pass
