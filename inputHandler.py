#input handling module

import os

clearScreen = lambda: os.system('cls')

#command list
simple_command_names = ["help","look","quit","inventory","map"]
complex_command_names = ["inspect","attack","go","take","drop","eat","equip","attack"]

def quitgame():
	dontquit = True
	while dontquit:
		print("No save feature! PROGRESS WILL BE LOST!")
		q=str(input("\nReally quit? "))
		if q.lower() == "yes":
			dontquit = False
		elif q.lower() == "no":
			clearScreen()
			return
		else:
			print("{} is not a valid response. Please answer with 'yes' or 'no'".format(q))
	quit()

def cmndlst():
    print("\n\t##+++++++++++++++++++++++++++++++++++++++++++++++")
    print("\n\t## List of usable commands ##")
    print("\n\t#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("\n\t## SIMPLE COMMANDS (need no verb)")
    print("\n\t## help - look - quit - inventory - map")
    print("\n\t##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("\n\t## COMPLEX COMMANDS (direct them at something)")
    print("\n\t## inspect - take - attack - drop - eat - go - equip")
    print("\n\t##+++++++++++++++++++++++++++++++++++++++++++++++\n\n\n")
#player input handling function
def pinp(player1,gfield):
  
    area = gfield.fetchMapObject()
    
    command_dict = {"go":gfield.attemptTravel,"look":area.describeYourself,"inspect":player1.inspect,"take":player1.take,\
        "drop":player1.drop,"help":cmndlst,"quit":quitgame,"inventory":player1.showInventory,"eat":player1.eat,"equip":player1.equipItem,\
        "attack":gfield.enterCombatLoop, "map":gfield.showGrid}


    inp = str(input("\n> ")).lower()
    clearScreen()
    #print(gfield.num_occupants_generated) #PRINT CREATURES LEFT TO KILL
    inp = validCommand(inp)
    if inp:
        #check if simple
        if type(inp) == tuple:
            #access function dict with input command
            #insert command -  insert item to interact with
            c = command_dict[inp[0]]
            c(area,inp[1])
        else:
            c = command_dict[inp]
            c()


    """
    if noun in [item.name.lower() for item in area.items.values()]:
        print("\nitem exists in the area!")
    else:
        print("\nitem doesn't exist!")
    """


def validCommand(inp): #check input for valid commands, return noun for further processing.
    for command in simple_command_names + complex_command_names:
        #print(command)
        if command == inp and command not in simple_command_names:
            print("\n'{}' needs to be directed at an object.".format(command))
            return False
        elif command in inp and command in complex_command_names:
            #strip inp of the command and spaces, leaving the noun
            noun = inp.replace(command," ").strip(" ")
            return (command,noun)
        if command == inp:
            return command

    print("\nUnknown command.")
    return False




#how can I handle an input such as 'look at rat'?
#First I have to check if one part of the input is 'look at'
#then, if it is, I have to check whether the remaining word(s) are
#indeed an item in the room or player's inventory - that the player can look at.

#how can I make that input friendly for program processing?
#return a list of the command and the remaining words
#if "look at" in inp