# voyager_plot.py
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from Voyager_data import VOYAGER_EVENTS

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

    def init_plot(self):
        self.figure.clear()
        # Show only 15 points
        idxs = np.linspace(0, len(self.xs)-1, self.display_points).astype(int)
        x_disp = np.array(self.xs)[idxs]
        y_disp = np.array(self.ys)[idxs]
        z_disp = np.array(self.zs)[idxs]

        if self.mode == "3D":
            self.ax = self.figure.add_subplot(111, projection="3d", facecolor="white")
            self.ax.plot(x_disp, y_disp, z_disp, color="blue", linestyle="--", linewidth=2, label="Voyager Path")
            for i in idxs:
                x, y, z = self.xs[i], self.ys[i], self.zs[i]
                self.ax.scatter(x, y, z, s=70, marker="o", color="orange")
                self.ax.text(x, y, z, f"{VOYAGER_EVENTS[i]['year']}", fontsize=8)
            self.voyager_marker = self.ax.scatter([], [], [], s=120, marker="*", color="red", label="Voyager 1")
            self.ax.set_title("Voyager 1 Path (3D)", fontsize=13, pad=15)
            self.ax.set_xlabel("X (km)")
            self.ax.set_ylabel("Y (km)")
            self.ax.set_zlabel("Z (km)")
            self.ax.legend()
        else:
            self.ax = self.figure.add_subplot(111, facecolor="#1e1e2e")
            self.ax.plot(x_disp, y_disp, color="#3c82f6", linestyle="--", linewidth=2)
            for i in idxs:
                self.ax.scatter(self.xs[i], self.ys[i], s=60, color="#ffb703")
            self.voyager_marker = self.ax.scatter([], [], s=120, marker="*", color="#00f5d4")
            self.ax.set_title("Top-Down XY Projection", color="white", fontsize=12, pad=10)
            self.ax.set_xlabel("X (km)", color="white")
            self.ax.set_ylabel("Y (km)", color="white")
            self.ax.tick_params(colors="white")

        self.draw()

    def set_mode(self, mode):
        self.mode = mode
        self.init_plot()

    def plot_trajectory(self):
        cx, cy, cz = self.path_x[self.current_index], self.path_y[self.current_index], self.path_z[self.current_index]
        if self.mode == "3D":
            self.voyager_marker._offsets3d = ([cx], [cy], [cz])
        else:
            self.voyager_marker.set_offsets([[cx, cy]])
        self.draw()

    def move_forward(self):
        self.current_index = (self.current_index + 1) % self.num_steps
        self.plot_trajectory()

    def show_event(self, coords):
        # Jump marker to specific coordinates
        self.current_index = int((coords[0] - self.xs[0]) / (self.xs[-1] - self.xs[0]) * (self.num_steps-1))
        self.plot_trajectory()

    def get_current_position(self):
        return self.path_x[self.current_index], self.path_y[self.current_index], self.path_z[self.current_index]