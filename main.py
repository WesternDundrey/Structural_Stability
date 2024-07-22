import numpy as np
import matplotlib.pyplot as plt

class Beam:
    def __init__(self,length):
        self.length = length
        self.loads = []

def add_point_load(self, magnitude, position):
    self.loads.append(("point", magnitude, position))

def add_distributed_load(self, magnitude, start, end):
    self.loads.append(("distributed", magnitude, start, end))

def calculate_reactions(self):
    total_force = 0
    total_moment = 0

    for load in self.loads:
        if load[0] == 'point':
            total_force +=  load[1]
            total_moment += load[1] * load[2]
        elif load[0] == 'distributed':
            force = load[1] * (load[3] - load[2])
            total_force += force 
            total_moment += force (load[2] + (load[3]- load[2]) / 2)
        
    reaction_b = total_moment / self.length
    reaction_a = total_force - reaction_b

    return reaction_a, reaction_b

def calculate_shear_force(self, x):
    shear = -self.calculate_reactions()[0]

    for load in self.loads:
        if load[0] == "point" and x > load[2]:
            shear =+ load[1]
        elif load[0] == "distributed":
            if x < load[3]:
                shear += load[1] * (x -load[2])
            else: 
                shear += load[1] * (load[3]- load[2])

    return shear

def calculate_bending_moment