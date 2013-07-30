"""Defining data for a game that uses rpgprotocol can seem tedious at first.
It is important to understand the order of dependency between the various classes."""

import random
from rpgprotocol import *

"""I optionally decided to define a few initial named values here, to make this
process easier.  The code is pretty self-explanatory at this point, as long as you
understand python.

The difference between perk points and perk credits:

Perk points are earned at every level and can be used at any time to raise stat values.

Perk credits are earned at every level and can be used at any time for in-game items.
A designer may choose to include multiple ways of allowing a character to receive perk
credits, so leveling up is just one possible way.
"""

EXPERIENCE_CURVE = [0, 500, 1500, 3000, 5000, 6500, 9500, 13000, 17000, 20500]
PERK_POINTS = [5, 3, 5, 3, 3, 5, 3, 3, 5, 15]
PERK_CREDITS = [3, 1, 2, 3, 4, 5, 5, 5, 7, 9]
BASE_STAT_MINIMUM = 5
PC_STATMOD = 0
NPC_BOSS_STATMOD = 0
NPC_MILITARY_STATMOD = -1
NPC_MILITIA_STATMOD = -2
NPC_CIVILIAN_STATMOD = -3
D100 = range(1, 100)
D20 = range(1, 20)
D12 = range(1, 12)
D10 = range(1, 10)
D8 = range(1, 8)
D6 = range(1, 6)
D4 = range(1, 4)
COIN = range(1, 2)

"""First of all, you want to define your Stat[s] that will be relevant to the game,
starting with base stats.  A base stat is the lowest level at which calculations
are done in an RPG.  This generally means you want to create base stats like strength,
dexterity, stamina, intelligence, etc.  But you can get as creative as you want and tailor
them to your designs.  Make sure you don't pass a derived_from value when instantiating
a base Stat."""

strength = Stat(value=BASE_STAT_MINIMUM, name='strength')
dexterity = Stat(value=BASE_STAT_MINIMUM, name='dexterity')
stamina = Stat(value=BASE_STAT_MINIMUM, name='stamina')
agility = Stat(value=BASE_STAT_MINIMUM, name='agility')

"""Next up is any derivative stats relevant to your game.
The best way to describe a derivative stat is to use the example of a character's total
maximum hit points.  The value assigned as hit points for characters is usually based on a
base stat such as stamina.  So you would want to pass the object for the earlier created
base Stat for stamina into the derived_from argument
for the derivative stat for max hit points.
"""

attack = Stat(value=0, name='attack', derived_from=dexterity)
maxhp = Stat(value=0, name='maxhp', derived_from=stamina)
dodge = Stat(value=0, name='dodge', derived_from=agility)

"""Derivative stats can even be derived from other derivative stats to track specific
values that can change more often."""
curhp = Stat(value=0, name='curhp', derived_from=maxhp)

"""Once you have all your stats in place, base and derivative, you want to utilize them
for one or more Skill instantiations.  The nice thing is, if you're creating a simple
adventure game or really any potential genre of a game, but you want to include
the concept of character advancement and growth, you do not need to go crazy with your
skills.  For a full-blown skill-based RPG, where everything you do is represented in
a skill that can be improved, you will probably want more skills.

Please note: rpgprotocol is capable of being extended
to allow creation of class-based RPGs, but the functionality is not there yet and is
relatively low on my list of priorities.  However, if you have any of your own ideas on
bringing that functionality in, do not hesitate to fork and send a pull request!"""

melee_values = {attack.name: attack.full_value(), maxhp.name: maxhp.full_value(), dodge.name: dodge.full_value(), curhp.name: curhp.full_value()}
melee = Skill(experience_curve=EXPERIENCE_CURVE, perk_points=PERK_POINTS, perk_credits=PERK_CREDITS, name='melee', involved_stats={attack.name: attack, maxhp.name: maxhp, dodge.name: dodge, curhp.name: curhp}, stat_values=melee_values)

"""Now with your skills in place, you can start the process of character design, and
create your entities.  An entity is any animate object in an rpgprotocol game, whether
it's player controlled or an NPC.

In this game, the player's character goes by the name of Ben (if you want the player to be
able to name their character, this is possible too, if you design a character creation
system in gamelogic.py, you would simply want to set the name field to an arbitrary value
in this file and you would just need to change the name field of the involved object as
part of your character customization logic e.g.: player.name = raw_input("What is your character's name?"))

see example.py for more information about gamelogic.py, as gamelogic.py simply loads
example.py for purposes of demonstration."""

playerexp = {melee.name: 0}
roommateexp = {melee.name: 3000}
stats = {attack.name: attack.full_value(), maxhp.name: maxhp.full_value(), dodge.name: dodge.full_value(), curhp.name: curhp.full_value()}

player = Entity(name='Ben', entity_type='PC', skills={melee.name: melee}, skillexp=playerexp, statmods=stats)

playersroommate = Entity(name='Joe', description='Current roommate and long time friend of Ben.', skills={melee.name: melee}, skillexp=roommateexp, statmods=stats, killreward=9001)

kitchenspiders = {}
for i in range(1, 5):
    kitchenspiders['spider ' + i] = Entity(name='a spider', description="One of five spiders that live in Ben and Joe's kitchen.  They would really like to get rid of them.", skills={melee.name: melee}, skillexp={melee.name: 0}, statmods=stats, killreward=75)

basementrats = {}
for i in range(1, 3):
    basementrats['rat ' + i] = Entity(name='a rat', description="One of three rats that live in Ben and Joe's basement.  They would really like to get rid of them.", skills={melee.name: melee}, skillexp={melee.name: 500}, statmods=stats, killreward=300)

troll = Entity(name='the troll', description="Some random troll that lives in Ben and Joe's backyard.  They would really like to get rid of it.", skills={melee.name: melee}. skillexp={melee.name: 1500}, statmods=stats, killreward=1500)

kitchendoor = Item(portal=Portal(leads_to='', is_from='', key_item=Item(portal=False, has_inventory=False, name="Kitchen Key")), name="kitchendoor")
backfromkitchen = Item(portal.Portal(leads_to='', is_from=''), name="backfromkitchen")
livingroom = Area({kitchendoor.name: kitchendoor}, {player.name: player, playersroommate.name: playersroommate})
kitchen = Area({backfromkitchen.name: backfromkitchen}, kitchenspiders)
livingroom.items[kitchendoor.name].portal.is_from = livingroom
livingroom.items[kitchendoor.name].portal.leads_to = kitchen
kitchen.items[backfromkitchen.name].portal.is_from = kitchen
kitchen.items[backfromkitchen.name].portal.leads_to = livingroom