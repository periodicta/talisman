from math import e
import random as r

error="\nUh, I'm not quite sure what that means. Please try again: " # Error Prompt
implem="Unfortunately this feature has not yet been implemented." # Implementation Error Prompt
version = "v0.1.6.1"
lastdate = "July 22, 2020"

adventures = ["Angel","Blizzard","Book of Spells","Devil","Evil Darkness","Imp","Magical Vortex","Market Day","Mephistopheles","Pestilence","Raiders","Siren","Storm","Wolf","Ape","Bear","Lion","Serpent","Giant","Spectre","Demon","Enchanter","Fairy","Healer","Hermit","Mage","Phantom","Sorcerer","Witch","Alchemist","Cursed by a Hag","Gnome","Maiden","Mercenary","Mule","Pixie","Poltergeist","Prince","Princess","Unicorn","Amulet","Cross","Holy Grail","Magic Belt","Orb of Knowledge","Potion of Strength","Ring","Solomon's Crown","Wand","Holy Lance","Runesword","Raft","Water Bottle","Armour","Helmet","Shield","Axe","Cave","Fountain of Wisdom","Magic Portal","Magic Stream","Market","Marsh","Maze","Pool of Life","Shrine"]+["Wild Boar","Goblin","Hobgoblin","Bandit","Ogre","Lemure","Shadow","Ghost","Wraith","Guide","Talisman","Sword"]*2+["Dragon","Two Bags of Gold"]*3+["Bag of Gold"]*8

def roll():
    return r.choice(range(1,7))

