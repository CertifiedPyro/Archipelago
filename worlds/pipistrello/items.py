from __future__ import annotations

import typing
from dataclasses import dataclass
from itertools import chain
from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

from .constants import Badges as B
from .constants import Moves as M
from .constants import OtherItems as OI
from .constants import SpecialItems as SI
from .constants import Upgrades as U

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

    ACTIONS: typing.ClassVar[list[ItemData]] = [
        ItemData(M.OFF, IC.progression | IC.useful),
        ItemData(M.DOG, IC.progression | IC.useful),
        ItemData(M.DASH, IC.progression | IC.useful),
        ItemData(M.UFO, IC.progression | IC.useful),
        ItemData(M.RIDE, IC.progression | IC.useful),
    ]
    CHARGED_MOVES: typing.ClassVar[list[ItemData]] = [
        ItemData(M.SLEEPER, IC.progression),
        ItemData(M.FLURRY, IC.useful),
        ItemData(M.CAT, IC.progression),
        # ItemData(M.MERRY, IC.useful),  # Unused charged move
    ]
    SPECIAL_MOVES: typing.ClassVar[list[ItemData]] = [
        ItemData(M.PARRY, IC.progression | IC.useful),
        ItemData(M.ATW, IC.progression | IC.useful),
        ItemData(M.COINFLIP, IC.progression | IC.useful),
    ]
    UPGRADES: typing.ClassVar[list[ItemData]] = [
        # -- Tier 1 upgrades --
        ItemData(U.BAT_POUCH, IC.progression),
        # Row 1
        ItemData(U.JUMBO_BREAKFAST, IC.progression),
        # ItemData(U.FOCUS_RING, IC.useful),
        # ItemData(U.BAT_POCKET, IC.progression),
        # # Row 2
        ItemData(U.RETRY_COOKIE, IC.useful),
        # ItemData(U.EMERGENCY_FUNDS IC.useful),
        # ItemData(U.SAFETY_NET, IC.useful),
        # # Row 3
        ItemData(U.WILD_INSTINCT, IC.useful),
        # ItemData(U.FURIOUS_BLOWS, IC.useful),
        # ItemData(U.BOLD_DETERMINATION, IC.useful),
        # # Row 4
        ItemData(U.BAT_BACKPACK, IC.progression),
        # ItemData(U.PREVENTIVE_STRIKE, IC.useful),
        # ItemData(U.BAT_SUITCASE, IC.progression),
        # # -- Tier 1 capstones --
        # ItemData(U.HEAVY_GLOVES, IC.useful),
        # ItemData(U.ELUSIVE_BREAKDANCER, IC.useful),
        # ItemData(U.CUTTING_CORNERS, IC.useful),
        # # -- Tier 2 upgrades --
        # # Row 1
        # ItemData(U.FOCUS_BRACELET, IC.useful),
        # ItemData(U.FOCUS_POCKET_WATCH, IC.useful),
        # # Row 2
        # ItemData(U.RETRY_CAKE, IC.useful),
        # ItemData(U.SWEET_REVENGE, IC.useful),
        # # Row 3
        # ItemData(U.DARING_AND_DANGEROUS, IC.useful),
        # ItemData(U.BAT_BAG, IC.progression),
        # # Row 4
        # ItemData(U.JAW_CRUSHER, IC.useful),
        # ItemData(U.HARD_ROCK, IC.useful),
        # # -- Tier 2 capstones --
        # ItemData(U.RETURN_ON_INVESTMENT, IC.useful),
        ItemData(U.PRODIGY, IC.progression),
    ]
    BADGES: typing.ClassVar[list[ItemData]] = [
        # ItemData(B.LIFE, IC.useful, num_in_pool=2),
        # ItemData(B.CANDY, IC.useful, num_in_pool=2),
        ItemData(B.SPROUT, IC.useful, num_in_pool=2),
        # ItemData(B.GHOST, IC.useful, num_in_pool=2),
        # ItemData(B.FIST, IC.useful, num_in_pool=2),
        # ItemData(B.DEMON, IC.useful, num_in_pool=2),
        # ItemData(B.AIRPLANE, IC.useful, num_in_pool=2),
        # ItemData(B.ANVIL, IC.useful, num_in_pool=2),
        # ItemData(B.SPRING, IC.useful, num_in_pool=2),
        # ItemData(B.ROCKET, IC.useful, num_in_pool=2),
        # ItemData(B.STARRY, IC.useful, num_in_pool=2),
        # ItemData(B.THORNY, IC.useful, num_in_pool=2),
        # ItemData(B.STUN, IC.useful, num_in_pool=2),
        ItemData(B.WHIP, IC.useful, num_in_pool=2),
        # ItemData(B.OPPORTUNIST, IC.useful, num_in_pool=2),
        # ItemData(B.MAGNET, IC.useful, num_in_pool=2),
        ItemData(B.COIN, IC.useful, num_in_pool=2),
        # ItemData(B.ROSE, IC.useful, num_in_pool=2),
        # ItemData(B.GREEN_THUMB, IC.useful, num_in_pool=2),
        # ItemData(B.FOCUS, IC.useful, num_in_pool=2),
        ItemData(B.ANGLED, IC.useful, num_in_pool=2),
        # ItemData(B.DIAGONAL, IC.useful, num_in_pool=2),
        # ItemData(B.WING, IC.useful, num_in_pool=2),
        ItemData(B.MIST, IC.useful, num_in_pool=2),
        # ItemData(B.REFLECTIVE, IC.useful, num_in_pool=2),
        ItemData(B.MOON, IC.progression, num_in_pool=2),
        ItemData(B.EYE, IC.useful, num_in_pool=2),
        ItemData(B.PITCHER, IC.useful, area="South Plaza", num_in_pool=2),
        # ItemData(B.TIGHT_KNOT, IC.useful, num_in_pool=2),
        # ItemData(B.TREASURE, IC.useful, num_in_pool=2),
        # ItemData(B.BERSERKER, IC.useful, num_in_pool=2),
        ItemData(B.SS, IC.progression, num_in_pool=2),
        # ItemData(B.CLONE, IC.useful, num_in_pool=2),
        # ItemData(B.FLAME, IC.useful, num_in_pool=2),
        # ItemData(B.HELLHOUND, IC.useful, num_in_pool=2),
        # ItemData(B.ELEPHANT, IC.useful, num_in_pool=2),
        ItemData(B.GOLDEN, IC.useful, area="South Plaza", num_in_pool=2),
        # ItemData(B.TURRET, IC.progression, num_in_pool=2),
        # ItemData("B.CHEATER_TRAIN", IC.progression | IC.useful, num_in_pool=2),
        # ItemData(B.CHEATER_RULER, IC.progression | IC.useful, num_in_pool=2),
        # ItemData(B.CHEATER_UNLEASHED, IC.progression | IC.useful, num_in_pool=2),
        # ItemData(B.CHEATER_TELEKINESIS, IC.progression | IC.useful, num_in_pool=2),
        # ItemData(B.CHEATER_FISH, IC.progression | IC.useful, num_in_pool=2),
        # ItemData(B.CHEATER_TELEPORT, IC.progression | IC.useful, num_in_pool=2),
    ]
    SPECIAL_ITEMS: typing.ClassVar[list[ItemData]] = [ItemData(SI.FARIA_STAFF_ID, IC.progression)]
    FILLER_ITEMS: typing.ClassVar[list[ItemData]] = [
        ItemData("Money Bag - $50", IC.filler),
        ItemData("Money Bag - $100", IC.filler),
        ItemData("Money Bag - $200", IC.filler),
    ]
    PETAL_CONTAINER = ItemData(OI.PETAL, IC.progression)
    BP_SHARD = ItemData(OI.BP, IC.progression)
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
        for data in chain(
            cls.ACTIONS, cls.CHARGED_MOVES, cls.SPECIAL_MOVES, cls.UPGRADES, cls.SPECIAL_ITEMS, cls.FILLER_ITEMS
        ):
            data.id = item_id
            cls._ITEM_CLASSIFICATIONS[data.name] = data
            item_id += 1
        for data in cls.BADGES:
            data.id = item_id
            data.num_in_pool = 2
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
            ItemTypes.ACTIONS,
            ItemTypes.CHARGED_MOVES,
            ItemTypes.SPECIAL_MOVES,
            ItemTypes.UPGRADES,
            ItemTypes.BADGES,
            ItemTypes.SPECIAL_ITEMS,
        )
        for _ in range(data.num_in_pool)
    ]
    itempool += [world.create_item(ItemTypes.PETAL_CONTAINER.name) for _ in range(12)]
    itempool += [world.create_item(ItemTypes.BP_SHARD.name) for _ in range(5)]

    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    if needed_number_of_filler_items > 0:
        itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += itempool
