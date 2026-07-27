# Pipistrello and the Cursed Yoyo

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need 
to configure and export a config file.

## What does randomization do to this game?

Currently, the randomizer is in early alpha, so only the South Plaza is randomized.
Most items and rewards are randomized and replaced with location checks.

The upgrade tree and badge refinements *are not* currently randomized.

## What items get shuffled?

By default, the following items are shuffled:
- Abilities
- Badges
  - Badges are progressive. The first item will be the base badge, and the second item will be the refined badge.
- BP shards
- Charged moves
- Petal containers
- Special moves
- Upgrades

Money bags are given as filler items.

Due to the small location pool in South Plaza, there are no upgrades in the item pool.
There may also be no charged moves if only the basic checks are enabled.

## What locations get shuffled?

By default, the following locations are enabled:
- Badges
- BP Shards
- Combats (required)
- Musical Notes
- Petal containers
- Quests (burger, etc.)
- Taxi phones unlock

Additionally, the following locations can be optionally included:
- Combats (optional)
- Money bags (standalone)
  - Money bags from combats/quests/etc are always enabled as locations

The following locations are **not** enabled:
- Diamonds
  - Excluded because turn-in is in 2nd half of the game

## What does another world's item look like in Pipistrello and the Cursed Yoyo?

Items from other worlds show up as an Archipelago sprite in the game world.
An Archipelago sprite is also shown on the map.
When you collect another world's item, you'll get a message showing the item name and recipient.

## When the player receives an item, what happens?

The item is instantly granted to you, and a message appears on the bottom of the screen showing the item name and sender.
