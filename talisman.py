'''
Talisman v0.2

Roadmap:
Places
Objects
Followers
Purchases
Sentinel

initialized in trinket.io
known bugs:
fate reroll mechanic
paying off Bandit
'''

# region: Initalization
import random as r # Random Module

error="\nUh, I'm not quite sure what that means. Please try again: " # Error Prompt
implem="Unfortunately this feature has not yet been implemented." # Implementation Error Prompt

# Outer Region Board
outer=("Tavern","Southwestern Fields","Ruins","Western Plains","Forest","Northwestern Fields","Village","Northern Fields","Graveyard","Northern Woods","Sentinel Space","Northern Hills","Chapel","Northeastern Fields","Crags","Eastern Plains","Eastern Woods","Southeastern Fields","City","Southern Fields","Southern Hills","Midsouthern Plains","Southern Woods","Southeastern Plains")

# Adventure Cards
adventures = ["Angel","Blizzard","Book of Spells","Devil","Evil Darkness","Imp","Magical Vortex","Market Day","Mephistopheles","Pestilence","Raiders","Siren","Storm","Wolf","Ape","Bear","Lion","Serpent","Giant","Spectre","Demon","Enchanter","Fairy","Healer","Hermit","Mage","Phantom","Sorcerer","Witch","Alchemist","Cursed by a Hag","Gnome","Maiden","Mercenary","Mule","Pixie","Poltergeist","Prince","Princess","Unicorn","Amulet","Cross","Holy Grail","Magic Belt","Orb of Knowledge","Potion of Strength","Ring","Solomon's Crown","Wand","Holy Lance","Runesword","Raft","Water Bottle","Armour","Helmet","Shield","Axe","Cave","Fountain of Wisdom","Magic Portal","Magic Stream","Market","Marsh","Maze","Pool of Life","Shrine"]+["Wild Boar","Goblin","Hobgoblin","Bandit","Ogre","Lemure","Shadow","Ghost","Wraith","Guide","Talisman","Sword"]*2+["Dragon","Two Bags of Gold"]*3+["Bag of Gold"]*8
events = ["Angel","Blizzard","Book of Spells","Devil","Evil Darkness","Imp","Magical Vortex","Market Day","Mephistopheles","Pestilence","Raiders","Siren","Storm"]
animals = ["Wild Boar","Wolf","Ape","Bear","Lion","Serpent"]
dragons = ["Dragon"]
monsters = ["Goblin","Hobgoblin","Bandit","Ogre","Giant"]
spirits = ["Lemure","Shadow","Spectre","Ghost","Wraith","Demon"]
enemies = animals + dragons + monsters + spirits
strangers = ["Enchanter","Fairy","Healer","Hermit","Mage","Phantom","Sorcerer","Witch"]
followers = ["Alchemist","Cursed by a Hag","Gnome","Guide","Maiden","Mercenary","Mule","Pixie","Poltergeist","Prince","Princess","Unicorn"]
objects = ["Amulet","Cross","Holy Grail","Magic Belt","Orb of Knowledge","Potion of Strength","Ring","Solomon's Crown","Talisman","Wand","Holy Lance","Runesword","Bag of Gold","Raft","Two Bags of Gold","Water Bottle","Armour","Helmet","Shield","Axe","Sword"]
magicobjects = ["Amulet","Cross","Holy Grail","Magic Belt","Orb of Knowledge","Potion of Strength","Ring","Solomon's Crown","Talisman","Wand","Holy Lance","Runesword"]
weapons = ["Holy Lance","Runesword","Axe","Sword"]
armours = ["Armour","Helmet","Shield","Axe","Sword"]

# Character Template
emptydict={
    "name":"",
    "start":"",
    "align":"",
    "strength":0,
    "craft":0,
    "life":0,
    "fate":0,
    "gold":1,
    "addinfo":"",
    "space":"",
    "mins":0,
    "minc":0,
    "maxl":0,
    "maxf":0
}

# Cards on Spaces
spacedict={}
for space in outer:
    spacedict.update({space:[]})

# Dice Rolling
def roll():
    return r.choice(range(1,7))

# Game Over
def gameover():
    print("\nSorry, but that's the whole game at the moment. Check again later, more coming soon! In the meantime, check out your stats: ")
    print("Strength: {strength}\nCraft: {craft}\nGold: {gold}\nFate: {fate}\nLife: {life} \nAlignment: {align}".format(**chardict))
    quit()
#endregion

# region: Player functions
# Lose Life
def wound():
    chardict["life"]-=1
    if chardict["life"]<=0:
        print("Sorry, you have died. GAME OVER")
        gameover()
