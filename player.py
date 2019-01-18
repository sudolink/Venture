 # the player class

class player():
    'player class placeholder'

    def __init__(self,name="Jesus"):
        self.name = name#str(input("\nEnter player name: \n"))
        self.health = 100
        self.inventory = {}
        self.hunger = 100
        self.current_hunger = None

    def hungerRise(self):
        hunger_levels = [("starving",19),("very hungry",35),("hungry",56),("fed",70)]
        self.hunger -= 6.5
        if self.hunger <= 0:
            print("{} starved to death!".format(self.name))
            quit()
        else:
            for hunger_level in hunger_levels:
                if self.hunger <= hunger_level[1] and self.current_hunger != hunger_level[1]:
                    print("{} is {}".format(self.name,hunger_level[0]))
                    self.current_hunger = hunger_level[0]
                    break

    def destroyThing(self,other):
        del self.inventory[other]#requires item tuple

    def eat(self,area=None,meal=None):
        #if no item specified, then eat whatever is in the vicinity or inventory
        if not area:
            print("just eat whatever is available")
        else:
        #check if in map or inventory
            areaItem = area.checkForItem(meal)
            ownItem = self.checkForItem(meal)

            if self.hunger <= 99:    
                try:
                    area.items[areaItem].edible
                except:
                    try:
                        self.inventory[ownItem].edible
                    except:
                        print("You can't eat that!")
                    else:
                        eatfrominventory = self.inventory[ownItem]
                        self.hunger += eatfrominventory.nutrition
                        print("You take the {} from your inventory and eat. You're {}.".format(ownItem[0],self.current_hunger))
                        self.destroyThing(ownItem)
                else:
                    eatfrommap = area.yieldItem(areaItem)
                    print("You pick up the {} and eat. You're {}.".format(areaItem[0],self.current_hunger))
                    self.hunger += eatfrommap.nutrition
                    del eatfrommap
            else:
                print("{} is already fully fed!".format(self.name))

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
        if item in ["everything","all"]:
            tkall = area.yieldItem("everything") #returns map's whole inventory dictionary
            for it_tup, it_ob in tkall.items(): #item tuple - item object
                self.inventory[it_tup] = it_ob
                print("You put '{}' in your inventory.".format(it_ob.name))
        else:
            item_tuple = area.checkForItem(item)
            if item_tuple:
                tk = area.yieldItem(item_tuple)
                self.inventory[item_tuple] = tk
                print("You put '{}' in your inventory.".format(tk.name))
                del item_tuple,tk
            else:
                print("No '{}' around to take.".format(item))

    def drop(self,area,item):
        if item in ["everything","all","inventory"]:
            area.takeItems([obj for obj in self.inventory.values()])
            for tup,obj in self.inventory.items():
                print("You drop '{}' from your inventory.".format(obj.name))
            self.inventory.clear() #purges list contents
        else:
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
            print()
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            
        else:
            print("There's nothing in your inventory!")

#working on creatures
humanoid_names = ["Defias Pillager","Defias Rogue","Kobold digger","Kobold Protector"]
animal_names = ["Fat rat","Starving dog","Hand-sized spider","Python"]


class creature():
    'The creature class all NPCs are created from'
    def __init__(self,name):
        self.name = name
        self.hp = 100
        self.attack = 10

    def attack(self,other):
        other.hp -= self.attack
