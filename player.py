 # the player class


class player():
    'player class placeholder'

    def __init__(self,name="Jesus"):
        self.name = name#str(input("\nEnter player name: \n"))
        self.health = 100
        self.inventory = {}
        self.hunger = 100
        self.lookInInventory = False

    def inspect(self,area = None,item = False): #item is a string, area is the maps object
        #use map's item contain checker
        #use player's item contain checker
        #else no 'item' around
        if area.checkForItem(item):
            print("In area:\n")
            area.items[item.capitalize()].giveDescription()
        elif self.checkForItem(item):
            print("In your inventory:\n")
            self.inventory[item.capitalize()].giveDescription()
        else:
            print("\nNo '{}' around.".format(item.capitalize()))        

    def take(self,area,item):
        try:
            tk = area.yieldItem(item.capitalize())
        except:
    	    print("Can't take that.")
        else:
            if tk:
                self.inventory[tk.name]=tk
                print("'{}'' put in inventory".format(tk.name))
            del tk

    def drop(self,area,item):
    	if self.checkForItem(item):
    	    drp = self.inventory.pop(item.capitalize())
    	    area.items[drp.name] = drp
    	    print("'{}' dropped from inventory".format(drp.name))
    	    del drp
    	else:
    	    print("You don't have that item!")

    def checkForItem(self,item):
    	return item.capitalize() in self.inventory.keys()

    def showInventory(self):
        if self.inventory:
            for item in self.inventory.keys():
                print("{}".format(item),end=" || ")
            print()
        else:
            print("There's nothing in your bags.")


p = player