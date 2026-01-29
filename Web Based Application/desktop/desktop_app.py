import sys
import requests

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QLabel, QFileDialog, QTextEdit
)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class DesktopApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer (Desktop)")
        self.setGeometry(100, 100, 700, 600)

        self.layout = QVBoxLayout()

        self.label = QLabel("Upload CSV File")
        self.layout.addWidget(self.label)

        self.upload_btn = QPushButton("Choose CSV & Upload")
        self.upload_btn.clicked.connect(self.upload_csv)
        self.layout.addWidget(self.upload_btn)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.layout.addWidget(self.output)

        # Matplotlib Figure
        self.figure = Figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.setLayout(self.layout)

    def upload_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV", "", "CSV Files (*.csv)"
        )

        if not file_path:
            return

        url = "http://127.0.0.1:8000/api/upload/"

        with open(file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(url, files=files)

        if response.status_code == 200:
            data = response.json()
            summary = data["summary"]

            self.output.setText(
                f"Upload Successful!\n\nSummary:\n{summary}"
            )

            self.plot_chart(summary["type_distribution"])
        else:
            self.output.setText("Upload Failed")

    def plot_chart(self, distribution):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        labels = list(distribution.keys())
        sizes = list(distribution.values())

        ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.set_title("Equipment Type Distribution")

        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DesktopApp()
    window.show()
    sys.exit(app.exec_())