import random, enemies, npc, items, player

class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def intro_text(self):
        raise NotImplementedError("Create a subclass instead!")

    def modify_player(self, player):
        pass

class StartTile(MapTile):
    def intro_text(self):
        return """
        You find yourself in a cave with a flickering torch
        on the wall.
        You can make out four paths, each equally as dark
        and foreboding.
        """
###Boss Tile###
class BossTile(MapTile):
    def __init__(self, x, y):
        self.enemy = enemies.AbyssalDemon()
        self.alive_text = "The door slams shut behind you, and you " \
                          "hear a low rumbling sound. Out of the darkness, " \
                          "you see the glow of a long whip engulfed in flames. " \
                          "It's the abyssal demon!"
        self.dead_text = "The remains of the abyssal demon lie in a pile of ashes on the ground. You may just want to keep going forward..."
        super().__init__(x, y)
    
    def intro_text(self):
        if self.enemy.is_alive():
            text = self.alive_text
        else:
            text = self.dead_text
        return text

    def modify_player(self,player):
        if self.enemy.is_alive():
            player.hp = player.hp - self.enemy.damage
            print("Abyssal Demon does {} damage. You have {} HP remaining.".format(self.enemy.damage, player.hp))


class EnemyTile(MapTile): # Needs to match the list in enemies.py
    def __init__(self, x, y):
        r = random.random()
        if r < 0.50:
            self.enemy = enemies.GiantSpider()
            self.alive_text = "A giant spider jumps down from " \
                              "its web in front of you!"
            self.dead_text = "The corpose of a dead spider rots on the ground."
        elif r < 0.80:
            self.enemy = enemies.Ogre()
            self.alive_text = "An ogre is blocking your path!"
            self.dead_text = "A dead ogre reminds you of your triumph."
        elif r < 0.95:
            self.enemy = enemies.BatColony()
            self.alive_text = "You hear a squeaking noise growing louder" \
                              "...suddenly you are lost in a swarm of bats!"
            self.dead_text = "Dozens of dead bats are scattered on the ground."
        else:
            self.enemy = enemies.RockMonster()
            self.alive_text = "You've disturbed a rock monster " \
                              "from his slumber!"
            self.dead_text = "Defeated, the monster has reverted " \
                             "into an ordinary rock."

        super().__init__(x, y)


    def intro_text(self):
        if self.enemy.is_alive():
            text = self.alive_text
        else:
            text = self.dead_text
        return text

    def modify_player(self,player):
        if self.enemy.is_alive():
            player.hp = player.hp - self.enemy.damage
            print("Enemy does {} damage. You have {} HP remaining.".format(self.enemy.damage, player.hp))

    #def intro_text(self):
    #    if self.enemy.is_alive():
    #        return "A {} awaits!".format(self.enemy.name)
    #    else:
    #        return "You've defeated the {}.".format(self.enemy.name)

#The below code WORKS. This will create a chest tile "CT" on the map.
#After the chest tile is created, it will add a Rusty Sword to the player's inventory. There is no randomness to the choice here.
#Works as of 08/18/18.
class SwordChest(MapTile):
    def __init__(self, x, y):
        self.item = items.RustySword()
        self.item_claimed = False
        super().__init__(x, y)

    def modify_player(self, player):
        if not self.item_claimed:
            self.item_claimed = True
            player.inventory.append(items.RustySword()) #Add to the list player.inventory using list.append(item)
            print("{} added to inventory.".format(self.item))

    def intro_text(self):
        if self.item_claimed:
            return """
            You have already claimed the item from the chest in this room. Press onwards!
            """
        else:
            return """
            You open the chest in the middle of the room...
            """

class FindGoldTile(MapTile):
    def __init__(self, x, y):
        self.gold = random.randint(1, 50)
        self.gold_claimed = False
        super().__init__(x, y)

    def modify_player(self, player):
        if not self.gold_claimed:
            self.gold_claimed = True
            player.gold = player.gold + self.gold
            print("+{} gold added.".format(self.gold))

    def intro_text(self):
        if self.gold_claimed:
            return """
            Another unremarkable part of the cave. You must forge onwards.
            """
        else:
            return """
            Someone dropped some gold. You pick it up.
            """

###Gamble Demon Tile### 
class GambleTile(MapTile):
    def __init__(self, x, y):
        self.gambler = npc.GambleDemon()
        self.gold = 100
        self.gambled = False
        super().__init__(x, y)

    def gamble(self, player):
        r = random.random()
        if not self.gambled:
            user_input = input("Would you play to gamble? It costs 100 gold to play, but you could double your wager [y/n]: ")
            if user_input in ['y', 'Y']:
                if player.gold >= 100:
                    if r < 0.50:
                        player.gold = player.gold + self.gold
                        self.gambler.gold = self.gambler.gold - 100
                        print("You beat the gambling demon! {} gold added!".format(self.gold))
                    else:
                        player.gold = player.gold - 100
                        print("Ouch! You lost to the gambling demon. {} gold removed.".format(self.gold))
                    self.gambled = True
                else:
                    print("You don't have enough gold to gamble! Get outta here!")  
        else:
            return
        
    def intro_text(self):
        if not self.gambled:
            return """
            You notice a strange looking creature sitting in the corner of the room. He's got a menacing smile on his face,
            but seems to be harmless...

            """
        else:
            return """
            The gambling demon doesn't seem to be here anymore...
            """