# region: Player Classes
# region: Player Base Class
class Player:
    # region: Player Initialization
    def __init__(self):
        self.gold = 1
        self.align = "Neutral"
        self.strength = 2
        self.craft = 4
        self.life = 4
        self.fate = 3
    
    def setup(self):
        self.minstrength = self.strength
        self.mincraft = self.craft
        self.maxlife = self.life
        self.maxfate = self.fate
        self.space = self.start
        outer.info[self.start].append(self.name)
        print("You are the {name}. {addinfo}".format(**vars(self)))

    def gameover(self):
        print(f"\nThe game is now over. Your stats were:\nStrength: {self.strength}\nCraft: {self.craft}\nLife: {self.life}\nFate: {self.fate}\nGold: {self.gold}\nAlignment: {self.align}")
        print(f"\nCurrent Game Version: {version}")
        print(f"Last Updated: {lastdate}")
        quit()
    #endregion
    
    # region: Turns and Combat
    def move(self):
        n = roll()
        current = outer.board.index(self.space)
        options = (outer.space(current+n),outer.space(current-n))
        outer.info[self.space].remove(self.name)
        while True:
            side = input("Would you like to move to the {} (1) or the {} (2)? ".format(*options))
            if side=="1":
                self.space = options[0]
                outer.info[self.space].append(self.name)
                print("\nYou are at the {space}.".format(**vars(self)))
                self.encounter()
                break
            if side=="2":
                self.space = options[1]
                outer.info[self.space].append(self.name)
                print("\nYou are at the {space}.".format(**vars(self)))
                self.encounter()
                break
            else:
                print(error)
    
    def battle(self, enemy):
        print(f"You battle the {enemy.name}.")
        charattack = self.strength + roll()
        print(f"You attack score is {charattack}.")
        enemyattack = enemy.strength + roll()
        print(f"The {enemy.name}'s attack score is {enemyattack}.")
        if self.fate > 0:
            reroll = input("Would you like to reroll for 1 fate(Y/N)? ")
            if reroll == "Y":
                charattack = self.strength + roll()
                self.loseFate()
                print(f"Your new attack score is {charattack}.")
            elif reroll == "N": pass
            else:
                print(error)
        if charattack > enemyattack:
            print(f"You have killed the {enemy.name}.")
        elif charattack < enemyattack:
            print(f"You have been defeated by the {enemy.name}.")
            self.loseLife()
        elif charattack == enemyattack:
            print(f"You have reached a standoff with the {enemy.name}.")
    def psychic(self, enemy):
        print(f"You engage in psychic combat with the {enemy.name}.")
        charattack = self.craft + roll()
        print(f"You attack score is {charattack}.")
        enemyattack = enemy.craft + roll()
        print(f"The {enemy.name}'s attack score is {enemyattack}.")
        if self.fate > 0:
            reroll = input("Would you like to reroll for 1 fate(Y/N)? ")
            if reroll == "Y":
                charattack = self.craft + roll()
                self.loseFate()
                print(f"Your new attack score is {charattack}.")
            elif reroll == "N": pass
            else:
                print(error)
        if charattack > enemyattack:
            print(f"You have killed the {enemy.name}.")
        elif charattack < enemyattack:
            print(f"You have been defeated by the {enemy.name}.")
            self.loseLife()
        elif charattack == enemyattack:
            print(f"You have reached a standoff with the {enemy.name}.")
    #endregion

    # region: Adventures
    def adventure(self):
        card = r.choice(adventures)

        if card == "Wild Boar":
            print("There is a Wild Boar romaing this area.")
            self.battle(Animal("Wild Boar",1))
        elif card == "Wolf":
            print("A vicious Wolf now dwells this area.")
            self.battle(Animal("Wolf",2))
        elif card == "Ape":
            print("A savage Ape is terrorising this area.")
            self.battle(Animal("Ape",3))
        elif card == "Bear":
            print("A ferocious Bear is runing amok in this area.")
            self.battle(Animal("Bear",3))
        elif card == "Lion":
            print("A Lion is preying on everything in this area.")
            self.battle(Animal("Lion",3))
        elif card == "Serpent":
            print("A Serpent has made its home in this area.")
            self.battle(Animal("Serpent",4))
        elif card == "Dragon":
            print("A fearson Dragon is terrorising this area.")
            self.battle(Dragon("Dragon",7))
        elif card == "Goblin":
            print("A Goblin is laying waste to this area.")
            self.battle(Monster("Goblin",2))
        elif card == "Hobgoblin":
            print("A brutal Hobgoblin is stalking this area.")
            self.battle(Monster("Hobgoblin",3))
        elif card == "Bandit":
            print("A Bandit is marauding in this area. He will not attack if you pay one gold. He will remain here until killed.")
            if self.gold == 0:
                print("However, you can't afford to pay him off.")
            else:
                while True:
                    payment = input("Do you wish to pay the bandit off(Y/N)? ")
                    if payment == "Y":
                        self.loseGold()
                        print("You have paid the bandit off.")
                        return
                    elif payment == "N":
                        break
                    else:
                        print(error)
            self.battle(Monster("Bandit",4))
        elif card == "Ogre":
            print("An Ogre has decided this area is easy pickings.")
            self.battle(Monster("Ogre",5))
        elif card == "Giant":
            print("An immense Giant has set up residence in this area.")
            self.battle(Monster("Giant",6))
        elif card == "Lemure":
            print("This lowly creature from the Underworld pounces at you from the shadows.")
            self.psychic(Spirit("Lemure",1))
        elif card == "Shadow":
            print("A Shadow is lurking in the dark corners of this area.")
            self.psychic(Spirit("Shadow",2))
        elif card == "Spectre":
            print("A Spectre has appeared in this area.")
            self.psychic(Spirit("Spectre",3))
        elif card == "Ghost":
            print(implem) # Implement: Ghost
        elif card == "Wraith":
            print("A Wraith is wreaking havoc in this area.")
            self.psychic(Spirit("Wraith",5))
        elif card == "Demon":
            print("A Demon has appeared from the underworld to cause chaos in this area.")
            self.psychic("Demon",10)
        else:
            print(f"You have encountered a {card}. "+implem) # Implement: More Adventures
    #endregion

    # region: Encounters
    def encounter(self):
        # Adventure Spaces
        if any(x in self.space for x in ["Fields","Plains","Woods","Hills","Sentinel"]):
            self.adventure()
        elif self.space == "Ruins":
            print(implem) # Implement: Adventure Spaces
        elif self.space == "Forest":
            forestEvent = roll()
            if forestEvent == 1:
                print("You are attacked by a brigand.")
                self.battle(Enemy("Brigand",4))
            elif forestEvent < 4:
                print("You are lost. "+implem) # Implement: Missing Turns
            elif forestEvent < 6:
                print("You are safe.")
            elif forestEvent == 6:
                print("A Ranger guides you out.")
                self.gainCraft()
        elif self.space == "Crags":
            cragsEvent = roll()
            if cragsEvent == 1:
                print("You are attacked by a spirit.")
                self.psychic(Spirit("Spirit",4))
            elif cragsEvent < 4:
                print("You are lost. "+implem) # Implement: Missing Turns
            elif cragsEvent < 6:
                print("You are safe.")
            elif cragsEvent == 6:
                print("A Barbarian guides you out.")
                self.gainStrength()
        elif self.space == "Graveyard":
            if self.align == "Good":
                self.loseLife()
            elif self.align == "Neutral":
                print("Nothing happens.")
            elif self.align == "Evil":
                graveyardEvent = roll()
                if graveyardEvent == 1:
                    print("Miss a turn. "+implem) # Implement: Missing Turns
                if graveyardEvent < 5:
                    self.healLife()
                elif graveyardEvent >= 5:
                    print("Gain 1 Spell. "+implem) # Implement: Spells
        elif self.space == "Tavern":
            tavernEvent = roll()
            if tavernEvent == 1:
                print("You get blind and drunk and collapse in a corner. "+implem) # Implement: Missing Turns
            if tavernEvent == 2:
                print("You get tipsy and get in a fight with a farmer.")
                self.battle(Enemy("Farmer",3))
            if tavernEvent == 3:
                print("You gamble.")
                self.loseGold()
            if tavernEvent == 4:
                print("You gamble.")
                self.gainGold()
            if tavernEvent == 5:
                print("A wizard offers to Teleport you to an Outer Region space of your choice as your next move. "+implem) # Implement: Teleportation
            if tavernEvent == 6:
                print("A boatman offers to ferry you to the Temple as your next Move. "+implem) # Implement: Middle Region
        elif self.space == "Village":
            while True:
                villageChoice = input("You may visit the Healer(H), the Blacksmith(B), or the Mystic(M): ")
                if villageChoice == "H":
                    print("The Healer will restore Lives at the cost of 1 gold each, up to your starting quota.")
                    if self.life >= self.maxlife:
                        print("However, you are already at full health.")
                        break
                    else:
                        while True:
                            healAmount = input("How many Gold Coins would you like to pay? ")
                            try:
                                healAmount = int(healAmount)
                                if healAmount < 0:
                                    print("Please input a positive integer.")
                                    continue
                            except:
                                print("Please input a positive integer.")
                                continue
                            if healAmount < self.gold:
                                print("You don't have enough gold for that.")
                                continue
                            elif healAmount > max(self.maxlife - self.life, 0):
                                print("That's too much gold, you don't need to heal that much.")
                            else:
                                self.loseGold(healAmount)
                                self.healLife(healAmount)
                                break
                    break
                elif villageChoice == "B":
                    print("The Blacksmith sells the following Objects at the following prices (if available): Helmet at 2G (H), Sword at 2G (S), Axe at 2G (A), Shield at 3G (S2), Armour at 4G (A2) "+implem) # Implement: Purchases
                    break
                elif villageChoice == "M":
                    mysticevent = roll()
                    if mysticevent < 4:
                        print("You are ignored.")
                    elif mysticevent == 4:
                        self.realign("Good")
                    elif mysticevent == 5:
                        self.gainCraft()
                    elif mysticevent == 6:
                        print("Gain 1 Spell. "+implem) # Implement: Spells
                    break
                else:
                    print(error)
        elif self.space == "Chapel":
            if self.align == "Evil":
                self.loseLife()
            elif self.align == "Neutral":
                print("You may be Healed back up to your starting quota at the cost of 1 gold per life.")
                if self.life >= self.maxlife:
                    print("However, you are already at full health.")
                else:
                    while True:
                        healAmount = input("How many Gold Coins would you like to pay? ")
                        try:
                            healAmount = int(healAmount)
                            if healAmount < 0:
                                print("Please input a positive integer.")
                                continue
                        except:
                            print("Please input a positive integer.")
                            continue
                        if healAmount < self.gold:
                            print("You don't have enough gold for that.")
                            continue
                        elif healAmount > max(self.maxlife - self.life, 0):
                            print("That's too much gold, you don't need to heal that much.")
                        else:
                            self.loseGold(healAmount)
                            self.healLife(healAmount)
                            break
            elif self.align == "Good":
                chapelevent = roll()
                if chapelevent < 5:
                    print("You are ignored.")
                elif chapelevent == 5:
                    self.gainLife()
                elif chapelevent == 6:
                    print("Gain 1 Spell. "+implem) # Implement: Spells
        elif self.space == "City":
            while True:
                cityevent = input("You may visit the Enchantress(E), the Doctor(D), or the Alchemist(A): ")
                if cityevent == "A":
                    print("He will turn any of your Objects into Gold Coin. Give him your Objects and get 1 Gold Coin for each. "+implem) # Implement: Alchemy
                elif cityevent == "D":
                    print("He will Heal up to 2 Lives at the cost of 1 Gold Coin each.")
                    if self.life >= self.maxlife:
                        print("However, you are already at full health.")
                        break
                    else:
                        while True:
                            healAmount = input("How many Gold Coins would you like to pay? ")
                            try:
                                healAmount = int(healAmount)
                                if healAmount < 0 or healAmount > 2:
                                    print("Please input an integer between 0 and 2.")
                                    continue
                            except:
                                print("Please input an integer between 0 and 2.")
                                continue
                            if healAmount < self.gold:
                                print("You don't have enough gold for that.")
                                continue
                            elif healAmount > max(self.maxlife - self.life, 0):
                                print("That's too much gold, you don't need to heal that much.")
                            else:
                                self.loseGold(healAmount)
                                self.healLife(healAmount)
                                break
                    break
                elif cityevent == "E":
                    enchantevent = roll()
                    if enchantevent == 1:
                        print("You are turned into a Toad for 3 turns. "+implem) # Implement: Missing Turns
                    elif enchantevent == 2:
                        self.loseStrength()
                    elif enchantevent == 3:
                        self.loseCraft()
                    elif enchantevent == 4:
                        self.gainCraft()
                    elif enchantevent == 5:
                        self.gainStrength()
                    elif enchantevent == 6:
                        print("Gain 1 Spell. "+implem) # Implement: Spells
                    break
                else:
                    print(error)
        else:
            print(implem)
    #endregion
                        
    # region: Player Methods
    def loseGold(self,n=1):
        if self.gold-n <= 0:
            self.gold = 0
            print("You are now bankrupt.")
        else:
            self.gold -= n
            print(f"You lose {n} gold.")
    
    def gainGold(self,n=1):
        self.gold += n
        print(f"You gain {n} gold.")
    
    def loseLife(self,n=1):
        if self.life-n <= 0:
            print("You are now dead. GAME OVER")
            self.gameover()
        else:
            self.life -= n
            print(f"You lose {n} life.")

    def healLife(self,n=1,full=False):
        if full:
            if self.life >= self.maxlife:
                pass
            else:
                self.life = self.maxlife
            print("You are at full health.")
            return
        if self.life >= self.maxlife:
            print("You are at full health.")
        elif self.life+n >= self.maxlife:
            self.life = self.maxlife
            print("You are at full health.")
        else:
            self.life += n
            print(f"You replenish {n} life.")
    
    def gainLife(self,n=1):
        self.life += n
        print(f"You gain {n} life.")
    
    def loseStrength(self,n=1):
        if self.strength-n <= self.minstrength:
            self.strength = self.minstrength
            print("Your strength is at its minimum.")
        else:
            self.strength -= n
            print(f"You lose {n} Strength.")
    
    def gainStrength(self,n=1):
        self.strength += n
        print(f"You gain {n} Strength.")
    
    def loseCraft(self,n=1):
        if self.craft-n <= self.mincraft:
            self.craft = self.mincraft
            print("Your craft is at its minimum.")
        else:
            self.craft -= n
            print(f"You lose {n} Craft.")
    
    def gainCraft(self,n=1):
        self.craft += n
        print(f"You gain {n} Craft.")

    def loseFate(self,n=1):
        if self.fate-n <= 0:
            self.fate = 0
            print("You have no fate left.")
        else:
            self.fate -= n
            print(f"You lose {n} fate.")
    
    def replenishFate(self,n=1,full=False):
        if full:
            if self.fate >= self.maxfate:
                pass
            else:
                self.fate = self.maxfate
            print("Your fate is at its maximum.")
            return
        if self.fate >= self.maxfate:
            print("Your fate is at its maximum.")
        elif self.fate+n >= self.maxfate:
            self.fate = self.maxfate
            print("Your fate is at its maximum.")
        else:
            self.fate += n
            print(f"You replenish {n} fate.")
    
    def gainFate(self,n=1):
        self.fate += n
        print(f"You gain {n} fate.")
    
    def realign(self,alignment):
        if self.align == alignment:
            print(f"You are already {alignment}.")
        else:
            print(f"You are now {alignment}.")
            self.align = alignment
    #endregion
