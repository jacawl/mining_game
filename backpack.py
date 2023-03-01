from block import Block

class Backpack:
    items = []
    weight = 1.111

    def __init__(self, capacity,durability, name):
        self.capacity = capacity
        self.durability = durability
        self.name = name
    
    def addItem(self, Block):
        self.items.append(Block)
        self.weight += Block.weight / 3
        self.capacity -= 1
        self.durability -= 1

class BasicBackpack(Backpack):
    def __init__(self):
        super().__init__(200, 1000, 'basic')