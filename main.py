import numpy as np
import matplotlib.pyplot as plt

class Beam:
    def __init__(self, length):
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
            if load[0] == "point":
                total_force += load[1]
                total_moment += load[1] * load[2]
            elif load[0] == "distributed":
                force = load[1] * (load[3] - load[2])
                total_force += force
                total_moment += force * (load[2] + (load[3] - load[2]) / 2)

        reaction_b = total_moment / self.length
        reaction_a = total_force - reaction_b

        return reaction_a, reaction_b

    def calculate_shear_force(self, x):
        shear = -self.calculate_reactions()[0]

        for load in self.loads:
            if load[0] == "point" and x > load[2]:
                shear += load[1]
            elif load[0] == "distributed":
                if x > load[2]:
                    if x < load[3]:
                        shear += load[1] * (x - load[2])
                    else:
                        shear += load[1] * (load[3] - load[2])

        return shear

    def calculate_bending_moment(self, x):
        moment = -self.calculate_reactions()[0] * x

        for load in self.loads:
            if load[0] == "point" and x > load[2]:
                moment += load[1] * (x - load[2])
            elif load[0] == "distributed":
                if x > load[2]:
                    if x < load[3]:
                        moment += load[1] * (x - load[2])**2 / 2
                    else:
                        moment += load[1] * (load[3] - load[2]) * (x - (load[2] + (load[3] - load[2]) / 2))

        return moment

    def plot_diagrams(self):
        x = np.linspace(0, self.length, 1000)
        shear = [self.calculate_shear_force(xi) for xi in x]
        moment = [self.calculate_bending_moment(xi) for xi in x]

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

        ax1.plot(x, shear)
        ax1.set_title("Shear Force Diagram")
        ax1.set_xlabel("Position along beam (m)")
        ax1.set_ylabel("Shear Force (N)")
        ax1.grid(True)

        ax2.plot(x, moment)
        ax2.set_title("Bending Moment Diagram")
        ax2.set_xlabel("Position along beam (m)")
        ax2.set_ylabel("Bending Moment (N·m)")
        ax2.grid(True)

        plt.tight_layout()
        plt.show()

# Example usage
beam = Beam(10)  # 10 meter long beam
beam.add_point_load(1000, 3)  # 1000 N point load at 3 meters
beam.add_distributed_load(500, 6, 10)  # 500 N/m distributed load from 6 to 10 meters

print("Reactions:", beam.calculate_reactions())
beam.plot_diagrams()