#the maps class

import random
import item
#randint for integers and uniform for floats, choice for random list picks

#map descriptions
map_desc = ["A cold and dark cavern","A deserted kitchen","A dusty bedroom with fresh linens on the bed",\
		"A wine cellar, with spider webs everywhere","A living room in disarray","A messy garage"]

class maps():
	'Maps have containers for items and beings. They can have effects on their occupants'

	def __init__(self, description):
		self.description = description
		self.items = {} #items in area
		self.occupants = []	#creature objects residing in map

	def acceptPlayer(self,player):
		try:
			self.occupants.append(player)
		except:
			print("Something went awry!")
		else:
			print("{} enters.".format(self.occupants[0].name))
			####this works during testing only!
			####(self.occupants[0].name) because only occupant

	def takeItems(self,items):
		if type(items) == list:
			for item in items:
				self.items[item.name] = item
		else:
			self.items[items.name] = items

	def describeYourself(self):
		print("\n{}".format(self.description))
		if self.items:
			print("\nYou see:")
			test = " // "
			for item in self.items.keys():
				test += (item+" // ")
			print("{}".format("~"*(len(test))))
			print(test)
			print("{}".format("~"*(len(test))))
		else:
			print("\nThere's nothing in this area.")

	def checkForItem(self,item):
		return item.capitalize() in self.items.keys() #does item exist - true/false

	def yieldItem(self,item):
		if self.checkForItem(item):
			if self.items[item].takeable == True: #if item has takeable property
				return self.items.pop(item)
			else:
				print("Can't take {}.".format(item))
				return
		else:
			print("No '{}' in the area".format(item))

######################################################################################################
######################################################################################################
######################################################################################################

class gameField():
	def __init__(self):
		self.player1 = None
		self.currentMap = None
		self.numberOfMaps = random.randint(5,25)
		self.genesis_location = tuple()
			#print(self.genesis_location)
		########################################
		##	gamefield lists
		######
		self.makeGrid() #generates quadrant lists
			#print()
			#self.showGrid() #show gameMap


		#call generator function here
		self.generateMap()


	def generateMap(self):
		justPlaced = self.genesis_location

		#make genesis here, it randomly appends itself
		self.genesisMap("placeholder")

		

	def makeGrid(self):
		print("{} map slots to create".format(self.numberOfMaps))
		grid_size = None #(number of lists and slots, times to append additional slots)
		leftover = None
		#determine grid parameters here
		for num in range(self.numberOfMaps,0,-1):#from number of slots, iterate down to zero
			if num * num <= self.numberOfMaps:
				grid_size = num
				leftover = self.numberOfMaps - (num*num)
				print("\nGrid size is:{}x{} Leftover is: {}".format(grid_size,grid_size,leftover))
				#highest num whose (num*num) result fits into self.numberOfMaps
				#break, because we've found the best candidate
				break

		##GRID BUILDING BELOW
		#making the object attributes
		for i in range(grid_size):
			setattr(self,"row{}".format(i),{})

		#some quality of life improvements, definitions for easier use and testing purposes below
		list_of_rows = [row for row in dir(self) if "row" in row]
		dictofrows= {k:v for k,v in self.__dict__.items() if "row" in k}
		print(list_of_rows,"\n",dictofrows)
		
		    ###full grid here
		coordinate_names = ["c{}".format(coordinate) for coordinate in range(self.numberOfMaps)] #list of all coordinates for this gamefield c0-c99
		#dictofrows["row0"]["c0"] = "placeholder"

		row = 0 #start on row 0
		for coordinate in coordinate_names:
			dictofrows["row{}".format(row)][coordinate] = "-"
			row +=1 #increment to next row
			if row > len(list_of_rows)-1: #when row number > number of object's row{x} attributes, reset to 0
				row = 0
		self.showGrid()



	def showGrid(self):
		print("\nTESTING! This will be the game map")
		rows = {k:v for k,v in self.__dict__.items() if "row" in k}
		for y in rows.values():
			print([x for x in y.values()])

		#SET UP AS IT IS FOR TESTING PURPOSES
		#YOU'LL HAVE TO MODIFY THIS TO ACCESS THE MAP OBJECT'S NAME?
		#ONLY SHOW WHAT HAS BEEN EXPLORED?




	def genesisMap(self,player1):
		genesis = maps(map_desc.pop())
		randomrow = random.choice([row for row in self.__dict__ if "row" in row])
		randomcoord = random.choice([coord for coord in self.__dict__[randomrow]])
		print("\nRandom row: {}\tRandom coord: {}".format(randomrow,randomcoord))
		maps(map_desc.pop())
		self.__dict__[randomrow][randomcoord] = genesis
		self.showGrid()
		pass