class AxeChest(MapTile):
    def __init__(self, x, y):
        self.item = items.RustySword()
        self.item_claimed = False
        super().__init__(x, y)

    def modify_player(self, player):
        if not self.item_claimed:
            self.item_claimed = True
            player.inventory.append(items.Axe()) #Add to the list player.inventory using list.append(item)
            print("{} added to inventory.".format(self.item))

    def intro_text(self):
        if self.item_claimed:
            return """
            You have already claimed the item from the chest in this room. Press onwards!
            """
        else:
            return """
            You open the chest in the middle of the room...
            """


                
class TraderTile(MapTile):
    def __init__(self, x, y):
        self.trader = npc.Trader()
        super().__init__(x, y)

    def check_if_trade(self, player):
        while True:
            print("Would you like to (B)uy, (S)ell, or (Q)uit?")
            user_input = input()
            if user_input in ['Q', 'q']:
                return
            elif user_input in ['B', 'b']:
                print("Here's whats available to buy: ")
                self.trade(buyer=player, seller=self.trader)
            elif user_input in ['S', 's']:
                print("Here's whats available to sell: ")
                self.trade(buyer=self.trader, seller=player)
            else:
                print("Invalid choice!")

    def trade(self, buyer, seller):
        for i, item in enumerate(seller.inventory, 1):
            print("{}. {} - {} Gold".format(i, item.name, item.value))
        while True:
            user_input = input("Choose an item or press Q to exit: ")
            if user_input in ['Q', 'q']:
                return
            else:
                try:
                    choice = int(user_input)
                    to_swap = seller.inventory[choice -1]
                    self.swap(seller, buyer, to_swap)
                except IndexError:
                    print("Invalid choice!")


    def swap(self, seller, buyer, item):
        if item.value > buyer.gold:
            print("That's too expensive")
            return
        seller.inventory.remove(item)
        buyer.inventory.append(item)
        seller.gold = seller.gold + item.value
        buyer.gold = buyer.gold - item.value
        print("Trade complete!")
        for i, item in enumerate(seller.inventory, 1):
            print("{}. {} - {} Gold".format(i, item.name, item.value))






    def intro_text(self):
        return """
        A frail non-quite-human, not-quite-creature squats in the corner
        clinking his gold coins together. He looks willing to trade.
        """

class VictoryTile(MapTile):
    def modify_player(self, player):
        player.victory = True    

    def intro_text(self):
        return """
        You see a bright light in the distance...
        ... it grows as you get closer! It's sunlight!


        Victory is yours!"""

world_dsl = """
|EN|EN|FG|EN|EN|  |  |VT|  |  |
|EN|GT|  |  |EN|FG|  |BT|  |  |
|EN|FG|EN|  |TT|EN|EN|EN|  |GT|
|TT|  |  |FG|EN|  |  |  |  |EN|
|FG|  |EN|  |FG|EN|TT|EN|EN|FG|
|EN|AC|EN|EN|EN|  |FG|  |GT|EN|
|FG|  |EN|EN|FG|EN|EN|FG|EN|  |
|  |FG|EN|FG|EN|ST|EN|EN|FG|EN|
|  |  |  |  |SC|FG|EN|TT|  |  |
|  |  |GT|EN|EN|EN|  |  |FG|EN|
"""
def is_dsl_valid(dsl):
    if dsl.count("|ST|") != 1:
        return False
    if dsl.count("|VT|") == 0:
        return False
    lines = dsl.splitlines()
    lines = [l for l in lines if l]
    pipe_counts = [line.count("|") for line in lines]
    for count in pipe_counts:
        if count != pipe_counts[0]:
            return False
    
    return True

tile_type_dict = {"VT": VictoryTile,
                  "EN": EnemyTile,
                  "ST": StartTile,
                  "FG": FindGoldTile,
                  "TT": TraderTile,
                  "SC": SwordChest,
                  "GT": GambleTile, 
                  "BT": BossTile,
                  "AC": AxeChest,
                  #"RC": RandomChest, #Need to create class
                  "  ": None}


world_map = []

start_tile_location = None

def parse_world_dsl():
    if not is_dsl_valid(world_dsl):
        raise SyntaxError("DSL is invalid!")

    dsl_lines = world_dsl.splitlines()
    dsl_lines = [x for x in dsl_lines if x]

    for y, dsl_row in enumerate(dsl_lines):
        row = []
        dsl_cells = dsl_row.split("|")
        dsl_cells = [c for c in dsl_cells if c]
        for x, dsl_cell in enumerate(dsl_cells):
            tile_type = tile_type_dict[dsl_cell]
            if tile_type == StartTile:
                global start_tile_location
                start_tile_location = x, y
            row.append(tile_type(x, y) if tile_type else None)

        world_map.append(row)

def tile_at(x, y):
    if x < 0 or y < 0:
        return None
    try:
        return world_map[y][x]
    except IndexError:
        return None

