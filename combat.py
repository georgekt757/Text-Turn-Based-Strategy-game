from time import sleep
from random import randint
from player import player
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

    for k in range(len(objects)):
        try:
            if objects[k].get_itv() == objects[k + 1].get_itv():
                objects[k + 1].set_itv(objects[k + 1].get_itv() - 1)
        except:
            pass
    return objects


def combat(list):
    fighters = insertion_sort(list)
    turn = 0
    itv = player.get_itv()
    in_combat = True
    died = False
    enemycount = len(fighters) - 1
    print(f"\n<< Combat initiated, there are {enemycount} target(s)! >>\n")
    sleep(2)
    while in_combat:
        turn += 1
        print(f"Turn {turn}.\n")
        
        for i in range(len(fighters)):
            try:
                if fighters[i].get_itv() > itv or fighters[i].get_itv() < itv:
                    e = fighters[i]
                    hit = randint(0, 100)
                    if e.get_damage() <= 0:
                        pass
                    elif hit <= e.get_hitRoll():
                        try:
                            dmg = e.get_atk() // player.get_dfe() + randint(0, e.get_atk() // 3)
                        except:
                            dmg = e.get_atk() + randint(0, e.get_atk() // 3)
                        print(f"{e.get_name()} dealt {dmg} damage using {e.get_wpn()}.")
                        player.deal_damage(dmg)
                    else:
                        print(f"{e.get_name()} missed!")

                elif fighters[i].get_itv() == itv:
                    if player.get_damage() <= 0:
                        in_combat = False
                        died = True
                        break
                    
                    p = fighters[i]
                    print(f"You have {player.get_damage()} HP left.")
                    print("Select target: ")
                    for j in range(len(fighters)):
                        if fighters[j] != p:
                            print(f"{j + 1}. {fighters[j].get_name()} - {fighters[j].get_damage()}")
                    target = int(input()) - 1
                    
                    e = fighters[target]

                    hit = randint(0, 100)
                    
                    if hit <= player.get_hitRoll():
                        try:
                            dmg = player.get_atk() // e.get_dfe() + randint(0, player.get_atk() // 3)
                        except:
                            dmg = player.get_atk() + randint(0, player.get_atk() // 3)
                        print(f"You dealt {dmg} damage using {player.get_wpn()} to {e.get_name()}.")
                        e.deal_damage(dmg)
                        if e.get_damage() <= 0:
                            print(f"{e.get_name()} was killed!")
                            fighters.remove(e)
                    else:
                        print("You missed!")
                else:
                    print("Someone fucked up somewhere.")
                sleep(0.8)
            except:
                pass
        enemycount = len(fighters) - 1
        if enemycount <= 0:
            in_combat = False

    
    if died:
        msg = "player_died"
        in_combat = False
    elif enemycount <= 0:
        in_combat = False
        print("All targets have been eliminated!")
        msg = "victory"
    else:
        pass
    
    return msg
        


# p_bob.set_itv(13)
# combat([player, p_bob, p_lisa, p_sbot])