###############################################################################
# Escape from Cave Terror                                                     #
# By: Jack Loomis                                                             #
# Latest Release: v1.1                                                        #
###############################################################################
from player import Player
from collections import OrderedDict
import world, player
import pygame

pygame.mixer.init()
pygame.mixer.music.load("background.mp3")
pygame.mixer.music.play(-1, 0.0)

def play():
    print("Escape from Cave Terror!")
    print("version 1.1.1")
    world.parse_world_dsl()
    player = Player()
    while player.is_alive() and not player.victory:
        room = world.tile_at(player.x, player.y)
        print(room.intro_text())
        room.modify_player(player)
        if player.is_alive() and not player.victory:
            choose_action(room,player)
        elif not player.is_alive():
            print("You have died! R.I.P")
        
    actions = OrderedDict()
    if player.inventory:
        actions['i'] = player.print_inventory
        actions['I'] = player.print_inventory
        print("i: View inventory")

def get_available_actions(room, player):
    actions = OrderedDict()
    print("Choose an action: ")
    if player.inventory:
        action_adder(actions, 'i', player.print_inventory, "Print inventory")
    if isinstance(room, world.TraderTile):
        action_adder(actions, 't', player.trade, "Trade")
    if isinstance(room, world.EnemyTile) and room.enemy.is_alive():
        action_adder(actions, 'a', player.attack, "Attack")
    elif isinstance(room, world.BossTile) and room.enemy.is_alive():
        action_adder(actions, 'a', player.attack, "Attack")
        action_adder(actions, 'h', player.heal, "Heal") # Allows the player to heal during the boss fight
    else:
        if world.tile_at(room.x, room.y - 1):
            action_adder(actions, 'n', player.move_north, "Go north")
        if world.tile_at(room.x, room.y + 1):
            action_adder(actions, 's', player.move_south, "Go south")
        if world.tile_at(room.x + 1, room.y):
            action_adder(actions, 'e', player.move_east, "Go east")
        if world.tile_at(room.x - 1, room.y):
            action_adder(actions, 'w', player.move_west, "Go west")
        if player.hp < 100:
            action_adder(actions, 'h', player.heal, "Heal")
        if isinstance(room, world.GambleTile):
            action_adder(actions, 'g', player.gamble, "Gamble")
        
    return actions

def action_adder(action_dict, hotkey, action, name):
    action_dict[hotkey.lower()] = action
    action_dict[hotkey.upper()] = action
    print("{}: {}".format(hotkey, name))

def choose_action(room, player):
    action = None
    while not action:
        available_actions = get_available_actions(room, player)
        action_input = input("Action: ")
        action = available_actions.get(action_input)
        if action:
            action()
        else:
            print("Invalid selection!")


play()