from __future__ import annotations

import typing
from dataclasses import dataclass
from itertools import chain
from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import PipWorld


@dataclass
class ItemData:
    name: str
    classification: ItemClassification
    area: str | None = None

    id: int = 0
    num_in_pool: int = 1


class ItemTypes:
    IC = ItemClassification
    _ITEM_CLASSIFICATIONS: typing.ClassVar[dict[str, ItemData]] = {}
    _ITEM_NAME_TO_ID: typing.ClassVar[dict[str, int]] = {}

    ACTIONS: typing.ClassVar = [
        ItemData("Offstring Throw", IC.progression | IC.useful),
        ItemData("Walk-the-Dog", IC.progression | IC.useful),
        ItemData("Wall-Dash", IC.progression | IC.useful),
        ItemData("UFO Throw", IC.progression | IC.useful),
        ItemData("Wall-Ride", IC.progression | IC.useful),
    ]
    CHARGED_MOVES: typing.ClassVar = [
        ItemData("Sleeper", IC.progression),
        ItemData("Flurry Attack", IC.useful),
        ItemData("Cat's Cradle", IC.progression),
        # ItemData("Merry-Go-Round", IC.useful),  # Unused charged move
    ]
    SPECIAL_MOVES: typing.ClassVar = [
        ItemData("Parry", IC.progression | IC.useful),
        ItemData("Around-the-World", IC.progression | IC.useful),
        ItemData("Coin-Flip", IC.progression | IC.useful),
    ]
    UPGRADES: typing.ClassVar = [
        # -- Tier 1 upgrades --
        # ItemData("Bat Pouch", IC.progression),
        # Row 1
        # ItemData("Jumbo Breakfast", IC.progression),
        # ItemData("Focus Ring", IC.useful),
        # ItemData("Bat Pocket", IC.progression),
        # # Row 2
        # ItemData("Retry Cookie", IC.useful),
        # ItemData("Emergency Funds", IC.useful),
        # ItemData("Safety Net", IC.useful),
        # # Row 3
        # ItemData("Wild Instinct", IC.useful),
        # ItemData("Furious Blows", IC.useful),
        # ItemData("Bold Determination", IC.useful),
        # # Row 4
        # ItemData("Bat Backpack", IC.progression),
        # ItemData("Preventive Strike", IC.useful),
        # ItemData("Bat Suitcase", IC.progression),
        # # -- Tier 1 capstones --
        # ItemData("Heavy Gloves", IC.useful),
        # ItemData("Elusive Breakdancer", IC.useful),
        # ItemData("Cutting Corners", IC.useful),
        # # -- Tier 2 upgrades --
        # # Row 1
        # ItemData("Focus Bracelet", IC.useful),
        # ItemData("Focus Pocket-Watch", IC.useful),
        # # Row 2
        # ItemData("Retry Cake", IC.useful),
        # ItemData("Sweet Revenge", IC.useful),
        # # Row 3
        # ItemData("Daring and Dangerous", IC.useful),
        # ItemData("Bat Bag", IC.progression),
        # # Row 4
        # ItemData("Jaw Crusher", IC.useful),
        # ItemData("Hard Rock", IC.useful),
        # # -- Tier 2 capstones --
        # ItemData("Return on Investment", IC.useful),
        # ItemData("Prodigy", IC.progression),
    ]
    BADGES: typing.ClassVar = [
        # ItemData("Progressive Life Badge", IC.useful, num_in_pool=2),
        # ItemData("Progressive Candy Badge", IC.useful, num_in_pool=2),
        # ItemData("Progressive Sprout Badge", IC.useful, num_in_pool=2),
        # ItemData("Progressive Ghost Badge", IC.useful, num_in_pool=2),
        # ItemData("Progressive Fist Badge", IC.useful, num_in_pool=2),
        # ItemData("Progressive Demon Badge", IC.useful, num_in_pool=2),
        # ItemData("Progressive Airplane Badge", IC.useful, num_in_pool=2),
        # ItemData("Progressive Anvil Badge", IC.useful, num_in_pool=2),
        # ItemData("Progressive Spring Badge", IC.useful, num_in_pool=2),
        # ItemData("Progressive Rocket Badge", IC.useful, num_in_pool=2),
        # ItemData("Progressive tarry Badge", IC.useful, num_in_pool=2),
        # ItemData("Progressive Thorny Badge", IC.useful, num_in_pool=2),
        # ItemData("Progressive Stun Badge", IC.useful, num_in_pool=2),
        # ItemData("Progressive Whip Badge", IC.useful, num_in_pool=2),
        # ItemData("Progressive Opportunist's Badge", IC.useful, num_in_pool=2),
        # ItemData("Progressive Magnet Badge", IC.useful, num_in_pool=2),
        # ItemData("Progressive Coin Badge", IC.useful, num_in_pool=2),
        # ItemData("Progressive Rose Badge", IC.useful, num_in_pool=2),
        # ItemData("Progressive Green-Thumb Badge", IC.useful, num_in_pool=2),
        # ItemData("Progressive Focus Badge", IC.useful, num_in_pool=2),
        # ItemData("Progressive Angled Badge", IC.useful, num_in_pool=2),
        # ItemData("Progressive Diagonal Badge", IC.useful, num_in_pool=2),
        # ItemData("Progressive Wing Badge", IC.useful, num_in_pool=2),
        # ItemData("Progressive Mist Badge", IC.useful, num_in_pool=2),
        # ItemData("Progressive Reflective Badge", IC.useful, num_in_pool=2),
        ItemData("Progressive Moon Badge", IC.progression, num_in_pool=2),
        # ItemData("Progressive Eye Badge", IC.useful, num_in_pool=2),
        ItemData("Progressive Pitcher's Badge", IC.useful, area="South Plaza", num_in_pool=2),
        # ItemData("Progressive Tight-Knot Badge", IC.useful, num_in_pool=2),
        # ItemData("Progressive Treasure Chest Badge", IC.useful, num_in_pool=2),
        # ItemData("Progressive Berserker Badge", IC.useful, num_in_pool=2),
        ItemData("Progressive Skipping Stone Badge", IC.progression, num_in_pool=2),
        # ItemData("Progressive Clone Badge", IC.useful, num_in_pool=2),
        # ItemData("Progressive Flame Badge", IC.useful, num_in_pool=2),
        # ItemData("Progressive Hellhound Badge", IC.useful, num_in_pool=2),
        # ItemData("Progressive Elephant Badge", IC.useful, num_in_pool=2),
        # ItemData("Progressive Golden Badge", IC.useful, area="South Plaza", num_in_pool=2),
        # ItemData("Progressive Turret Badge", IC.progression, num_in_pool=2),
        # ItemData("Progressive Cheater's Train Badge", IC.progression | IC.useful, num_in_pool=2),
        # ItemData("Progressive Cheater's Ruler Badge", IC.progression | IC.useful, num_in_pool=2),
        # ItemData("Progressive Cheater's Unleashed Badge", IC.progression | IC.useful, num_in_pool=2),
        # ItemData("Progressive Cheater's Telekinesis Badge", IC.progression | IC.useful, num_in_pool=2),
        # ItemData("Progressive Cheater's Fishing Rod Badge", IC.progression | IC.useful, num_in_pool=2),
        # ItemData("Progressive Cheater's Teleportation Badge", IC.progression | IC.useful, num_in_pool=2),
    ]
    FILLER_ITEMS: typing.ClassVar[list[ItemData]] = [
        ItemData("Money Bag - $50", IC.filler),
        ItemData("Money Bag - $100", IC.filler),
        ItemData("Money Bag - $200", IC.filler),
    ]
    PETAL_CONTAINER = ItemData("Petal Container", IC.progression)
    BP_SHARD = ItemData("BP Shard", IC.progression)
    # TODO: Give taxi phones

    @classmethod
    def item_classifications(cls):
        if len(cls._ITEM_CLASSIFICATIONS) == 0:
            cls._init_cls_variables()
        return cls._ITEM_CLASSIFICATIONS

    @classmethod
    def item_name_to_id(cls):
        if len(cls._ITEM_NAME_TO_ID) == 0:
            cls._init_cls_variables()
        return cls._ITEM_NAME_TO_ID

    @classmethod
    def _init_cls_variables(cls):
        item_id = 1
        for data in chain(cls.ACTIONS, cls.CHARGED_MOVES, cls.SPECIAL_MOVES, cls.UPGRADES):
            data.id = item_id
            cls._ITEM_CLASSIFICATIONS[data.name] = data
            item_id += 1
        for data in cls.BADGES:
            data.id = item_id
            data.num_in_pool = 2
            cls._ITEM_CLASSIFICATIONS[data.name] = data
            item_id += 1
        for data in cls.FILLER_ITEMS:
            data.id = item_id
            cls._ITEM_CLASSIFICATIONS[data.name] = data
            item_id += 1

        # Set amount of Petal/BP containers in item pool later.
        cls.PETAL_CONTAINER.id = item_id
        cls._ITEM_CLASSIFICATIONS[cls.PETAL_CONTAINER.name] = cls.PETAL_CONTAINER
        item_id += 1
        cls.BP_SHARD.id = item_id
        cls._ITEM_CLASSIFICATIONS[cls.BP_SHARD.name] = cls.BP_SHARD
        item_id += 1

        for data in cls._ITEM_CLASSIFICATIONS.values():
            cls._ITEM_NAME_TO_ID[data.name] = data.id


