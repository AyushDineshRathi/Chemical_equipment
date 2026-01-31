from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
    QPushButton, QLabel, QFileDialog, QMessageBox, QFrame, QListWidget, QSplitter
)
from PyQt5.QtCore import Qt
from api import upload_csv, get_history, generate_report
from charts import ChartCanvas

# --- Qt Stylesheet (CSS for Desktop) ---
STYLESHEET = """
QMainWindow {
    background-color: #f8fafc;
}
QWidget {
    font-family: 'Segoe UI', sans-serif;
    color: #1e293b;
}
QPushButton {
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: bold;
    border: 1px solid #cbd5e1;
}
QPushButton#UploadBtn {
    background-color: #3b82f6;
    color: white;
    border: none;
}
QPushButton#UploadBtn:hover {
    background-color: #2563eb;
}
QPushButton#DownloadBtn {
    background-color: #10b981;
    color: white;
    border: none;
}
QPushButton#DownloadBtn:hover {
    background-color: #059669;
}
QPushButton#DownloadBtn:disabled {
    background-color: #94a3b8;
}
QFrame#Card {
    background-color: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
}
QListWidget {
    background-color: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 8px;
    outline: none;
}
QListWidget::item {
    padding: 10px;
    border-bottom: 1px solid #f1f5f9;
}
QListWidget::item:selected {
    background-color: #e2e8f0;
    color: #1e293b;
}
QLabel#Header {
    font-size: 18px;
    font-weight: bold;
    color: #0f172a;
}
QLabel#SectionTitle {
    font-size: 14px;
    font-weight: bold;
    color: #64748b;
    margin-bottom: 5px;
}
"""

