import json
from random import randint

from player import player, inv
from locations import crashsite, new_hope
from menu import main_menu

class Core:
    def __init__(self, state, location, stage):
        self._state = state # Predetermined strings to tell the top of the loop what state the game is in (in combat, configuration, etc.)
        self._location = location # Integer that'll serve as an ID for the real thing
        # Check Core - State list for further information
        self._stage = stage # For quest stage. A tree may be necessary to comprehend this. 
    
    def set_state(self, state):
        self._state = state
    def get_state(self):
        return self._state
    
    def set_location(self, location):
        self._location = location
    def get_location(self):
        return self._location
    
    def set_stage(self, stage):
        self._stage = stage
    def get_stage(self):
        return self._stage
    
core_info = Core("loading", 0, 0)

def save():
    save_data = {
        "name": player.get_name(),
        "hp": player.get_hp(),
        "damage": player.get_damage(),
        "wpn": player.get_wpn(),
        "wpnDesc": player.get_wpnDesc(),
        "atk": player.get_atk(),
        "amr": player.get_amr(),
        "amrDesc": player.get_amrDesc(),
        "dfe": player.get_dfe(),
        "itv": player.get_itv(),
        "clipSize": player.get_clipSize(),
        "hitRoll": player.get_hitRoll(),
        "fireType": player.get_fireType(),
        "count1": inv.get_count1(),
        "count2": inv.get_count2(),
        "count3": inv.get_count3(),
        "location": core_info.get_location(),
        "stage": core_info.get_stage(),

        # Location specific data
        "prospectors": crashsite.get_prospector_surived(),

        "new_hope_available": new_hope.get_available(),
        "new_hope_bartender_convinced": new_hope.get_convinced(),
        "new_hope_prospector_survived": new_hope.get_prospector_surived()
    }

    try:
        with open(f'{player.get_name()}_data.json','w') as data:
            data.write(json.dumps(save_data))
        print("Saved to this directory successfuly. You may move the file wherever you want.")
        
    except:
        rename = int(input("\n\nYour data could not be saved. If your name has special characters that messes with Windows's file management, you can change it now and save again. Would you like to?\n1. Yes\nInput anything else to pass.\n"))
        if rename == 1:
            player.set_name(input("New name: "))
            save()

def load():

    with open(input(r"Input the directory of the JSON: "),'r') as data:
        save_data = json.load(data)
        player.set_name(save_data["name"])
        player.set_hp(save_data["hp"])
        player.set_damage(save_data["damage"])
        player.set_wpn(save_data["wpn"])
        player.set_wpnDesc(save_data["wpnDesc"])
        player.set_atk(save_data["atk"])
        player.set_amr(save_data["amr"])
        player.set_amrDesc(save_data["amrDesc"])
        player.set_dfe(save_data["dfe"])
        player.set_itv(save_data["itv"])
        player.set_clipSize(save_data["clipSize"])
        player.set_hitRoll(save_data["hitRoll"])
        player.set_fireType(save_data["fireType"])
        inv.set_count1(save_data["count1"])
        inv.set_count2(save_data["count2"])
        inv.set_count3(save_data["count3"])
        core_info.set_location(save_data["location"])
        core_info.set_stage(save_data["stage"])

        # Location specific data
        crashsite.set_prospector_survived(save_data["prospectors"])

        new_hope.set_available(save_data["new_hope_available"])
        new_hope.set_convinced(save_data["new_hope_bartender_convinced"])
        new_hope.set_prospector_survived(save_data["new_hope_prospector_survived"])


    core_info.set_state("idle")
    transit(save_data["location"])

