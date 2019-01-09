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
		self.dict_of_quadrants = {name:val for name,val in self.__dict__.items() if "quadrant_" in name}
		self.list_of_quadrants = [name for name in self.dict_of_quadrants]
		print()
		self.generateMap()
		self.showGrid() #show gameMap


		#call generator function here
		#self.generateMaps()


	def generateMap(self):
		print("Number of maps to append: {}\nNumber of emptySlots: {}".format(self.numberOfMaps,self.emptySlots))
		justPlaced = self.genesis_location

		#make genesis here, it randomly appends itself
		self.genesisMap(self.player1)
		
		#append maps here
		#use gridlocationgenerator to yield random locations
		#only append if location is adjacent to a map and doesn't contain a map
		for location in self.gridLocationGenerator():
			quadrant,index = location[0],location[1]
			location = self.__dict__[quadrant][index]
			if location != "map" and location != "genesis": #if location doesn't contain a map object
				if self.isAdjacentToAnyMap((quadrant,index)):
					self.__dict__[quadrant][index] = "map" #append a map new object
					self.numberOfMaps -= 1
				else:
					pass

	def isAdjacentToAnyMap(self,location):
		isAdjacent = False
		location = location
		quadrant,quadrant_num,index = location[0][0:-1],location[0][-1],location[1]


		trythese = {"quadrant_{}".format(str(int(quadrant_num)+1)):index,\
		"quadrant_{}".format(str(int(quadrant_num)-1)):index,\
		"quadrant_{}".format(quadrant_num):index+1,\
		"quadrant_{}".format(quadrant_num):index-1,\
		}#HEREIN LIES THE ISSUE TO MAP OBJECTS NOT BEING CONNECTED
		#IF AN INDEX OF 0 IS PASSED ALONG, THEN IT'S MODIFIED TO BE -1, WHICH PUTS THE LOCATION TO THE END OF THE LIST
		#IT'S STILL CONSIDEREND TO BE 'ADJACENT' SINCE LISTS CAN LOOP LIKE THAT.
		#UNHELPFUL TO MY CAUSE HOWEVER AND I'LL NEED TO FIGURE THIS OUT.
		#DREADING HAVING TO MIGRATE EVERYTHING INTO DICTIONARIES.
		
		for q,i in trythese.items():
			try:
				trie = self.__dict__[q][i]
			except:
				continue
				print("pasd")
			else:
				if trie == "map" or trie == "genesis":
					isAdjacent = True

		return isAdjacent
		
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
		for iteration in range(grid_size):#number of lists and their slots
			setattr(self,"quadrant_{}".format(iteration+1),list_contents*grid_size)
		    ###append leftover slots to basic grid below
		while leftover > 0: #while still items to append
			for pair in {k:v for k,v in self.__dict__.items() if "quadrant" in str(k)}: #if object attribute is quadrant, append a slot
				if leftover > 0: #inner check, otherwise it iterates through the whole dict even if leftover is 0
					#append slot
					self.__dict__[str(pair)].append("??")
					#one less to append
					leftover -= 1
				else:
					#nothing left to append
					pass
		    
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