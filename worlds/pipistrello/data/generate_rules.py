import json
from pathlib import Path

import jinja2

from .. import locations, regions
from ..constants import Badges as B
from ..constants import Moves as M
from ..constants import OtherItems as OI
from ..constants import SpecialItems as SI
from .locations_generated import EVENTS, LOCATIONS
from .regions_generated import CONNECTIONS

DATA_DIR = Path(__file__).resolve().parent
CONNECTIONS_RULES_OUTPUT_FILE = DATA_DIR / "rules_generated.py"

RULE_DICT = {
    # Abilities
    "ot": f"Has('{M.OFF}')",
    "off": f"Has('{M.OFF}')",
    "offstring": f"Has('{M.OFF}')",
    "dog": f"Has('{M.DOG}')",
    "walk": f"Has('{M.DOG}')",
    "walkthedog": f"Has('{M.DOG}')",
    "dash": f"Has('{M.DASH}')",
    "walldash": f"Has('{M.DASH}')",
    "ufo": f"Has('{M.UFO}')",
    "ufothrow": f"Has('{M.UFO}')",
    "ride": f"Has('{M.RIDE}')",
    "wallride": f"Has('{M.RIDE}')",
    # Charged moves
    "sleeper": f"Has('{M.SLEEPER}')",
    "fa": f"Has('{M.FLURRY}')",
    "flurry": f"Has('{M.FLURRY}')",
    "flurryattack": f"Has('{M.FLURRY}')",
    "cc": f'Has("{M.CAT}")',
    "cat": f'Has("{M.CAT}")',
    "catscradle": f'Has("{M.CAT}")',
    "mgr": f"Has('{M.MERRY}')",
    "merry": f"Has('{M.MERRY}')",
    "merrygoround": f"Has('{M.MERRY}')",
    # Special moves
    "parry": f"Has('{M.PARRY}')",
    "atw": f"Has('{M.ATW}')",
    "aroundtheworld": f"Has('{M.ATW}')",
    "cf": f"Has('{M.COINFLIP}')",
    "flip": f"Has('{M.COINFLIP}')",
    "coinflip": f"Has('{M.COINFLIP}')",
    "cf+": "COIN_FLIP_PLUS",
    "flip+": "COIN_FLIP_PLUS",
    "coinflip+": "COIN_FLIP_PLUS",
    # Badges
    "moon": f"Has('{B.MOON}')",
    "ss": "SS_NORMAL",
    "skippingstone": "SS_NORMAL",
    "ss+": "SS_PLUS",
    "skippingstone+": "SS_PLUS",
    "wing": f"Has('{B.WING}')",
    # Special items
    "mb2": f"Has('{SI.MEGA_BATTERY_FARIA}')",
    "staffid": f"Has('{SI.FARIA_STAFF_ID}')",
    # Health
    "heart+1": f"Has('{OI.PETAL}', 8)",
    "heart+2": f"Has('{OI.PETAL}', 16)",
    "heart+3": f"Has('{OI.PETAL}', 24)",
    # Difficulty
    "hard": "DIFF_HARD",
    "expert": "DIFF_EXPERT",
    # Interactables
    "bomb": "BOMB",
    "buoy": "BUOY",
    "chest": "CHEST",
    "cog": "COG",
    "hook": "HOOK",
    "key": "KEY",
    "lever": "LEVER",
    "manhole": "MANHOLE",
    # Difficult tricks
    "midairufo": "MID_AIR_UFO",
    "dash-midair-ufo": "DASH_MIDAIR_UFO",
    "dash-midair-off": "DASH_MIDAIR_OFF",
    "trick-dash": "TRICK_DASH",
    "drop": "DROP",
    "sleeper-drop": "SLEEPER_DROP",
}

AREA_DICT = {
    "fsb": "Faria Slimer Borough",
    "fsb-i": "Faria Slimer Borough (Interiors)",
    "sp": "South Plaza",
    "sp-i": "South Plaza (Interiors)",
    "ses": "SlimeCorp Excavation Site",
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
        # TODO: Bomb by itself should be Bomb item + Coin Flip+
        column_strs = rule_str.translate(remove_map).lower().split(",")
        column_rule_strs = []
        for column_str in column_strs:
            if column_str == "none":
                continue

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
                room1 = regions.get_room_by_region_name(region_name)
                room2 = room1
            else:
                room1 = regions.get_room_by_region_name(region_name)
                room2 = regions.get_room_by_region_name(region_name2)

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
from rule_builder.rules import Has, HasAll, HasAny, HasFromList, Rule, True_

from ..options import Difficulty

DIFF_HARD = [OptionFilter(Difficulty, Difficulty.option_hard, operator="ge")]
DIFF_EXPERT = [OptionFilter(Difficulty, Difficulty.option_expert, operator="ge")]

BP_PLUS1_UPGRADES = ["Bat Pouch", "Bat Backpack"]
BP_PLUS1 = Has("BP Shard", 2) | HasFromList(*BP_PLUS1_UPGRADES, count=1)
BP_PLUS2 = (
    Has("BP Shard", 4)
    | (Has("BP Shard", 2) & HasFromList(*BP_PLUS1_UPGRADES, count=1))
    | HasFromList(*BP_PLUS1_UPGRADES, count=2)
)

COIN_FLIP_PLUS = HasAll("Coin-Flip", "Prodigy")
SS_PLUS = Has("Progressive Skipping Stone Badge", 2) & BP_PLUS1  # Requires 4 BP (from base 3 BP)
SS_NORMAL = SS_PLUS | (Has("Progressive Skipping Stone Badge", 1) & BP_PLUS2)  # Requires 5 BP (from base 3 BP)

MID_AIR_UFO = Has("UFO Throw") & DIFF_EXPERT
DASH_MIDAIR_UFO = HasAll("Wall-Dash", "UFO Throw") & DIFF_HARD
DASH_MIDAIR_OFF = HasAll("Wall-Dash", "Offstring Throw") & DIFF_HARD
TRICK_DASH = Has("Wall-Dash") & (DIFF_EXPERT | (DIFF_HARD & HasAny("Offstring Throw", "UFO Throw")))
DROP = HasAny("Parry", "Around-the-World", "Coin-Flip") & DIFF_HARD
SLEEPER_DROP = Has("Sleeper") & HasAny("Parry", "Around-the-World") & DIFF_HARD

BOMB = True_()
BUOY = True_()
CHEST = True_()
COG = True_()
HOOK = True_()
KEY = True_()
LEVER = True_()
MANHOLE = True_()

HAS_MONEY = True_()

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
