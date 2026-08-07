import json
from pathlib import Path

import jinja2

from .. import locations, regions
from .locations_generated import EVENTS, LOCATIONS
from .regions_generated import CONNECTIONS

DATA_DIR = Path(__file__).resolve().parent
CONNECTIONS_RULES_OUTPUT_FILE = DATA_DIR / "rules_generated.py"

# Abilities
OT = "Offstring Throw"
DOG = "Walk-the-Dog"
DASH = "Wall-Dash"
UFO = "UFO Throw"
RIDE = "Wall Ride"

# Charged moves
SLEEPER = "Sleeper"
FA = "Flurry Attack"
CC = "Cat's Cradle"
MGR = "Merry-Go-Round"

# Special moves
PARRY = "Parry"
ATW = "Around-the-World"
CF = "Coin-Flip"

# Badges
SS = "Progressive Skipping Stone Badge"

RULE_DICT = {
    # Abilities
    "ot": f"Has('{OT}')",
    "off": f"Has('{OT}')",
    "offstring": f"Has('{OT}')",
    "dog": f"Has('{DOG}')",
    "walkthedog": f"Has('{DOG}')",
    "dash": f"Has('{DASH}')",
    "walldash": f"Has('{DASH}')",
    "ufo": f"Has('{UFO}')",
    "ufothrow": f"Has('{UFO}')",
    "midairufo": "HAS_MID_AIR_UFO",
    "midairufothrow": "HAS_MID_AIR_UFO",
    "ride": f"Has('{RIDE}')",
    "wallride": f"Has('{RIDE}')",
    # Charged moves
    "sleeper": f"Has('{SLEEPER}')",
    "fa": f"Has('{FA}')",
    "flurry": f"Has('{FA}')",
    "flurryattack": f"Has('{FA}')",
    "cc": f'Has("{CC}")',
    "cat": f'Has("{CC}")',
    "catscradle": f'Has("{CC}")',
    "mgr": f"Has('{MGR}')",
    "merry": f"Has('{MGR}')",
    "merrygoround": f"Has('{MGR}')",
    # Special moves
    "parry": f"Has('{PARRY}')",
    "atw": f"Has('{ATW}')",
    "aroundtheworld": f"Has('{ATW}')",
    "cf": f"Has('{CF}')",
    "flip": f"Has('{CF}')",
    "coinflip": f"Has('{CF}')",
    "cf+": "COIN_FLIP_PLUS",
    "flip+": "COIN_FLIP_PLUS",
    "coinflip+": "COIN_FLIP_PLUS",
    # Badges
    "ss": "HAS_SS_NORMAL",
    "skippingstone": "HAS_SS_NORMAL",
    "ss+": "HAS_SS_PLUS",
    "skippingstone+": "HAS_SS_PLUS",
    # Health
    "+1heart": "Has('Petal Container', 8)",
    "heart+1": "Has('Petal Container', 8)",
    # Difficulty
    "hard": "DIFF_HARD",
    "expert": "DIFF_EXPERT",
    # Interactables
    "bomb": "True_()",
    "buoy": "True_()",
    "chest": "CHEST",
    "key": "True_()",
    "lever": "True_()",
    "manhole": "True_()",
}

AREA_DICT = {
    "fsb": "Faria Slimer Borough",
    "fsb-i": "Faria Slimer Borough (Interiors)",
    "sp": "South Plaza",
    "sp-i": "South Plaza (Interiors)",
}


def process_connections() -> dict[str, str]:
    entrance_rules: dict[str, str] = {}
    for data in CONNECTIONS:
        rule_str = process_row(data.rule_strs, data.start_region_name, data.end_region_name)
        if rule_str:
            entrance_rules[f"{data.start_region_name} -> {data.end_region_name}"] = rule_str
    return entrance_rules


def process_locations() -> dict[str, str]:
    location_rules: dict[str, str] = {}
    all_locations = sorted(EVENTS + LOCATIONS, key=lambda d: (d.room_area, d.map_name.lower()))
    for data in all_locations:
        rule_str = process_row(data.rule_strs, data.region_name)
        if rule_str:
            location_rules[data.full_location_name] = rule_str
    return location_rules


