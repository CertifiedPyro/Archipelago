from dataclasses import dataclass

from Options import Choice, DeathLink, PerGameCommonOptions, Range, Toggle


class Difficulty(Choice):
    """
    Determines the logic difficulty.

    - **Normal**: Vanilla difficulty logic.
    - **Hard**: May require solo trick buttons, somewhat tight timings, or unusual solutions.
    - **Expert**: May require difficult yoyo tricks (e.g. Wall-Ride around corners), or very tight timings.
    """

    display_name = "Difficulty"

    option_normal = 0
    option_hard = 1
    option_expert = 2

    default = option_normal


class DeathLinkAmnesty(Range):
    """
    How many deaths it takes to send a DeathLink.
    """

    display_name = "Death Link Amnesty"
    range_start = 1
    range_end = 10
    default = 1


class Moneysanity(Toggle):
    """
    Adds standalone money bags and money bags from optional combat encounters as location checks.
    """

    display_name = "Moneysanity"


@dataclass
class PipOptions(PerGameCommonOptions):
    difficulty: Difficulty
    death_link: DeathLink
    death_link_amnesty: DeathLinkAmnesty

    moneysanity: Moneysanity


# option_groups = [
#     OptionGroup(
#         "Gameplay Options",
#         [Difficulty, Moneysanity],
#     ),
# ]

option_presets = {
    "normal": {
        "difficulty": Difficulty.option_normal,
        "moneysanity": False,
    },
    "hard": {
        "difficulty": Difficulty.option_hard,
        "moneysanity": True,
    },
}
