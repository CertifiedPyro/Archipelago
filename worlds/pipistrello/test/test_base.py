from collections.abc import Iterable
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from BaseClasses import CollectionState, Location, Region

from .. import regions
from ..data.locations_generated import LOCATIONS
from ..options import Difficulty, Moneysanity
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
    possible_items: dict[int, Iterable[Iterable[str]] | None]


class LogicTestMixinBase(_LogicTestBase):
    run_default_tests = False

    origin_room_label = ""
    test_case: ClassVar[TestCase]

    def test_generic(self) -> None:
        self._set_origin_region()

        current_difficulty = self.options["difficulty"]
        filtered_possible_items = {k: v for k, v in self.test_case.possible_items.items() if k <= current_difficulty}
        if len(filtered_possible_items) == 0:
            self.skipTest(f"{self._get_test_name()} is not applicable at difficulty {current_difficulty}")

        check = self._get_check(self.test_case.room_name, self.test_case.location_map_name)
        if None in filtered_possible_items.values():
            state = CollectionState(self.multiworld)
            state.sweep_for_advancements()
            self.assertTrue(state.can_reach(check), f"{check.name} not reachable without items")
        else:
            all_possible_items = [item for sublist in filtered_possible_items.values() for item in sublist]
            self.assert_access_dependency([check], all_possible_items)

    def _get_check(self, room_label: str, location_map_name: str | None = None) -> Location | Region:
        room = regions.get_room_by_room_label(room_label)
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

    def _get_test_name(self) -> str:
        return (
            f"{self.test_case.room_name}: {self.test_case.location_map_name}"
            if self.test_case.location_map_name
            else self.test_case.room_name
        )
