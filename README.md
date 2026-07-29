# ⚡ GridSense: Smart Micro-Grid Command Center

**GridSense** is a **Predictive, Equitable, and Privacy-First Micro-Grid Defense System.** Built for hackathons and energy innovation challenges, this project simulates a 50-node neighborhood grid and uses Machine Learning to forecast and prevent catastrophic transformer overloads.

\---

### 📖 The Problem vs. The GridSense Solution

#### The Problem

Traditional power grids are **reactive**. When a heatwave hits and neighborhood load exceeds transformer capacity, the transformer blows, causing a localized blackout. Furthermore, trying to prevent this usually involves invasive whole-home energy monitoring, which violates consumer privacy.

#### The Solution

GridSense introduces a **Predictive Digital Twin** built on an **Opt-In Privacy Architecture.**

* **Predictive:** It uses Scikit-Learn's Linear Regression on a sliding time-series window to predict power spikes before they happen.
* **Equitable:** It prevents overloads by temporarily pausing heavy, non-essential loads (like water geysers). It uses a mathematically equitable algorithm (inspired by **Jain's Fairness Index**) to ensure no single home bears the burden of grid defense.
* **Private:** It only tracks and interacts with voluntarily enrolled smart plugs, completely ignoring the rest of the household's private energy data.

\---

### ✨ Key Features

* 🏘️ **50-Node Digital Twin:** A live physics engine simulating 50 virtual homes, calculating base loads, AC surges during heatwaves, and Vehicle-to-Grid (V2G) EV battery discharging.
* 📈 **Live AI Forecasting:** Real-time Plotly charts displaying actual power demand vs. the AI-predicted **"Ghost Line"** (5 seconds into the future).
* 🤖 **Equitable Edge Logic:** A simulated Edge Node that intercepts predicted overloads (> 100kW limit) and surgically pauses the *least-recently-paused* Geysers to save the grid.
* ⏱️ **Self-Healing \& Auto-Revert:** The system features a built-in auto-revert mechanism. After a simulated crisis (like a 30-second heatwave) concludes, the AI automatically restores baseline weather conditions and safely powers paused appliances back on.
* 🎛️ **Command Center UI:** A stunning dark-mode Streamlit dashboard featuring an AI Action Ledger, Before/After impact metrics, and a 50-node virtual LED status panel.

\---

### 🏗️ Architecture \& Data Flow

The project is broken into three lightweight, 100% Python components to ensure maximum stability and ease of deployment:

|File|Role|Responsibility|
|-|-|-|
|`simulation.py`|**The Physics Engine**|Generates the virtual neighborhood. Tracks `current_temp`, manages AC surges, and calculates the live aggregate power load.|
|`edge_node.py`|**The Virtual Brain**|Acts as the simulated local transformer microchip. Receives the AI's prediction, checks if the 100kW threshold is breached, and calculates the fairest house to pause based on historical `cut_counts`.|
|`app.py`|**The Command Center**|The Streamlit frontend. Runs the continuous data loop, executes the scikit-learn predictive model, handles UI rendering, and logs the AI's decision-making process.|

```
[ simulation.py ]  ──►  [ app.py (AI Predictor) ]  ──►  [ edge_node.py ]
  50 Virtual Houses         Linear Regression               Fairness Scheduler
  Heatwave Physics          Ghost Line Forecast             Min-Cut Selection
  V2G Discharging           Threshold Check                 Geyser Pause/Resume
        ▲                         │                               │
        └─────────────────────────┴───────────────────────────────┘
                        State feedback loop
```

\---

### 🚀 Installation \& Quick Start

🔥 Try it right now: https://gridsense-esp32-ezjvvsfaakashvb5sfxssn.streamlit.app/

GridSense is also designed to run completely locally on your own machine without complex database setups.

## 🎥 GridSense Demo Video

https://drive.google.com/file/d/1jkNMzStuFfsnSDN0qe4BXRkxuVNcVk5m/view?usp=drive_link

#### 1\. Clone the Repository

```bash
git clone https://github.com/YourUsername/GridSense.git
cd GridSense
```

#### 2\. Install Dependencies

Make sure you have Python 3.9+ installed, then run:

```bash
pip install -r requirements.txt
```

#### 3\. Run the Dashboard

```bash
streamlit run app.py
```

\---

### 🎮 Interactive Demo Guide

Once the dashboard opens in your browser (`http://localhost:8501`):

1. **Watch the baseline** — Observe the total load hovering around 60–80 kW in the **"Safe"** green zone.
2. **Trigger a Heatwave** — Click the 🔥 **Simulate Heatwave (40°C)** button.
3. **Observe the AI Defense:**

   * Watch the yellow dashed **"AI Forecast"** (Ghost Line) spike above the 100kW red limit.
   * See the **Grid Status** turn to `🟢 SECURED`.
   * Read the **AI Action Ledger** as it actively pauses geysers.
   * Look at the **50-Node Virtual LED Panel** to see individual homes turn from **Orange** (Geyser ON) to **Neon Blue** (🤖 PAUSED).
4. **Watch the Auto-Revert** — After 30 seconds, the heatwave will automatically end, dynamically returning the weather to normal and safely powering the paused appliances back on — *without human intervention.*

\---

### 🛠️ Built With

|Library|Purpose|
|-|-|
|[Streamlit](https://streamlit.io/)|Reactive, pure-Python web frontend|
|[Scikit-Learn](https://scikit-learn.org/)|Time-series Linear Regression forecasting|
|[Plotly](https://plotly.com/)|High-performance, real-time data visualization|
|[NumPy](https://numpy.org/)|Matrix reshaping and fast array operations|

### 🎯 Conclusion:
GridSense proves that smart grids can prevent blackouts without relying on invasive consumer surveillance. By combining predictive machine learning with fair load-shedding algorithms, it creates a self-healing micro-grid.

This project successfully demonstrates proactive resilience, algorithmic equity, and data privacy—offering a lightweight, highly practical blueprint for the future of automated and sustainable energy distribution.
