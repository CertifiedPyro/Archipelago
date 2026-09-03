from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region

from .data.regions_generated import CONNECTIONS, ROOMS

if TYPE_CHECKING:
    from .world import PipWorld


REGION_NAME_TO_ROOM = {d.region_name: d for d in ROOMS}
ROOM_NAME_TO_ROOM = {d.room_label: d for d in ROOMS}


def create_and_connect_regions(world: PipWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: PipWorld) -> None:
    world.multiworld.regions += [Region(d.region_name, world.player, world.multiworld) for d in ROOMS]


def connect_regions(world: PipWorld) -> None:
    for d in CONNECTIONS:
        world.get_region(d.start_region_name).connect(world.get_region(d.end_region_name))
