#Venture mainloop

import game_maps
import player
import item
import inputHandler
import os

clearScreen = lambda: os.system('cls') ##for clearing the output for readability
clearScreen()
#Greetings to the player
print("\n\t~~~###*** Welcome to VENTURE!***###~~~\n\n")
#inputHandler.cmndlst() #print available commands for the first time

#Placeholders for objects when travelling occurs
visited_areas = []
area = None
player1 = None


#TESTING PHASE
###FIGURE OUT A NICE WAY OF DOING THESE

#inputHandler.clearScreen()

#make the starting area
gField = game_maps.gameField()
player1 = player.player()

quit()

#main loop
while True:
	inputHandler.pinp(player1,gField.currentMap)