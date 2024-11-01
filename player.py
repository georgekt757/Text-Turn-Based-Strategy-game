import json
from random import randint
from dataclasses import dataclass

class Player:
    def __init__(self, name, hp, wpn, wpnDesc, atk, amr, amrDesc, dfe, itv): # Name, inventory, hitpoints (need to create damage formulae), active weapon, attack, defence, initiative
        self._name = name
        self._hp = hp
        self._wpn = wpn
        self._wpnDesc = wpnDesc
        self._atk = atk
        self._amr = amr
        self._amrDesc = amrDesc
        self._dfe = dfe
        self._itv = itv

        self._contents = None
        self._clipSize = 0
        self._ammoSpent = 0
        self._hitRoll = 0
        self._damage = hp
        self._fireType = ""

    def set_name(self, name):
        self._name = name
    def get_name(self):
        return self._name

    def set_hp(self, hp): # Distinct from damage as this is the maximum
        self._hp = hp
        self._damage = hp
    def get_hp(self):
        return self._hp

    def set_wpn(self, wpn):
        self._wpn = wpn
    def get_wpn(self):
        return self._wpn

    def set_wpnDesc(self, wpnDesc):
        self._wpnDesc = wpnDesc
    def get_wpnDesc(self):
        return self._wpnDesc

    def set_atk(self, atk):
        self._atk = atk
    def get_atk(self):
        return self._atk

    def set_amr(self, amr):
        self._amr = amr
    def get_amr(self):
        return self._amr

    def set_amrDesc(self, amrDesc):
        self._amrDesc = amrDesc
    def get_amrDesc(self):
        return self._amrDesc

    def set_dfe(self, dfe):
        self._dfe = dfe
    def get_dfe(self):
        return self._dfe

    def set_itv(self, itv):
        if itv < 0:
            itv = 0
        elif itv > 20:
            itv = 20
        self._itv = itv
    def get_itv(self):
        return self._itv

    def set_clipSize(self, clipSize):
        self._clipSize = clipSize
    def get_clipSize(self):
        return self._clipSize

    def set_ammoSpent(self, ammoSpent):
        if ammoSpent > self.get_clipSize():
            ammoSpent = self.get_clipSize()
        elif ammoSpent < 0:
            ammoSpent = 0
        self._ammoSpent = ammoSpent
    def get_ammoSpent(self):
        return self._ammoSpent
    def consume_ammo(self):
        if self._fireType == "single":
            self._ammoSpent += 1
        elif self._fireType == "burst":
            self._ammoSpent += -(self._clipSize // -randint(2, 5))
        
        if self._ammoSpent > self._clipSize:
            self._ammoSpent = self._clipSize
        elif self._ammoSpent < 0:
            self._ammoSpent = 0
    
    def set_hitRoll(self, hitRoll):
        self._hitRoll = hitRoll
    def get_hitRoll(self):
        return self._hitRoll
    
    def set_fireType(self, fireType):
        self._fireType = fireType
    def get_fireType(self):
        return self._fireType
    
    def set_damage(self, damage):
        self._damage = damage
    def get_damage(self):
        return self._damage
    def deal_damage(self, damage): # Use negative damage parameter for healing
        if damage > self._hp:
            damage = self._hp
        self._damage -= damage

    # Utilises the already existing setter methods for amr and dfe. Works excellently.
    def change_amr(self, amr):
        with open(r'JSON\protection.json','r') as prot:
            self._contents = json.load(prot)
        self.set_amr(self._contents[amr]["name"])
        self.set_amrDesc(self._contents[amr]["desc"])
        self.set_dfe(self._contents[amr]["def"])
        self.set_itv(player.get_itv() - self._contents[amr]["itvPenalty"])
    
    # Direct copy of change_amr that was modified to the needs of the weapons.
    def change_wpn(self, wpn):
        with open(r'JSON\weapons.json','r') as weap:
            self._contents = json.load(weap)
        self.set_wpn(self._contents[wpn]["name"])
        self.set_wpnDesc(self._contents[wpn]["desc"])
        self.set_atk(self._contents[wpn]["atk"])
        self.set_clipSize(self._contents[wpn]["ammo"])
        self.set_hitRoll(self._contents[wpn]["hitRoll"])
        self._fireType = self._contents[wpn]["fireType"]

@dataclass
class Inventory:
    SLOT1: str # Healthshots
    DESC1: str
    count1: int
    SLOT2: str # Impact grenades
    DESC2: str
    count2: int
    SLOT3: str # Focus shots
    DESC3: str
    count3: int

    def get_SLOT1(self):
        return self.SLOT1
    def get_DESC1(self):
        return self.DESC1
    def set_count1(self, count1):
        self.count1 = count1
    def get_count1(self):
        return self.count1
    def add_SLOT1(self, amount): # Can also work for subtraction if parameter is negative
        self.count1 += amount

    def get_SLOT2(self):
        return self.SLOT2
    def get_DESC2(self):
        return self.DESC2
    def set_count2(self, count2):
        self.count2 = count2
    def get_count2(self):
        return self.count2
    def add_SLOT2(self, amount):  # Can also work for subtraction if parameter is negative
        self.count2 += amount

    def get_SLOT3(self):
        return self.SLOT3
    def get_DESC3(self):
        return self.DESC3
    def set_count3(self, count3):
        self.count3 = count3
    def get_count3(self):
        return self.count3
    def add_SLOT3(self, amount):  # Can also work for subtraction if parameter is negative
        self.count3 += amount
    
def init():
    with open(r'JSON\items.json','r') as (data):
        items = json.load(data)
    inv = Inventory(items["stim"]["name"], items["stim"]["desc"], 0,
                    items["impact"]["name"], items["impact"]["desc"], 0,
                    items["focus"]["name"], items["focus"]["desc"], 0)
    return inv

inv = init()

player = Player(None, 30, 
                None, "You have no weapon equipped!", 0, 
                None, "You have no armour equipped!", 0, 
                13)