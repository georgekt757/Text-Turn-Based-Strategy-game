from player import player, inv
from locations import crashsite, new_hope, guardian_station

class Menu:
    def __init__(self):
        self._MAIN = '''What would you like to do?:
    1. Talk
    2. Open inventory
    3. Board fighter
    8. Save
    99. Exit game
'''
        self._inMain = True
        self._inInv = False
        self._inFighter = False
        self._dialogue_outcome = None
        self._location = ""
        self._location_desc = ""
        self._temp = None

        self._NO_TALK = "There's nobody here to talk to."
        self._NEW_LOCATION = "new_location"

    def location_stage_handling(self, location):
        if location == 1:
            self._location = crashsite.get_name()
            self._location_desc = crashsite.get_desc()
        elif location == 2:
            self._location = new_hope.get_name()
            self._location_desc = new_hope.get_desc()
        elif location == 3:
            self._location = guardian_station.get_name()
            self._location_desc = guardian_station.get_desc()
        else:
            print("Error - Invalid location data")

    def dialogue(self, location, stage):
        if location == 1 and not crashsite.get_canTalk(): # crash site
            print(self._NO_TALK)
            self._dialogue_outcome = "goodbye"
        elif location == 1 and crashsite.get_canTalk():
            self._dialogue_outcome = crashsite.initiate_dialogue(stage)

        elif location == 2 and not new_hope.get_canTalk():
            print(self._NO_TALK)
        elif location == 2 and new_hope.get_canTalk():
            self._dialogue_outcome = new_hope.initiate_dialogue(stage)

        elif location == 3 and guardian_station.get_canTalk():
            self._dialogue_outcome = guardian_station.initiate_dialogue(stage)
        elif location == 3 and not guardian_station.get_canTalk():
            print(self._NO_TALK)
            self._dialogue_outcome = "goodbye"

        else:
            print("Dialogue has yet to be programmed at that location.")
    
    def check_dialogue_outcome(self):
        if self._dialogue_outcome == "goodbye":
            pass

        elif self._dialogue_outcome == "resolved":
            self._dialogue_outcome = "advance"

        elif self._dialogue_outcome == "placeholder":
            print("Still under construction. Whoops!")

        else:
            # print("Summin ain't right.")
            pass
        self._inMain = False
    
    def inventory(self):
        self._inInv = True
        while self._inInv:

            print(f'''
{player.get_wpn()} - {player.get_wpnDesc()} It deals {player.get_atk()} damage and holds {player.get_clipSize()} bullets.
{player.get_amr()} - {player.get_amrDesc()} It provides {player.get_dfe()} points of protection.
{inv.get_SLOT1()} - {inv.get_DESC1()} You have {inv.get_count1()}.
{inv.get_SLOT2()} - {inv.get_DESC2()} You have {inv.get_count2()}.
{inv.get_SLOT3()} - {inv.get_DESC3()} You have {inv.get_count3()}.

1. Use healthshot
9. Exit inventory menu''')
            self._choice = int(input())
            if self._choice == 1 and inv.get_count1() > 0:
                if player.get_damage() == player.get_hp():
                    print("You are already at max HP!")
                else: 
                    print(f"You restore 10 hitpoints. You currently have {player.get_damage()} hitpoints.")
                    player.deal_damage(-10)
                    inv.add_SLOT1(-1)
            elif self._choice == 1 and inv.get_count1() <= 0:
                print("You have no healthshots.")
            elif self._choice == 9:
                self._inInv = False
    
    def fighter(self, stage):
        self._inFighter = True
        while self._inFighter:
            print(f"You are at: {self._location}")
            print(self._location_desc)
            print(f"You have {player.get_damage()}/{player.get_hp()} HP remaining.")
            print("Current objective:")
            if stage == 0:
                print('''Find out the fate of the Intragalactic Peacekeeping Navy Ship Whistler.

Using what little info the IPF provided me, I have to figure out what the hell is going on here. Bizzarly, there are prospectors already on-site.
Salvation isn't a rich colony by any means. But they're sure as shit not this poor to loot of the corpses of those who are protecting them.''')
            
            elif stage == 1 and crashsite.get_prospector_surived():
                print('''Head to the nearby town of New Hope for more information.
                      
The prospectors have (reluctantly) left in peace, but I have no info on what to do next. Perhaps the denizens of New Hope will have more information for me.
If there's a bar, that'll be as good a place as any. I could certainly use the drink after this.''')
            elif stage == 1 and not crashsite.get_prospector_surived():
                print('''Head to the nearby town of New Hope for more information.
                      
I've killed the prospectors, but I have no info on what to do next. Perhaps the denizens of New Hope will have more information for me.
If there's a bar, that'll be as good a place as any. I could certainly use the drink after this.''')

            elif stage == 1:
                print('''Head to the nearby town of New Hope for more information.
                      
I've dealt with the prospectors, but have no info on what to do next. Perhaps the denizens of New Hope will have more information for me.
If there's a bar, that'll be as good a place as any. I could certainly use the drink after this.''')
            
            elif stage == 2 and new_hope.get_prospector_surived():
                print('''Find someone who can decode black box data.
                      
The prospectors have very kindly given me the black box they must've skilfully removed from the crash site, what with the fires and all, but I have no way to read it due to the unusually heavy encryption.
Bolt suggested I go to the IPF to decode this data. Better than risking my life doing it through... Less legitimate means.''')
            
            elif stage == 2 and not new_hope.get_prospector_surived() and not crashsite.get_prospector_surived():
                print('''Find someone who can decode black box data.
                      
As per the bartender's suggestion, I picked up the black box from Bolt's corpse. He must've been there but got away from the crash site when I started shooting. Coward.
The bartender suggested I go to the IPF to decode this data. Better than risking my life doing it through... Less legitimate means.''')
                
            elif stage == 2 and not new_hope.get_prospector_surived() and crashsite.get_prospector_surived():
                print('''Find someone who can decode black box data.
                      
As per the bartender's suggestion, I picked up the black box from Bolt's corpse. He must've been at the crash site but left earlier. Shame I had to kill him.
The bartender suggested I go to the IPF to decode this data. Better than risking my life doing it through... Less legitimate means.''')

            else:
                print("<< Nothing. Await further assignment >>")

            print('''Would you like to go elsewhere?
1. Yes, enter cockpit and input coordinates.
Anything else - Remain at current location''')
            try:
                self._choice = int(input())
                if self._choice == 1:
                    return self._NEW_LOCATION
            except ValueError:
                print(f"Your input was not an integer. Try again.")
        
            self._inFighter = False

    def main_menu_runtime(self, location, stage):
        self._inMain = True
        self._choice = 0
        self._temp = None

        self.location_stage_handling(location)
        
        while self._inMain:
            if player.get_damage() <= 0 or self._dialogue_outcome == "player_died": # Checks for death 
                self._inMain = False
                return "player_died"
            if self._dialogue_outcome == "advance":
                self._dialogue_outcome = None
                self._inMan = False
                return "advance"
            print(self._MAIN)
            self._choice = int(input())

            try:

                if self._choice == 1:
                    self.dialogue(location, stage)
                    self.check_dialogue_outcome()

                # elif self._choice == 2:
                #     print(f"You point your {player.get_wpn()} at your targets, but shake as you forget your training. You get gunned to death instead.")
                #     player.deal_damage(player.get_damage())

                elif self._choice == 2:
                    self.inventory()

                elif self._choice == 3:
                    self._temp = self.fighter(stage)
                    if self._temp == self._NEW_LOCATION:
                        self._inMain = False
                        return self._NEW_LOCATION
                    
                elif self._choice == 8:
                    self._inMain = False
                    return "save"

                elif self._choice == 99:
                    self._inMain = False
                    return "exit"
            
            except ValueError as e:
                print(f"Your input wasn't an integer: {e}. Try again.")

main_menu = Menu()
