# voyager_plot.py
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from voyager_data import VOYAGER_EVENTS

class VoyagerPlot(FigureCanvas):
    def __init__(self, figure=None, mode="3D", display_points=15):
        self.mode = mode
        self.display_points = display_points
        fig = Figure(figsize=(7, 7), facecolor="white")
        super().__init__(fig)
        self.setParent(parent)
        
        # Full path arrays
        self.xs = [e["coords"][0] for e in VOYAGER_EVENTS]
        self.ys = [e["coords"][1] for e in VOYAGER_EVENTS]
        self.zs = [e["coords"][2] for e in VOYAGER_EVENTS]

        # For animation
        self.num_steps = 500
        self.path_x = np.linspace(self.xs[0], self.xs[-1], self.num_steps)
        self.path_y = np.linspace(self.ys[0], self.ys[-1], self.num_steps)
        self.path_z = np.linspace(self.zs[0], self.zs[-1], self.num_steps)
        self.current_index = 0

        self.init_plot()