def first_load():
    done = False
    choice = 0
    
    while player.get_name() == None:
      try:
        player.set_name(input("What is your character's name?: "))
        if player.get_name() == "":
            print("You have a name. So why don't you use it?")
            player.set_name(None)
      except:
        print("That's not valid now, is it?")
    print(f"Nice to meet you, {player.get_name()}!")

    # Nice little part of the code that sets the armour.
    print("Protection is essential for withstanding damage, but be warned - All of these penalise initiative to some extent. You can deal with that just after, though...")
    print("Select which armour class you'd prefer:")
    while player.get_amr() == None:
        print('''
    1. Standard
    2. Light
    3. Heavy
            ''')
        try:
            choice = int(input())
            if choice == 1:
                player.change_amr("med")
            elif choice == 2:
                player.change_amr("low")
            elif choice == 3:
                player.change_amr("high")
            elif choice == 13: # Gives players debug armour. Not listed for obvious reasons.
                player.change_amr("dbg")
            else:
                print("Went out of range, buddy!")
        except:
            print("Whoops, caught an exception here! Choose another piece of armour for now.")
    print(f"You have chosen {player.get_amr()}. {player.get_amrDesc()}")

    # Initiative
    print("Initiative is a statistic that determines whose turn will be next during combat. The minimum is 0, the maximum is 20.")
    print(f'''
Your current initiative is {player.get_itv()}, your penalty has already been applied, but you can roll for a chance at an increase... or a decrease.")
Do you take the roll... Or not?
''')
    
    while not done:
        print('''
    1. Yes
    2. No
              ''')
        
        try: 
            choice = int(input())
            if choice == 1:
                a = randint(-11,10)
                # Decided to make another nested if statement comparing it and leaving some cheeky messages behind. For lulz. 
                # Won't be any more. I thought even this was pushing it but failed to find an alternative.
                if (player.get_itv() + a) <= 0:
                    print("Your initiative is now 0. Have fun!")
                elif player.get_itv() > player.get_itv() + a:
                    print("Looks like your initiative went down. Oh well. Especially considering you have few opportunities to change this mid-game.")
                elif player.get_itv() < player.get_itv() + a:
                    print("Well, looks like fortune favours you as your initiative went up! Even better, this can't be lowered mid-game, so no more penalties for you!")
                else:
                    print("No change in initiative score. Consider yourself lucky - Especially considering initiative cannot be changed often.")
                player.set_itv(player.get_itv() + a)
                print(f"Your new initiative is {player.get_itv()}.")
                done = True
            elif choice == 2:
                print(f"You decide not to roll. Your initiative is still {player.get_itv()}")
                done = True
            else:
                print("Went out of range, buddy!")
        except:
            print("Your response was invalid, you likely input a string! Just do either 1 or 2, nothing more.")
    
    print('''Now that your armour and initiative has been sorted out, there's only one thing left - Weapons.
It should go without saying that these are highly important, just as much as armour, and you've got five choices:''')

    # This will mimic the armour selection as they are inherently quite similar
    while player.get_wpn() == None:
        print('''
            1. Assault Rifle - Good damage and accuracy, great magazine size
            2. Pistol - Low damage, exceptional accuracy, good magazine size
            3. Shotgun - Great damage, mediocre accuracy, low magazine size
            4. Sniper Rifle - Great damage, exceptional accuracy, poor magazine size
            5. Light Machine Gun - Exceptional damage and magazine size, poor accuracy
            ''')
        
        try:
            choice = int(input())
            if choice == 1:
                player.change_wpn("arl")
            elif choice == 2:
                player.change_wpn("ptl")
            elif choice == 3:
                player.change_wpn("sgn")
            elif choice == 4:
                player.change_wpn("srl")
            elif choice == 5:
                player.change_wpn("lmg")
            elif choice == 757: # Gives the player the Debug Gun. Not listed for obvious reasons.
                player.change_wpn("dbg")
            elif choice == 47: # Staller gun
                player.change_wpn("stl")

            else:
                print("Went out of range, buddy. Try again!")
        except:
            print("Whoops, caught an exception here! Choose another weapon for now.")
    print(f"You have chosen the {player.get_wpn()}. {player.get_wpnDesc()}")

    print('''
You are also to receive three stims, two impact grenades and one focus shot.
Stims restore a small amount of health,
Impact grenades deal light damage to all enemies,
and Focus Shots deal massive damage to a single enemy, but destroy themselves upon use.''')
    inv.add_SLOT1(3)
    inv.add_SLOT2(2)
    inv.add_SLOT3(1)

    print("\nYou have completed character creation. Good job, sir or madam!")
    print('''\nThe Intragalactic Peacekeeping Force has contracted you to investigate the disappearance of one of their ships, the IPNS Whistler, a Sol-class observation ship.
It was performing a training exercise with its crew before suddenly disappearing off radar. They have lead to conclude that the Whistler was, somehow, destroyed.
You are to go to the crash site on Salvation, a small border colony, and assess the situation as the IPF would rather not get the public involved as of right now. Suspiscious...
But the pay is enough to keep you going for the next three months, so regardless, you accept.''')
    
    core_info.set_state("idle")
    transit(1)
    save()

