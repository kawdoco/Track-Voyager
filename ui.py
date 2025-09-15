import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from voyager_api import VoyagerAPI
from voyager_plotter import VoyagerPlotter

class VoyagerApp(tk.Tk):
    """
    Tkinter GUI Application for Voyager Location Finder.
    """

    def __init__(self):
        super().__init__()
        self.title("Voyager Location Finder (OOP)")
        self.geometry("950x600")

        # Default API instance
        self.api = VoyagerAPI(voyager="1", observer="@sun")
        self.plotter = VoyagerPlotter()

        self._build_ui()

    def _build_ui(self):
        # Top controls
        ctrl = ttk.Frame(self)
        ctrl.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(ctrl, text="Voyager:").grid(row=0, column=0, sticky="w")
        self.voyager_var = tk.StringVar(value="1")
        ttk.Combobox(ctrl, textvariable=self.voyager_var, values=["1","2"], width=5).grid(row=0, column=1)

        ttk.Label(ctrl, text="Observer:").grid(row=0, column=2, sticky="w")
        self.obs_var = tk.StringVar(value="@sun")
        ttk.Combobox(ctrl, textvariable=self.obs_var, values=["@sun","@399"], width=10).grid(row=0, column=3)

        ttk.Label(ctrl, text="Date (YYYY-MM-DD):").grid(row=0, column=4, sticky="w")
        self.date_entry = ttk.Entry(ctrl, width=15)
        self.date_entry.insert(0, "2025-09-01")
        self.date_entry.grid(row=0, column=5)

        ttk.Button(ctrl, text="Get Position", command=self.show_position).grid(row=0, column=6, padx=10)
        ttk.Button(ctrl, text="Plot Range", command=self.show_plot).grid(row=0, column=7, padx=10)

        # Text output
        self.output = tk.Text(self, width=50, height=25)
        self.output.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

        # Plot area
        self.plot_frame = ttk.Frame(self)
        self.plot_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.canvas = None

    def show_position(self):
        try:
            self.api = VoyagerAPI(self.voyager_var.get(), self.obs_var.get())
            eph = self.api.get_position(self.date_entry.get())

            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, f"Voyager {self.voyager_var.get()} at {eph['datetime_str']}\n\n")
            self.output.insert(tk.END, f"RA: {eph['RA']} deg\n")
            self.output.insert(tk.END, f"DEC: {eph['DEC']} deg\n")
            self.output.insert(tk.END, f"Distance: {eph['delta']} AU\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_plot(self):
        try:
            self.api = VoyagerAPI(self.voyager_var.get(), self.obs_var.get())
            eph_range = self.api.get_range("2025-09-01", "2025-09-10", "1d")

            fig = self.plotter.plot_distance(eph_range, title=f"Voyager {self.voyager_var.get()} Distance")
            if self.canvas:
                self.canvas.get_tk_widget().destroy()
            self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        except Exception as e:
            messagebox.showerror("Error", str(e))
