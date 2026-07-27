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
        return self.options.as_dict("moneybags", "optional_combats")
