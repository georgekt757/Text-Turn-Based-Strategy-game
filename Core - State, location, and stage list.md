# State list

## States

- "loading"
  - Initialised state when core_info is declared. Responsible for creating and loading characters.
- "idle"
  - The player is out of combat or dialogue and is able to save and exit.
- "transit"
  - Player is moving from one location to another.

### Locations

- 0
  - Nowhere, technically. Initialised location when core_info is declared.
- 1
  - The Crash Site, the area at which you're supposed to investigate.

## Stages

- 0
  - When the player is first tasked to investigate the crash site
- 1
  - When the player suggests there may be more info at a bar
