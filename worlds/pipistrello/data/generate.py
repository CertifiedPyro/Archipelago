import csv
import json
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path

import jinja2

# This dict maps area names to their user-facing region names.
# This configures which areas are emitted.
AREA_NAMES = {
    "South Plaza": "SP",
    "South Plaza (Interiors)": "SP Interiors",
    "South Plaza (Sewers)": "SP Sewers",
}

DATA_DIR = Path(__file__).resolve().parent
FULL_ROOMS_CSV = DATA_DIR / "full_rooms.csv"
CONNECTIONS_CSV = DATA_DIR / "connections.csv"
LOCATIONS_CSV = DATA_DIR / "locations.csv"

REGIONS_OUTPUT_FILE = DATA_DIR / "generated_regions.py"
LOCATIONS_OUTPUT_FILE = DATA_DIR / "generated_locations.py"
OBJECT_ID_OUTPUT_FILE = DATA_DIR / "object_id_mapping.json"


@dataclass
class RoomData:
    room_label: str
    """The full room label in the spreadsheet (e.g. South Plaza (X-2, Y-3) - ren223 (Main))."""
    room_area: str
    """The map area in-game (e.g. South Plaza)."""
    region_name: str
    """The Archipelago region name."""
    global_room_id: str
    """The global room ID (e.g. city/ren223 (Main))."""
    suffix: str
    """The Archipelago region suffix (e.g. (Main))."""
    full_global_room_id: str = field(init=False, repr=False)
    """The full global room ID (including suffix)."""

    def __post_init__(self) -> None:
        self.full_global_room_id = f"{self.global_room_id}{self.suffix}"


@dataclass
class ConnectionData:
    start_region_name: str
    """The connection start's Archipelago region name."""
    end_region_name: str
    """The connection end's Archipelago region name."""


@dataclass
class LocationData:
    region_name: str
    """The Archipelago region name."""
    location_name: str
    """The Archipelago location name (excluding region name)."""
    global_object_id: str
    """The global object ID in-game (e.g. city/ren223/yug2063)."""
    map_name: str
    """The Canva map name (e.g. Moneybag 1)."""
    id: int
    """The Archipelago location ID (e.g. 1)."""
    full_location_name: str = field(init=False, repr=False)
    """The full Archipelago location name (including region name)."""

    def __post_init__(self) -> None:
        self.full_location_name = f"{self.region_name}: {self.location_name}"


@dataclass
class EventData:
    region_name: str
    """The Archipelago region name."""
    location_name: str
    """The Archipelago location name (excluding region name)."""
    item_name: str
    """The Archipelago event item name (excluding region/location name)."""
    global_object_id: str
    """The global object ID in-game (e.g. city/ren223/yug5535)."""
    map_name: str
    """The Canva map name (e.g. Moneybag 1)."""
    full_location_name: str = field(init=False, repr=False)
    """The full Archipelago location name (including region name)."""
    full_item_name: str = field(init=False, repr=False)
    """The full Archipelago item name (including region/location name)."""

    def __post_init__(self) -> None:
        self.full_location_name = f"{self.region_name}: {self.location_name}"
        # self.full_item_name = f"{self.full_location_name}: {self.item_name}"
        self.full_item_name = f"{self.full_location_name}"


RoomDict = dict[str, RoomData]
"""A dict of room labels to :class:`RoomData`."""


