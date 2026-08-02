from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Toggle


class Difficulty(Choice):
    """
    Determines the logic difficulty.

    - **Normal**: Vanilla difficulty logic
    - **Hard**: May require binding solo trick buttons, mid-air UFO Throws, or somewhat tight timings.
    - **Expert**: May require difficult yoyo tricks (e.g. Wall-Ride around corners).
    """

    display_name = "Difficulty"

    option_normal = 0
    option_hard = 1
    option_expert = 2

    default = option_normal


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
    difficulty: Difficulty
    moneybags: MoneyBags
    optional_combats: OptionalCombats


option_groups = [
    OptionGroup(
        "Gameplay Options",
        [Difficulty, MoneyBags, OptionalCombats],
    ),
]

option_presets = {
    "basic": {
        "difficulty": Difficulty.option_normal,
        "moneybags": False,
        "optional_combats": False,
    },
    "full": {
        "difficulty": Difficulty.option_normal,
        "moneybags": True,
        "optional_combats": True,
    },
}