#endregion

# region: Player Subclasses
class Assassin(Player):
    def __init__(self):
        super().__init__()
        self.name = "Assassin"
        self.start = "City"
        self.align = "Evil"
        self.strength = 3
        self.craft = 3
        self.addinfo = "You may assassinate when you attack a character or creature. You cannot assassinate when you are attacked by another character. When you assassinate, battle takes place as normal except that your victim may not roll a die to add to his Strength. If you win, you must force the loser to lose 1 life; you cannot take an Object or gold instead. You may not assassinate while at the Crown of Command."
        super().setup()

class Druid(Player):
    def __init__(self):
        super().__init__()
        self.name = "Druid"
        self.start = "Forest"
        self.addinfo = "You begin the game with one Spell. You may change your alignment at will. At any given time though, you can only be of one alignment. For example, if you are carrying the Runesword and you wish to pray at the Chapel, you must ditch the Runesword. Whenever you land on the Woods, you may gain your full complement of Spells, according to your current Craft."
        super().setup()

class Dwarf(Player):
    def __init__(self):
        super().__init__()
        self.name = "Dwarf"
        self.start = "Crags"
        self.strength = 3
        self.craft = 3
        self.life = 5
        self.fate = 5
        self.addinfo = "You need not roll the die in the Crags or the Chasm unless you wish to. If you choose to roll, you must accept the result. You may evade creatures and characters in the Hills. After rolling the die in the Cave, you may add 1 to the score. You need only roll 1 die if you attempt to open the Portal of Power by Craft. You need only roll 2 dice in the Mines. You are unaffected by the Maze."
        super().setup()

