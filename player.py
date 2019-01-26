 # the player class
import random
import item

class player():
    'player class placeholder'

    def __init__(self,name="Jesus"):
        self.name = str(input("\nEnter player name: \n"))
        self.hp = 44
        self.inventory = {}
        self.hunger = 100
        self.current_hunger = "Well fed"
        self.equipped = {"weapon":None,"shield":None,"armor":None}
        self.attack = 40

    def attemptAttack(self):        
        #generate hitchance here
        hitchance = random.randint(48,70)
        tohit = random.randint(0,100)
        if hitchance > tohit:
            del hitchance, tohit
            if self.equipped["weapon"]: #if weapon equipped, add its damage to attack
                return -self.attack - self.equipped["weapon"].attack
            else:
                return -self.attack
        else:
            return False

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

    def manageHealth(self,adjust):
        self.hp += adjust
        if self.hp < 1:
            print("{} was mortally wounded!".format(self.name))
            quit()
        else:
            print("{} recieves {} damage. HP remaining: {}".format(self.name,abs(adjust),self.hp))


    def equipItem(self,area,item):
        equip = self.checkForItem(item)
        equippednow = False
        #determine the type of equipment
        try:
            "weapon" in str(type(self.inventory[equip]))
        except:
            print("oh oh")
        else:
            if self.equipped["weapon"] != None:
                self.take(area,self.equipped["weapon"],True)
            self.equipped["weapon"] = self.inventory[equip]
            del self.inventory[equip]
            equippednow = True

        if equippednow:
            print("You equipped '{}'".format(equip[0]))
        self.showInventory()

    def destroyThing(self,other):
        del self.inventory[other]#requires item tuple

    def eat(self,area=None,meal=None):
        hpchange = 0
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
                        hpchange += eatfrominventory.nutrition / 2
                        try:
                            eatfrominventory.regeneration == int
                        except:
                            pass
                        else:
                            hpchange += eatfrominventory.regeneration
                        self.hp += hpchange
                        print("You take the {} from your inventory and eat. You're {}.".format(ownItem[0],self.current_hunger))
                        print("You healed for {}. HP: {}".format(hpchange, self.hp))
                        self.destroyThing(ownItem)
                else:
                    eatfrommap = area.yieldItem(areaItem)
                    print("You pick up the {} and eat. You're {}.".format(areaItem[0],self.current_hunger))
                    self.hunger += eatfrommap.nutrition
                    hpchange += eatfrommap.nutrition / 2
                    try:
                        eatfrommap.regeneration == int
                    except:
                        pass
                    else:
                        hpchange += eatfrommap.regeneration
                    print("You pick up {} and eat. You're {}.".format(areaItem[0],self.current_hunger))
                    print("You healed for {}. HP: {}".format(hpchange, self.hp))
                    del eatfrommap
            else:
                print("{} is already fully fed!".format(self.name))

    def inspect(self,area = None,item = False): #item is a string, area is the maps object
        if item.lower() == "self":
            print("HP: {}".format(self.hp))
            print("Damage: {}".format(self.attack))
            print("Equipped: {}".format([equipped.name for name,equipped in self.equipped.items() if equipped != None]))
            print("Energy level: {}%".format(self.hunger))
        else:
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

    def take(self,area,item,unequipping = False):
        if item in ["everything","all"]:
            tkall = area.yieldItem("everything") #returns map's whole inventory dictionary
            for it_tup, it_ob in tkall.items(): #item tuple - item object
                self.inventory[it_tup] = it_ob
                print("You put '{}' in your inventory.".format(it_ob.name))
        else:
            if unequipping:
                for slot,obj in self.equipped.items():
                    if obj == item:
                        self.inventory[item.name_id] = item
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
        print("Equipment:")
        for equipment in self.equipped.values():
            if equipment != None:
                print(equipment.name,end=" ")
        print("\n\n")

#working on creatures
humanoid_names = ["Defias pillager","Defias rogue","Kobold digger","Kobold protector"]
animal_names = ["Fat rat","Starving dog","Hand-sized spider","Python"]

randomoccupant = random.choice(humanoid_names+animal_names)


class creature():
    'The creature class all NPCs are created from'
    def __init__(self,name,id_num):
        self.id = id_num
        self.name = name
        #print(self.name) #prints creature name on initialization
        self.hp = 88
        self.attack = 3
        self.equipped = {"weapon":None,"shield":None,"armor":None}
        self.drops = {}
        self.dead = False

    def attemptAttack(self):
        hitchance = random.randint(48,70)
        tohit = random.randint(0,100)
        if hitchance > tohit:
            del hitchance, tohit
            if self.equipped["weapon"]: #if weapon equipped, add its damage to attack
                return -self.attack - self.equipped["weapon"].attack
            else:
                return -self.attack
        else:
            return False
    def dropItems(self,areaMap):
        for dropname,drop in self.drops.items():
            areaMap.items[dropname] = drop

        if self.drops:
            print("{} dropped:".format(self.name))
            print("{}".format([x[0] for x in self.drops]))

    def alive(self):
        if self.hp >= 1:
            return True
        else:
            False

    def manageHealth(self,adjust,areaMap,gfield):
        self.hp += adjust
        if self.hp < 1:
            print("{} killed!".format(self.name))
            self.dropItems(areaMap)
            areaMap.killOccupant(self)
            gfield.num_occupants_generated -= 1
            return False
        else:
            print("{} recieves {} damage.".format(self.name,abs(adjust)))
            #drop items

def occupantGenerator4000(gfield):
    occupant_list = []
    random_occupant_num = random.randint(0,3)
    #make occupants
    while len(occupant_list) < random_occupant_num:
        creature_obj = creature(random.choice(humanoid_names+animal_names),gfield.num_occupants_generated)
        if creature_obj.name not in [occ.name for occ in occupant_list]:
            creature_items = item.itemPopulator3000(gfield,random.randint(0,2))
            creature_obj.drops = {(item.name,item.name_id):item for item in creature_items}

            occupant_list.append(creature_obj)
            gfield.num_occupants_generated += 1
    #print([occ.name for occ in occupant_list])
    return occupant_list
    #append to list
    #give occupants drops