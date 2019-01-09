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
		self.numberOfMaps = random.randint(5,8)#for testing purposes keep between 1 and 5	
		self.emptySlots = int(self.numberOfMaps / 2) + 3
		self.genesis_location = tuple()
		print(self.genesis_location)
		########################################
		##	gamefield lists
		######
		self.makeGrid() #generates quadrant lists
		print()
		self.showGrid() #show gameMap


		#call generator function here
		#self.generateMaps()


	def generateMap(self):
		print("Number of maps to append: {}\nNumber of emptySlots: {}".format(self.numberOfMaps,self.emptySlots))
		justPlaced = self.genesis_location

		#make genesis here, it randomly appends itself
		self.genesisMap(self.player1)
		


		
	def gridLocationGenerator(self):
		print("List of quadrants: {}".format(self.list_of_quadrants))
		while self.numberOfMaps > 0:
			random_quadrant = random.choice(self.list_of_quadrants)
			random_index = random.randint(0,len(self.dict_of_quadrants[random_quadrant])-1)
			yield (random_quadrant,random_index)
			#find an available location adjacent to the previously placed map.
			#yield location	
		

	def makeGrid(self):
		numberofSlots = self.numberOfMaps + self.emptySlots
		grid_size = None #(number of lists and slots, times to append additional slots)
		leftover = None
		#determine grid parameters here
		for num in range(numberofSlots,0,-1):#from number of slots, iterate down to zero
			if num * num <= numberofSlots:
				grid_size = num
				leftover = numberofSlots - (num*num)
				#print("\n\nGrid size is:{} Leftover is: {}".format(grid_size,leftover))
				#highest num whose (num*num) result fits into numberOfSlots
				#break, because we've found the best candidate
				break

		##GRID BUILDING BELOW
		    ###basic grid here
		list_contents = ["00"]
		
		    
	def showGrid(self):
		print("\nTESTING! This is the game map")
		self.quadrants = {att:val for att,val in self.__dict__.items() if att in ["quadrant_0","quadrant_1","quadrant_2","quadrant_3","quadrant_4","quadrant_5","quadrant_6"]}
		for quadrant,slots in self.quadrants.items():
			print(quadrant,slots)




	def genesisMap(self,player1):
		random_quadrant = random.choice(self.list_of_quadrants)
		random_index = random.randint(1,len(self.dict_of_quadrants[random_quadrant])-1)
		self.dict_of_quadrants[random_quadrant].pop(random_index)
		#genesis = self.maps(map_desc.pop())
		#map.acceptplayer
		#genesis.takeItems(item.itempopulator300("Genesis"))
		#map.describeyourself
		self.dict_of_quadrants[random_quadrant].insert(random_index,"genesis")#map object
		self.genesis_location = (random_quadrant,random_index)