from collections.abc import Iterable
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from BaseClasses import Location, Region

from ..data.locations_generated import LOCATIONS
from ..options import Difficulty, Moneysanity
from ..regions import ROOM_NAME_TO_ROOM
from .bases import PipTestBase

if TYPE_CHECKING:
    _LogicTestBase = PipTestBase
else:
    _LogicTestBase = object


class TestNormalLogic(PipTestBase):
    options = {"difficulty": Difficulty.option_normal, "moneysanity": Moneysanity.option_true}


class TestHardLogic(PipTestBase):
    options = {"difficulty": Difficulty.option_hard, "moneysanity": Moneysanity.option_true}


class TestExpertLogic(PipTestBase):
    options = {"difficulty": Difficulty.option_expert, "moneysanity": Moneysanity.option_true}


@dataclass
class TestCase:
    room_name: str
    location_map_name: str | None
    possible_items: dict[int, Iterable[Iterable[str]]]


class LogicTestMixinBase(_LogicTestBase):
    run_default_tests = False

    origin_room_label = ""
    test_cases: ClassVar[list[TestCase]]

    def test_generic(self) -> None:
        self._set_origin_region()
        current_difficulty = self.options["difficulty"]
        for test_case in self.test_cases:
            all_possible_items = []
            for difficulty, possible_items in test_case.possible_items.items():
                if difficulty <= current_difficulty:
                    all_possible_items += possible_items

            if len(all_possible_items) == 0:
                continue

            check = self._get_check(test_case.room_name, test_case.location_map_name)
            if test_case.possible_items is None:
                self.assertTrue(self.multiworld.state.can_reach(check))
            else:
                with self.subTest(check.name):
                    self.assert_access_dependency([check], all_possible_items)

    def _get_check(self, room_label: str, location_map_name: str | None = None) -> Location | Region:
        room = ROOM_NAME_TO_ROOM[room_label]
        if location_map_name is None:
            return self.world.get_region(room.region_name)

        location_data = next(
            data for data in LOCATIONS if data.region_name == room.region_name and data.map_name == location_map_name
        )
        return self.world.get_location(location_data.full_location_name)

    def _set_origin_region(self) -> None:
        region = self._get_check(self.origin_room_label, None)
        if isinstance(region, Region):
            self.world.origin_region_name = region.name
        else:
            raise Exception(f"Could not find region from room label {self.origin_room_label}")
