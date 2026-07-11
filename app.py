import streamlit as st
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression
import simulation
import edge_node
import time
from datetime import datetime

HEATWAVE_DURATION_SECONDS = 30  # auto-revert after this long

# --- AI PREDICTOR ---
def predict_future_load(history_list):
    X = np.arange(len(history_list)).reshape(-1, 1)
    y = np.array(history_list)
    model = LinearRegression()
    model.fit(X, y)
    future_time_step = np.array([[len(history_list) + 4]])
    predicted_value = model.predict(future_time_step)
    return predicted_value[0]

# --- UI SETUP ---
st.set_page_config(page_title="Grid Sense Dashboard", layout="wide")

FONT = "'Courier Prime', 'Special Elite', 'Courier New', Courier, monospace"

st.markdown(
    "<style>"
    "@import url('https://fonts.googleapis.com/css2?family=Courier+Prime:wght@400;700&family=Special+Elite&display=swap');"
    ".stApp { background-color: #121212; }"
    ".block-container { padding-top: 4.5rem; padding-bottom: 1rem; }"
    "[data-testid='stHeader'] {"
    "  background-color: #121212 !important;"
    "  border-bottom: 1px solid #222222 !important;"
    "}"
    "[data-testid='stHeader'] * {"
    "  color: #ffffff !important;"
    "  fill: #ffffff !important;"
    "}"
    f"html, body, [class*='st-'], .stMarkdown, .stApp * {{ font-family: {FONT} !important; }}"
    "html, body, [class*='st-'], .stMarkdown, .stApp, label {"
    "  color: #ffffff !important;"
    "}"
    "div.stButton > button {"
    "  background-color: #333333; color: white !important;"
    "  font-weight: bold; border: none; border-radius: 4px; padding: 8px 14px;"
    "}"
    "div.stButton > button:hover { background-color: #444444; color: white !important; border: none; }"
    "</style>",
    unsafe_allow_html=True
)

st.markdown(
    f"<div style='font-family:{FONT};font-weight:bold;font-size:56px;"
    "color:#00ffff;text-align:center;letter-spacing:6px;padding:0;margin:0;"
    "text-shadow: 0 0 15px rgba(0, 255, 255, 0.4);'>"
    "GRID SENSE</div>"
    f"<div style='font-family:{FONT};font-weight:bold;font-size:18px;"
    "color:#ffffff;text-align:center;padding:2px 0 14px 0;letter-spacing:1px;'>"
    "⚡ 50-Node Neighborhood Digital Twin — Command Center</div>",
    unsafe_allow_html=True
)

if "history" not in st.session_state:
    st.session_state.history = []
if "event_log" not in st.session_state:
    st.session_state.event_log = ["System Booting... Grid is stable."]
if "heatwave_start" not in st.session_state:
    st.session_state.heatwave_start = None

section_style = f"font-family:{FONT};font-weight:bold;font-size:16px;color:white;margin-top:6px;"