def process_row(rule_strs: list[str], region_name: str, region_name2: str | None = None) -> str | None:
    if len(rule_strs) == 0:
        return None

    remove_map = str.maketrans("", "", " '")
    row_rules = []
    for rule_str in rule_strs:
        column_strs = rule_str.translate(remove_map).lower().split(",")
        column_rule_strs = []
        for column_str in column_strs:
            # Check if string is a known one.
            rule_value_str = RULE_DICT.get(column_str)
            if rule_value_str is not None:
                column_rule_strs.append(rule_value_str)
                continue

            # Check if string is a cost
            # TODO: Handle cost rules
            if "$" in column_str:
                column_rule_strs.append("HAS_MONEY")
                continue

            # Else, string must be an event instead.
            if region_name2 is None:
                room1 = regions.REGION_NAME_TO_ROOM[region_name]
                room2 = room1
            else:
                room1 = regions.REGION_NAME_TO_ROOM[region_name]
                room2 = regions.REGION_NAME_TO_ROOM[region_name2]

            area_abbrev_start_idx = column_str.find("[")
            area_abbrev_end_idx = column_str.find("]")
            # Determine if there's an area abbreviation (e.g. "[SP] Lever 1")
            if area_abbrev_start_idx != -1 and area_abbrev_end_idx != -1:
                area_abbrev = column_str[area_abbrev_start_idx + 1 : area_abbrev_end_idx]
                room_area = AREA_DICT[area_abbrev]
                column_str = column_str[area_abbrev_end_idx + 1 :]
            elif room1.room_area == room2.room_area:
                room_area = room1.room_area
            else:
                raise Exception(f"Area abbreviation must be provided for {room1.room_label} -> {room2.room_label}")

            event = next(
                (
                    d
                    for d in locations.EVENTS
                    if d.map_name.translate(remove_map).lower() == column_str and d.room_area == room_area
                ),
                None,
            )
            if event:
                column_rule_strs.append(f"Has('{event.full_item_name}')")
            else:
                raise Exception(f"Could not find rule value: {room1.room_label}, {room2.room_label}, {column_str}")

        full_column_rule = str.join(" & ", column_rule_strs)
        if len(column_rule_strs) > 1:
            full_column_rule = f"({full_column_rule})"

        row_rules.append(full_column_rule)

    return str.join(" | ", row_rules)


def write_connection_rules(entrance_rules: dict[str, str], location_rules: dict[str, str]):
    template = jinja2.Environment(
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template.filters["quote"] = json.dumps

    output = template.from_string("""# THIS FILE IS AUTOMATICALLY GENERATED. DO NOT MANUALLY EDIT.
# RUN "Reformat Code" AFTER GENERATION.
from __future__ import annotations

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule, True_

from ..options import Difficulty, MoneyBags, OptionalCombats

COIN_FLIP_PLUS = HasAll("Coin-Flip", "Prodigy")
HAS_MID_AIR_UFO = Has("UFO Throw", options=[OptionFilter(Difficulty, Difficulty.option_hard)])
HAS_SS_NORMAL = Has("Progressive Skipping Stone Badge", 1) & Has("BP Shard", 4)  # Requires 5 BP (from base 3 BP)
HAS_SS_PLUS = Has("Progressive Skipping Stone Badge", 2) & Has("BP Shard", 2)  # Requires 4 BP (from base 3 BP)

DIFF_HARD = True_(options=[OptionFilter(Difficulty, Difficulty.option_hard)])
DIFF_EXPERT = True_(options=[OptionFilter(Difficulty, Difficulty.option_expert)])

HAS_MONEY = True_()
CHEST = True_()

ENTRANCE_RULES: dict[str, Rule] = {
{% for entrance_name, rule in entrance_rules.items() %}
    {{ entrance_name | quote }}: ({{ rule }}),
{% endfor %}
}

LOCATION_RULES: dict[str, Rule] = {
{% for location_name, rule in location_rules.items() %}
    {{ location_name | quote }}: ({{ rule }}),
{% endfor %}
}
\n""").render(entrance_rules=entrance_rules, location_rules=location_rules)
    CONNECTIONS_RULES_OUTPUT_FILE.write_text(output, encoding="utf-8")


if __name__ == "__main__":
    connection_rules = process_connections()
    loc_rules = process_locations()
    write_connection_rules(connection_rules, loc_rules)
