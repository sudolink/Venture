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
        inAreaTuple = area.checkForItem(item)
        inInventoryTuple = self.checkForItem(item)

        if inAreaTuple:
            area.items[inAreaTuple].giveDescription()
        elif inInventoryTuple:
            self.inventory[inInventoryTuple].giveDescription()
        else:
            print("No {} around.".format(item))

        del inAreaTuple,inInventoryTuple

    def take(self,area,item):
        item_tuple = area.checkForItem(item)
        if item_tuple:
            tk = area.yieldItem(item_tuple)
            self.inventory[item_tuple] = tk
            print("You put '{}' in your inventory.".format(tk.name))
        else:
            print("No '{}' around to take.".format(item))
        del item_tuple,tk

    def drop(self,area,item):
        item_tuple = self.checkForItem(item)
        if item_tuple:
            tk = self.inventory[item_tuple]
            del self.inventory[item_tuple]
            print("You drop '{}' from your inventory.".format(tk.name))
            area.takeItems(tk)
        else:
            print("No '{}' in inventory!".format(item))

    def checkForItem(self,item):
        for it in self.inventory:
            if it[0] == item.capitalize():
                return it
        return False

    def showInventory(self):
        if self.inventory:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(" || ",end="")
            for item in self.inventory:
                print("{}".format(item[0]),end=" || ")
            
        else:
            print("There's nothing in your inventory!")

p = player