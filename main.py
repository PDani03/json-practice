import json 
import random
import os

'''
short game about going around collecting loot, but you can only carry 3 stuff at once
you can always see your inventory, and when presented with a new item, you can choose which one to discard, or to keep your 3 items
your items are saved
'''

JSONFILE="items.json"

class Item:
    def __init__(self, type, value):
        self.type=type          #0 sword / 1 shield / 2 salad
        self.value=value        #multiplier

    def types(self):
        return {
            0:"sword",
            1:"shield",
            2:"salad"}
    
    def to_dict(self): #to turn it into a json item
        return {
            "type": self.type,
            "value": self.value
        }

items=[] #currently equipped items
maxItems=3 #max amount of items allowed to be equipped

def vanItem():
    return len(items)>0

def fullItem():
    return len(items)==maxItems

def createItem():
    return Item(random.randint(0,2), random.randint(100,200)/100)

def addItem(item):
    items.append(item)

def deleteItem(index):
    if vanItem():
        return [items.pop(index),index]

def strItem(item):
    return f"{item.types()[item.type]}, with a multiplier of {item.value}"

def printItems():
    if vanItem():
        for i in range(len(items)):
            print(f"{i+1}. {strItem(items[i])}")
        
def loadData():
    try:
        with open(JSONFILE) as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}

def main():
    if not os.path.exists(JSONFILE): #make sure the file exists
        with open(JSONFILE, "w") as file:
            json.dump([], file) 
    
    data = loadData()
        
    for i in data:
        items.append(Item(i["type"],i["value"]))

    while True:
        tmpItem=createItem()
        print(f"\n\nyou see an item: {strItem(tmpItem)}\n")

        print("your items: ")
        printItems()
        print()

        
        if input("do you want the item? (y/n) ").lower()=="y":
            deletedIndex=len(items)
            while fullItem():
                inp=input("your backpack is full. do you want to delete an item to make space? (y/n) ").lower()

                if inp=="y":
                    while True:
                        try:
                            deleted,deletedIndex = deleteItem(int(input("which one? (number of item) "))-1)
                            break
                        except ValueError:
                            print("invalid input, try again")
                        except IndexError:
                            print("invalid input, try again")
                    print(f"successfully removed {strItem(deleted)}.")

                elif inp=="n":
                    break

                else:
                    print("incorrect input")
            
            if fullItem():
                print("you walk past the item.")

            else:
                input(f"you grabbed the {strItem(tmpItem)} and walked away.")
                items.insert(deletedIndex,tmpItem)
        else:
            print("you walk past the item.")
        
        itemsJSON=[item.to_dict() for item in items]

        with open(JSONFILE, "w") as file:
            json.dump(itemsJSON, file, indent = 4)


if __name__ == "__main__":
    main()

        
    
