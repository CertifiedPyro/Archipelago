from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location

from . import items
from .data.locations_generated import EVENTS, LOCATIONS

if TYPE_CHECKING:
    from .world import PipWorld


class PipLocation(Location):
    game = "Pipistrello and the Cursed Yoyo"


LOCATION_NAME_TO_ID = {d.full_location_name: idx + 1 for idx, d in enumerate(LOCATIONS)}
"""Map of location name to numerical id. This is required for the Archipelago world."""


def create_all_locations(world: PipWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: PipWorld) -> None:
    for idx, d in enumerate(LOCATIONS):
        loc_name_lower = d.full_location_name.lower()
        if "money bag" in loc_name_lower and not world.options.moneysanity:
            continue

        if "combat" in loc_name_lower and "optional" in loc_name_lower and not world.options.moneysanity:
            continue

        r = world.get_region(d.region_name)
        r.add_locations({d.full_location_name: idx + 1}, PipLocation)


def create_events(world: PipWorld) -> None:
    pl = PipLocation
    pi = items.PipItem
    for d in EVENTS:
        r = world.get_region(d.region_name)
        r.add_event(d.full_location_name, d.full_item_name, location_type=pl, item_type=pi)
