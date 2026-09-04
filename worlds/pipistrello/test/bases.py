import itertools
import typing
from warnings import deprecated

from BaseClasses import CollectionState, Entrance, Location, Region
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
        checks: list[Location | Entrance | Region],
        possible_items: list[list[str]],
    ) -> None:
        """Asserts that the provided locations can't be reached without the listed items but can be reached with any
        one of the provided combinations"""
        # Don't collect any event items either.
        all_possible_items = [item_name for item_names in possible_items for item_name in item_names]
        event_items = [item.name for item in self.multiworld.get_items() if item.is_event]
        all_items = all_possible_items + event_items

        # Ensure that checks cannot be reached if all other non-event items are collected.
        state = CollectionState(self.multiworld)
        self.collect_all_but(all_items, state)
        for check in checks:
            self.assertFalse(
                state.can_reach(check, player=self.player),
                f"{check.name} is reachable without event items and {sorted(set(all_possible_items))}",
            )

        for item_names in possible_items:
            # Reset state each time.
            state = CollectionState(self.multiworld)
            self.collect_all_but(all_items, state)

            # Find specific item, then collect.
            # This avoids collecting all of an item, for example.
            for item_name in item_names:
                item = self.get_item_by_name(item_name)
                state.collect(item)
            for check in checks:
                self.assertTrue(
                    state.can_reach(check, player=self.player), f"{check.name} is not reachable with {item_names}"
                )

    def assert_no_access_dependency_combos(
        self, checks: list[Location | Entrance | Region], possible_items: list[list[str]], check_items: list[list[str]]
    ) -> None:
        """Asserts that the provided locations can't be reached with a missing item from check_items"""
        # Don't collect any event items either.
        all_possible_items = [item_name for item_names in possible_items for item_name in item_names]
        event_items = [item.name for item in self.multiworld.get_items() if item.is_event]
        all_items = all_possible_items + event_items

        for item_names in check_items:
            # If there's more than 1 item in item_names,
            # check that collecting everything but 1 of those items doesn't make the check reachable.
            if len(item_names) > 1:
                combinations = list(itertools.combinations(item_names, len(item_names) - 1))
                for combo in combinations:
                    # Reset state each time.
                    state = CollectionState(self.multiworld)
                    self.collect_all_but(all_items, state)

                    # Find specific item, then collect.
                    # This avoids collecting all of an item, for example.
                    for item_name in combo:
                        item = self.get_item_by_name(item_name)
                        state.collect(item)
                    for check in checks:
                        self.assertFalse(
                            state.can_reach(check, player=self.player), f"{check.name} is reachable with {combo}"
                        )