class Elf(Player):
    def __init__(self):
        super().__init__()
        self.name = "Elf"
        self.start = "Forest"
        self.align = "Good"
        self.strength = 3
        self.addinfo = "You need not roll the die in the Forest unless you wish to. If you choose to roll, you must accept the result. You may evade creatures and characters in the Woods. If you are on the Woods, instead of rolling the die for your move, you may move to any other Woods in the same Region."
        super().setup()

class Ghoul(Player):
    def __init__(self):
        super().__init__()
        self.name = "Ghoul"
        self.start = "Graveyard"
        self.align = "Evil"
        self.fate = 4
        self.addinfo = "When you attack another character, you may choose to make the attack psychic combat. You may not do this when you are attacked by another character. Whenever you defeat a character in psychic combat, if you choose to take one of his lives, add it to your own. When you kill an Enemy in battle, you may raise it from the dead and keep it as a Follower instead of a trophy. You may have one of your raised Followers add its Strength to yours for one battle, after which it disintegrates to the discard pile. You may only use one raised Follower per battle."
        super().setup()

class Minstrel(Player):
    def __init__(self):
        super().__init__()
        self.name = "Minstrel"
        self.start = "Tavern"
        self.align = "Good"
        self.fate = 5
        self.addinfo = "Animals and Dragons will not attack you, although you may choose to attack them. If you do not attack an Animal, you may attempt to charm it. To do so, roll 1 die: if you roll higher than the Animal's Strength, it joins you as a Follower and adds its Strength to yours in battle. You may only use one charmed Animal per battle. You may take the Maiden and Princess from a character you land on."
        super().setup()

