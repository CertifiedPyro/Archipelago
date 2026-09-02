from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.rules import CanReachRegion

from . import regions
from .data.rules_generated import ENTRANCE_RULES, LOCATION_RULES

if TYPE_CHECKING:
    from .world import PipWorld


def set_all_rules(world: PipWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: PipWorld) -> None:
    for entrance_name, rule in ENTRANCE_RULES.items():
        world.set_rule(world.get_entrance(entrance_name), rule)


def set_all_location_rules(world: PipWorld) -> None:
    for location_name, rule in LOCATION_RULES.items():
        loc_name_lower = location_name.lower()
        if "money bag" in loc_name_lower and not world.options.moneysanity:
            continue

        if "combat" in loc_name_lower and "optional" in loc_name_lower and not world.options.moneysanity:
            continue

        world.set_rule(world.get_location(location_name), rule)


def set_completion_condition(world: PipWorld) -> None:
    # TODO: Set to North Plaza
    end_region = regions.REGION_NAME_TO_ROOM["S Plaza (X-1, Y-6) (North)"].region_name
    world.set_completion_rule(CanReachRegion(end_region))
