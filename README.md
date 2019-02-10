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




IMPLEMENTED COMMANDS:





look - gives an area's description

go [north,east,south,west] - self explanatory, move through areas

take [thing, all] - pick up something (or everything) and put it in your inventory

attack [who] - start combat loop with creature
              (in combat loop) attack - attempt to deal damage, run - attempt to run from combat
              
drop [thing, all] - drop something (or everything) from inventory to the area you're currently in

eat [thing] - eat a food item that's contained in your inventory or the current area

equip / unequip [thing] - equip an equippable item (armor,weapon), which increases your combat related stats

inspect [item] - returns an item's description and its attributes

help - print a list of commands(not updated)

inventory - print items in your inventory

quit - quit the game






FINISHED:


Stopping work on this game.
It has now become a hacky mess and has fulfilled its purpose.
I worked on this for around two weeks, figuring out how to design and make the systems in it work properly was fun and educating.
I relied on google minimally so I'm content to stop working on this and leave it as is. It's evident it's not a complete game, there aren't enough items in the game, the mobs are equally undiverse and the combat is basic. The winning scenario is also dull (kill every mob).
I learned a good deal as I worked at this, more than anything: persistance is integral in anything you want to accomplish.

I also learned how important planning the code out beforehand is. Thinking about how to approach a problem and writing it out is so damn helpful, as opposed to brute forcing the solution, the coding part then just flows. In fact, I think the most difficult part of programming is figuring out the logic of how to do something, the coding part couldn't be easier if you know the language somewhat.

I doubt anyone will ever stumble over this repo, but if they do, view it as an amateur's sojourn.
