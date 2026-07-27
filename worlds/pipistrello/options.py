from dataclasses import dataclass

from Options import OptionGroup, PerGameCommonOptions, Toggle

# In this file, we define the options the player can pick.
# The most common types of options are Toggle, Range and Choice.

# Options will be in the game's template yaml.
# They will be represented by checkboxes, sliders etc. on the game's options page on the website.
# (Note: Options can also be made invisible from either of these places by overriding Option.visibility.
#  APQuest doesn't have an example of this, but this can be used for secret / hidden / advanced options.)


class MoneyBags(Toggle):
    """
    Adds money bags as location checks.
    """

    display_name = "Money Bags"


class OptionalCombats(Toggle):
    """
    Adds optional combat encounters (i.e. ones that don't lock you in the room) as location checks.
    """

    display_name = "Optional Combat Encounters"


@dataclass
class PipOptions(PerGameCommonOptions):
    moneybags: MoneyBags
    optional_combats: OptionalCombats


option_groups = [
    OptionGroup(
        "Gameplay Options",
        [MoneyBags, OptionalCombats],
    ),
]

option_presets = {
    "basic": {
        "moneybags": False,
        "optional_combats": False,
    },
    "full": {
        "moneybags": True,
        "optional_combats": True,
    },
}