# Heal Life
def heal(n):
    if chardict["life"]+n<=chardict["maxl"]:
        chardict["life"]+=n
        if chardict["life"]>=chardict["maxl"]:
            chardict["life"]=chardict["maxl"]
            print("You are now at max life.")
    else:
        print("Sorry, you are already at max life.")
# Lose Gold
def poor(n):
    if chardict["gold"]-n>0:
        chardict["gold"]-=n
    else:
        chardict["gold"]=0
        print("You are now bankrupt.")
# Lose Strength
def weak():
    if chardict["strength"]>chardict["mins"]:
        chardict["strength"]+=1
    else:
        print("Your strength is already at its minimum.")
# Lose Craft
def dumb():
    if chardict["craft"]>chardict["minc"]:
        chardict["craft"]+=1
    else:
        print("Your craft is already at its minimum.")
# Lose Fate
def losefate():
    if chardict["fate"]>1:
        chardict["fate"]-=1
    else:
        print("Your have no fate left.")
# Replenish Fate
def replenish():
    if chardict["fate"]>=chardict["maxf"]:
        print("You are already at max fate.")
    else:
        chardict["fate"] = chardict["maxf"]
# Change Alignment
def realign(new):
    if chardict["align"] != new: chardict["align"] = new
    else: print("You were already {align}.".format(**chardict))
#endregion

# region: Turns and battles
# Game Turn
def turn():
    x=roll()
    while True:
        side=input("Would you like to move to the {} (1) or the {} (2)? ".format(outer[(outer.index(chardict["space"])+x)%len(outer)],outer[(outer.index(chardict["space"])-x)%len(outer)]))
        if side=="1":
            chardict["space"]=outer[(outer.index(chardict["space"])+x)%len(outer)]
            print("\nYou are at the {space}.".format(**chardict))
            encounter()
            break
        elif side=="2":
            chardict["space"]=outer[(outer.index(chardict["space"])-x)%len(outer)]
            print("\nYou are at the {space}.".format(**chardict))
            encounter()
            break
        else:
            print(error)
# Battles
def battle(name,strength):
    charattack = roll() + chardict["strength"]
    print(f"Your attack score is {charattack}.")
    enemyattack = roll() + strength
    print(f"The {name}'s attack score is {enemyattack}.")
    while chardict["fate"] > 0:
        reroll = input("Would you like to reroll for 1 fate(Y/N)? ")
        if reroll=="Y":
            charattack = roll() + chardict["strength"]
            print(f"Your attack score is {charattack}.")
            losefate()
            break
        elif reroll=="N": break
        else: print(error)
    if charattack > enemyattack:
        print(f"You have killed the {name}.")
        return 1
    elif charattack < enemyattack:
        print(f"You have been defeated by the {name}.")
        wound()
        return -1
    else:
        print(f"You have reached a stand-off with the {name}.")
        return 0
# Psychic Combat
def psychic(name,craft):
    charattack = roll() + chardict["craft"]
    print(f"Your attack score is {charattack}.")
    enemyattack = roll() + craft
    print(f"The {name}'s attack score is {enemyattack}.")
    while chardict["fate"] > 0:
        reroll = input("Would you like to reroll for 1 fate(Y/N)? ")
        if reroll=="Y":
            charattack = roll() + chardict["craft"]
            print(f"Your attack score is {charattack}.")
            losefate()
            break
        elif reroll=="N": break
        else: print(error)
    if charattack > enemyattack:
        print(f"You have killed the {name}.")
        return 1
    elif charattack < enemyattack:
        print(f"You have been defeated by the {name}.")
        wound()
        return -1
    else:
        print(f"You have reached a stand-off with the {name}.")
        return 0
#endregion

