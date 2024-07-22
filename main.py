import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk



class BeamAnalysisGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Beam Analysis Tool")
        self.master.geometry("800x600")

        self.beam = None
        self.load_entries = []

        self.create_widgets()
    def create_widgets(self):
        # Beam length input
        ttk.Label(self.master, text="Beam Length (m):").grid(row=0, column=0, padx=5, pady=5)
        self.length_entry = ttk.Entry(self.master)
        self.length_entry.grid(row=0, column=1, padx=5, pady=5)

        # Load type selection
        ttk.Label(self.master, text="Load Type:").grid(row=1, column=0, padx=5, pady=5)
        self.load_type = ttk.Combobox(self.master, values=["Point Load", "Distributed Load"])
        self.load_type.grid(row=1, column=1, padx=5, pady=5)

        # Add load button
        ttk.Button(self.master, text="Add Load", command=self.add_load_fields).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Analyze button
        ttk.Button(self.master, text="Analyze Beam", command=self.analyze_beam).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Frame for load inputs
        self.load_frame = ttk.Frame(self.master)
        self.load_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Frame for plots
        self.plot_frame = ttk.Frame(self.master)
        self.plot_frame.grid(row=0, column=2, rowspan=5, padx=5, pady=5)

    def add_load_fields(self):
        load_type = self.load_type.get()
        row = len(self.load_entries)

        if load_type == "Point Load":
            ttk.Label(self.load_frame, text="Magnitude (N):").grid(row=row, column=0)
            magnitude = ttk.Entry(self.load_frame)
            magnitude.grid(row=row, column=1)

            ttk.Label(self.load_frame, text="Position (m):").grid(row=row, column=2)
            position = ttk.Entry(self.load_frame)
            position.grid(row=row, column=3)

            self.load_entries.append((load_type, magnitude, position))

        elif load_type == "Distributed Load":
            ttk.Label(self.load_frame, text="Magnitude (N/m):").grid(row=row, column=0)
            magnitude = ttk.Entry(self.load_frame)
            magnitude.grid(row=row, column=1)

            ttk.Label(self.load_frame, text="Start (m):").grid(row=row, column=2)
            start = ttk.Entry(self.load_frame)
            start.grid(row=row, column=3)

            ttk.Label(self.load_frame, text="End (m):").grid(row=row, column=4)
            end = ttk.Entry(self.load_frame)
            end.grid(row=row, column=5)

            self.load_entries.append((load_type, magnitude, start, end))

    def analyze_beam(self):
        try:
            length = float(self.length_entry.get())
            self.beam = Beam(length)

            for load_entry in self.load_entries:
                if load_entry[0] == "Point Load":
                    magnitude = float(load_entry[1].get())
                    position = float(load_entry[2].get())
                    self.beam.add_point_load(magnitude, position)
                elif load_entry[0] == "Distributed Load":
                    magnitude = float(load_entry[1].get())
                    start = float(load_entry[2].get())
                    end = float(load_entry[3].get())
                    self.beam.add_distributed_load(magnitude, start, end)

            self.plot_diagrams()

        except ValueError:
            tk.messagebox.showerror("Error", "Invalid input. Please check all entries.")

    def plot_diagrams(self):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

        x = np.linspace(0, self.beam.length, 1000)
        shear = [self.beam.calculate_shear_force(xi) for xi in x]
        moment = [self.beam.calculate_bending_moment(xi) for xi in x]

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

        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        reactions = self.beam.calculate_reactions()
        tk.Label(self.plot_frame, text=f"Reaction at A: {reactions[0]:.2f} N").pack()
        tk.Label(self.plot_frame, text=f"Reaction at B: {reactions[1]:.2f} N").pack()


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