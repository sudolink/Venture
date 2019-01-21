#the maps class

import random
import item
import player
import os
#randint for integers and uniform for floats, choice for random list picks

clearScreen = lambda: os.system('cls')

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

	def __init__(self,description,location,id_num):
		self.description = description
		self.id_num = id_num
		self.items = {} #items in area
		self.occupants = {}	#creature objects residing in map
		self.location = location
		self.visited = False
		self.hasPlayer = False
		self.adjacent_exits = {}
		self.player_name = None

	def acceptPlayer(self,player):
		self.occupants[player.name] = player
		self.player_name = player.name
		self.hasPlayer = True
		if self.visited == False:
			self.visited = True
		print("{} enters:".format(self.occupants[player.name].name))####(self.occupants[0].name) because only occupant
		self.describeYourself()

	def findPlayer(self):
		for occupant in self.occupants.items():
			print(occupant)

	def killOccupant(self,who):
		print(who.name)
		del self.occupants[who.name]

	def giveOccupant(self,playername,direction):
		if direction in self.adjacent_exits: #check whether move is valid
			try:
				self.occupants[playername] #check if present
			except:
				pass
			else:
				del self.occupants[playername]
				self.hasPlayer = False # ONLY if "playername" not in self.occupants
				return self.adjacent_exits[direction]
				#to gamefield
		pass

	def takeItems(self,items):
		if type(items) == list:
			for item in items:
				self.items[item.name_id] = item
		else:
			self.items[items.name_id] = items

	def takeOccupants(self,occ):
		if type(occ) == list:
			for occupant in occ:
				
				self.occupants[occupant.name] = occupant
		else:
			self.occupants[occupant.name] = occupant

	def describeYourself(self):
		print("\t{}".format(self.description))
		print("\nExits: {}".format(list(self.adjacent_exits.keys())))
		print("\nYou see:")
		if self.items:
			print("Items:")
			contained = {}
			for tup in self.items:
				if tup[0] not in contained:
					contained[tup[0]] = 1
				else:
					contained[tup[0]] += 1

			print("{}".format("~"*(50)))
			print("|| ", end="")
			for name,amount in contained.items():
				if amount > 1:
					print("{}x {}".format(amount,name),end=" || ")
				else:
					print("{}".format(name),end=" || ")
			print("\n{}".format("~"*(50)))
			
		else:
			print("\nThere's no items in this area.")
		if len(self.occupants) > 1:
			print("\nCreatures:")
			print("{}".format("~"*50))
			print("|| ",end="")
			for occupant in self.occupants:
				if occupant != self.player_name:
					print("{}".format(occupant),end=" || ")
			print("\n{}".format("~"*50))

	def checkForItem(self,item):
		for it in self.items:
			if it[0] == item.capitalize():
				return it

		return False

	def checkForOccupant(self,other):
		for occupant in self.occupants:
			if occupant == other:
				return self.occupants[occupant]
		return False


	def yieldItem(self,item_tuple):
		if item_tuple == "everything":
			takeables = {item_tuple:item_object for item_tuple,item_object in self.items.items() if item_object.takeable} #return dict of
			for item_tuple,item_obj in takeables.items():
				del self.items[item_tuple]
			return takeables
		else:
			give_item = self.items[item_tuple]
			if give_item.takeable:
				del self.items[item_tuple]
				return give_item
			else:
				print("You can't take that!")
######################################################################################################
######################################################################################################
######################################################################################################

