import random

class Block:
    def __init__(self, durability, color, tool, weight, rarity, abv, name):
        self.durability = durability
        self.color = color
        self.tool = tool
        self.weight = weight
        self.rarity = rarity
        self.quality = self.set_quality()
        self.abv = abv
        self.name = name
    
    def set_quality(self):
        scale = ['worthless','low','med-low','med-high','high','perfect']
        chance = [20,47,13.5,13.5,5.5,0.5]
        results = random.choices(scale,chance,k=1)
        return(results)

class Mined(Block):
    def __init__(self):
        super().__init__(0,'black',None,0,None, '   ', 'empty')

class Stone(Block):
    def __init__(self):
        super().__init__(10,'dark_grey','pick-axe',5,'common', 'STN', 'stone')

class Dirt(Block):
    def __init__(self):
        super().__init__(5,'light_yellow','shovel',2,'common', 'DRT', 'dirt')

class Clay(Block):
    def __init__(self):
        super().__init__(8,'light_red','shovel',2,'common', 'CLY', 'clay')

class Gravel(Block):
    def __init__(self):
        super().__init__(13,'light_grey','shovel',3,'common', 'GVL', 'gravel')

class Granite(Block):
    def __init__(self):
        super().__init__(14,'white','pick-axe',6,'common','GNT', 'granite')


        