from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class ChartCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # Create charts ONCE
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        
        # Store axes as instance variables
        self.ax1 = self.fig.add_subplot(211) # Top chart
        self.ax2 = self.fig.add_subplot(212) # Bottom chart
        
        # Adjust layout to prevent overlap
        self.fig.tight_layout(pad=3.0)

        super(ChartCanvas, self).__init__(self.fig)
        self.setParent(parent)

    def update_charts(self, data):
        """
        Updates the charts with new data.

        Args:
            data (dict): The API response data containing statistics.
        """
        self.ax1.clear()
        self.ax2.clear()

        # 1. Equipment Type Distribution (Bar Chart)
        type_dist = data.get("type_distribution", {})
        types = list(type_dist.keys())
        counts = list(type_dist.values())

        self.ax1.bar(types, counts, color='skyblue')
        self.ax1.set_title("Equipment Type Distribution")
        self.ax1.set_xlabel("Equipment Type")
        self.ax1.set_ylabel("Count")

        # 2. Average Parameters (Bar Chart)
        avg_flow = data.get("average_flowrate", 0)
        avg_press = data.get("average_pressure", 0)
        avg_temp = data.get("average_temperature", 0)

        params = ['Flowrate', 'Pressure', 'Temperature']
        values = [avg_flow, avg_press, avg_temp]

        self.ax2.bar(params, values, color=['#ff9999', '#66b3ff', '#99ff99'])
        self.ax2.set_title("Average Parameters")
        self.ax2.set_ylabel("Value")

        # Redraw
        self.draw()