class gameField():
	def __init__(self,player1):
		self.player1 = player1
		self.currentMap = None #contains the coordinates of the map not the object itself
		self.numberOfMaps = random.randint(5,25)
		self.allmapcoords = [] #map coordinates
		self.allmaps = [] #map objects
		self.adjacentMaps = {}
		self.num_items_generated = 0
		self.num_occupants_generated = 0
		self.passTimeTicks = {"hunger":0,"food":0} #control for passing time function triggers, i.e. every how many player inputs
		########################################
		##	gamefield lists
		######
		self.makeGrid() #generates quadrant lists

		#self.showGrid("coords") #show gameMap

		#generate maps here
		self.generateMap()
		self.showGrid("slots")

		#testing if maps got their items
		#print("______________________________________")
		#print("\nDid the all maps get items properly?\n")
		#for x in self.allmaps:
		#	print("{}\n{}".format(x.description,[x for x in x.items.keys()]))
		#	print("")
		#print("______________________________________")


		#lastly, give player object to genesis to start the game
		self.__dict__[self.currentMap[0]][self.currentMap[1]].acceptPlayer(self.player1)

	def putPlayerIntoRandomMap(self):
		mapObj = self.fetchMapObject()
		goto = random.choice([direction for direction in mapObj.adjacent_exits.keys()])
		
		print("\nYou run {}!".format(goto))

		self.attemptTravel(mapObj,goto)

	def enterCombatLoop(self,area,who):
		who = who.capitalize()
		whoObj = area.checkForOccupant(who)
		print(whoObj)
		if whoObj:
			#enter combat loop
			print("You've entered into combat with '{}'".format(who))
			print("You can either 'attack' or try to 'run' each round.")
			while whoObj.alive(): #while combatant alive
				#loop for fight or flight
				action = None
				while action not in ["attack","run"]:
					action = str(input("Attack or run? ")).lower()
					if action not in ["attack","run"]:
						print("You can either 'run' or 'attack'!")
					else:
						break
				if action == "run":
					if random.choice([True,False]):
						print("You manage to escape!")
						self.putPlayerIntoRandomMap() #run to an adjacent room
						break
					else:
						print("You couldn't run away!")
						#get hit
				else:
					attempt = 0
					attempt -= self.player1.attemptAttack() #turn damage negative
					if attempt:
						#subtract damage from attackee
						whoObj.manageHealth(-attempt,area)
					else:
						#failed to do damage
						print("Your attack missed!")
						pass
					pass
					attempt = 0
					attempt -=  whoObj.attemptAttack()
					if attempt:
						#subtract damage from player
						self.player1.manageHealth(-attempt)
					else:
						print("{}'s attack misses!".format(who))
			print("Combat ended! Your HP: {}".format(self.player1.hp))
			area.describeYourself()
		else:
			print("No '{}' around to attack!".format(who))

	def passTime(self):
		hunger_trigger = 3  #every how many turns do functions trigger
		food_trigger = 4
		#a collection of object functions that time passing should affect
		area = self.fetchMapObject()
			#player hunger
		if self.passTimeTicks["hunger"] >= hunger_trigger:
			self.player1.hungerRise()
			self.passTimeTicks["hunger"] = 0
		if self.passTimeTicks["food"] >= food_trigger:
			to_rot = []
			to_rot_inv = []
			#area
			for food in area.items:
				try:
					area.items[food].spoil()
				except:
					pass
					#print("{} can't spoil".format(food[0]))
				else:
					self.passTimeTicks["food"] = 0
				if area.items[food].durability <= 0:
					print("{} rotted away!".format(food[0]))
					to_rot.append(food)
			if to_rot:
				for food in to_rot:
					del area.items[food]
			#inventory
			for food in self.player1.inventory:
				try:
					self.player1.inventory[food].spoil()
				except:
					pass
					#print("{} can't spoil".format(food[0]))
				else:
					self.passTimeTicks["food"] = 0
				if self.player1.inventory[food].durability <= 0:
					print("{} rotted away in your inventory!".format(food[0]))
					to_rot_inv.append(food)
			if to_rot_inv:
				for food in to_rot:
					del self.player1.inventory[food]
			food_tick = 0
		#food spoilage

		self.passTimeTicks["hunger"] += 1
		self.passTimeTicks["food"] += 1

	def fetchMapObject(self,coords=None):#default is to fetch the current map object
		if coords == None:
			return self.__dict__[self.currentMap[0]][self.currentMap[1]]
		else:
			return self.__dict__[coords[0]][coords[1]]
			#THE ELSE DOESN'T WORK AS INTENDED, FIX IT

	def attemptTravel(self,area,where):
                if where.lower() in area.adjacent_exits:
                        travelto = area.giveOccupant(self.player1.name,where)
                        x = travelto[0]
                        y = travelto[1]
                        self.currentMap = self.__dict__[x][y].location
                        self.__dict__[x][y].acceptPlayer(self.player1)
                else:
                	print("There is no exit to the {}!".format(where.capitalize()))

	def fillMap(self,map_instance):
		new_items = item.itemPopulator3000(self)
		new_occupants = player.occupantGenerator4000(self)
		map_instance.takeItems(new_items)
		map_instance.takeOccupants(new_occupants)
		#populate with creatures

	def giveMapsExits(self):
		for area in self.allmaps:
			area.adjacent_exits = self.checkForAdjacent(area.location,"find_exits")
			#print(area.adjacent_exits)
	
	def generateMap(self):
		#make genesis here, it inserts itself randomly into the map matrix
		self.genesisMap("placeholder")
		#print("\nGenesis location: {}".format(self.allmapcoords[0]))

		#append other maps below
		self.numberOfMaps = int(self.numberOfMaps / 2) #to allow for empty slots in gameField.
		#print("\nMaps to append: {}".format(self.numberOfMaps))

		#run map_placement until numberofmaps is depleted
		for map_id in range(1,self.numberOfMaps+1): #genesis_id is manually set at 0
			#until map is placed, keep trying
			notPlaced = True
			while notPlaced:
				#pick a random position of row and coord in that row
				randomrow = random.choice([row for row in self.__dict__ if "row" in row])
				randomcoord = random.choice([coord for coord in self.__dict__[randomrow]])
				new_map_location = (randomrow,randomcoord)
				#are map coordinates already in use?
				if new_map_location not in self.allmapcoords:
					#check if new random coords are adjacent to any already placed map
					if self.checkForAdjacent(new_map_location,"slotfind"): 
							#then make map
						makeMap = maps(map_desc.pop(-1),new_map_location,map_id)
							#init maps here
						self.fillMap(makeMap)
							#place map in matrix
						self.__dict__[randomrow][randomcoord] = makeMap
							#put the newly used coords in the list
						self.allmapcoords.append(new_map_location)
							#put the map in a list
						self.allmaps.append(makeMap)
						#print("MAP PLACED @ {}-{}".format(randomrow,randomcoord))
						notPlaced = False
					else:
						#print("Coords not adjacent to any other map!")
						continue
				else:
					#print("Map coordinates already in use!")
					continue

		#print("\n*done appending maps*")
		self.giveMapsExits()


	def checkForAdjacent(self,location,mode="slotfind"):
		#print("\ncheckForAdjacent checks if new random position is adjacent to any existing map\n")
		#print("\nThese are all used map coordinates:\n{}".format(self.allmapcoords))
		isAdjacent = False
		nowrow = location[0]
		nowcoord = location[1]

		#THE DEFINITIONS BELOW ARE USED TO CHECK IN ALL DIRECTIONS FROM A GIVEN COORDINATE
		#all that's done here is incrementing the row or coordinate number
		#	checking row above
		rowup = "{}{}".format(nowrow[0:3], int(nowrow[3:]) + 1)
		coordup = "{}{}".format(nowcoord[0], int(nowcoord[1:]) + 1)
		north = (rowup,coordup)
		
		#	checking row below
		rowdown	= "{}{}".format(nowrow[0:3], int(nowrow[3:])-1)
		coorddown = "{}{}".format(nowcoord[0], int(nowcoord[1:])-1)
		south = (rowdown,coorddown)
		
		#	checking same row coordinates left and right
		coordleft = "{}{}".format(nowcoord[0:1], int(nowcoord[1:])-self.grid_size)  # +- gridsize is because different sized grids' adjacent
		coordright= "{}{}".format(nowcoord[0:1], int(nowcoord[1:])+self.grid_size) # coordinates have number differences of grid_size, because of the way I build in makeGrid
		east = (nowrow,coordright)
		west = (nowrow,coordleft)
		
		#	make a list of all the directions to check in
		possibleChecks = {"north":north,"south":south,"east":east,"west":west}

		if mode == "slotfind":
			for coordinates in self.allmapcoords:
				#print("Current coords to check: {}\n".format(coordinates))
				for direction, coord_tuple in possibleChecks.items():
					if coordinates == coord_tuple:
						return True
						#print("adjacent! {} - {}".format(coordinates,possible))
					else:
						isAdjacent = False
						#print("not adjacent! {} - {}".format(coordinates,possible))
			
			return isAdjacent
	
		elif mode == "find_exits":
			map_loc = (nowrow,nowcoord)
			map_adjacents = {}
			for direction, coord_tuple in possibleChecks.items():
				try:
					self.__dict__[coord_tuple[0]][coord_tuple[1]]
				except:
					#print("{} is not a map coordinate!".format((coord_tuple[0],coord_tuple[1])))
					continue
				else:
					if type(self.__dict__[coord_tuple[0]][coord_tuple[1]]) == maps :
						map_adjacents[direction] = coord_tuple
					else:
						#print("No map object @ {}".format((coord_tuple[0],coord_tuple[1])))
						pass
			return map_adjacents
		else:
			print("*** checkForAdjacent should NOT come here.")
			return False


	def makeGrid(self):
		#print("Map slots to create: {}".format(self.numberOfMaps))
		self.grid_size = None #(number of lists and slots, times to append additional slots)
		leftover = None
		#determine grid parameters here
		for num in range(self.numberOfMaps,0,-1):#from number of slots, iterate down to zero
			if num * num <= self.numberOfMaps:
				self.grid_size = num
				leftover = self.numberOfMaps - (num*num)
				#print("Grid size:{}x{} Leftover is: {}".format(num,num,leftover))

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

		coordinate_names = ["c{}".format(coordinate) for coordinate in range(self.numberOfMaps)] #list of all coordinates for this gamefield c0-c99

		row = 0 #start on row 0
		for coordinate in coordinate_names: #Goes through rows, appending leftover map slots however many times needed
			dictofrows["row{}".format(row)][coordinate] = "0"
			row +=1 #increment to next row
			if row > len(list_of_rows)-1: #when row number > number of object's row{x} attributes, reset to 0
				row = 0



	def showGrid(self,switch=None):
		print("\nTESTING! This will be the game map")
		print("Currently shows each map's ID")
		rows = {k:v for k,v in self.__dict__.items() if "row" in k}
		
		if switch == "coords":
			#this one prints keys - coordinate names
			for v in rows.values():
				print([x for x in v])
		elif switch == "slots":
			#this one prints values - coordinate contents (where the maps are inserted)
			for y in rows.values():
				print("\n") #breaks after each row  # @'s are maps, ' 's are empty slots
				for room in [x.id_num if type(x) == maps else " " for x in y.values()]:
					print("{}  ".format(room),end="")
				#print("{} \t {}".format(y,[x for x in y.values()]))
			print("\n\n")
		else:
			print("No display mode specified!")
		print()

		#for x,y in ((area.description,area.coords) for area in self.allmaps):
		#	print("{}\t{}".format(y,x))

		#SET UP AS IT IS FOR TESTING PURPOSES
		#Only show what has been explored, i.e.
		#access the map's .visited boolean




	def genesisMap(self,player1):
			#pick a completely random position for the genesis map
		randomrow = random.choice([row for row in self.__dict__ if "row" in row])
		randomcoord = random.choice([coord for coord in self.__dict__[randomrow]])
		genesis_location = (randomrow,randomcoord)
			#take a random map description, and remove it from list; tell the map where it's located
		genesis = maps(map_desc.pop(-1),genesis_location,0)
		genesis.occupants[player.randomoccupant] = player.creature(player.randomoccupant,self.num_occupants_generated)
			#if "genesis" is passed to itempopulator3k then at least one food item will be put in map
		generated_for_genesis = item.itemPopulator3000(self,None,"Genesis")
		genesis.takeItems(generated_for_genesis)
		self.__dict__[randomrow][randomcoord] = genesis
		self.allmapcoords.append(genesis_location)
		self.allmaps.append(genesis)
		self.currentMap = genesis_location