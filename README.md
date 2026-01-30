# Chemical Equipment Visualizer

A comprehensive full-stack solution for analyzing and visualizing chemical equipment parameters. This project includes a robust Django backend, a modern React web dashboard, and a native PyQt5 desktop application.

## 🚀 Overview

The **Chemical Equipment Visualizer** allows engineers and operators to upload CSV datasets containing equipment metrics (Flowrate, Pressure, Temperature). The system processes this data to provide instant visual insights, statistical summaries, and downloadable PDF reports.

## ✨ Features

### Core Functionality
- **CSV Data Ingestion**: Robust parsing of equipment datasets.
- **Automated Analysis**: Instant calculation of averages (flow, pressure, temp) and equipment counts.
- **PDF Reporting**: Server-side generation of detailed PDF reports compatible with both Web and Desktop clients.
- **Secure Authentication**: Token-based login and registration system.

### 🌐 Web Dashboard (React)
- **Modern UI**: Clean, responsive dashboard styled with a custom CSS theme.
- **Visualizations**:
  - KPI Cards for quick metrics.
  - Interactive Charts for parameter averages and type distribution.
  - Upload Trend analysis.
- **User Experience**: Drag-and-drop file upload, instant feedback, and history tracking.

![Web Dashboard Screenshot](Web%20Based%20Application/images/web.png)


### 🖥 Desktop Application (PyQt5)
- **Native Experience**: Fast and responsive desktop interface.
- **Integrated Plotting**: Embedded Matplotlib charts for high-fidelity data visualization.
- **Seamless Sync**: Shares the same backend and history with the web platform.
- **Professional Styling**: Polished QSS (Qt Stylesheets) for a modern look.

![Desktop Application Screenshot](Web%20Based%20Application/images/desktop.png)

## 🛠 Tech Stack

| Component | Technologies |
|-----------|--------------|
| **Backend** | Django, Django REST Framework (DRF), Pandas, ReportLab, SQLite |
| **Web Frontend** | React.js, Axios, Chart.js / Recharts, CSS Variables |
| **Desktop App** | Python, PyQt5, Matplotlib, Requests |

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.9+
- Node.js & npm

### 1. Backend Setup (Django)

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   cd server
   python manage.py migrate
   ```
5. Start the server:
   ```bash
   python manage.py runserver
   ```
   *The backend will run at `http://127.0.0.1:8000/`*

### 2. Web Frontend Setup (React)

1. Navigate to the web directory:
   ```bash
   cd web/chemical_equipment_web
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm start
   ```
   *The web app will open at `http://localhost:3000/`*

### 3. Desktop Application Setup (PyQt5)

1. Navigate to the desktop directory:
   ```bash
   cd desktop
   ```
2. Ensure you have the required Python libraries (you can install them in the same venv as backend if preferred, or separately):
   ```bash
   pip install PyQt5 requests matplotlib
   ```
3. Run the application:
   ```bash
   python main.py
   ```

---

## 📖 Usage Guide

1. **Register/Login**: Create an account or log in with existing credentials.
2. **Upload Data**: 
   - Use the **Web Dashboard** drag-and-drop area.
   - Or use the **Desktop App** "Upload New CSV" button.
   - *Sample CSV format*: `Equipment Name, Type, Flowrate, Pressure, Temperature`.
3. **Analyze**: View the generated KPIs and Charts immediately after upload.
4. **Report**: Click "Download Report" to get a PDF summary of the current dataset.
5. **History**: View past uploads in the sidebar (Web) or left panel (Desktop).

## 📂 Project Structure

```
├── backend/               # Django Backend
│   ├── requirements.txt   # Python Dependencies
│   └── server/            # Django Project & App
├── web/                   # React Frontend
│   └── chemical_equipment_web/
│       ├── src/
│       │   ├── components/# React UI Components (Card, KPI, etc.)
│       │   ├── styles/    # Global Theme (theme.css)
│       │   └── services/  # API Integration
├── desktop/               # PyQt5 Desktop App
│   ├── main.py            # Entry Point
│   ├── ui.py              # UI Layout & QSS Styling
│   ├── charts.py          # Matplotlib Integration
│   └── api.py             # Backend Communication
└── README.md              # Project Documentation
```