def init():
    print("Welcome to my turn-based strategy game. As of right now, saving and loading existing characters is still a work in progress, but works perfectly fine for the bulk of the game data.")
    while core_info.get_state() == "loading":
        try:
            a = int(input("1. Create new character.\n2. Load from existing character.\n"))
            if a == 1:
                first_load()
            elif a == 2:
                load()
            else:
                print("Your input was not one of the numbers listed. Try again.")
        except:
            print("Programme caught exception. Try again.")

def transit(target):
    try:
        if core_info.get_location() == 0: # Initialisation
            print('''You board your ship, a rather large modified fighter...
It is capable of going nearly everywhere, and allows you to perform your own analyses of situations without interruption.''')
        elif core_info.get_location() == 1: # Crash site
            print("You board your ship and leave the crash site. You can still see the fires...")
        elif core_info.get_location() == 2:
            print("You board your fighter and leave New Hope. Such a pleasant town, if only it weren't dragged into this mess...")

        core_info.set_location(target)
        if target == 1: # Crash site
            crashsite.enter(core_info.get_stage())
        elif target == 2: # New Hope
            new_hope.enter(core_info.get_stage())
    except:
        print("Your fighter says your coordinates are invalid. Please try again.")

def perk():
    running = True
    while running:
        print('''You've advanced enough to be able to enhance one of your attributes. Pick any from the following:
        1. Increase attack by 3 points
        2. Increase accuracy by 5 points
        3. Increase defense by 1 point.
        4. Increase initiative by 2 points
        ''')

        try:
            choice = int(input())
        except:
            print("Input was not an integer.")

        if choice == 1:
            player.set_atk(player.get_atk() + 3)
            print(f"Attack has gone up to {player.get_atk()}.")
            running = False

        elif choice == 2:
            player.set_hitRoll(player.get_hitRoll() + 5)
            print(f"Accuracy has gone up to {player.get_hitRoll()}")
            running = False

        elif choice == 3:
            player.set_dfe(player.get_dfe() + 1)
            print(f"Defense has gone up to {player.get_dfe()}")
            running = False

        elif choice == 4:
            player.set_itv(player.get_itv() + 2)
            print(f"Initiative has gone up to {player.get_itv()}")

        else:
            print("Your input was out of range.")


def main_loop():
    location_list = [crashsite, new_hope]
    running = True
    choice = None
    while running:
        loop_control = main_menu.main_menu_runtime(core_info.get_location(), core_info.get_stage())

        if loop_control == "exit":
            running = False
            print("Thank you for playing. Have a nice day.")

        elif loop_control == "save":
            save()

        elif loop_control == "new_location":
            print("Where to?: ")
            for i in range(len(location_list)):
                if location_list[i].get_available() and location_list[i].get_ID() != core_info.get_location():
                    print(f"{i + 1}. {location_list[i].get_name()}")
            print("9. Cancel")
            try:
                choice = int(input())
            except:
                print("Your input was not an integer. Try again.")

            if choice == 9:
                print("Aborting transport.")
            else:
                transit(choice)

        elif loop_control == "advance":
            core_info.set_stage(core_info.get_stage() + 1)
            player.set_hp(player.get_hp() + 20)
            player.set_damage(player.get_hp())
            print(f"You have advanced a stage. Good job, {player.get_name()}! Check back at your ship for more info on what to do next.")

            # if core_info.get_stage() % 2 == 0:
            perk()

            if core_info.get_stage() >= 1:
                new_hope.set_available(True)

        elif loop_control == "player_died":
            msg = "You have been killed."
            a = randint(0,2)
            if a == 0:
                print(f"{msg} Your corpse is cast away like trash, only to be picked on by vermin...")
            elif a == 1:
                print(f"{msg} Out of respect for your valiant fighting, your enemy gives you one last salute before turning and leaving...")
            elif a == 2:
                print(f"{msg} And while you die cold and lonely... You do not die afraid.")
            else:
                print("Get fucked.")
            running = False
            
        # else:
        #     print("Weird exit condition, something's definitely not right...")
       