class Monk(Player):
    def __init__(self):
        super().__init__()
        self.name = "Monk"
        self.start = "Village"
        self.align = "Good"
        self.craft = 3
        self.fate = 5
        self.addinfo = "Your inner belief allows you to add your Craft value to your Strength during battle. After rolling the die when praying, you may add 1 to the score. You may not use any Weapon or Armour during battle."
        super().setup()

class Priest(Player):
    def __init__(self):
        super().__init__()
        self.name = "Priest"
        self.start = "Chapel"
        self.align = "Good"
        self.fate = 5
        self.addinfo = "You begin the game with one Spell. After rolling the die when praying, you may add 1 to the score. You may choose to automatically destroy any Spirits without resorting to psychic combat. When you destroy a Spirit in this manner, you may not keep the Enemy as a trophy but you may gain one Spell. You may not use any Weapon during battle."
        super().setup()

class Prophetess(Player):
    def __init__(self):
        super().__init__()
        self.name = "Prophetess"
        self.start = "Chapel"
        self.align = "Good"
        self.fate = 2
        self.addinfo = "You begin the game with one Spell. During the game, you always have at least one Spell. (Gain a Spell each time you cast your last Spell). Whenever you have to draw Adventure Cards, you may discard one card of your choice that you do not wish to encounter and draw one more card to replace it, which you must encounter. At any time during the game, you may look at the Spell Cards held by other characters."
        super().setup()

