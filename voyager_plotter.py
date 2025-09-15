from matplotlib.figure import Figure

class VoyagerPlotter:
    """
    Handles creating plots for Voyager data.
    """
    @staticmethod
    def plot_distance(eph_table, title="Voyager Distance vs Time"):
        fig = Figure(figsize=(6,4), dpi=100)
        ax = fig.add_subplot(111)
        times = [row['datetime_str'] for row in eph_table]
        distances = [row['delta'] for row in eph_table]  # delta = distance from observer
        ax.plot(times, distances, marker="o")
        ax.set_title(title)
        ax.set_xlabel("Date")
        ax.set_ylabel("Distance (AU)")
        fig.autofmt_xdate(rotation=30)
        return fig