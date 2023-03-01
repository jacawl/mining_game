import os
from block import *
from backpack import *
from tools import *
from chunks import *
from pynput import *
import time
import termcolor
from termcolor import cprint
import progressbar
import colorama

# to show colored text in powershell
colorama.init()

key_pressed = 'record'
on_edge = False
curr_tool = None
tool_arr = []
chunk = None
player_location = 0

def clear():
    os.system('cls' if os.name=='nt' else 'clear')

def load_blocks(size):
    scale = [Stone, Dirt, Clay, Gravel, Granite]
    chance = [80,5,5,5,5]
    results = random.choices(scale,chance,k=size)
    return(results)

def go_left(loc):
    global chunk
    global player_location

    # left edges of chunk
    left_index = [0,15,30,45,60]
    for i in range(len(left_index)):
        if left_index[i] == loc:
            if chunk.left_chunk == None:
                new_chunk = Chunk(load_blocks(75))
                chunk.left_chunk = new_chunk
                new_chunk.right_chunk = chunk
                chunk = new_chunk
            else:
                chunk = chunk.left_chunk
            return loc + 14
    return loc - 1

def go_right(loc):
    global chunk
    global player_location

    # left edges of chunk
    right_index = [14,29,44,59,74]
    for i in range(len(right_index)):          

        if right_index[i] == loc:
            if chunk.right_chunk == None:
                new_chunk = Chunk(load_blocks(75))
                chunk.right_chunk = new_chunk
                new_chunk.left_chunk = chunk
                chunk = new_chunk
            else:
                chunk = chunk.right_chunk
            return loc - 14
        
    return loc + 1

def go_up(loc):
    global chunk
    global player_location

    up_index = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    for i in range(len(up_index)):
        if up_index[i] == loc:
            if chunk.above_chunk == None:
                new_chunk = Chunk(load_blocks(75))
                chunk.setAboveChunk(new_chunk)
                new_chunk.setBelowChunk(chunk)
                chunk = new_chunk
            else:
                chunk = chunk.above_chunk
            return loc + 60
        
    return loc - 15

def go_down(loc):
    global chunk
    global player_location

    down_index = [60,61,62,63,64,65,66,67,68,69,70,71,72,73,74]
    for i in range(len(down_index)):
        if down_index[i] == loc:
            if chunk.below_chunk == None:
                new_chunk = Chunk(load_blocks(75))
                chunk.setBelowChunk(new_chunk)
                new_chunk.setAboveChunk(chunk)
                chunk = new_chunk
            else:
                chunk = chunk.below_chunk
            return loc - 60
        
    return loc + 15

def print_map(map, player_location, last_block, pack, axe, durability):
    global curr_tool
    global tool_arr
    global on_edge

    clear()

    edges = [14,29,44,59,74]
    for i in range(len(map)):
        block = map[i]()
        if i == player_location:
            mined_block = last_block()

            if last_block.__name__ != 'Mined':
                pack.addItem(mined_block)
                axe.use_tool(mined_block)

            if on_edge:
                if tool_arr[curr_tool].name == 'pick-axe':
                    print("--)|")
                if tool_arr[curr_tool].name == 'shovel':
                    print("--D|")
            else:
                if tool_arr[curr_tool].name == 'pick-axe':
                    print("--)|",end='')
                if tool_arr[curr_tool].name == 'shovel':
                    print("--D|",end='')
                

        else:
            cprint(f"{block.abv}|", block.color, end='')
            for j in range(len(edges)):
                if edges[j] == i:
                    print()
        if i == 74:
            print(f'tool:{tool_arr[curr_tool].name} | level:{tool_arr[curr_tool].level} | dblty:{tool_arr[curr_tool].durability} | mat:{tool_arr[curr_tool].handle_material}')
            print(f'pack:{pack.name} | strg:{pack.capacity} | lbs:{round(pack.weight,2)} | dblty:{pack.durability}')

            if durability > 0:
                    widgets=[
                        f'mining {mined_block.name}',
                        progressbar.Percentage(),
                    ]
                    for i in progressbar.progressbar(range(durability), widgets=widgets, redirect_stdout=True):
                        if mined_block.tool != tool_arr[curr_tool].name:
                            time.sleep(0.3)
                        else:
                            time.sleep(0.1)

            




    

