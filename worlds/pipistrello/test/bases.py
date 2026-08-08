import typing
from warnings import deprecated

from BaseClasses import CollectionState
from test.bases import WorldTestBase

from ..world import PipWorld


class PipTestBase(WorldTestBase):
    game = "Pipistrello and the Cursed Yoyo"
    world: PipWorld

    @typing.override
    @deprecated("Use assert_access_dependency() instead")
    def assertAccessDependency(
        self,
        locations: list[str],
        possible_items: typing.Iterable[typing.Iterable[str]],
        only_check_listed: bool = False,
    ) -> None:
        pass

    def assert_access_dependency(
        self,
        locations: list[str],
        possible_items: typing.Iterable[typing.Iterable[str]],
    ) -> None:
        """Asserts that the provided locations can't be reached without the listed items but can be reached with any
        one of the provided combinations"""
        all_items = [item_name for item_names in possible_items for item_name in item_names]

        state = CollectionState(self.multiworld)
        self.collect_all_but(all_items, state)
        for location in locations:
            self.assertFalse(
                state.can_reach(location, "Location", self.player), f"{location} is reachable without {all_items}"
            )

        for item_names in possible_items:
            # Find specific item, then collect.
            # This avoids collecting all of an item, for example.
            for item_name in item_names:
                item = self.get_item_by_name(item_name)
                state.collect(item)
            for location in locations:
                self.assertTrue(
                    state.can_reach(location, "Location", self.player), f"{location} not reachable with {item_names}"
                )
            for item_name in item_names:
                item = self.get_item_by_name(item_name)
                state.remove(item)
