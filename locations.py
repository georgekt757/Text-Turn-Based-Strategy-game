from json import load
from random import randint
from time import sleep

from combat import combat
from player import player
from npc import *


class Location:
    def __init__(self, ID, name, desc, canTalk, available):
        self._ID = ID 
        self._name = name
        self._desc = desc
        self._canTalk = canTalk
        self._available = available

        self._contents = None

    def get_ID(self):
        return self._ID
    
    def set_name(self, name):
        self._name = name
    def get_name(self):
        return self._name
    
    def set_desc(self, desc):
        self._desc = desc
    def get_desc(self):
        return self._desc
    
    def set_canTalk(self, canTalk):
        self._canTalk = canTalk
    def get_canTalk(self):
        return self._canTalk
    
    def set_available(self, available):
        self._available = available
    def get_available(self):
        return self._available
    
class Crash_Site(Location):
    def __init__(self, ID, name, desc, canTalk, available):
        super().__init__(ID, name, desc, canTalk, available)
        self._prospector_survived = None

    def set_prospector_survived(self, prospector_survived):
        self._prospector_survived = prospector_survived
    def get_prospector_surived(self):
        return self._prospector_survived
    
    def enter(self, stage):
        print(f"You arrive at: {self.get_name()}. {self.get_desc()}")
        if stage == 0:
            self._canTalk = True
            print("Some prospectors, showing no respect for this tragedy, are already at the crash site. They've spotted you.\n")
        elif stage == 1 and self._prospector_survived:
            self._canTalk = False
            print("The site is a lot calmer now that the prospectors have moved on.\n")
        elif stage == 1 and not self._prospector_survived:
            self._canTalk = False
            print("The corpses of the prospectors lay still.\n")
        elif stage >= 2:
            self._canTalk = True

        else:
            self._canTalk = False
            print("")

    def initiate_dialogue(self, stage): # when the code is spaghetti
        if stage >= 1:
            self._canTalk = False
            self._status = None
        else:

            with open(r"JSON\dialogue.json") as speech:
                self._contents = load(speech)
            self._status = "talk"
            self._running = True
            print(self._contents["prospectors"]["greeting"])
            while self._running:
                self._choice = int(input('''
        1. What are you doing here?
        2. You aren't supposed to be here. Leave before someone gets shot.
        3. [ROLL] You're out here, disrespecting the dead by looting off of them. I think you should leave.
'''))
                if self._choice == 1:
                    print(self._contents["prospectors"]["angry"])
                elif self._choice == 2:
                    print(self._contents["prospectors"]["threatened"])
                    self._status = combat([player, p_bob, p_lisa, p_sbot])
                    if self._status == "player_died":
                        self._running = False
                    elif self._status == "victory":
                        self._prospector_survived = False
                        self._status = "resolved"
                        self._running = False
                
                elif self._choice == 3:
                    self._roll = randint(1, 10)
                    if self._roll >= 5:
                        print(self._contents["prospectors"]["roll_pass"]) 

                        self._prospector_survived = True
                        self._status = "resolved"
                        self._running = False
                    else:
                        print(self._contents["prospectors"]["roll_fail"])
                        self._status = combat([player, p_bob, p_lisa, p_sbot])
                        if self._status == "player_died":
                            self._running = False
                        elif self._status == "victory":
                            self._prospector_survived = False
                            self._status = "resolved"
                            self._running = False
                if self._status == "talk":
                    print(self._contents["prospectors"]["generic"])
                else:
                    pass
        return self._status

