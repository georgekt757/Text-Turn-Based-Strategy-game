# Changelog

(DD/MM/YYYY)

## 11/11/2024

### Minor update - Perks

- Added a perk method to [core.py](core.py), where every 2 stages will grant a perk that will increase an attribute, with the choices being:
  - Attack by 3 points
  - Accuracy by 5 points
  - Defense by 1 point
  - Initiative by 2 points
- Tweaked some of [Bolt's and the Bartender's dialogue](JSON/dialogue.json) to better fit the next stage.
- Removed a handful of unecessary whitespace, and added some where it was needed.

## 04/11/2024

### Major Update - New Hope and QoL changes

- Finished New Hope, it is now fully functional and complete with dialogue.
  - Two new NPCs, Bolt and another Scrapper Drone.
  - Dialogue is a bit more complex here:
    - You talk to two groups of NPCs, one you can fight too.
    - The outcome of the crash site affects dialogue here... Choose wisely.
- Tweaked the save/load options so that they are separate.
- Removed the `Attack` option in the main menu as it has been rendered obsolete, for now at least.
Until a day comes where I decide to make it useful again, it has been commented out.
- Tweaked NPC initiative so that it may never fall below 1.
- Created the next stage - Find who can decode a black box

## 01/11/2024

### Minor Update - New Month

- Implimented ammunition into [combat](combat.py).
- Increased time between enemy and player dealing damage by 0.2s to 1s.
- Reduced the player's starting HP from 50 to 30, but for every stage advancement, player health goes up by 20
- Created new location - New Hope

To do: Finish off New Hope. This is the part where programming this game (should) become a breeze.

## 31/10/2024

### Minor update - Halloween

- Created the fighter method in [the main menu](main.py), where the player is able inspect their objective and where they are in case they're an amnesiac.
It'll also be useful for going to other places, probably.
- Edited the prospector's dialogue in [the JSON](JSON/dialogue.json) to make more sense.
- Increased the chance for the Scrapper Drone to hit from 18% to 30% as it was hitting the player far too little.
- Fixed a bug that caused the player to transit twice to a location - The transit function was being called twice for some reason.
- Tweaked the save method so that if an error occurs it handles it a bit more conveniently.
- Also did minor tweaks to the load method by removing some indents to improve efficiency by probably 0.0001% on modern hardware.

To do: Fix the remaining issues before moving onto bigger things, this is honestly a great stage to end at for now.

## 30/10/2024

### Major update - Beta

- Following the surprisingly simple creation of [combat.py](combat.py), I am proud to announce that **this TBS game is officialy out of alpha!**
  - Combat is done by getting a list of the NPCs required as a parameter, and doing an insertion sort to correct their initiative.
  - The player is then, once it's their turn, given an input choice to select target. They then deal damage to that target.
  If they are killed, they are removed from the list. If the player is killed, it breaks and returns `"player_died"`.
  If all targets are eliminated it aptly prints `All targets have been eliminated!` and returns `"victory"`.
- Increased player's starting health from 30 to 50
- All weapons have seen a minor increase in damage
- Furthermore, this game's versions are now to be numbered. We are now at **v0.1.1**, where the digits denote:
  - Major update
  - Minor update
  - Bug fixes, patches, and hotfixes

Ammunition hasn't quite been done yet, but we shall cross that bridge when we get to it.
In any case, the game is playable, and I will continue work on it until it is done.

## 28/10/2024

- For some reason when advancing, it returns `None` as the loop control value first, afterwards it then does what it is supposed to do.
**Just commented out the else statement. I don't have a flipping clue how to fix that properly.** But what baffles me most is why return `None` first and *then* what I want?

To do: Fix the weird bug when loading where it repeats the same message twice. Make it sure that it isn't saying the bad message when doing a new character and attempting to talk in the crash site after the conflict has been resolved for the first time. Furthermore - create combat.py.

## 26/10/2024

- Updated [the readme](README.md) so that instructions on how to run this programme are clear for those who are unfamiliar with the process.
- Created [dialogue.json](JSON/dialogue.json) where NPC dialogue text is stored. Player response is to be stored and handled in [locations.py](locations.py).
- Dialogue in-game, while not as extravagent as what was initially anticipated, is mostly complete with the prospectors.
- Return conditions for the loop control have been updated so that the stage may advance. This was a bloody pain in the arse.

To do: Fix what's going on with the weird exit condition after finishing dialogue. Also, check if the stage has actually gone up or not.

## 20/10/2024

- Created the first NPCs, the prospectors more specifically. They're in the aptly-named npc.py.
- Got started on dialogue. It has been... Difficult.
- **No backup has been made for this version due to the volatile changes made.**

I refuse to let this become another one of my failures shelved away never to be touched again. I've gotten this far.

## 18/10/2024

- Fixed a bug that caused the player to die instantly upon loading.
- Moved all JSON data, excluding save/load data created during runtime, to a [folder](JSON). Changed strings for file pathing to the new file path as raw strings.
- Created [npc.py](npc.py), which will serve as framework for the NPCs

To do: Get those NPCs working. How? Lord knows.

## 17/10/2024

- Moved all the inventory stuff to [player](player.py). Deleted inventory.py as a consequence.
- Changed Location ID from strings to integers.
- Created [menu.py](menu.py) which handles the main menu, and later everything else menu-related.

To do: Fix the bug in player causing the player to just die instantly, by having damage initialised at 0 when it should be at the player's max health.
Create first location, the crash site.

## 14/10/2024

- Completed [inventory.py](inventory.py), with integration into [core](core.py).
- Fixed a bug in [player](player.py) that caused set_ammoSpent to be comparing the new value to its present rather than the clip size.
- Saving and loading finally possible! So long as you know what a file directory is.
- Reworked the [state list](<Core - State and location list.md>) so that creating and loading characters is unified under 'loading'.
Changes in [core](core.py) reflect this. It has also been renamed to "Core - State and location list" as locations will be included to save file space.
- Created new state "idle", where the player can do whatever the fuck they want at that point, including saving.

To do: Create locations and transit between them. This is gonna be a tough one!

## 11/10/2024

- Removed plan.pptx as I cannot remember the last time it was used.
- Removed inventory from the player class in [player.py](player.py) as, after attempting to get it to work, one lone list was deemed unsuitable.
How I did not foresee this is beyond me. Seperate module, [inventory.py](inventory.py), has been created in its place.
- Oh, and the two markdown files (this one and [the readme](README.md)) were renamed to be capitalised.

To do: Finish off [inventory.py](inventory.py). Running the code from [main](main.py) will not cause any error right now, however, as it has not been integrated and won't be until it is complete.

## 05/10/2024

- Changelog started long after this project started lol
- Fixed the shitty indentation in [player.py](player.py). Thanks for not obeying PEP 8, Trinket!
- Completed the code for armour and initiative. Shouldn't have to worry too much about either now.
- Created [weapons.json](weapons.json) which has laid the foundation for the many weapons this game will have. These include the assault rifle, pistol, shotgun, sniper rifle, light machine gun, and the debug gun.
- Created integration for weapons in [core.py](core.py) - Players may finally arm themselves!
- Deleted generic.json as it did absolutely nothing, and I forgot what it was originally supposed to do.

Have to move faster going forward - All of that took two hours. Could've been way quicker.
