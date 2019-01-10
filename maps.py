#the maps class

import random
import item
#randint for integers and uniform for floats, choice for random list picks

#map descriptions
map_desc = ["A cold and dark cavern","A deserted kitchen","A dusty bedroom with fresh linens on the bed",\
		"A wine cellar, with spider webs everywhere","A living room in disarray","A messy garage",
		"An attic, packed with old furniture","A bathroom, mirror broken on the wall","An underground tunnel",\
		"A small antechamber","A grand underground cave","A dormitory","An armory","A hall with a natural pool in the middle",\
		"A dungeon with 6 holding cells","A sunlit cave","A chapel chamber","A storage room","A room filled with webs... and spiders",\
		"A treasury room","An underground passage","A water-filled cave","A wet cavern with a stream in the middle","A clearing in the forest with a hole in the ground",\
		"A cabin in the woods","Inside the trunk of a car."]

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
		self.allmapcoords = []
		########################################
		##	gamefield lists
		######
		self.makeGrid() #generates quadrant lists

		self.showGrid("coords") #show gameMap

		#generate maps here
		self.generateMap()
		self.showGrid("slots")
	
	def generateMap(self):
		#make genesis here, it inserts itself randomly into the map matrix
		self.genesisMap("placeholder")
		print("\nGenesis location: {}".format(self.allmapcoords[0]))

		#append other maps below
		self.numberOfMaps = int(self.numberOfMaps / 2) #to allow for empty slots in gameField.
		print("\nMaps to append: {}".format(self.numberOfMaps))

		#run map_placement until numberofmaps is depleted
		for map_placement in range(self.numberOfMaps):
			#until map is placed, keep trying
			notPlaced = True
			while notPlaced:
				randomrow = random.choice([row for row in self.__dict__ if "row" in row])
				randomcoord = random.choice([coord for coord in self.__dict__[randomrow]])
				#are map coordinates already in use?
				if (randomrow,randomcoord) not in self.allmapcoords:
					#check if new random coords are adjacent to any other
					if self.checkIfAdjacent((randomrow,randomcoord)):
						#then place new map at position
						makeMap = maps(map_desc.pop(-1))
						self.__dict__[randomrow][randomcoord] = "HERE"
						self.allmapcoords.append((randomrow,randomcoord))
						print("MAP PLACED @ {}-{}".format(randomrow,randomcoord))
						notPlaced = False
					else:
						#print("Coords not adjacent to any other map!")
						continue
				else:
					#print("Map coordinates already in use!")
					continue

		print("\n*done appending maps*")


	def checkIfAdjacent(self,location):
		#print("\ncheckIfAdjacent checks if new random position is adjacent to any existing map\n")
		#print("\nThese are all used map coordinates:\n{}".format(self.allmapcoords))
		isAdjacent = False
		nowrow = location[0]
		nowcoord = location[1]

		#THE DEFINITIONS BELOW ARE USED TO CHECK IN ALL DIRECTIONS FROM A GIVEN COORDINATE
		#all that's done here is incrementing the row or coordinate number
		#	checking row above
		rowup = "{}{}".format(nowrow[0:3], int(nowrow[3:]) + 1)
		coordup = "{}{}".format(nowcoord[0], int(nowcoord[1:]) + 1)
		#	checking row below
		rowdown	= "{}{}".format(nowrow[0:3], int(nowrow[3:])-1)
		coorddown = "{}{}".format(nowcoord[0], int(nowcoord[1:])-1)
		#	checking same row coordinates left and right
		coordleft = "{}{}".format(nowcoord[0:1], int(nowcoord[1:])-self.grid_size)  # +- gridsize is because different sized grids' adjacent
		coordright= "{}{}".format(nowcoord[0:1], int(nowcoord[1:])+self.grid_size) # coordinates have number differences of grid_size, because of the way I build in makeGrid
		#	make a list of all the directions to check in
		possibleChecks = {"up":(rowup,coordup),"down":(rowdown,coorddown),"left":(nowrow,coordleft),"right":(nowrow,coordright)}

		for coordinates in self.allmapcoords:
			#print("Current coords to check: {}\n".format(coordinates))
			for direction,possible in possibleChecks.items():
				if coordinates == possible:
					return True
					#print("adjacent! {} - {}".format(coordinates,possible))
				else:
					isAdjacent = False
					#print("not adjacent! {} - {}".format(coordinates,possible))
		return isAdjacent


	def makeGrid(self):
		print("Map slots to create: {}".format(self.numberOfMaps))
		self.grid_size = None #(number of lists and slots, times to append additional slots)
		leftover = None
		#determine grid parameters here
		for num in range(self.numberOfMaps,0,-1):#from number of slots, iterate down to zero
			if num * num <= self.numberOfMaps:
				self.grid_size = num
				leftover = self.numberOfMaps - (num*num)
				print("Grid size:{}x{} Leftover is: {}".format(num,num,leftover))

				#highest num whose (num*num) result fits into self.numberOfMaps
				#break, because we've found the best candidate
				break

		##GRID BUILDING BELOW
		#making the object attributes
		for i in range(self.grid_size):
			setattr(self,"row{}".format(i),{})

		#some quality of life improvements, definitions for easier use and testing purposes below
		list_of_rows = [row for row in dir(self) if "row" in row]
		dictofrows= {k:v for k,v in self.__dict__.items() if "row" in k}

		#print(list_of_rows,"\n",dictofrows)
		
		    ###Gridmaking here
		coordinate_names = ["c{}".format(coordinate) for coordinate in range(self.numberOfMaps)] #list of all coordinates for this gamefield c0-c99
		#dictofrows["row0"]["c0"] = "placeholder"

		row = 0 #start on row 0
		for coordinate in coordinate_names:
			dictofrows["row{}".format(row)][coordinate] = "0"
			row +=1 #increment to next row
			if row > len(list_of_rows)-1: #when row number > number of object's row{x} attributes, reset to 0
				row = 0



	def showGrid(self,switch=None):
		print("\nTESTING! This will be the game map")
		rows = {k:v for k,v in self.__dict__.items() if "row" in k}
		
		if switch == "coords":
			#this one prints keys - coordinate names
			for v in rows.values():
				print([x for x in v])
		elif switch == "slots":
			#this one prints values - coordinate contents (where the maps are inserted)
			for y in rows.values():
				print("{} \t {}".format(y,[x for x in y.values()]))
		else:
			print("No display mode specified!")
		print()


		#SET UP AS IT IS FOR TESTING PURPOSES
		#YOU'LL HAVE TO MODIFY THIS TO ACCESS THE MAP OBJECT'S NAME?
		#ONLY SHOW WHAT HAS BEEN EXPLORED?




	def genesisMap(self,player1):
		genesis = maps(map_desc.pop(-1))
		randomrow = random.choice([row for row in self.__dict__ if "row" in row])
		randomcoord = random.choice([coord for coord in self.__dict__[randomrow]])
		self.__dict__[randomrow][randomcoord] = "genesis"#genesis
		self.allmapcoords.append((randomrow,randomcoord))