if __name__ == "__main__":

    # Initialize map
    chunk = Chunk(load_blocks(75))

    # set player location and boundaries of map
    chunk.map[37] = Mined
    player_location = 37

    # set player up
    pack = BasicBackpack()
    axe = Pickaxe()
    shovel = Shovel()

    tool_arr = [axe, shovel]
    curr_tool = 0

    # draw map
    print_map(chunk.map, player_location, chunk.map[37], pack, axe,0)


    curr_key = None
    last_block = None
    right_index = [14,29,44,59,74]

    # The event listener will be running in this block - main game loop
    with keyboard.Events() as events:
        for event in events:
            # exit if esc
            if event.key == keyboard.Key.esc:
                break
            else:
                # action if a key is pressed
                if type(event) is keyboard.Events.Press and curr_key != event.key:
                    curr_key = event.key
                    durr = 0


                    #### CONTROLS


                    # if left key mine block to left, set player location
                    if event.key == keyboard.Key.left:
                        for j in range(len(right_index)):
                            if player_location - 1 == right_index[j]:
                                on_edge = True
                        hold_chunk = chunk
                        last_block = chunk.map[go_left(player_location)]
                        durr = last_block().durability
                        chunk.map[go_left(player_location)] = Mined
                        player_location = go_left(player_location)
                        if hold_chunk == chunk:
                            print_map(chunk.map, player_location, last_block, pack, axe,durr)

                    # if right key mine block to right, set player location
                    if event.key == keyboard.Key.right:
                        for j in range(len(right_index)):
                            if player_location + 1 == right_index[j]:
                                on_edge = True
                        hold_chunk = chunk
                        last_block = chunk.map[go_right(player_location)]
                        durr = last_block().durability
                        chunk.map[go_right(player_location)] = Mined
                        player_location = go_right(player_location)
                        if hold_chunk == chunk:
                            print_map(chunk.map, player_location, last_block, pack, axe,durr)

                    # if up key mine block above, set player location
                    if event.key == keyboard.Key.up:
                        for j in range(len(right_index)):
                            if player_location == right_index[j]:
                                on_edge = True
                        hold_chunk = chunk
                        last_block = chunk.map[go_up(player_location)]
                        durr = last_block().durability                       
                        chunk.map[go_up(player_location)] = Mined
                        player_location = go_up(player_location)
                        if hold_chunk == chunk:
                            print_map(chunk.map, player_location, last_block, pack, axe,durr)

                    # if down key mine block below, set player location
                    if event.key == keyboard.Key.down:
                        for j in range(len(right_index)):
                            if player_location == right_index[j]:
                                on_edge = True
                        hold_chunk = chunk
                        last_block = chunk.map[go_down(player_location)]
                        durr = last_block().durability                       
                        chunk.map[go_down(player_location)] = Mined
                        player_location = go_down(player_location)
                        if hold_chunk == chunk:
                            print_map(chunk.map, player_location, last_block, pack, axe,durr)

                    # if tha 'a' key is hit change tools
                    if event.key == keyboard.KeyCode.from_char('a'):
                        if curr_tool == 0:
                            curr_tool = 1
                        else:
                            curr_tool = 0


                    #### END CONTROLS


                    # print map after mining is done
                    if last_block != None:
                        for j in range(len(right_index)):
                            if player_location == right_index[j]:
                                on_edge = True
                        print_map(chunk.map, player_location, Mined, pack, axe,0)
                        on_edge = False



                if type(event) is keyboard.Events.Release and curr_key == event.key:
                    curr_key = None

    

    

    # granite = Granite()
    # stone = Stone()
    # print(granite.__dict__)
    # print(stone.__dict__)
                                                                                
                                                                                
                                                                               