class PipItem(Item):
    game = "Pipistrello and the Cursed Yoyo"


def get_random_filler_item_name(world: PipWorld) -> str:
    moneybag_rand = world.random.randint(0, 99)
    if moneybag_rand < 25:
        return "Money Bag - $50"
    if moneybag_rand < 75:
        return "Money Bag - $100"
    return "Money Bag - $200"


def create_item_with_correct_classification(world: PipWorld, name: str) -> PipItem:
    data = ItemTypes.item_classifications()[name]
    return PipItem(data.name, data.classification, data.id, world.player)


def create_all_items(world: PipWorld) -> None:
    itempool = [
        world.create_item(data.name)
        for data in chain(
            ItemTypes.ACTIONS, ItemTypes.CHARGED_MOVES, ItemTypes.SPECIAL_MOVES, ItemTypes.UPGRADES, ItemTypes.BADGES
        )
        for _ in range(data.num_in_pool)
    ]
    itempool += 1 * [world.create_item(ItemTypes.PETAL_CONTAINER.name)]
    itempool += 1 * [world.create_item(ItemTypes.BP_SHARD.name)]

    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    # TODO: Remove once at least one area's locations are complete
    if needed_number_of_filler_items > 0:
        itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]
    else:
        charged_move_names = {x.name for x in ItemTypes.CHARGED_MOVES}
        itempool = [x for x in itempool if x.name not in charged_move_names]

    world.multiworld.itempool += itempool