class MainWindow(QMainWindow):
    def __init__(self, token):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.setGeometry(100, 100, 1100, 850)
        self.setStyleSheet(STYLESHEET)
        
        self.token = token
        self.dataset_id = None
        self.init_ui()
        self.load_history()

    def init_ui(self):
        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # --- Header Section ---
        header_layout = QHBoxLayout()
        title = QLabel("Chemical Equipment Visualizer")
        title.setObjectName("Header")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # Logout / User info could go here
        user_info = QLabel("Logged in")
        user_info.setStyleSheet("color: #64748b; font-style: italic;")
        header_layout.addWidget(user_info)
        
        main_layout.addLayout(header_layout)

        # --- Top Controls ---
        controls_frame = QFrame()
        controls_frame.setObjectName("Card")
        controls_layout = QHBoxLayout(controls_frame)
        controls_layout.setContentsMargins(15, 15, 15, 15)
        
        self.upload_btn = QPushButton("Upload New CSV")
        self.upload_btn.setObjectName("UploadBtn")
        self.upload_btn.setCursor(Qt.PointingHandCursor)
        self.upload_btn.clicked.connect(self.on_upload)
        
        self.download_btn = QPushButton("Download Report")
        self.download_btn.setObjectName("DownloadBtn")
        self.download_btn.setCursor(Qt.PointingHandCursor)
        self.download_btn.setEnabled(False)
        self.download_btn.clicked.connect(self.download_report)

        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet("color: #64748b;")

        controls_layout.addWidget(self.upload_btn)
        controls_layout.addWidget(self.file_label)
        controls_layout.addStretch()
        controls_layout.addWidget(self.download_btn)
        
        main_layout.addWidget(controls_frame)

        # --- Content Splitter ---
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(1)
        splitter.setStyleSheet("QSplitter::handle { background-color: #cbd5e1; }")
        
        # Left Panel: History
        history_container = QWidget()
        history_layout = QVBoxLayout(history_container)
        history_layout.setContentsMargins(0, 0, 10, 0)
        
        hl_title = QLabel("Upload History")
        hl_title.setObjectName("SectionTitle")
        history_layout.addWidget(hl_title)
        
        self.history_list = QListWidget()
        history_layout.addWidget(self.history_list)
        splitter.addWidget(history_container)

        # Right Panel: Dashboard
        dashboard_container = QWidget()
        dashboard_layout = QVBoxLayout(dashboard_container)
        dashboard_layout.setContentsMargins(10, 0, 0, 0)

        # KPIs
        kpi_title = QLabel("Key Indicators")
        kpi_title.setObjectName("SectionTitle")
        dashboard_layout.addWidget(kpi_title)

        kpi_grid = QGridLayout()
        kpi_grid.setSpacing(15)
        self.kpi_labels = {}
        
        metrics = [
            ("Total Equipments", "total_equipment", "Units"),
            ("Avg Flowrate", "average_flowrate", "L/min"),
            ("Avg Pressure", "average_pressure", "bar"),
            ("Avg Temperature", "average_temperature", "°C")
        ]

        for i, (name, key, unit) in enumerate(metrics):
            # Each KPI is a Card
            k_frame = QFrame()
            k_frame.setObjectName("Card")
            k_frame.setStyleSheet("QFrame#Card { background-color: white; border-radius: 10px; }")
            kvbox = QVBoxLayout(k_frame)
            kvbox.setAlignment(Qt.AlignCenter)
            
            lbl_name = QLabel(name.upper())
            lbl_name.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: bold; letter-spacing: 1px;")
            
            lbl_val = QLabel("-")
            lbl_val.setStyleSheet("font-size: 22px; font-weight: bold; color: #3b82f6;")
            
            lbl_unit = QLabel(unit)
            lbl_unit.setStyleSheet("color: #cbd5e1; font-size: 10px;")

            kvbox.addWidget(lbl_name)
            kvbox.addWidget(lbl_val)
            kvbox.addWidget(lbl_unit)
            
            kpi_grid.addWidget(k_frame, 0, i)
            self.kpi_labels[key] = lbl_val

        dashboard_layout.addLayout(kpi_grid)
        dashboard_layout.addSpacing(10)

        # Charts
        chart_title = QLabel("Visual Analysis")
        chart_title.setObjectName("SectionTitle")
        dashboard_layout.addWidget(chart_title)
        
        chart_frame = QFrame()
        chart_frame.setObjectName("Card")
        chart_layout = QVBoxLayout(chart_frame)
        
        self.chart_canvas = ChartCanvas(self, width=5, height=6, dpi=100)
        chart_layout.addWidget(self.chart_canvas)
        
        dashboard_layout.addWidget(chart_frame)
        
        splitter.addWidget(dashboard_container)
        splitter.setSizes([250, 850])
        splitter.setCollapsible(0, False)
        
        main_layout.addWidget(splitter)

    def load_history(self):
        self.history_list.clear()
        try:
            history = get_history(self.token)
            for item in history:
                name = item.get('file_name', 'Unknown')
                date = item.get('uploaded_at', '').split('T')[0]
                self.history_list.addItem(f"{date}  |  {name}")
        except Exception as e:
            print(f"Error loading history: {e}")

    def on_upload(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV", "", "CSV Files (*.csv)")
        if not file_path:
            return

        try:
            filename = file_path.split("/")[-1]
            self.file_label.setText(f"Uploading: {filename}...")
            
            data = upload_csv(file_path, self.token)
            
            self.file_label.setText(f"File: {filename}")
            QMessageBox.information(self, "Success", "File uploaded successfully!")
            
            summary_data = data.get("summary", {})
            
            if not summary_data:
                QMessageBox.warning(self, "Warning", "Received empty summary data from server.")
                return

            self.dataset_id = data.get("dataset_id")
            self.download_btn.setEnabled(True)

            self.update_kpis(summary_data)
            self.update_charts(summary_data)
            
            self.load_history()
            
        except Exception as e:
            self.file_label.setText("Upload Failed")
            QMessageBox.critical(self, "Upload Error", str(e))

    def download_report(self):
        if not self.dataset_id:
            QMessageBox.warning(self, "Warning", "Please upload a dataset first.")
            return

        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Report", f"equipment_report_{self.dataset_id}.pdf", "PDF Files (*.pdf)"
            )
            
            if not file_path:
                return

            content = generate_report(self.token, self.dataset_id)

            with open(file_path, "wb") as f:
                f.write(content)
            
            QMessageBox.information(self, "Success", f"Report saved to {file_path}")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def update_kpis(self, data):
        # Format mapping for display
        formatters = {
            "total_equipment": lambda x: f"{x}",
            "average_flowrate": lambda x: f"{x:.2f}",
            "average_pressure": lambda x: f"{x:.2f}",
            "average_temperature": lambda x: f"{x:.2f}"
        }

        for key, label_widget in self.kpi_labels.items():
            if key in data:
                val = data[key]
                try:
                    text = formatters[key](val)
                except:
                    text = str(val)
                label_widget.setText(text)
            else:
                label_widget.setText("-")

    def update_charts(self, data):
        self.chart_canvas.update_charts(data)

