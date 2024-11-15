import sys
import math
from typing import Optional

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
        self.harvested = False

    @staticmethod
    def get_distance(entity1, entity2):
        return math.sqrt((entity1.x - entity2.x)**2 + (entity1.y - entity2.y)**2)

    def isObstacle(self):
        return self._type == "WALL" or self._type == "ROOT" or self._type == "BASIC"
    
    def is_owner(self):
        return self.owner == 1

    def gets_harvested_by_us(self, map):
        right =  map[self.x+1][self.y]
        down =  map[self.x][self.y+1]
        left =  map[self.x-1][self.y]
        up =  map[self.x][self.y-1]
        if right != None and right._type == "HARVESTER" and right.organ_dir == "W" and right.is_owner():
            return True
        elif down != None and down._type == "HARVESTER" and down.organ_dir == "N" and down.is_owner():
            return True
        elif left != None and left._type == "HARVESTER" and left.organ_dir == "E" and left.is_owner():
            return True
        elif up != None and up._type == "HARVESTER" and up.organ_dir == "S" and up.is_owner():
            return True
        return False

    def get_free_neighbor_coords(self, map):
        right =  map[self.x+1][self.y]
        down =  map[self.x][self.y+1]
        left =  map[self.x-1][self.y]
        up =  map[self.x][self.y-1]
        if right == None:
            return (self.x+1, self.y)
        if down == None:
            return (self.x, self.y+1)
        if left == None:
            return (self.x-1, self.y)
        if up == None:
            return (self.x, self.y-1)
        return None

class ProteinStock:
    def __init__(self, my_a, my_b, my_c, my_d):
        self.a = my_a
        self.b = my_b
        self.c = my_c
        self.d = my_d

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

    def get_all_entities_by_type(self, type):
        entities = []
        for row in self.map:
            for entity in row:
                if entity is None:
                    continue
                elif entity._type == type:
                    entities.append(entity)
        # Debugging output
        #print(f"Entities found of type '{type}': {[e._type for e in entities]}")
        return entities

    def can_create_harvester(self, my_protein_stock):
        if my_protein_stock.c < 1 and my_protein_stock.d < 1:
            return False
        return True

    def get_all_entities_by_owner(self, owner):
        entities = []
        for row in self.map:
            for entity in row:
                if entity is None:
                    continue
                elif entity.owner == owner:
                    entities.append(entity)
        # Debugging output
        #print(f"Entities found of type '{type}': {[e.owner for e in entities]}")
        return entities

    def get_nearest_protein(self, entity):
        proteins = self.get_all_entities_by_type("A")
        # Filter out proteins that are harvested by us
        proteins = [p for p in proteins if not p.gets_harvested_by_us(self.map)]
        if len(proteins) == 0:
            return None
        distances = [(protein, Entity.get_distance(entity, protein)) for protein in proteins]
        # Find the protein with the minimum distance
        nearest_protein = min(distances, key=lambda x: x[1])[0]
        return nearest_protein

    def get_nearest_owner_protein_pair(self):
        owners = self.get_all_entities_by_owner(1)
        distances = {}
        for owner in owners:
            nearest_protein = self.get_nearest_protein(owner)
            if nearest_protein == None:
                return None, None
            distances[(owner, nearest_protein)] = Entity.get_distance(owner, nearest_protein)

        # Find the (owner, nearest_protein) pair with the minimum distance
        nearest_pair = min(distances.items(), key=lambda item: item[1])[0]

        return nearest_pair

    def get_next_move(self, nearest_pair, my_protein_stock):
        organ, protein = nearest_pair
        dist = Entity.get_distance(organ, protein)

        #Harvester
        if self.can_create_harvester(my_protein_stock):
            if dist == 2:
                # Horizontal cases (either left or right)
                if organ.y - protein.y == 0:
                    # Protein is right from organ
                    if protein.x - organ.x > 0:
                        return f"GROW {organ.organ_id} {organ.x + 1} {organ.y} HARVESTER E"
                    # Protein is left from organ
                    elif protein.x - organ.x < 0:
                        return f"GROW {organ.organ_id} {organ.x - 1} {organ.y} HARVESTER W"
                # Vertical cases (either up or down)
                elif organ.x - protein.x == 0:
                    # Protein is under the organ
                    if protein.y - organ.y > 0:
                        return f"GROW {organ.organ_id} {organ.x} {organ.y + 1} HARVESTER S"
                    # Protein is over the organ
                    elif protein.y - organ.y < 0:
                        return f"GROW {organ.organ_id} {organ.x} {organ.y - 1} HARVESTER N"

            elif dist < 2 and dist > 1:
                #protein ist links vom organ
                if organ.x - protein.x > 0:
                    #nach oben
                    if organ.y - protein.y > 0:
                        return f"GROW {organ.organ_id} {organ.x-1} {organ.y} HARVESTER N"
                    #nach unten
                    else:
                        return f"GROW {organ.organ_id} {organ.x-1} {organ.y} HARVESTER S"
                #protein ist rechts vom organ
                if organ.x - protein.x < 0:
                    #nach oben
                    if organ.y - protein.y > 0: 
                        return f"GROW {organ.organ_id} {organ.x+1} {organ.y} HARVESTER N"
                    else: 
                        return f"GROW {organ.organ_id} {organ.x+1} {organ.y} HARVESTER S"
        #Basic
        return f"GROW {organ.organ_id} {protein.x} {protein.y} BASIC"

    def default_move(self):
        owners = self.get_all_entities_by_owner(1)
        for o in owners:
            coords = o.get_free_neighbor_coords(self.map)
            if coords == None:
                continue
            else:
                return f"GROW {o.organ_id} {coords[0]} {coords[1]} BASIC"

    #def hasObstacle(entity1, entity2):

    #def give_cost_for_path(self, organ, protein):
    #    cost = 0
    #
    #    protein_found = False
    #    while not protein_found:
    #        org



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
    my_protein_stock = ProteinStock(my_a, my_b, my_c, my_d)
    # opp_d: opponent's protein stock
    opp_a, opp_b, opp_c, opp_d = [int(i) for i in input().split()]
    opp_protein_stock = ProteinStock(opp_a, opp_b, opp_c, opp_d)
    required_actions_count = int(input())  # your number of organisms, output an action for each one in any order

    print(map.get_printable_map(), file=sys.stderr, flush=True)


    for i in range(required_actions_count):
    
        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr, flush=True)
        #proteins = map.get_all_entities_by_type("A")

        #nearest_protein = map.get_nearest_protein(map.get_all_entities_by_type("A")[0])
        #print(f"Nearest protein coords: {nearest_protein.x} , {nearest_protein.y}", file=sys.stderr, flush=True)
        
        # 1 Chase available proteins
        # 2 Chase opponents root
        # 3 Default

        owner, protein = map.get_nearest_owner_protein_pair()
        command = "HELP"
        # Case: No more protein :(
        if owner == None or protein == None or owner._type == "HARVESTER":
            command = map.default_move()
        else:
            command = map.get_next_move(map.get_nearest_owner_protein_pair(), my_protein_stock)
        
        

        print(command)
        #print("GROW 1 16 8 BASIC")




