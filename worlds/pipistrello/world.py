from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from worlds.AutoWorld import World

from . import items, locations, options, regions, rules, web_world


class PipWorld(World):
    """
    Pipistrello and the Cursed Yoyo combines combat, platforming action, puzzle-solving, and exploration —
    all enveloped in a delightful character-driven story about corporate shenanigans!
    Face off against the rival crime entrepreneurs and their underlings
    using the weapon you know best: your prized yoyo!
    """

    game = "Pipistrello and the Cursed Yoyo"
    web = web_world.PipWebWorld()

    options_dataclass = options.PipOptions
    options: options.PipOptions

    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ItemTypes.item_name_to_id()

    ut_can_gen_without_yaml = True

    def generate_early(self) -> None:
        # Handle yaml-less Universal Tracker generation.
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            # Get the passed through slot data from the real generation.
            slot_data: dict[str, Any] = re_gen_passthrough[self.game]

            slot_options: dict[str, Any] = slot_data.get("options", {})
            # Set all your options here instead of getting them from the yaml.
            for key, value in slot_options.items():
                opt = getattr(self.options, key, None)
                if opt is not None:
                    # You can also set .value directly but that won't work if you have OptionSets.
                    setattr(self.options, key, opt.from_any(value))

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.PipItem:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return {"options": self.options.as_dict("difficulty", "death_link", "death_link_amnesty", "moneysanity")}

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        # Trigger a regen in UT
        return slot_data

    def custom_ut_sort(self, region_label: str, location_label: str) -> str | int:
        return f"{regions.REGION_NAME_TO_ROOM[region_label].sort_key} | {location_label}"