class Sorceress(Player):
    def __init__(self):
        super().__init__()
        self.name = "Sorceress"
        self.start = "Graveyard"
        self.align = "Evil"
        self.addinfo = "You begin the game with one Spell. When you attack another character, you may choose to make the attack psychic combat. You may not do this when you are attacked by another character. You may attempt to beguile a character that you land on, allowing you to take one gold or Object of your choice. To do so, roll one die: you must roll a 6 to beguile a good character; 5 or 6 for a neutral character; or a 4, 5, or 6 for an evil character. You may take any one Follower, except the Maiden, Unicorn, or Princess from a character that you land on."
        super().setup()

class Thief(Player):
    def __init__(self):
        super().__init__()
        self.name = "Thief"
        self.start = "City"
        self.strength = 3
        self.craft = 3
        self.addinfo = "You may take one gold or Object of your choice from a character that you land on. Whenever you visit the Market, Market Day, or Village you may take one card of your choice from the Purchase deck for free."
        super().setup()

class Troll(Player):
    def __init__(self):
        super().__init__()
        self.name = "Troll"
        self.start = "Crags"
        self.strength = 6
        self.craft = 1
        self.life = 6
        self.fate = 1
        self.addinfo = "You need not roll the die in the Crags unless you wish to. If you choose to roll, you must accept the result. Whenever you roll a 6 for your move, you may regenerate instead of moving. If you choose to regenerate, heal one life and your turn immediately ends."
        super().setup()