# Adventures
def adventure(card = None, prior = False):
    if card == None:
        card = r.choice(adventures)

    if card=="Wild Boar":
        print("There is a Wild Boar roaming this area.")
        result = battle("Wild Boar",1)
    elif card=="Wolf":
        print("A vicious Wolf now dwells this area.")
        result = battle("Wolf",2)
    elif card=="Ape":
        print("A savage Ape is terrorising this area.")
        result = battle("Ape",3)
    elif card=="Bear":
        print("A ferocious Bear is running amok in this area.")
        result = battle("Bear",3)
    elif card=="Lion":
        print("A Lion is preying on everything in this area.")
        result = battle("Lion",3)
    elif card=="Serpent":
        print("A Serpent has made its home in this area.")
        result = battle("Serpent",4)
    elif card=="Dragon":
        print("A fearsome Dragon is terrorising this area.")
        result = battle("Dragon",7)
    elif card=="Goblin":
        print("A Goblin is laying waste to this area.")
        result = battle("Goblin",2)
    elif card=="Hobgoblin":
        print("A brutal Hobgoblin is stalking this area.")
        result = battle("Hobgoblin",3)
    elif card=="Bandit":
        print("A Bandit is marauding in this area. He will not attack if you pay 1 gold. He will remain here until he is killed.")
        if chardict["gold"] > 0:
            while True:
                payment = input("Do you wish to pay the bandit off(Y/N)? ")
                if payment=="Y":
                    poor(1)
                    print("You have paid the bandit off.")
                    break
                elif payment=="N":
                    break
                else:
                    print(error)
        result = battle("Bandit",4)
    elif card=="Ogre":
        print("An Ogre has decided this area is easy pickings.")
        result = battle("Ogre",5)
    elif card=="Giant":
        print("An immense Giant has set up residence in this area.")
        result = battle("Giant",6)
    elif card=="Lemure":
        print("This lowly creature from the Underworld pounces at you from the shadows.")
        result = psychic("Lemure",1)
    elif card=="Shadow":
        print("A Shadow is lurking in the dark corners of this area.")
        result = psychic("Shadow",2)
    elif card=="Spectre":
        print("A Spectre has appeared in this area.")
        result = psychic("Spectre",3)
    elif card=="Ghost":
        if "Ghost" in spacedict[chardict["space"]]:
            print("A Ghost haunts this area.")
            result = psychic("Ghost",4)
        else:
            place = r.choice(("City","Village","Graveyard","Chapel","Castle"))
            print(f"A Ghost materialises in the {place}. It now haunts this area and will remain until it is killed.")
            spacedict[place].append("Ghost")
            result = 1
    elif card=="Wraith":
        print("A Wraith is wreaking havoc in this area.")
        result = psychic("Wraith",5)
    elif card=="Demon":
        print("A Demon has appeared from the underworld to cause chaos in this area.")
        result = psychic("Demon",10)
    elif card=="Angel":
        print("An Angel has arrived.")
        if chardict["align"]=="Good":
            print("Gain 1 Life.")
            chardict["life"]+=1
        elif chardict["align"]=="Evil":
            print("Lose 1 Life.")
            wound()
        else:
            print("Nothing happens.")
        result = 1
    elif card=="Blizzard":
        print("Winter has come with a vengeance and a Blizzard envelops the land. For two rounds, all characters, no matter what Region they are in, may only move one space per turn. The Blizzard then abates to the discard pile. "+implem)
        result = 1
    elif card=="Book of Spells":
        print("You have found the fabled Book of Spells. You gain your full complement of Spells, according to your current Craft. "+implem)
        result = 1
    elif card=="Devil":
        print("You are visited by a Devil.")
        if chardict["align"]=="Good":
            print("Lose 1 Life.")
            wound()
        elif chardict["align"]=="Evil":
            print("Gain 1 Life.")
            chardict["life"]+=1
        else:
            print("Nothing happens.")
        result = 1
    elif card=="Evil Darkness":
        print("An Evil Darkness from the nether worlds sweeps the land. An Evil Darkness from the nether worlds sweeps the land. All characters except those of evil alignment must miss one turn. "+implem)
        result = 1
    elif card=="Imp":
        place = r.choice(("Crags","Forest","Tavern","Ruins")) # Add Hidden Valley and Cursed Glade
        print(f"You meet a mischievous Imp. He teleports you to the {place}.")
        chardict["space"] = place
        result = 1
    elif card=="Magical Vortex":
        print("A Magical Vortex absorbs all Spells from every character. "+implem)
        result = 1
    elif card=="Market Day":
        print("It's Market Day across the land. You may buy: a Sword (1G), a Helmet (1G), a Mule (2G), a Shield (2G), a Water Bottle (1G), or a Raft (3G). "+implem)
        result = 1
    elif card=="Mephistopheles":
        print("You have been encountered by Mephistopheles on a mission to this land.")
        if chardict["align"]=="Evil":
            print("Gain 1 Craft.")
            chardict["craft"]+=1
        else:
            print("You become Evil.")
            realign("Evil")
        result = 1
    elif card=="Pestilence":
        print("Pestilence has befouled this Region.")
        wound()
        result = 1
    elif card=="Raiders":
        print("A band of Raiders attacks you and steals all your gold. They immediately stash the gold at the Oasis and retreat to their hide-out. Note: The Oasis has not yet been implemented.") # Add gold to Oasis
        chardict["gold"] = 0
        result = 1
    elif card=="Siren":
        print("A Siren's song can be heard throughout the Region. "+implem) # All characters in Region miss 1 Turn
        result = 1
    elif card=="Storm":
        print("A Storm sweeps through this Region." +implem) # All the characters in this Region must miss 1 turn.
        result = 1
    elif card=="Enchanter":
        print("An Enchanter seeks an able adventurer.")
        if chardict["craft"] < 4:
            print("You do not have enough Craft.")
            result = 0
        else:
            while True:
                enchant=input("Choose one: Gain 1 Spell (S), Gain 1 gold (G), Gain 1 Strength (S2), Gain 1 Craft (C), Gain 1 Life (L), Gain 1 Fate (F), or teleport to any space in this region (T). ")
                if enchant=="S":
                    print(implem)
                    break
                if enchant=="G":
                    print("Gain 1 gold.")
                    chardict["gold"]+=1
                    break
                if enchant=="S2":
                    print("Gain 1 Strength.")
                    chardict["strength"]+=1
                    break
                if enchant=="C":
                    print("Gain 1 Craft.")
                    chardict["craft"]+=1
                    break
                if enchant=="L":
                    print("Gain 1 Life.")
                    chardict["life"]+=1
                    break
                if enchant=="F":
                    print("Gain 1 fate.")
                    chardict["fate"]+=1
                    break
                if enchant=="T":
                    options = list(enumerate(outer,1))
                    while True:
                        place = input("Would you like to move to the: {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), or {} ({})? ".format(*options))
                        if place in range(1,25):
                            chardict["space"] = outer[place]
                            break
                        else: print(error)
                    break
                else:
                    print(error)
        result = 1
    elif card=="Fairy":
        print("A Fairy seeks a champion.")
        if chardict["align"] != "Good":
            print("You are not Good enough.")
        else:
            while True:
                enchant=input("Choose one: Gain 1 Spell (S), Gain 1 gold (G), Gain 1 Strength (S2), Gain 1 Craft (C), Gain 1 Life (L), Gain 1 Fate (F), or teleport to any space in this region (T). ")
                if enchant=="S":
                    print(implem)
                    break
                if enchant=="G":
                    print("Gain 1 gold.")
                    chardict["gold"]+=1
                    break
                if enchant=="S2":
                    print("Gain 1 Strength.")
                    chardict["strength"]+=1
                    break
                if enchant=="C":
                    print("Gain 1 Craft.")
                    chardict["craft"]+=1
                    break
                if enchant=="L":
                    print("Gain 1 Life.")
                    chardict["life"]+=1
                    break
                if enchant=="F":
                    print("Gain 1 fate.")
                    chardict["fate"]+=1
                    break
                if enchant=="T":
                    options = list(enumerate(outer,1))
                    while True:
                        place = input("Would you like to move to the: {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), or {} ({})? ".format(*options))
                        if place in range(1,25):
                            chardict["space"] = outer[place]
                            break
                        else: print(error)
                    break
                else:
                    print(error)
        result = 1
    elif card=="Healer":
        print("A Healer has made his home here for the rest of the game. He will heal up to 2 lives per visit for any character landing here.")
        heal(2)
        result = 0
    elif card=="Hermit":
        place = r.choice(("Crags","Forest")) # Add Crypt, Plain of Peril, Cursed Glade, Oasis
        print(f"The Hermit moves to the {place}. He will give the first person to visit him there a Talisman. "+implem) # Implement
        result = 1
    elif card=="Mage":
        print("A kindly Mage has made his home here for the rest of the game. He will give one Spell per visit to each Good character landing here. "+implem)
        result = 1
    elif card=="Phantom":
        print("A Phantom will haunt this space until it has granted the first evil character to visit it one of the following wishes.")
        if chardict["align"] != "Evil":
            print("You are not Evil enough.")
        else:
            while True:
                enchant=input("Choose one: Gain 1 Spell (S), Gain 1 gold (G), Gain 1 Strength (S2), Gain 1 Craft (C), Gain 1 Life (L), Gain 1 Fate (F), or teleport to any space in this region (T). ")
                if enchant=="S":
                    print(implem)
                    break
                if enchant=="G":
                    print("Gain 1 gold.")
                    chardict["gold"]+=1
                    break
                if enchant=="S2":
                    print("Gain 1 Strength.")
                    chardict["strength"]+=1
                    break
                if enchant=="C":
                    print("Gain 1 Craft.")
                    chardict["craft"]+=1
                    break
                if enchant=="L":
                    print("Gain 1 Life.")
                    chardict["life"]+=1
                    break
                if enchant=="F":
                    print("Gain 1 fate.")
                    chardict["fate"]+=1
                    break
                if enchant=="T":
                    options = list(enumerate(outer,1))
                    while True:
                        place = input("Would you like to move to the: {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), {} ({}), or {} ({})? ".format(*options))
                        if place in range(1,25):
                            chardict["space"] = outer[place]
                            break
                        else: print(error)
                    break
                else:
                    print(error)
        result = 1
    elif card=="Sorcerer":
        print("A Sorcerer has set up shop here and will remain for the rest of the game. He sells Spells at the price of 1 gold per Spell. You may buy one Spell per visit. "+implem)
        result = 1
    elif card=="Witch":
        print("A Witch lurks in this space for the rest of the game.")
        witch = roll()
        if witch==1:
            print("Become a Toad for 3 turns. "+implem)
        elif witch==2:
            print("Lose 1 Life.")
            wound()
        elif witch==3:
            print("Gain 1 Strength.")
            chardict["strength"]+=1
        elif witch==4:
            print("Gain 1 Craft.")
            chardict["craft"]+=1
        elif witch==5:
            print("Gain 1 Spell. "+implem)
        elif witch==6:
            print("Replenish all fate.")
            replenish()
        result = 0
    elif card=="Cave":
        print("This Cave will remain here. See what you discover: ")
        cavevent = roll()
        if cavevent==1:
            print("You encounter a Dragon.")
            battle("Dragon",7)
        elif cavevent==2:
            print("You encounter a Goblin.")
            battle("Goblin",2)
        elif cavevent==3:
            print("You are lost. "+implem)
        elif cavevent==4 or cavevent == 5:
            print("Gain 2 gold.")
            chardict["gold"]+=2
        elif cavevent==6:
            print("Gain 3 gold.")
            chardict["gold"]+=3
        result = 0
    elif card=="Fountain of Wisdom":
        if prior == False:
            fountain = 4
            print("The Fountain of Wisdom is revealed. You may drink from the Fountain once per visit and gain 1 Craft. Once 4 Craft is taken, the Fountain shall vanish.")
            chardict["craft"]+=1
            fountain-=1
            result = 0
        else:
            print("You drink from the Fountain of Wisdom and gain 1 Craft.")
            chardict["craft"]+=1
            fountain-=1
            if fountain > 0:
                print(f"There are {fountain} drinks remaining.")
                result = 0
            else:
                print("The Fountain of Wisdom disappears.")
                result = 1

    else:
        print(f"You encounter a {card}. "+implem)
        result = 1
    
    if result <= 0 and prior == False:
        spacedict[chardict["space"]].append(card)
    elif result == 1 and prior == True:
        spacedict[chardict["space"]].remove(card)
    
    if result <= 0 and card in enemies:
        return 0
    else:
        return 1

