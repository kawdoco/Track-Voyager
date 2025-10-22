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