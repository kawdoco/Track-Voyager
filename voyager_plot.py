import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import cm
import matplotlib.image as mpimg
from Voyager_data import VOYAGER_EVENTS


class VoyagerPlot(FigureCanvas):
    def __init__(self, parent=None, mode="3D", display_points=15, dark_mode=True):
        self.mode = mode
        self.display_points = display_points
        self.dark_mode = dark_mode

        fig = Figure(figsize=(7, 7), facecolor="black" if dark_mode else "white")
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

        # Load Voyager ship image (optional)
        try:
            self.voyager_img = mpimg.imread("voyager_ship.png")
        except:
            self.voyager_img = None

        self.init_plot()

    def init_plot(self):
        """Initialize the plot based on mode and theme."""
        self.figure.clear()

        # Theme colors
        bg_color = "#0d1117" if self.dark_mode else "white"
        text_color = "white" if self.dark_mode else "black"
        path_color = "#3b82f6" if self.dark_mode else "blue"
        voyager_color = "#00f5d4" if self.dark_mode else "red"

        # Display subset of events
        idxs = np.linspace(0, len(self.xs) - 1, self.display_points).astype(int)
        x_disp = np.array(self.xs)[idxs]
        y_disp = np.array(self.ys)[idxs]
        z_disp = np.array(self.zs)[idxs]

        if self.mode == "3D":
            # === 3D VIEW ===
            self.ax = self.figure.add_subplot(111, projection="3d", facecolor=bg_color)
            self.ax.plot(
                x_disp, y_disp, z_disp,
                color=path_color, linestyle="--", linewidth=2, label="Voyager Path"
            )
            for i in idxs:
                x, y, z = self.xs[i], self.ys[i], self.zs[i]
                self.ax.scatter(x, y, z, s=70, marker="o", color="#ffb703")
                self.ax.text(x, y, z, f"{VOYAGER_EVENTS[i]['year']}", fontsize=8, color=text_color)

            # Voyager marker (ship image or star)
            if self.voyager_img is not None:
                self.voyager_marker = self.ax.scatter([], [], [], s=0)  # Hidden placeholder
                self.ship_img = self.voyager_img
            else:
                self.voyager_marker = self.ax.scatter([], [], [], s=120, marker="*", color=voyager_color, label="Voyager 1")

            self.ax.set_title("Voyager 1 Path (3D)", fontsize=13, color=text_color, pad=15)
            self.ax.set_xlabel("X (km)", color=text_color)
            self.ax.set_ylabel("Y (km)", color=text_color)
            self.ax.set_zlabel("Z (km)", color=text_color)
            self.ax.tick_params(colors=text_color)
            self.ax.legend(facecolor=bg_color, edgecolor=text_color, labelcolor=text_color)

        else:
            # === 2D VIEW ===
            self.ax = self.figure.add_subplot(111, facecolor=bg_color)
            cmap = cm.get_cmap("cool")

            # Voyager path
            self.ax.plot(
                x_disp, y_disp,
                color=path_color, linestyle="--", linewidth=2.5, label="Voyager Path"
            )

            # Events
            for i, idx in enumerate(idxs):
                color = cmap(i / len(idxs))
                self.ax.scatter(
                    self.xs[idx], self.ys[idx],
                    s=100, color=color,
                    edgecolor="white" if self.dark_mode else "black",
                    linewidth=0.6, alpha=0.9, zorder=3
                )
                self.ax.text(
                    self.xs[idx], self.ys[idx],
                    f"{VOYAGER_EVENTS[idx]['year']}",
                    color=text_color, fontsize=8, ha="center", va="bottom", zorder=4
                )

            # Voyager ship image marker
            if self.voyager_img is not None:
                self.voyager_marker = self.ax.imshow(
                    self.voyager_img, extent=[0, 0, 0, 0], zorder=5
                )
            else:
                self.voyager_marker = self.ax.scatter(
                    [], [], s=150, marker="*", color=voyager_color, edgecolor="white", linewidth=0.6, zorder=5
                )

            self.ax.set_title("Voyager 1 - XY Projection", color=text_color, fontsize=12, pad=10)
            self.ax.set_xlabel("X (km)", color=text_color)
            self.ax.set_ylabel("Y (km)", color=text_color)
            self.ax.tick_params(colors=text_color)
            self.ax.grid(True, color="#333" if self.dark_mode else "#ccc", linestyle=":", linewidth=0.7)
            self.ax.legend(facecolor=bg_color, edgecolor=text_color, labelcolor=text_color)

        self.draw()

    def set_mode(self, mode):
        self.mode = mode
        self.init_plot()
    
    def set_theme(self, dark_mode:bool):
        """Update theme dynamically from UI toggle."""
        self.dark_mode = dark_mode
        self.figure.set_facecolor("black" if dark_mode else "white")
        self.init_plot()

    def plot_trajectory(self):
        cx, cy, cz = (
            self.path_x[self.current_index],
            self.path_y[self.current_index],
            self.path_z[self.current_index],
        )

        if self.mode == "3D":
            if self.voyager_img is None:
                self.voyager_marker._offsets3d = ([cx], [cy], [cz])
        else:
            if self.voyager_img is not None:
                size = 0.3
                self.voyager_marker.set_extent([cx - size, cx + size, cy - size, cy + size])
            else:
                self.voyager_marker.set_offsets([[cx, cy]])

        self.draw()

    def move_forward(self):
        self.current_index = (self.current_index + 1) % self.num_steps
        self.plot_trajectory()

    def show_event(self, coords):
        self.current_index = int(
            (coords[0] - self.xs[0]) / (self.xs[-1] - self.xs[0]) * (self.num_steps - 1)
        )
        self.plot_trajectory()

    def get_current_position(self):
        return (
            self.path_x[self.current_index],
            self.path_y[self.current_index],
            self.path_z[self.current_index],
        )
