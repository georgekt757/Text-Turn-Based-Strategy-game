import json
from random import randint

class NPC:
    def __init__(self, name, hp, wpn, atk, dfe, itv, clipSize, hitRoll): 
        self._name = name
        self._hp = hp
        self._wpn = wpn
        self._atk = atk
        self._dfe = dfe
        self._itv = itv
        self._clipSize = clipSize
        self._ammoSpent = 0
        self._hitRoll = hitRoll
        self._damage = hp

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

    def set_atk(self, atk):
        self._atk = atk
    def get_atk(self):
        return self._atk

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
        if ammoSpent > self._clipSize:
            ammoSpent = self._clipSize
        elif ammoSpent < 0:
            ammoSpent = 0
        self._ammoSpent = ammoSpent
    def get_ammoSpent(self):
        return self._ammoSpent

    def set_hitRoll(self, hitRoll):
        self._hitRoll = hitRoll
    def get_hitRoll(self):
        return self._hitRoll
    
    def set_damage(self, damage):
        self._damage = damage
    def get_damage(self):
        return self._damage
    def deal_damage(self, damage): # Use negative damage parameter for healing
        if damage > self._hp:
            damage = self._hp
        elif damage > self._damage:
            damage = self._damage
        self._damage -= damage

with open(r'JSON\weapons.json','r') as w:
    weap = json.load(w)
with open(r'JSON\protection.json','r') as p:
    prot = json.load(p)

# Prospectors
p_bob = NPC("Robert", 10,
            weap["arl"]["name"], weap["arl"]["atk"],
            prot["low"]["def"], randint(16, 20),
            weap["arl"]["ammo"], weap["arl"]["hitRoll"])

p_lisa = NPC("Lisa", 8,
            weap["ptl"]["name"], weap["ptl"]["atk"],
            prot["low"]["def"], randint(4, 18),
            weap["ptl"]["ammo"], weap["ptl"]["hitRoll"])

p_sbot = NPC("Scrapper Drone", 30,
            weap["wel"]["name"], weap["wel"]["atk"],
            prot["med"]["def"], randint(0, 20),
            weap["wel"]["ammo"], weap["wel"]["hitRoll"])

