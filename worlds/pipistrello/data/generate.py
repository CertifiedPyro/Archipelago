import csv
import json
import re
from collections.abc import Iterable
from pathlib import Path

import jinja2

from .data_classes import ConnectionData, EventData, LocationData, RoomData

# This dict maps area names to their user-facing region names.
# This configures which areas are emitted.
AREA_NAMES = {
    "Safe House": "Safe House",
    "South Plaza": "S Plaza",
    "South Plaza (Interiors)": "S Plaza Interiors",
    "South Plaza (Sewers)": "S Plaza Sewers",
    "Faria Slimer Borough": "Faria",
    "Faria Slimer Borough (Interiors)": "Faria Interiors",
    "Faria Slimer Borough (Sewers)": "Faria Sewers",
    "SlimeCorp Skyscraper": "Skyscraper",
    "SlimeCorp Excavation Site": "Excavation",
}
AREA_NAMES_KEYS = list(AREA_NAMES.keys())

DATA_DIR = Path(__file__).resolve().parent
FULL_ROOMS_CSV = DATA_DIR / "full_rooms.csv"
CONNECTIONS_CSV = DATA_DIR / "connections.csv"
LOCATIONS_CSV = DATA_DIR / "locations.csv"

REGIONS_OUTPUT_FILE = DATA_DIR / "regions_generated.py"
LOCATIONS_OUTPUT_FILE = DATA_DIR / "locations_generated.py"
OBJECT_ID_OUTPUT_FILE = DATA_DIR / "object_id_mapping.json"

RULE_HEADER_PATTERN = re.compile(r"^Rule \d+$")

RoomDict = dict[str, RoomData]
"""A dict of room labels to :class:`RoomData`."""


def read_full_rooms_csv() -> RoomDict:
    room_dict: RoomDict = {"Menu": RoomData("Menu", "Menu", "Menu", "", "")}
    with FULL_ROOMS_CSV.open(encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            room_area = row["Area"]
            if room_area not in AREA_NAMES or row["Exclude"] == "TRUE":
                continue

            room_label = row["Full Room Label"]
            region_area = AREA_NAMES[room_area]
            region_name = f"{region_area} (X{int(row['X']):+},Y{int(row['Y']):+}){row['Suffix']}"
            sort_index = AREA_NAMES_KEYS.index(room_area) * 10_000 + (abs(int(row["X"])) * 100 + int(row["Y"]))
            sort_key = f"{sort_index:04}{row['Suffix']}"
            room_dict[room_label] = RoomData(
                room_label=room_label,
                room_area=room_area,
                region_name=region_name,
                global_room_id=f"{row['Map ID']}/{row['Room ID']}",
                sort_key=sort_key,
            )
    return room_dict


def read_connections_csv(room_dict: RoomDict) -> list[ConnectionData]:
    connections: list[ConnectionData] = [
        ConnectionData(
            room_dict["Menu"].region_name, room_dict["South Plaza (X-2, Y-3) - ren223 (Main)"].region_name, []
        )
    ]
    with CONNECTIONS_CSV.open(encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            room1 = row["Room Label 1"]
            room2 = row["Room Label 2"]
            # Check that both rooms are in included areas.
            if room1 not in room_dict or room2 not in room_dict:
                continue

            # Get any non-empty rule values
            rule_strs = [v for k, v in row.items() if RULE_HEADER_PATTERN.match(k) and v]

            # Add connections
            connections.append(
                ConnectionData(
                    start_region_name=room_dict[room1].region_name,
                    end_region_name=room_dict[room2].region_name,
                    rule_strs=rule_strs,
                )
            )
            if row["↔️"] == "TRUE":
                connections.append(
                    ConnectionData(
                        start_region_name=room_dict[room2].region_name,
                        end_region_name=room_dict[room1].region_name,
                        rule_strs=rule_strs,
                    )
                )
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

            # Get any non-empty rule values
            rule_strs = [v for k, v in row.items() if RULE_HEADER_PATTERN.match(k) and v]

            if row["Type"] == "Event":
                events.append(
                    EventData(
                        region_name=region_name,
                        location_name=location_name,
                        global_object_id=f"{room_data.global_room_id}/{object_ids[0]}",
                        map_name=row["Map Name"],
                        room_area=room_data.room_area,
                        rule_strs=rule_strs,
                    )
                )
            elif len(object_ids) == 1:
                locations.append(
                    LocationData(
                        region_name=region_name,
                        location_name=location_name,
                        global_object_id=f"{room_data.global_room_id}/{object_ids[0]}",
                        map_name=row["Map Name"],
                        room_area=room_data.room_area,
                        rule_strs=rule_strs,
                    )
                )
            else:
                locations.extend(
                    LocationData(
                        region_name=region_name,
                        location_name=f"{location_name} {j + 1}",
                        global_object_id=f"{room_data.global_room_id}/{object_ids[j]}",
                        map_name=row["Map Name"],
                        room_area=room_data.room_area,
                        rule_strs=rule_strs,
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

from .data_classes import ConnectionData, RoomData

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

from BaseClasses import Location

from .data_classes import EventData, LocationData


class PipLocation(Location):
    game = "Pipistrello and the Cursed Yoyo"


LOCATIONS: list[LocationData] = [
{% for d in locations %}
    {{ d }},
{% endfor %}
]

EVENTS: list[EventData] = [
{% for d in events %}
    {{ d }},
{% endfor %}
]
\n""").render(locations=locations, events=events)
    LOCATIONS_OUTPUT_FILE.write_text(output, encoding="utf-8")


def write_object_id_mapping(locations: list[LocationData]):
    mapping: dict[str, str] = {}
    for location in locations:
        mapping[location.global_object_id] = location.full_location_name

    output = json.dumps(mapping, indent=2)
    OBJECT_ID_OUTPUT_FILE.write_text(output, encoding="utf-8")


if __name__ == "__main__":
    room_data_dict = read_full_rooms_csv()
    connection_datas = read_connections_csv(room_data_dict)
    location_datas, event_datas = read_locations_csv(room_data_dict)
    write_generated_regions(room_data_dict.values(), connection_datas)
    write_generated_locations(location_datas, event_datas)
    write_object_id_mapping(location_datas)
