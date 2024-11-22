import json
from time import sleep
from random import randint

from player import player, inv
from npc import *

def insertion_sort(objects): # Yes, I used ChatGPT for this. No, I am not ashamed. No, I have not used it for anything else barring information on *how* to do things rather than the code itself.
    # Loop over each element in the array starting from the second element
    for i in range(1, len(objects)):
        current = objects[i]
        j = i - 1
        
        # Compare and shift elements to the right to make room for the current element
        while j >= 0 and objects[j].get_itv() < current.get_itv():
            objects[j + 1] = objects[j]
            j -= 1
            
        # Insert the current element in its correct position
        objects[j + 1] = current

    for k in range(len(objects) * 3): # Three passes
        try:
            if objects[k].get_itv() == objects[k + 1].get_itv():
                objects[k + 1].set_itv(objects[k + 1].get_itv() - 1)
        except:
            pass
    return objects

def combat(list):
    p = list[0]
    fighters = insertion_sort(list)
    turn = 0
    itv = player.get_itv()
    in_combat = True
    died = False
    enemycount = len(fighters) - 1
    player.set_ammoSpent(0)

    with open(r'JSON\items.json','r') as (data):
        items = json.load(data)
        stim = items["stim"]["HP"]
        hi_grenade_atk = items["impact"]["atk"]
        hi_grenade_atk_max = items["impact"]["atkMax"]
        focus = items["focus"]["atk"]
        focus_backfire = items["focus"]["atkSelf"]

    print(f"\n<< Combat initiated, there are {enemycount} target(s)! >>\n")
    sleep(2)
    while in_combat:
        turn += 1
        print(f"\nTurn {turn}.\n")
        
        for i in range(len(fighters)):
            try:
                if fighters[i].get_itv() > itv or fighters[i].get_itv() < itv:
                    e = fighters[i]
                    hit = randint(0, 100)
                    if e.get_damage() <= 0:
                        print(f"{e.get_name()} was killed!")
                        fighters.remove(e)
                    elif hit <= e.get_hitRoll():
                        try:
                            dmg = e.get_atk() // player.get_dfe() + randint(0, e.get_atk() // 3)
                        except:
                            dmg = e.get_atk() + randint(0, e.get_atk() // 3)
                        print(f"{e.get_name()} dealt {dmg} damage using {e.get_wpn()}.")
                        player.deal_damage(dmg)
                    else:
                        print(f"{e.get_name()} missed!")

                elif fighters[i] == p: # Player's turn
                    if player.get_damage() <= 0:
                        in_combat = False
                        died = True
                        break
                    
                    print(f"You have {player.get_damage()} HP left.\nYou have {player.get_clipSize() - player.get_ammoSpent()} bullet(s) remaining.")
                    print("Select target: ")
                    for j in range(len(fighters)):
                        if fighters[j] != p and fighters[j].get_damage() > 0:
                            print(f"{j + 1}. {fighters[j].get_name()} - {fighters[j].get_damage()} HP remaining")
                    target = int(input()) - 1
                    
                    e = fighters[target]

                    hit = randint(0, 100)

                    choice = int(input(f'''
Would you like to:
1. Use healthshot - {inv.get_count1()} remaining
2. Use HI grenade - {inv.get_count2()} remaining
3. Use focus shot - {inv.get_count3()} remaining
9. Do nothing else
'''))
                    
                    if player.get_ammoSpent() >= player.get_clipSize():
                        print(f"You have no ammo left for your {player.get_wpn()}! Reloading!")
                        player.set_ammoSpent(0)
                    elif hit <= player.get_hitRoll():
                        try:
                            dmg = player.get_atk() // e.get_dfe() + randint(0, player.get_atk() // 3)
                        except:
                            dmg = player.get_atk() + randint(0, player.get_atk() // 3)
                        player.consume_ammo()
                        print(f"You dealt {dmg} damage using {player.get_wpn()} to {e.get_name()}.")
                        e.deal_damage(dmg)
                    else:
                        player.consume_ammo()
                        print(f"You missed with your {player.get_wpn()}!")
                    
                    if choice == 1 and inv.get_count1() > 0:
                        restore = stim + randint(-6,6)
                        player.deal_damage(restore)
                        inv.add_SLOT1(-1)
                        print(f"You restore {abs(restore)} HP.")
                    elif choice == 1 and inv.get_count1() <= 0:
                        print("You have no healthshots!")
                    
                    elif choice == 2 and inv.get_count2() > 0:
                        inv.add_SLOT2(-1)
                        for k in range(len(fighters)):
                            if fighters[k] != p:
                                dmg = randint(hi_grenade_atk, hi_grenade_atk_max)
                                fighters[k].deal_damage(hi_grenade_atk)
                                print(f"You deal {dmg} damage to {fighters[k].get_name()}")
                    elif choice == 2 and inv.get_count2() <= 0:
                        print("You have no grenades!")

                    elif choice == 3 and inv.get_count3() > 0 and player.get_damage() > focus_backfire:
                        inv.add_SLOT3(-1)
                        e.deal_damage(focus)
                        player.deal_damage(focus_backfire)
                        print(f"You deal {focus} damage to {e.get_name()}, but also deal {focus_backfire} damage to yourself.")
                    elif choice == 3 and inv.get_count3() > 0 and player.get_damage() <= focus_backfire:
                        print("The focus shot does not fire, under the belief it would kill you.")
                    elif choice == 3 and inv.get_count3 <= 0:
                        print("You have no focus shots!")

                    if e.get_damage() <= 0:
                        print(f"{e.get_name()} was killed!")
                        fighters.remove(e)

                else:
                    print("Someone fucked up somewhere.")
                sleep(1)
            except:
                pass
        enemycount = len(fighters) - 1
        if enemycount <= 0:
            in_combat = False

    
    if died:
        in_combat = False
        msg = "player_died"
    elif enemycount <= 0:
        in_combat = False
        print("All targets have been eliminated!")
        msg = "victory"
    else:
        pass
    
    return msg