def read_full_rooms_csv() -> RoomDict:
    room_dict: RoomDict = {"Menu": RoomData("Menu", "Menu", "Menu", "", "")}
    with FULL_ROOMS_CSV.open(encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            room_area = row["Area"]
            if room_area not in AREA_NAMES:
                continue

            room_label = row["Full Room Label"]
            region_area = AREA_NAMES[room_area]
            region_name = f"{region_area} ({int(row['X']):+},{int(row['Y']):+}){row['Suffix']}"
            room_dict[room_label] = RoomData(
                room_label=room_label,
                room_area=room_area,
                region_name=region_name,
                global_room_id=f"{row['Map ID']}/{row['Room ID']}",
                suffix=row["Suffix"],
            )
    return room_dict


def read_connections_csv(room_dict: RoomDict) -> list[ConnectionData]:
    connections: list[ConnectionData] = [
        ConnectionData(room_dict["Menu"].region_name, room_dict["South Plaza (X-2, Y-3) - ren223 (Main)"].region_name)
    ]
    with CONNECTIONS_CSV.open(encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            room1 = row["Room Label 1"]
            room2 = row["Room Label 2"]
            # Check that both rooms are in included areas.
            if room1 not in room_dict or room2 not in room_dict:
                continue

            connections.append(ConnectionData(room_dict[room1].region_name, room_dict[room2].region_name))
            if row["↔️"] == "TRUE":
                connections.append(ConnectionData(room_dict[room2].region_name, room_dict[room1].region_name))
    return connections


def read_locations_csv(room_dict: RoomDict) -> tuple[list[LocationData], list[EventData]]:
    locations: list[LocationData] = []
    events: list[EventData] = []
    with LOCATIONS_CSV.open(encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            # Only include locations that are in eligible rooms and are not excluded.
            room_label = row["Room Label"]
            if room_label not in room_dict or row["❌"] == "TRUE":
                continue

            room_data = room_dict[room_label]
            region_name = room_data.region_name
            object_ids = row["Object Ids"].split(",")
            location_name = row["Name"]

            if row["Type"] == "Event":
                item_name = ""
                if "Combat" in location_name:
                    item_name = "Complete"
                elif "Burger" == location_name or "Key" in location_name:
                    item_name = "Acquired"
                elif "Lever" in location_name:
                    item_name = "Activated"
                events.append(
                    EventData(
                        region_name,
                        location_name,
                        item_name,
                        f"{room_data.global_room_id}/{object_ids[0]}",
                        row["Map Name"],
                    )
                )
            elif len(object_ids) == 1:
                locations.append(
                    LocationData(
                        region_name,
                        location_name,
                        f"{room_data.global_room_id}/{object_ids[0]}",
                        row["Map Name"],
                        i * 10 + 1,
                    )
                )
            else:
                locations.extend(
                    LocationData(
                        region_name,
                        f"{location_name} {j + 1}",
                        f"{room_data.global_room_id}/{object_ids[j]}",
                        row["Map Name"],
                        i * 10 + j + 1,
                    )
                    for j in range(len(object_ids))
                )

    return locations, events


def write_generated_regions(
    rooms: Iterable[RoomData],
    connections: Iterable[ConnectionData],
) -> None:
    template = jinja2.Environment(
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template.filters["quote"] = json.dumps

    output = template.from_string("""# THIS FILE IS AUTOMATICALLY GENERATED. DO NOT MANUALLY EDIT.
# RUN "Reformat Code" AFTER GENERATION.
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RoomData:
    room_label: str
    '''The full room label in the spreadsheet (e.g. South Plaza (X-2, Y-3) - ren223 (Main)).'''
    room_area: str
    '''The map area in-game (e.g. South Plaza).'''
    region_name: str
    '''The Archipelago region name.'''
    global_room_id: str
    '''The global room ID (e.g. city/ren223 (Main)).'''
    suffix: str
    '''The Archipelago region suffix (e.g. (Main)).'''
    full_global_room_id: str = field(init=False, repr=False)
    '''The full global room ID (including suffix).'''

    def __post_init__(self) -> None:
        self.full_global_room_id = f"{self.global_room_id}{self.suffix}"


@dataclass
class ConnectionData:
    start_region_name: str
    '''The connection start's Archipelago region name.'''
    end_region_name: str
    '''The connection end's Archipelago region name.'''


ROOMS: list[RoomData] = [
{% for d in rooms %}
    {{ d }},
{% endfor %}
]

CONNECTIONS: list[ConnectionData] = [
{% for d in connections %}
    {{ d }},
{% endfor %}
]
\n""").render(rooms=rooms, connections=connections)
    REGIONS_OUTPUT_FILE.write_text(output, encoding="utf-8")


def write_generated_locations(
    locations: list[LocationData],
    events: list[EventData],
) -> None:
    template = jinja2.Environment(
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template.filters["quote"] = json.dumps

    output = template.from_string("""# THIS FILE IS AUTOMATICALLY GENERATED. DO NOT MANUALLY EDIT.
# RUN "Reformat Code" AFTER GENERATION.
from __future__ import annotations

from dataclasses import dataclass, field

from BaseClasses import Location


class PipLocation(Location):
    game = "Pipistrello and the Cursed Yoyo"


@dataclass
class LocationData:
    region_name: str
    '''The Archipelago region name.'''
    location_name: str
    '''The Archipelago location name (excluding region name).'''
    global_object_id: str
    '''The global object ID in-game (e.g. city/ren223/yug2063).'''
    map_name: str
    '''The Canva map name (e.g. Moneybag 1).'''
    id: int
    '''The Archipelago location ID (e.g. 1).'''
    full_location_name: str = field(init=False, repr=False)
    '''The full Archipelago location name (including region name).'''

    def __post_init__(self) -> None:
        self.full_location_name = f"{self.region_name}: {self.location_name}"


@dataclass
class EventData:
    region_name: str
    '''The Archipelago region name.'''
    location_name: str
    '''The Archipelago location name (excluding region name).'''
    item_name: str
    '''The Archipelago event item name (excluding region/location name).'''
    global_object_id: str
    '''The global object ID in-game (e.g. city/ren223/yug5535).'''
    map_name: str
    '''The Canva map name (e.g. Moneybag 1).'''
    full_location_name: str = field(init=False, repr=False)
    '''The full Archipelago location name (including region name).'''
    full_item_name: str = field(init=False, repr=False)
    '''The full Archipelago item name (including region/location name).'''

    def __post_init__(self) -> None:
        self.full_location_name = f"{self.region_name}: {self.location_name}"
        # self.full_item_name = f"{self.full_location_name}: {self.item_name}"
        self.full_item_name = f"{self.full_location_name}"


LOCATION_DATA: list[LocationData] = [
{% for d in locations %}
    {{ d }},
{% endfor %}
]

EVENT_DATA: list[EventData] = [
{% for d in events %}
    {{ d }},
{% endfor %}
]
\n""").render(locations=locations, events=events)
    LOCATIONS_OUTPUT_FILE.write_text(output, encoding="utf-8")


def write_object_id_mapping(locations: list[LocationData]):
    global_object_id_to_id: dict[str, str] = {}
    for location in locations:
        global_object_id_to_id[location.global_object_id] = location.full_location_name

    output = json.dumps(global_object_id_to_id, indent=2)
    OBJECT_ID_OUTPUT_FILE.write_text(output, encoding="utf-8")


if __name__ == "__main__":
    room_data_dict = read_full_rooms_csv()
    connection_datas = read_connections_csv(room_data_dict)
    location_datas, event_datas = read_locations_csv(room_data_dict)
    write_generated_regions(room_data_dict.values(), connection_datas)
    write_generated_locations(location_datas, event_datas)
    write_object_id_mapping(location_datas)
