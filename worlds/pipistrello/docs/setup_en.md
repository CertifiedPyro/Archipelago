# Pipistrello and the Cursed Yoyo Setup Guide

## Required Software

* [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
* [MelonLoader](https://melonwiki.xyz/#/README?id=requirements)
  * Requires [Microsoft Visual C++ 2015-2019 Redistributable 64 Bit](https://aka.ms/vs/16/release/vc_redist.x64.exe)
  * Requires [dotnet 6.0](https://dotnet.microsoft.com/en-us/download/dotnet/6.0#runtime-desktop-6.0.19)
* [MelonPreferencesManager](https://github.com/piepieonline/MelonPreferencesManager/releases)
* [Pipistrello Archipelago Mod](https://github.com/CertifiedPyro/PipistrelloArchipelago/releases)

## Installation

### Prerequisites
1. Run the MelonLoader installer, select "Pipistrello and the Cursed Yoyo", and click "Install".
2. If you're running Linux:
    1. Export the following environment variable: `WINEDLLOVERRIDES="version=n,b"`
    2. On Steam, you can set the launch options to: `WINEDLLOVERRIDES="version=n,b" %command%`
3. Launch the game to create the required mod folders.
4. Navigate to your game's installation installation folder.
    1. You can find this in Steam by right-clicking > Manage > Browse Local Files.
    2. This is usually  `C:\Program Files (x86)\Steam\steamapps\common\Pipistrello and the Cursed Yoyo`
5. Download the latest release of MelonPreferencesManager.
6. Extract the two dlls into the `Mods/` folder under your game's installation directory.

### Archipelago mod

1. Download `PipistrelloArchipelago.zip` from the latest release.
2. Extract the .zip file's contents directly into the game's installation folder.
    1. Make sure `PipistrelloArchipelago.dll` is in `Mods/` and `Archipelago.MultiClient.Net.dll` is in `UserLibs/`.
3. Launch the game, and you should see a Connect button on the main menu.

### Archipelago tools

1. Make sure Archipelago is installed.
2. Download `pipistrello.apworld` from the latest release.
3. Double-click on `pipistrello.apworld`. Archipelago should install the apworld automatically.
4. Open the Archipelago Launcher and run "Generate Template Options" to create the options template file.
    1. Alternatively, you can download `Pipistrello.and.the.Cursed.Yoyo.yaml` from the latest release.

## Generating a game

Follow [the official instructions](https://archipelago.gg/tutorial/Archipelago/setup_en#generating-a-game).

## Joining a multiworld game
1. Start the game after installing all necessary mods.
2. Press F5 to open MelonPreferencesManager and input your connection information.
3. Press the **Connect** button in-game.
4. Once connected, you can press **Load Game**.
5. Start with a *new* save file. The game will stall for a few seconds before loading.
6. You should now be starting in South Plaza!

## Hints and trackers

If you need to interact with the server, you can use the Archipelago Text Client. There is no visual tracker yet, so
please use Universal Tracker for now.
