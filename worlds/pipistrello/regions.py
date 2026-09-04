from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region

from .data.data_classes import RoomData
from .data.regions_generated import CONNECTIONS, ROOMS

if TYPE_CHECKING:
    from .world import PipWorld


_REGION_NAME_TO_ROOM = {d.region_name: d for d in ROOMS}
_ROOM_LABEL_TO_ROOM = {d.room_label: d for d in ROOMS}


def create_and_connect_regions(world: PipWorld) -> None:
    _create_all_regions(world)
    _connect_regions(world)


def get_room_by_region_name(region_name: str) -> RoomData:
    if region_name in _REGION_NAME_TO_ROOM:
        return _REGION_NAME_TO_ROOM[region_name]

    raise KeyError(f"No room found for region name {region_name}")


def get_room_by_room_label(room_label: str) -> RoomData:
    if room_label in _ROOM_LABEL_TO_ROOM:
        return _ROOM_LABEL_TO_ROOM[room_label]

    raise KeyError(f"No room found for room label {room_label}")


def _create_all_regions(world: PipWorld) -> None:
    world.multiworld.regions += [Region(d.region_name, world.player, world.multiworld) for d in ROOMS]


def _connect_regions(world: PipWorld) -> None:
    for d in CONNECTIONS:
        world.get_region(d.start_region_name).connect(world.get_region(d.end_region_name))