# Encounters
def encounter():
    # Check if cards already exist
    count = len(spacedict[chardict["space"]])
    for i in range(count):
        encounter = adventure(spacedict[chardict["space"]][0],prior=True)
        if encounter == 0: return
    # Adventure Spaces
    if any(x in chardict["space"] for x in ["Fields","Plains","Woods","Hills","Sentinel"]):
        if count == 0:
            encounter = adventure() # Draw an Adventure card
            if encounter == 0: return
    elif chardict["space"] == "Ruins":
        for i in range(2-count):
            adventure()
    elif chardict["space"]=="Forest":
        forevent=roll()
        if forevent==1:
            print("You are attacked by a brigand.")
            result = battle("Brigand",4)
            if result <= 0: return
        elif forevent<4:
            print("You are lost. "+implem) # Miss a Turn
        elif forevent<6:
            print("You are safe.")
        elif forevent==6:
            print("A Ranger guides you out. You gain 1 Craft.")
            chardict["craft"]+=1
    elif chardict["space"]=="Crags":
        cragevent=roll()
        if cragevent==1:
            print("You are attacked by a spirit.")
            result = psychic("Spirit",4)
            if result <= 0: return
        elif cragevent<4:
            print("You are lost. "+implem) # Miss a Turn
        elif cragevent<6:
            print("You are safe.")
        elif cragevent==6:
            print("A Barbarian guides you out. Gain 1 Strength.")
            chardict["strength"]+=1
    elif chardict["space"]=="Graveyard":
        if chardict["align"]=="Good":
            print("You lose 1 Life.")
            wound()
        elif chardict["align"]=="Neutral":
            print("No effect.")
        elif chardict["align"]=="Evil":
            gravevent=roll()
            if gravevent==1:
                print("Miss 1 turn. "+implem)
            elif gravevent<5:
                print("Heal 1 Life.")
                heal(1)
            elif gravevent>=5:
                print("Gain 1 spell. "+implem)
    elif chardict["space"]=="Tavern":
        tavevent=roll()
        if tavevent==1:
            print("You get blind and drunk and collapse in a corner. "+implem) # Miss a Turn
        if tavevent==2:
            print("You get tipsy and get in a fight with a farmer.")
            result = battle("Farmer",3)
            if result <= 0: return
        if tavevent==3:
            print("You gamble and lose 1 Gold Coin.")
            poor(1)
        if tavevent==4:
            print("You gamble and win 1 Gold Coin.")
            chardict["gold"]+=1
        if tavevent==5:
            print("A wizard offers to Teleport you to an Outer Region space of your choice as your next Move. "+implem)
        if tavevent==6:
            print("A boatman offers to ferry you to the Temple as your next Move. "+implem)
    elif chardict["space"]=="Village":
        while True:
            vill=input("You may visit the Healer(H), the Blacksmith(B), or the Mystic(M): ")
            if vill=="H":
                print("The Healer will restore Lives at the cost of 1 Gold Coin each, up to your starting quota.")
                if chardict["life"]==chardict["maxl"]:
                    print("However, you are already at full health.")
                    break
                else:
                    while True:
                        med=input("How many Gold Coins would you like to pay? ")
                        if med in ["0","1","2","3","4","5"]:
                            med=int(med)
                            if med<chardict["gold"]:
                                print("You don't have that much gold.")
                                continue
                            elif med>(chardict["maxl"]-chardict["life"]):
                                print("That's too much gold, you don't need to heal that much.")
                                continue
                            else:
                                poor(med)
                                heal(med)
                                break
                        else:
                            print(error)
                break
            elif vill=="B":
                print("The Blacksmith sells the following Objects at the following prices (if available): Helmet at 2G (H), Sword at 2G (S), Axe at 2G (A), Shield at 3G (S2), Armour at 4G (A2) "+implem)
                break
            elif vill=="M":
                mystevent=roll()
                if mystevent<4:
                    print("You are ignored.")
                elif mystevent==4:
                    print("You become Good.")
                    realign("Good")
                elif mystevent==5:
                    print("Gain 1 Craft.")
                    chardict["craft"]+=1
                elif mystevent==6:
                    print("Gain 1 Spell. "+implem)
                break
            else:
                print(error)
    elif chardict["space"]=="Chapel":
        if chardict["align"]=="Evil":
            print("You lose one life.")
            wound()
        elif chardict["align"]=="Neutral":
            print("You may be Healed back up to your starting quota at the cost of 1 Gold Coin per Life. ")
            if chardict["life"]==chardict["maxl"]:
                print("However, you are already at full health.")
            else:
                while True:
                    med=input("How many Gold Coins would you like to pay? ")
                    if med in ["0","1","2","3","4","5"]:
                        med=int(med)
                        if med<chardict["gold"]:
                            print("You don't have that much gold.")
                            continue
                        elif med>(chardict["maxl"]-chardict["life"]):
                            print("That's too much gold, you don't need to heal that much.")
                            continue
                        else:
                            poor(med)
                            heal(med)
                            break
                    else:
                        print(error)
        elif chardict["align"]=="Good":
            chapevent=roll()
            if chapevent<5:
                print("You are ignored.")
            elif chapevent==5:
                print("Gain 1 Life.")
                chardict["life"]+=1
            elif chapevent==6:
                print("Gain 1 Spell. "+implem)
    elif chardict["space"]=="City":
        while True:
            cit=input("You may visit the Enchantress(E), the Doctor(D), or the Alchemist(A): ")
            if cit=="A":
                print("He will turn any of your Objects into Gold Coin. Give him your Objects and get 1 Gold Coin for each. "+implem)
                break
            elif cit=="D":
                print("He will Heal up to 2 Lives at the cost of 1 Gold Coin each.")
                if chardict["life"]==chardict["maxl"]:
                    print("However, you are already at full health.")
                    break
                else:
                    while True:
                        med=input("How many Gold Coins would you like to pay? (0, 1, or 2) ")
                        if med in ["0","1","2"]:
                            med=int(med)
                            if med<chardict["gold"]:
                                print("You don't have that much gold.")
                                continue
                            elif med>(chardict["maxl"]-chardict["life"]):
                                print("That's too much gold, you don't need to heal that much.")
                                continue
                            else:
                                poor(med)
                                heal(med)
                                break
                        else:
                            print(error)
                break
            elif cit=="E":
                enchevent=roll()
                if enchevent==1:
                    print("You are turned into a Toad for 3 turns. "+implem)
                elif enchevent==2:
                    print("Lose 1 Strength.")
                    weak()
                elif enchevent==3:
                    print("Lose 1 Craft.")
                    dumb()
                elif enchevent==4:
                    print("Gain 1 Craft.")
                    chardict["craft"]+=1
                elif enchevent==5:
                    print("Gain 1 Strength.")
                    chardict["strength"]+=1
                elif enchevent==6:
                    print("Gain 1 Spell. "+implem)
                break
            else:
                print(error)
           
    else:
        print(implem)