@st.fragment(run_every=2.5)
def live_dashboard():
    # --- AUTO-REVERT HEATWAVE ---
    if st.session_state.heatwave_start is not None:
        elapsed = time.time() - st.session_state.heatwave_start
        if elapsed >= HEATWAVE_DURATION_SECONDS:
            simulation.current_temp = 30
            for house in simulation.houses:
                if house.get('paused_by_ai', False):
                    house['geyser_on'] = True
                    house['paused_by_ai'] = False
            st.session_state.heatwave_start = None
            timestamp = datetime.now().strftime("%H:%M:%S")
            st.session_state.event_log.insert(0, f"[{timestamp}] 🌤️ Heatwave ended — Grid returned to Normal Day automatically.")

    # --- RUN SIMULATION STEP ---
    current_load = simulation.get_current_load()
    st.session_state.history.append(current_load)

    if len(st.session_state.history) >= 10:
        recent_window = st.session_state.history[-10:]
        predicted_load = predict_future_load(recent_window)
    else:
        predicted_load = current_load

    # --- AI DECISION (Local logic only) ---
    target_house_index = None
    fallback_house = edge_node.check_and_act(predicted_load)
    if fallback_house is not None:
        target_house_index = fallback_house - 1

    if target_house_index is not None:
        simulation.houses[target_house_index]['geyser_on'] = False
        simulation.houses[target_house_index]['paused_by_ai'] = True

        timestamp = datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] ⚠️ Overload Predicted ({predicted_load:.1f}kW)! [AI] pausing Geyser at House #{target_house_index + 1}."
        st.session_state.event_log.insert(0, log_msg)

    paused_count = sum(1 for house in simulation.houses if house.get('paused_by_ai', False))
    unmanaged_load = current_load + (paused_count * 2.0)

    # --- VIRTUAL ALERT LED ---
    alert_active = current_load > 100.0 or predicted_load > 100.0
    alert_color = "#ffd93b" if alert_active else "#333333"
    alert_glow = "box-shadow: 0 0 14px #ffd93b;" if alert_active else ""

    heatwave_badge = ""
    if st.session_state.heatwave_start is not None:
        remaining = max(0, HEATWAVE_DURATION_SECONDS - int(time.time() - st.session_state.heatwave_start))
        heatwave_badge = (
            f"<span style='margin-left:20px; color:#ff9900; font-size:12px;'>"
            f"🔥 Heatwave active — auto-reverts in {remaining}s</span>"
        )

    st.markdown(
        f"<div style='display:flex; align-items:center; gap:10px; margin-bottom:10px;'>"
        f"<div style='width:20px; height:20px; border-radius:50%; background:{alert_color}; {alert_glow}'></div>"
        f"<span style='color:#aaaaaa; font-size:13px; letter-spacing:1px;'>GRID ALERT LED</span>"
        f"{heatwave_badge}"
        f"</div>",
        unsafe_allow_html=True
    )

    # --- DRAW METRICS ---
    col1, col2, col3 = st.columns(3)

    box_style = (
        "background-color:#121212;border:1px solid #333;border-radius:8px;"
        f"padding:10px 8px;text-align:center;font-family:{FONT};"
    )
    label_style = "color:#aaaaaa;font-size:12px;letter-spacing:1px;text-transform:uppercase;"
    value_style = "font-size:20px;font-weight:bold;"

    if current_load > 100.0 or predicted_load > 100.0:
        status_text = f"<span style='color:#ff3333;'>⚠️ OVERLOADED ({current_load:.1f} kW)</span>"
    elif paused_count > 0:
        status_text = f"<span style='color:#00ffff;'>🟢 SECURED ({current_load:.1f} kW)</span>"
    else:
        status_text = f"<span style='color:#00ff00;'>🟢 SAFE ({current_load:.1f} kW)</span>"

    with col1:
        st.markdown(
            f"<div style='{box_style}'>"
            f"<div style='{label_style}'>⚡ Grid Status</div>"
            f"<div style='{value_style}'>{status_text}</div>"
            f"</div>",
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"<div style='{box_style}'>"
            f"<div style='{label_style}'>🤖 AI Impact (Before vs After)</div>"
            f"<div style='{value_style}'><span style='color:#ff3333;'>{unmanaged_load:.1f} kW</span> vs <span style='color:#00ff00;'>{current_load:.1f} kW</span></div>"
            f"</div>",
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"<div style='{box_style}'>"
            f"<div style='{label_style}'>🔌 AI Control Activity</div>"
            f"<div style='{value_style} color:#00ffff;'>{paused_count} / 50 Geysers Paused</div>"
            f"</div>",
            unsafe_allow_html=True
        )

    st.markdown(f"<div style='{section_style}'>Weather Controls</div>", unsafe_allow_html=True)
    if st.button("🔥 Simulate Heatwave (40°C)", use_container_width=True, key="heatwave_btn"):
        simulation.current_temp = 40
        st.session_state.heatwave_start = time.time()
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.event_log.insert(0, f"[{timestamp}] 🔥 Heatwave triggered manually — will auto-revert in {HEATWAVE_DURATION_SECONDS}s.")

    col_chart, col_grid, col_log = st.columns([2, 2, 1])

    with col_chart:
        st.markdown(f"<div style='{section_style}'>📈 Live Power Demand</div>", unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=st.session_state.history, mode="lines", name="Load", line=dict(color="#00ff00", width=3)))

        if len(st.session_state.history) >= 10:
            last_x = len(st.session_state.history) - 1
            last_y = st.session_state.history[-1]
            fig.add_trace(go.Scatter(
                x=[last_x, last_x + 4],
                y=[last_y, predicted_load],
                mode="lines+markers",
                name="AI Forecast",
                line=dict(color="#ffff00", dash="dot")
            ))

        fig.add_hline(y=100, line_dash="dash", line_color="red", annotation_text="Transformer Limit (100 kW)")
        fig.add_hrect(y0=100, y1=150, fillcolor="red", opacity=0.15, line_width=0)
        fig.update_layout(
            xaxis_title="Time (seconds)",
            yaxis_title="Load (kW)",
            template="plotly_dark",
            paper_bgcolor="#121212",
            plot_bgcolor="#121212",
            font=dict(family="Courier Prime, Special Elite, Courier New, Courier, monospace"),
            margin=dict(l=0, r=0, t=10, b=50),
            height=360,
            legend=dict(orientation="h", yanchor="bottom", y=-0.35, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig, use_container_width=True, key="load_chart")

    with col_log:
        st.markdown(f"<div style='{section_style}'>🤖 AI Action Ledger</div>", unsafe_allow_html=True)
        log_text = "<br><br>".join(st.session_state.event_log[:6])
        log_style = (
            "background-color:#1e1e1e;border-left:4px solid #00ffff;border-radius:6px;"
            f"padding:12px;font-family:{FONT};font-size:13px;line-height:1.5;"
            "color:#ffffff;height:340px;overflow-y:auto;"
        )
        st.markdown(f"<div style='{log_style}'>{log_text}</div>", unsafe_allow_html=True)

    with col_grid:
        st.markdown(f"<div style='{section_style}'>🏘️ Neighborhood (Virtual LED Panel — 50 Houses)</div>", unsafe_allow_html=True)
        boxes = []
        for house in simulation.houses:
            if house.get('paused_by_ai', False):
                bg_color = "#00d2ff"
                status = "🤖 PAUSED"
                text_color = "#121212"
            elif house['geyser_on']:
                bg_color = "#ff9900"
                status = "Geyser ON"
                text_color = "white"
            else:
                bg_color = "#1e3d2f"
                status = "Geyser OFF"
                text_color = "white"

            ev_status = "🚗 EV" if house['ev_plugged_in'] else "No EV"

            box = (
                f"<div style='background-color: {bg_color}; color: {text_color}; padding: 6px; "
                f"border-radius: 5px; width: 62px; text-align: center; font-family: {FONT};'>"
                f"<b>H{house['id']}</b><br>"
                f"<span style='font-size: 9px; font-weight: bold;'>{status}</span><br>"
                f"<span style='font-size: 9px;'>{ev_status}</span>"
                f"</div>"
            )
            boxes.append(box)

        grid_html = (
            "<div style='background-color:#1e1e1e;border-radius:8px;padding:10px;"
            "height:340px;overflow-y:auto;'>"
            "<div style='display: flex; flex-wrap: wrap; gap: 8px;'>"
            + "".join(boxes) +
            "</div></div>"
        )
        st.markdown(grid_html, unsafe_allow_html=True)


live_dashboard()