class MainWindow(QMainWindow):
    def __init__(self, token):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer (Desktop)")
        self.setGeometry(100, 100, 1000, 800)
        self.token = token
        self.dataset_id = None
        self.init_ui()
        self.load_history()

    def init_ui(self):
        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # --- Top Section: Upload & File Info ---
        top_layout = QHBoxLayout()
        
        self.upload_btn = QPushButton("Upload New CSV")
        self.upload_btn.setStyleSheet("background-color: #2563eb; color: white; padding: 10px; font-weight: bold; border-radius: 5px;")
        self.upload_btn.clicked.connect(self.on_upload)
        top_layout.addWidget(self.upload_btn)

        self.download_btn = QPushButton("Download Report")
        self.download_btn.setStyleSheet("background-color: #10b981; color: white; padding: 10px; font-weight: bold; border-radius: 5px;")
        self.download_btn.setEnabled(False)
        self.download_btn.clicked.connect(self.download_report)
        top_layout.addWidget(self.download_btn)

        self.file_label = QLabel("No file uploaded")
        self.file_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #555; margin-left: 10px;")
        top_layout.addWidget(self.file_label)
        top_layout.addStretch()

        main_layout.addLayout(top_layout)

        # --- Content Splitter (Left: History, Right: Dashboard) ---
        splitter = QSplitter(Qt.Horizontal)
        
        # History Panel
        history_widget = QWidget()
        history_layout = QVBoxLayout(history_widget)
        history_layout.addWidget(QLabel("Upload History"))
        self.history_list = QListWidget()
        history_layout.addWidget(self.history_list)
        splitter.addWidget(history_widget)

        # Dashboard Panel
        dashboard_widget = QWidget()
        dashboard_layout = QVBoxLayout(dashboard_widget)

        # --- KPI Display Section ---
        kpi_frame = QFrame()
        kpi_frame.setFrameShape(QFrame.StyledPanel)
        kpi_frame.setStyleSheet("background-color: #f8f9fa; border-radius: 8px;")
        kpi_layout = QGridLayout(kpi_frame)
        dashboard_layout.addWidget(kpi_frame)

        self.kpi_labels = {}
        # Changed keys to match backend response keys (e.g., total_equipment)
        metrics = [
            ("Total Equipments", "total_equipment"),
            ("Avg Flowrate", "average_flowrate"),
            ("Avg Pressure", "average_pressure"),
            ("Avg Temperature", "average_temperature")
        ]

        for i, (name, key) in enumerate(metrics):
            vbox = QVBoxLayout()
            title_lbl = QLabel(name)
            title_lbl.setAlignment(Qt.AlignCenter)
            title_lbl.setStyleSheet("color: #666; font-size: 12px;")
            
            value_lbl = QLabel("-")
            value_lbl.setAlignment(Qt.AlignCenter)
            value_lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
            
            vbox.addWidget(title_lbl)
            vbox.addWidget(value_lbl)
            kpi_layout.addLayout(vbox, 0, i)
            self.kpi_labels[key] = value_lbl

        # --- Chart Visualization Section ---
        self.chart_canvas = ChartCanvas(self, width=5, height=6, dpi=100)
        dashboard_layout.addWidget(self.chart_canvas)

        splitter.addWidget(dashboard_widget)
        splitter.setSizes([200, 800]) # Initial sizes
        main_layout.addWidget(splitter)

    def load_history(self):
        self.history_list.clear()
        try:
            history = get_history(self.token)
            for item in history:
                name = item.get('file_name', 'Unknown')
                date = item.get('uploaded_at', '').split('T')[0]
                self.history_list.addItem(f"{date}: {name}")
        except Exception as e:
            print(f"Error loading history: {e}")

    def on_upload(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV", "", "CSV Files (*.csv)")
        if not file_path:
            return

        try:
            filename = file_path.split("/")[-1]
            self.file_label.setText(f"Uploading: {filename}...")
            
            data = upload_csv(file_path, self.token)
            
            self.file_label.setText(f"Current File: {filename}")
            QMessageBox.information(self, "Success", "File uploaded successfully!")
            
            # Backend response structure:
            # { "dataset_id": 1, "summary": { "total_equipment": ... } }
            # Access the nested 'summary' object
            summary_data = data.get("summary", {})
            
            if not summary_data:
                QMessageBox.warning(self, "Warning", "Received empty summary data from server.")
                return
                QMessageBox.warning(self, "Warning", "Received empty summary data from server.")
                return

            self.dataset_id = data.get("dataset_id")
            self.download_btn.setEnabled(True)

            self.update_kpis(summary_data)
            self.update_charts(summary_data)
            
            # Refresh history
            self.load_history()
            
        except Exception as e:
            self.file_label.setText("Upload Failed")
            self.file_label.setText("Upload Failed")
            QMessageBox.critical(self, "Upload Error", str(e))

    def download_report(self):
        if not self.dataset_id:
            QMessageBox.warning(self, "Warning", "Please upload a dataset first.")
            return

        try:
            # 1. Ask user where to save
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Report", f"equipment_report_{self.dataset_id}.pdf", "PDF Files (*.pdf)"
            )
            
            if not file_path:
                return

            # 2. Call API
            content = generate_report(self.token, self.dataset_id)

            # 3. Write file
            with open(file_path, "wb") as f:
                f.write(content)
            
            QMessageBox.information(self, "Success", f"Report saved to {file_path}")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def update_kpis(self, data):
        # Format mapping for display
        formatters = {
            "total_equipment": lambda x: f"{x}",
            "average_flowrate": lambda x: f"{x:.2f} L/min",
            "average_pressure": lambda x: f"{x:.2f} bar",
            "average_temperature": lambda x: f"{x:.2f} °C"
        }

        for key, label_widget in self.kpi_labels.items():
            if key in data:
                val = data[key]
                try:
                    text = formatters[key](val)
                except:
                    text = str(val)
                label_widget.setText(text)
            else:
                label_widget.setText("N/A")

    def update_charts(self, data):
        self.chart_canvas.update_charts(data)
