# Venture
A text-based adventure game

A game I began working on to practice my Python skills

Rather than going through mindless practice routines focusing on narrow subjects like list comprehensions,

I thought taking on an ambitious (to present me) project would throw enough problems my way that I could solve, and get to know Python
better in the process.


The game is about exploration, combat, and loot; most aspects of it will have an element of randomness.



Some features I'm aiming to include:


The map size is to be randomly generated, within preset restraints.

The map objects themselves will automatically check adjacent map objects in the map matrix (which is a set of dictionaries for each row),
  and setup exits to those adjacent maps that the player can use to travel around.

Upon initialization, the maps are to randomly generate items with different generation chances that the player can pick up and use.

Items are currently to be of the food and weapon type.

There will be a time factor; the player's hunger will increase, impacting their health;

Combat will of course be turn-based, again with an element of randomness.

I want to have an option to save the game state so the player can quit and return to where they left off.
I will probably need to look into setting up some kind of database; I doubt it's cleanly doable with a simple text file.

The goal for now is to explore every room and survive.