class New_Hope(Location):
    def __init__(self, ID, name, desc, canTalk, available):
        super().__init__(ID, name, desc, canTalk, available)

        self._convinced = False
        self._prospector_survived = None
        # If the bartender is convinced of your trustworthiness, this will be true.
    
    def set_convinced(self, convinced):
        self._convinced = convinced
    def get_convinced(self):
        return self._convinced
    
    def set_prospector_survived(self, prospector_survived):
        self._prospector_survived = prospector_survived
    def get_prospector_surived(self):
        return self._prospector_survived

    def enter(self, stage):
        print(f"You arrive at: {self.get_name()}. {self.get_desc()}")
        if stage == 1:
            self._canTalk = True
            print("You decide to enter The New Hope Central. It's a rather quiet bar, with a band playing smooth jazz and the general atmosphere being calm.")
            print("Though in town as small as this, that shouldn't be of any surprise. The bartender's grin is welcoming, albeit creepy.")
    
    def initiate_dialogue(self, stage):
        with open(r"JSON\dialogue.json") as speech:
            self._contents = load(speech)
        self._status = "talk"
        self._running = True

        if stage <= 1 and not self._convinced:
            print(self._contents["new_hope_bartender"]["greeting"])
            while self._running:
                self._choice = int(input('''
    1. I'm looking for some information, actually.
    2. What's the lightest thing you have? I need to keep a straight head.
'''))
                if self._choice == 1:
                    pass
                elif self._choice == 2:
                    print(self._contents["new_hope_bartender"]["serve"])
                    sleep(3.0)
                    print("Thanks. Now, I require some information, if you don't mind.")
                    sleep(3.0)

                print(self._contents["new_hope_bartender"]["info1"])
                sleep(3.0)
                print("There was a ship crash not long ago. I've been tasked to investigate it.")
                sleep(3.0)
                print(self._contents["new_hope_bartender"]["info2"])
                sleep(3.0)
                print("Really? Is there nothing else you can tell me about what may have happened? Did any survivors not come through here?")
                sleep(3.0)
                print(self._contents["new_hope_bartender"]["info3"])
                sleep(3.0)
                print("I will. Thank you for your time (You decide talking to the people the bartender points to. They bear the same insignia the prospectors had.).")
                self.set_convinced(True)
                self._running = False
                self._status = "goodbye"
        
        elif stage <= 1 and self._convinced and crashsite.get_prospector_surived():
            print(self._contents["new_hope_prospectors"]["greeting"])
            while self._running:
                self._choice = int(input('''
    1. Hey, you're with those guys I met at the crash site!
    2. Oh Christ, not you people again...
'''))
                if self._choice == 1 or self._choice == 2:
                    print(self._contents["new_hope_prospectors"]["distrustful1"])
                    self._choice = int(input('''
    1. [ROLL] No quarrel, honest! I would just like to know why you were there, or if you happen to know anything about the crash.
    2. I should've killed you while I was there!
'''))
                    if self._choice == 1:
                        self._roll = randint(0, 10)
                        if self._roll >= 4:
                            print(self._contents["new_hope_prospectors"]["distrustful_pass"])
                            sleep(3.0)
                            print("No! I've been paid to investigate why this had happened, not because I wish to salvage.")
                            sleep(3.0)
                            print(self._contents["new_hope_prospectors"]["distrustful2"])
                            sleep(3.0)
                            print(self._contents["new_hope_prospectors"]["distrustful3"])
                            sleep(3.0)
                            print(self._contents["new_hope_prospectors"]["distrustful4"])
                            sleep(3.0)
                            print("Thank you. This helps out massively.")
                            sleep(3.0)
                            print(self._contents["new_hope_prospectors"]["distrustful5"])
                            sleep(3.0)
                            print("I forgive you.")
                            sleep(3.0)
                            self._prospector_survived = True
                            self._status = "resolved"
                            self._running = False
                        
                        else:
                            print("I'm not telling you squat.")
                    
                    if self._choice == 2 or self._roll < 4:

                        print(self._contents["new_hope_prospectors"]["distrustful_fail"])
                        self._status = combat([player, nh_bolt, nh_sbot, p_bob, p_lisa, p_sbot])
                        if self._status == "player_died":
                            self._running = False
                        elif self._status == "victory":
                            self._prospector_survived = False
                            self._status = "resolved"

                            print(self._contents["new_hope_bartender"]["grateful1"])
                            sleep(3.0)
                            print("I don't know if those salvagers were responsible for the crash, but they are responsible for looting it.")
                            sleep(3.0)
                            print(self._contents["new_hope_bartender"]["grateful2"])
                            sleep(3.0)
                            print(self._contents["new_hope_bartender"]["grateful3"])
                            sleep(3.0)
                            self._running = False


        elif stage <= 1 and self._convinced and not crashsite.get_prospector_surived():
            print(self._contents["new_hope_prospectors"]["greeting"])
            while self._running:
                sleep(3.0)
                print("Hey, you're with those guys I killed at the crash site!")
                sleep(3.0)
                print(self._contents["new_hope_prospectors"]["vengeful"])
                sleep(3)
                self._status = combat([player, nh_bolt, nh_sbot])
                if self._status == "player_died":
                    self._running = False
                elif self._status == "victory":
                    self._prospector_survived = False
                    self._status = "resolved"

                    print(self._contents["new_hope_bartender"]["grateful1"])
                    sleep(3.0)
                    print("I don't know if those salvagers were responsible for the crash, but they are responsible for looting it.")
                    sleep(3.0)
                    print(self._contents["new_hope_bartender"]["grateful2"])
                    sleep(3.0)
                    print(self._contents["new_hope_bartender"]["grateful3"])
                    sleep(3.0)
                    self._running = False

        elif stage >= 2:
            print(self._contents["new_hope_bartender"]["generic"])
            self._running = False
            self._status = "goodbye"
        
        return self._status




crashsite = Crash_Site(1, "Crash site",
                    "Crash site of the IPNS Whistler, an ageing Sol-class observation ship. Fires can be seen all around the crash site. There were definitely no survivors here.",
                    False, True)

new_hope = New_Hope(2, "New Hope",
                    "A small town with all amenities necessary for its survival, including a bar named 'The New Hope Central'. ",
                    False, False)