class Warrior(Player):
    def __init__(self):
        super().__init__()
        self.name = "Warrior"
        self.start = "Tavern"
        self.strength = 4
        self.craft = 2
        self.life = 5
        self.fate = 1
        self.addinfo = "You may roll two dice in battle and use the higher attack roll to determine your attack score. You may use two Weapons at the same time."
        super().setup()

class Wizard(Player):
    def __init__(self):
        super().__init__()
        self.name = "Wizard"
        self.start = "Graveyard"
        self.align = "Evil"
        self.craft = 5
        self.addinfo = "You begin the game with two Spells. During the game, you always have at least one Spell. (Gain a Spell each time you cast your last Spell) When you attack another character, you may choose to make the attack psychic combat. You may not do this when you are attacked by another character."
        super().setup()
#endregion
#endregion

# region: Enemy Classes
class Enemy():
    def __init__(self, name, strength = None, craft = None):
        self.name = name
        if strength: self.strength = strength
        if craft: self.craft = craft

class Spirit(Enemy):
    def __init__(self, name, craft):
        super().__init__(name, craft = craft)

class Animal(Enemy):
    def __init__(self, name, strength):
        super().__init__(name, strength)

class Dragon(Enemy):
    def __init__(self, name, strength):
        super().__init__(name, strength)

class Monster(Enemy):
    def __init__(self, name, strength):
        super().__init__(name, strength)
#endregion

# region: Board
class Region:
    def __init__(self, spaces):
        self.board = []
        self.info = {}
        self.state = 1
        for space in spaces:
            self.board.append(space)
            self.info[space] = []
    
    def space(self, n):
        return self.board[n % len(outer.board)]

outer = Region(("Tavern","Southwestern Fields","Ruins","Western Plains","Forest","Northwestern Fields","Village","Northern Fields","Graveyard","Northern Woods","Sentinel Space","Northern Hills","Chapel","Northeastern Fields","Crags","Eastern Plains","Eastern Woods","Southeastern Fields","City","Southern Fields","Southern Hills","Midsouthern Plains","Southern Woods","Southeastern Plains"))
#endregion

# region: Game
print(f"Welcome to a Python implementation of Talisman (Revised 4th Edition). In this simplified version ({version}), there is no winning objective. To play the game, type a letter to signal your decision when given a prompt.")
while True:
    ack=input("Type Yes(Y) to acknowledge: ")
    if ack == "Y":
        print("\nGreat! Then let us begin.")
        break
    else:
        print(error)

print("Now you need to choose which character you will enter the land of Talisman as.")
while True:
    charchoice = input("Will you be the Assassin(A), the Druid(D), the Dwarf(D2), the Elf(E), the Ghoul(G), the Minstrel(M), the Monk(M2), the Priest(P), the Prophetess(P2), the Sorceress(S), the Thief(T), the Troll(T2), the Warrior(W), or the Wizard(W2)? ")
    if charchoice in ["A","D","D2","E","G","M","M2","P","P2","S","T","T2","W","W2"]:
        if charchoice == "A": player = Assassin()
        elif charchoice == "D": player = Druid()
        elif charchoice == "D2": player = Dwarf()
        elif charchoice == "E": player = Elf()
        elif charchoice == "G": player = Ghoul()
        elif charchoice == "M": player = Monk()
        elif charchoice == "M2": player = Minstrel()
        elif charchoice == "P": player = Priest()
        elif charchoice == "P2": player = Prophetess()
        elif charchoice == "S": player = Sorceress()
        elif charchoice == "T": player = Thief()
        elif charchoice == "T2": player = Troll()
        elif charchoice == "W": player = Warrior()
        elif charchoice == "W2": player = Wizard()
        break
    else:
        print(error)

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


for i in range(10): player.move()

player.gameover()
#endregion