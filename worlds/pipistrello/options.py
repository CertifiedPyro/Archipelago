from dataclasses import dataclass

from Options import Choice, DeathLink, PerGameCommonOptions, Range, Toggle


class Difficulty(Choice):
    """
    Determines the logic difficulty.

    - **Normal**: Vanilla difficulty logic.
    - **Hard**: More difficult but consistent tricks, or unusual solutions. Requires the following knowledge:
      - Binding abilities to solo buttons and unbinding "Walk-the-Dog (+ Trick)" is required for most of these tricks.
      - Dash-Throw: Wall-Dash + midair UFO Throw or Offstring Throw. Timing is very lenient.
      - Trick-Dash: UFO Throw or Offstring Throw near a wall to perform a Wall-Dash while keeping an item on the yoyo.
      - Drop: Input any Special Move to drop a held item slightly behind you.
      - Sleeper-Drop: Hold an item with Sleeper, then use Parry or Around-the-World to drop the item near the yoyo.
    - **Expert**: Very difficult tricks. Requires the following knowledge:
      - Midair UFO Throw: Perform a midair UFO Throw after jumping. Timing is very tight.
      - Hard Trick-Dash: Hold trick stance when Wall-Dashing, then release trick stance.
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

# option_presets = {
#     "normal": {
#         "difficulty": Difficulty.option_normal,
#         "moneysanity": False,
#     },
#     "hard": {
#         "difficulty": Difficulty.option_hard,
#         "moneysanity": True,
#     },
# }