# region: Game
# Introduction
print("Welcome to a Python implementation of Talisman (Revised 4th Edition). In this simplified version (v), there is no winning objective. To play the game, type a letter to signal your decision when given a prompt.")
# Acknowledgement
while True:
    ack=input("Type Yes(Y) to acknowledge: ")
    if ack == "Y":
        print("\nGreat! Then let us begin.")
        break
    else:
        print(error)
# Character Setup
print("Now you need to choose which character you will enter the land of Talisman as.")
while True:
    char=input("Will you be the Assassin(A), the Druid(D), the Dwarf(D2), the Elf(E), the Ghoul(G), the Minstrel(M), the Monk(M2), the Priest(P), the Prophetess(P2), the Sorceress(S), the Thief(T), the Troll(T2), the Warrior(W), or the Wizard(W2)? ")
    if char in ["A","D","D2","E","G","M","M2","P","P2","S","T","T2","W","W2"]:
        chardict=emptydict.copy()
        if char == "A":
            chardict.update({"name":"Assassin","start":"City","align":"Evil","strength":3,"craft":3,"life":4,"fate":3})
            chardict["addinfo"]="You may assassinate when you attack a character or creature. You cannot assassinate when you are attacked by another character. When you assassinate, battle takes place as normal except that your victim may not roll a die to add to his Strength. If you win, you must force the loser to lose 1 life; you cannot take an Object or gold instead. You may not assassinate while at the Crown of Command."
        elif char=="D":
            chardict.update({"name":"Druid","start":"Forest","align":"Neutral","strength":2,"craft":4,"life":4,"fate":4})
            chardict["addinfo"]="You begin the game with one Spell. You may change your alignment at will. At any given time though, you can only be of one alignment. For example, if you are carrying the Runesword and you wish to pray at the Chapel, you must ditch the Runesword. Whenever you land on the Woods, you may gain your full complement of Spells, according to your current Craft."
        elif char == "D2":
            chardict.update({"name":"Dwarf","start":"Crags","align":"Neutral","strength":3,"craft":3,"life":5,"fate":5})
            chardict["addinfo"]="You need not roll the die in the Crags or the Chasm unless you wish to. If you choose to roll, you must accept the result. You may evade creatures and characters in the Hills. After rolling the die in the Cave, you may add 1 to the score. You need only roll 1 die if you attempt to open the Portal of Power by Craft. You need only roll 2 dice in the Mines. You are unaffected by the Maze."
        elif char == "E":
            chardict.update({"name":"Elf","start":"Forest","align":"Good","strength":3,"craft":4,"life":4,"fate":3})
            chardict["addinfo"]="You need not roll the die in the Forest unless you wish to. If you choose to roll, you must accept the result. You may evade creatures and characters in the Woods. If you are on the Woods, instead of rolling the die for your move, you may move to any other Woods in the same Region."
        elif char == "G":
            chardict.update({"name":"Ghoul","start":"Graveyard","align":"Evil","strength":2,"craft":4,"life":4,"fate":4})
            chardict["addinfo"]="When you attack another character, you may choose to make the attack psychic combat. You may not do this when you are attacked by another character. Whenever you defeat a character in psychic combat, if you choose to take one of his lives, add it to your own. When you kill an Enemy in battle, you may raise it from the dead and keep it as a Follower instead of a trophy. You may have one of your raised Followers add its Strength to yours for one battle, after which it disintegrates to the discard pile. You may only use one raised Follower per battle."
        elif char == "M":
            chardict.update({"name":"Minstrel","start":"Tavern","align":"Good","strength":2,"craft":4,"life":4,"fate":5})
            chardict["addinfo"]="Animals and Dragons will not attack you, although you may choose to attack them. If you do not attack an Animal, you may attempt to charm it. To do so, roll 1 die: if you roll higher than the Animal's Strength, it joins you as a Follower and adds its Strength to yours in battle. You may only use one charmed Animal per battle. You may take the Maiden and Princess from a character you land on."
        elif char == "M2":
            chardict.update({"name":"Monk","start":"Village","align":"Good","strength":2,"craft":3,"life":4,"fate":5})
            chardict["addinfo"]="Your inner belief allows you to add your Craft value to your Strength during battle. After rolling the die when praying, you may add 1 to the score. You may not use any Weapon or Armour during battle."
        elif char == "P":
            chardict.update({"name":"Priest","start":"Chapel","align":"Good","strength":2,"craft":4,"life":4,"fate":5})
            chardict["addinfo"]="You begin the game with one Spell. After rolling the die when praying, you may add 1 to the score. You may choose to automatically destroy any Spirits without resorting to psychic combat. When you destroy a Spirit in this manner, you may not keep the Enemy as a trophy but you may gain one Spell. You may not use any Weapon during battle."
        elif char == "P2":
            chardict.update({"name":"Prophetess","start":"Chapel","align":"Good","strength":2,"craft":4,"life":4,"fate":2})
            chardict["addinfo"]="You begin the game with one Spell. During the game, you always have at least one Spell. (Gain a Spell each time you cast your last Spell). Whenever you have to draw Adventure Cards, you may discard one card of your choice that you do not wish to encounter and draw one more card to replace it, which you must encounter. At any time during the game, you may look at the Spell Cards held by other characters."
        elif char == "S":
            chardict.update({"name":"Sorceress","start":"Graveyard","align":"Evil","strength":2,"craft":4,"life":4,"fate":3})
            chardict["addinfo"]="You begin the game with one Spell. When you attack another character, you may choose to make the attack psychic combat. You may not do this when you are attacked by another character. You may attempt to beguile a character that you land on, allowing you to take one gold or Object of your choice. To do so, roll one die: you must roll a 6 to beguile a good character; 5 or 6 for a neutral character; or a 4, 5, or 6 for an evil character. You may take any one Follower, except the Maiden, Unicorn, or Princess from a character that you land on."
        elif char == "T":
            chardict.update({"name":"Thief","start":"City","align":"Neutral","strength":3,"craft":3,"life":4,"fate":2})
            chardict["addinfo"]="You may take one gold or Object of your choice from a character that you land on. Whenever you visit the Market, Market Day, or Village you may take one card of your choice from the Purchase deck for free."
        elif char == "T2":
            chardict.update({"name":"Troll","start":"Crags","align":"Neutral","strength":6,"craft":1,"life":6,"fate":1})
            chardict["addinfo"]="You need not roll the die in the Crags unless you wish to. If you choose to roll, you must accept the result. Whenever you roll a 6 for your move, you may regenerate instead of moving. If you choose to regenerate, heal one life and your turn immediately ends."
        elif char == "W":
            chardict.update({"name":"Warrior","start":"Tavern","align":"Neutral","strength":4,"craft":2,"life":5,"fate":1})
            chardict["addinfo"]="You may roll two dice in battle and use the higher attack roll to determine your attack score. You may use two Weapons at the same time."
        elif char == "W2":
            chardict.update({"name":"Wizard","start":"Graveyard","align":"Evil","strength":2,"craft":5,"life":4,"fate":3})
            chardict["addinfo"]="You begin the game with two Spells. During the game, you always have at least one Spell. (Gain a Spell each time you cast your last Spell) When you attack another character, you may choose to make the attack psychic combat. You may not do this when you are attacked by another character."
        print("\nGood choice! You are now the {name}. You are a {align} character who starts in the {start}. You have {strength} strength, {craft} craft, {life} life, and {fate} fate. {addinfo}".format(**chardict))
        break
    else:
        print(error)
# Begin Game
while True:
    ready=input("Are you ready to proceed(Y/N)? ")
    if ready=="Y":
        print("\nThen we are ready to begin.")
        break
    elif ready=="N":
        print("\nHm, I'm sorry you don't feel ready, but I'm afraid we must proceed anyways.")
        continue
    else:
        print(error)
# Starting Setup
chardict["space"]=chardict["start"]
chardict["mins"]=chardict["strength"]
chardict["minc"]=chardict["craft"]
chardict["maxl"]=chardict["life"]
chardict["maxf"]=chardict["fate"]
print("You start at the {space}. You must now move.".format(**chardict),end=" ")

[turn() for i in range(1000)] # Game

# Conclusion
gameover()
#endregion