#items class

import random #used for giving random item tables to maps (and maybe random item stats?)

#generate nums in specified range.
inrange = lambda bottom,top: random.randint(bottom,top)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class item(object):
	def __init__(self,name,undetermined_dict_of_attributes,id_num):
		self.name_id = (name,id_num)
		self.name = self.name_id[0]
		self.setAttributes(undetermined_dict_of_attributes)
		#list of attributes not to be displayed when giveDescription is called
		self.hiddenAttributes = ("name","description","takeable","hiddenAttributes",\
			"unique","name_id")

	def setAttributes(self,undetermined_dict_of_attributes):
		for (attribute,value) in undetermined_dict_of_attributes.items():
			setattr(self,attribute,value)

	def giveDescription(self):
		#prints its own item desc,puts ~'s around it' 
		print("{}".format("~"*(len(self.description)+2)))#length of text +2 because of the ''s
		print("'{}'".format(self.description))
		print("{}".format("~"*(len(self.description)+2)))
		#checks in object's own attribute dictionary
		#excludes attributes defined in the hiddenAttributes list"
		showDict = {(k,v) for k,v in self.__dict__.items() if not k in self.hiddenAttributes}
		for pair in showDict:
			print("// {}:\t{}".format(pair[0].capitalize(),pair[1]))
			#print("{}".format("-"*(len(pair[0]+str(pair[1])*4)))) #separator?
		print("")

class food(item):

	def __init__(self,name,undetermined_dict_of_attributes,id_num):
		super(food, self).__init__(name,undetermined_dict_of_attributes,id_num)
		self.takeable = True
		self.unique = False
		self.edible = True
		try:
			self.regeneration == int
		except:
			pass
		else:
			self.regeneration = random.randint(20,55)

	def spoil(self):
		self.durability -= 11
		if self.durability <= 0:
			del self

class weapon(item):

	def __init__(self,name,undetermined_dict_of_attributes,id_num):
		super(weapon, self).__init__(name,undetermined_dict_of_attributes,id_num)
		self.unique = True
		self.takeable = True
		self.equipable = True

class tool(item):
	def __init__(self,name,undetermined_dict_of_attributes,container=False):
		super(tool, self).__init__(name,undetermined_dict_of_attributes)
		self.container = container
		if self.container == True: self.container_size = 6


###########################################################################################
##	TOOLS
##
tools = {}

###############
##	FOOD
##
food_list = ["Apple","Beef jerky"]
food_attributes = ["description","durability","nutrition","unique"]#for readability

foods = {"Apple":{"description":"A juicy red apple","durability":100,"nutrition":15,"unique":False},\
	"Beef jerky":{"description":"A chewy piece of dried beef","durability":100,"nutrition":25,"unique":False},\
	"Crickets":{"description":"A crawling bunch of crickets","durability":100,"nutrition":5,"unique":False},\
	"Banana":{"description":"A ripe, spotted banana","durability":100,"nutrition":20,"unique":False},\
	"Berries" : {"description":"A big bowl of berries","durability":100,"nutrition":13,"unique":False},\
	"Health potion": {"description":"A bottle of red liquid","durability":100,"nutrition":20,"regeneration":0},\
	}

###############
##	WEAPONS
##
weapon_list = ["Wooden dagger","Rusty sword"]
weapon_attributes = ["description","durability","attack","speed","unique"]#readability

weapons = {"Wooden dagger":{"description":"A wooden splinter resembling a dagger.","durability":100,"attack":0.2,"speed":1.0,"unique":True},\
	"Rusty sword":{"description":"A sword, encased in rust","durability":50,"attack":0.5,"speed":2.0,"unique":True},\
	"Long hammer":{"description":"A hammer with a long haft for powerful swings. It's heavy.","durability":100,"attack":2,"speed":3.3,"unique":True},\
	}

item_placeholder = dict(foods)
item_placeholder.update(weapons)
###########################################################################################

def checkItemExists(name):
	if name in foods.keys():
		return "infoods"
	elif name in weapons.keys():
		return "inweapons"
	#elif name in tools.keys():
	#	pass
	else:
		print("{} isn't in any item lists!".format(name))
		return False

def itemPopulator3000(gfield,item_limit=None,area=None):
	item_names = [name for name in foods] + [name for name in weapons]
	generated_items = []
	max_weapons_in_map = 1 #use this for controlling max numbers
	weapons_in_map = 0  #of same-type items in map
	max_food_in_map = 2
	food_in_map = 0

	if item_limit == None:
		for name in item_names: #iterate through item names
			chance = 22
			if inrange(0,100) < chance: #chance is chance out of 100
				if checkItemExists(name) == "infoods": #self explanatory
					if food_in_map < max_food_in_map: #if more food generated than allowed, do nothing
						generated_items.append(food(name,foods[name],gfield.num_items_generated))#make item from item attribute dict
						gfield.num_items_generated += 1
						food_in_map += 1
				elif checkItemExists(name) == "inweapons":
					if weapons_in_map < max_weapons_in_map:
						generated_items.append(weapon(name,weapons[name],gfield.num_items_generated))
						gfield.num_items_generated += 1
						weapons_in_map += 1
					pass
				else:
					pass

		if not generated_items and area=="Genesis": #if no items are generated, generate a food item if it's the genesis map.
			tmp = random.choice(food_list)
			generated_items.append(food(tmp,foods[tmp],gfield.num_items_generated))
			gfield.num_items_generated += 1

		return generated_items
	else:
		for num in range(item_limit):
			name = random.choice([name for name in item_placeholder.keys()])
			if checkItemExists(name) == "infoods":
				generated_items.append(food(name,foods[name],gfield.num_items_generated))
				gfield.num_items_generated += 1
			elif checkItemExists(name) == "inweapons":
				generated_items.append(weapon(name,weapons[name],gfield.num_items_generated))
				gfield.num_items_generated += 1
			else:
				print("major malfunction")
		return generated_items

