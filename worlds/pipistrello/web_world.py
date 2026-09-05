from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld


class PipWebWorld(WebWorld):
    game = "Pipistrello and the Cursed Yoyo"
    # theme = "grass"
    rich_text_options_doc = True

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Pipistrello and the Cursed Yoyo for Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["CertifiedPyro"],
    )

    tutorials = [setup_en]

    # option_groups = option_groups
    # options_presets = option_presets
