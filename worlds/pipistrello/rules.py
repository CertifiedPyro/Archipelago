from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.rules import CanReachRegion, Has, HasAll, HasAny, Rule, True_

from . import locations, regions

if TYPE_CHECKING:
    from .world import PipWorld

OT = "Offstring Throw"
DOG = "Walk-the-Dog"
DASH = "Wall-Dash"
UFO = "UFO Throw"
RIDE = "Wall-Ride"
H_SS = Has("Progressive Skipping Stone Badge") & Has("BP Shard", 4)  # Requires 5 BP
H_SS_PLUS = Has("Progressive Skipping Stone Badge") & Has("BP Shard", 2)  # Requires 4 BP
H_MOON = HasAll("Progressive Moon Badge", OT) & Has("BP Shard", 4)  # Requires 5 BP


def set_all_rules(world: PipWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_entrance_rule(world: PipWorld, global_room_id1: str, global_room_id2: str, rule: Rule, two_way: bool):
    region1 = regions.get_room(global_room_id1).region_name
    region2 = regions.get_room(global_room_id2).region_name
    world.set_rule(world.get_entrance(f"{region1} -> {region2}"), rule)
    if two_way:
        world.set_rule(world.get_entrance(f"{region2} -> {region1}"), rule)


def set_location_rule(world: PipWorld, global_object_id: str, rule: Rule):
    location = locations.get_location(global_object_id)
    world.set_rule(world.get_location(location.full_location_name), rule)


def set_event_rule(world: PipWorld, global_object_id: str, rule: Rule):
    location = locations.get_event(global_object_id)
    world.set_rule(world.get_location(location.full_location_name), rule)


def set_all_entrance_rules(world: PipWorld) -> None:
    set_entrance_rules_south_plaza(world)


def set_entrance_rules_south_plaza(world: PipWorld) -> None:
    set_entrance_rule(
        world,
        "city/ren223 (Main)",
        "city/ren223 (South)",
        H_SS | HasAny(DOG, DASH, UFO, RIDE),
        True,
    )
    set_entrance_rule(
        world,
        "city/ren223 (Main)",
        "city/ren223 (Southwest)",
        H_SS | HasAny(DOG, UFO, RIDE),
        True,
    )
    set_entrance_rule(
        world,
        "city/ren223 (Main)",
        "city/ren223 (Southeast)",
        HasAny(DASH, UFO, RIDE),
        True,
    )
    # set_new_entrance_rule(
    #     world,
    #     "city/ren4152",
    #     "city/ren4147",
    #     Has(locations.get_event_item("city/ren4152/lor2079")),
    #     False,
    # )
    set_entrance_rule(
        world,
        "city/ren4152",
        "city/ren223 (Southwest)",
        Has(locations.get_event_item("city/ren4152/lor2079")),
        False,
    )
    set_entrance_rule(world, "city/yug4939 (West)", "city/yug4939 (East)", HasAny(DASH, UFO, RIDE), False)
    set_entrance_rule(
        world,
        "city_underground/ren984",
        "city_underground/lor230",
        HasAll(
            locations.get_event_item("city_underground/ren984/lor227"),
            locations.get_event_item("city_underground/ren984/lor228"),
        ),
        False,
    )
    set_entrance_rule(
        world,
        "city_underground/lor871",
        "city_underground/yug1700 (West)",
        HasAny(DOG, RIDE) | (Has(UFO) & H_SS),
        False,
    )
    set_entrance_rule(
        world,
        "city_underground/yug1700 (West)",
        "city_underground/yug1700 (East)",
        (Has(OT) & HasAny(DOG, RIDE)) | (Has(DOG) & H_SS),
        False,
    )


def set_all_location_rules(world: PipWorld) -> None:
    """
    Create all the location rules.
    All locations will have their rules written, even if there are none.
    """
    set_location_rules_south_plaza(world)


def set_location_rules_south_plaza(world: PipWorld) -> None:
    # ----- South Plaza -----
    # Badge
    # set_new_location_rule(world, "city/lor2248/yug4337", )
    # set_new_location_rule(world, "city/ren355/yug3158", )
    set_location_rule(world, "city/yug5210/yug5250", Has(locations.get_event_item("city/yug4930/yug4979")))

    # BP Shard
    set_location_rule(world, "city/yug5154/yug5202", HasAny(UFO, RIDE))

    # Combat
    if world.options.optional_combats:
        set_event_rule(world, "city/ren223/ren4804", True_())
        set_location_rule(world, "city/ren223/ren4805", Has(locations.get_event_item("city/ren223/ren4804")))
    set_event_rule(world, "city/ren4152/lor2079", True_())
    set_location_rule(world, "city/ren4152/lor2096", Has(locations.get_event_item("city/ren4152/lor2079")))
    set_event_rule(world, "city/yug4930/yug4954", True_())

    # Diamond
    # set_new_location_rule(world, "city/lor2248/lor2469", )

    # Key
    set_event_rule(world, "city/yug4930/yug4979", Has(locations.get_event_item("city/yug4930/yug4954")))

    # Lever
    set_event_rule(world, "city/ren223/yug5535", True_())
    set_event_rule(world, "city/ren223/yug5536", True_())
    # set_event_rule(world, "city/lor2248/lor3247", )

    # Mole Brother
    set_event_rule(world, "city/ren223/lor1227", True_())

    # Money Bag
    if world.options.moneybags:
        set_location_rule(world, "city/ren223/cap369", True_())
        set_location_rule(world, "city/ren223/lor3388", True_())
        set_location_rule(world, "city/ren223/lor380", True_())
        set_location_rule(world, "city/ren223/lor397", True_())
        # set_location_rule(world, "city/ren223/ren4803", H_MOON)
        set_location_rule(world, "city/ren223/yug2147", True_())
        # set_new_location_rule(world, "city/ren355/lor1120", True_())
        set_location_rule(world, "city/ren355/lor3013", True_())
        set_location_rule(world, "city/lor2248/yug5046", True_())
        set_location_rule(world, "city/yug4939/yug5160", True_())
        set_location_rule(world, "city/yug4939/yug5162", True_())
        set_location_rule(
            world,
            "city/yug4939/yug5203",
            CanReachRegion(regions.get_room("city/yug4939 (East)").region_name)
            | (CanReachRegion(regions.get_room("city/yug4939 (West)").region_name) & H_MOON),
        )
        set_location_rule(world, "city/yug4939/yug5166", True_())

    # Musical Notes
    set_event_rule(world, "city/ren223/yug5074", Has(OT))
    set_location_rule(world, "city/ren223/yug5100", Has(locations.get_event_item("city/ren223/yug5074")))
    set_location_rule(world, "city/ren223/yug5101", Has(locations.get_event_item("city/ren223/yug5074")))
    set_location_rule(world, "city/ren223/yug5102", Has(locations.get_event_item("city/ren223/yug5074")))
    set_location_rule(world, "city/ren223/yug5103", Has(locations.get_event_item("city/ren223/yug5074")))
    # TODO: Check if wall-ride is reasonable for Musical Notes 2
    set_event_rule(
        world,
        "city/ren223/yug5127",
        # HasAny(OT, RIDE, "Around-the-World"),
        HasAny(OT, "Around-the-World"),
    )
    set_location_rule(world, "city/ren223/yug5144", Has(locations.get_event_item("city/ren223/yug5127")))
    set_location_rule(world, "city/ren223/yug5146", Has(locations.get_event_item("city/ren223/yug5127")))
    set_location_rule(world, "city/ren223/yug5147", Has(locations.get_event_item("city/ren223/yug5127")))

    # Petal Container
    set_location_rule(
        world,
        "city/ren223/yug5534",
        HasAll(locations.get_event_item("city/ren223/yug5535"), locations.get_event_item("city/ren223/yug5536")),
    )

    # Quest
    set_event_rule(world, "city/ren223/yug3946", Has(locations.get_event_item("city_interiors/ren85/yug421")))
    set_location_rule(world, "city/ren223/yug5539", Has(locations.get_event_item("city/ren223/yug3946")))
    set_location_rule(world, "city/ren223/yug5540", Has(locations.get_event_item("city/ren223/yug3946")))
    set_location_rule(world, "city/ren223/yug5541", Has(locations.get_event_item("city/ren223/yug3946")))
    set_location_rule(world, "city/ren223/yug5545", Has(locations.get_event_item("city/ren223/yug3946")))

    # Taxi phone
    # TODO: Taxi phone costs $100
    # set_new_location_rule(world, "city/ren223/lor2057", )

    # ----- South Plaza (Interiors) -----
    # Burger
    # TODO: Burger costs $15
    # set_event_rule(world, "city_interiors/ren85/yug421", )

    # ----- South Plaza (Sewers) -----
    # Lever
    set_event_rule(
        world,
        "city_underground/ren984/lor227",
        H_SS_PLUS | Has(DOG) | (Has(DASH) & H_SS) | Has(UFO) | (Has(RIDE) & H_SS),
    )
    set_event_rule(
        world,
        "city_underground/ren984/lor228",
        HasAny(DASH, UFO, RIDE),
    )
    # Money Bag
    # set_new_location_rule(world, "city_underground/yug1700/yug2209", True_())
    # set_new_location_rule(world, "city_underground/yug1700/yug2291", True_())
    # set_new_location_rule(world, "city_underground/yug1700/yug2292", True_())
    # set_new_location_rule(world, "city_underground/yug1700/yug2063", Has(OT) & HasAny(DOG, RIDE))


def set_completion_condition(world: PipWorld) -> None:
    end_region = regions.get_room("city_underground/lor230").region_name
    world.set_completion_rule(CanReachRegion(end_region))
