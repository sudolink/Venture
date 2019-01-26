#Venture mainloop

import maps
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
player1 = None

#TESTING PHASE
###FIGURE OUT A NICE WAY OF DOING THESE

#inputHandler.clearScreen()

#make the starting area
player1 = player.player()
gField = maps.gameField(player1)

#main loop
while True:
	inputHandler.pinp(player1,gField)
	gField.passTime()
	if gField.checkWinCondish():
		break

clearScreen()
print("\t\tCongratulations! You've won the game!")