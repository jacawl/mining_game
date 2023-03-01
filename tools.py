from block import Block

class Tool:
    def __init__(self, durability, level, efficieny, material, name):
        self.durability = durability
        self.level = level
        self.efficiency = efficieny
        self.handle_material = material
        self.name = name
        self.mined_block = 0
    
    def use_tool(self, Block):
        self.durability -= Block.durability
        self.mined_block += 1

class Pickaxe(Tool):
    def __init__(self):
        super().__init__(1000, 1, 1, 'wood','pick-axe')

class Shovel (Tool):
    def __init__(self):
        super().__init__(1000, 1, 1, 'wood', 'shovel')
