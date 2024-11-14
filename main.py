import sys
import math
from typing import Optional

#def get_coords_by_type(type):
#    for i in input():
#    if type == "WALL":
#        input()
#    #elif type == "ROOT":
#
#    #elif type == "BASIC":
#
#    else:
#        print("Error: No behaviour defined for type: " + type, file=sys.stderr, flush=True)
#

def get_distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

#def is_wall_between(x1, y1, x2, y2):

#def get_nearest_a(x, y):

class Entity:

    def __init__(self, entity):
        self.x = int(entity[0])
        self.y = int(entity[1])
        self._type = entity[2]
        self.owner = int(entity[3])
        self.organ_id = int(entity[4])
        self.organ_dir = entity[5]
        self.organ_parent_id = int(entity[6])
        self.organ_root_id = int(entity[7])

    @staticmethod
    def get_distance(entity1, entity2):
        return math.sqrt((entity1.x - entity2.x)**2 + (entity1.y - entity2.y)**2)

class Map:
    def __init__(self, width, height):
        # Initialize a 2D list with None as placeholder values, allowing Entity objects later
        self.map: list[list[Optional[Entity]]] = [[None for _ in range(height)] for _ in range(width)]
        self.width = width
        self.height = height

    def insert(self, inputs):
        self.map[int(inputs[0])][int(inputs[1])] = Entity(inputs)

    def get_printable_map(self):
        map_str = ""
        for y in range(self.height):
            row_str = ""
            for x in range(self.width):
                cell = self.map[x][y]
                if cell is None:
                    row_str += "EMPTY\t"  # Empty cell
                else:
                    row_str += f"{cell._type}\t"  # Use the entity's type as its symbol
            map_str += row_str.strip() + "\n"  # Remove trailing space and add newline
        return map_str.strip()  # Strip the final newline


# Grow and multiply your organisms to end up larger than your opponent.

# width: columns in the game grid
# height: rows in the game grid
width, height = [int(i) for i in input().split()]

# game loop
while True:
    map = Map(width, height)
    entity_count = int(input())
    for i in range(entity_count):
        inputs = input().split()
        #print(input(), file=sys.stderr, flush=True)
        x = int(inputs[0])
        y = int(inputs[1])  # grid coordinate
        _type = inputs[2]  # WALL, ROOT, BASIC, TENTACLE, HARVESTER, SPORER, A, B, C, D
        owner = int(inputs[3])  # 1 if your organ, 0 if enemy organ, -1 if neither
        organ_id = int(inputs[4])  # id of this entity if it's an organ, 0 otherwise
        organ_dir = inputs[5]  # N,E,S,W or X if not an organ
        organ_parent_id = int(inputs[6])
        organ_root_id = int(inputs[7])

        map.insert(inputs)
    # my_d: your protein stock
    my_a, my_b, my_c, my_d = [int(i) for i in input().split()]
    # opp_d: opponent's protein stock
    opp_a, opp_b, opp_c, opp_d = [int(i) for i in input().split()]
    required_actions_count = int(input())  # your number of organisms, output an action for each one in any order

    print(map.get_printable_map(), file=sys.stderr, flush=True)


    for i in range(required_actions_count):

        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr, flush=True)
        print("GROW 1 16 8 BASIC")




