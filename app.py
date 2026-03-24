import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Oxygen-Hb Discovery Session", layout="wide")

st.title("🫁 Oxyhemoglobin Curve: Interactive Workshop")

def get_sao2(pa_o2_kpa):
    p_mmhg = pa_o2_kpa * 7.5006
    if p_mmhg <= 0: return 0
    return ((((p_mmhg**3 + 150*p_mmhg)**-1)*23400) + 1)**-1 * 100

# --- PHASE 1: LABELING ---
st.sidebar.header("Phase 1: Label the Graph")
x_label_input = st.sidebar.text_input("What is the X-axis?", "")
y_label_input = st.sidebar.text_input("What is the Y-axis?", "")

# --- PHASE 2: PLOTTING ---
st.sidebar.header("Phase 2: Plot the Points")
names = ["Doctor 1", "Doctor 2", "Doctor 3", "Doctor 4", "Doctor 5", "Doctor 6"]
inputs = []
for name in names:
    val = st.sidebar.number_input(f"{name} PaO2 (kPa)", 0.0, 20.0, value=0.0, step=0.1)
    inputs.append(val)

fig = go.Figure()

# Plot Fellows' points
for i, val in enumerate(inputs):
    if val > 0:
        sat = round(get_sao2(val), 1)
        fig.add_trace(go.Scatter(
            x=[val], y=[sat], 
            mode='markers+text',
            text=[f"{names[i]}<br>({val}, {sat}%)"], 
            textposition="top center",
            marker=dict(size=18, color='crimson', symbol='circle'),
            showlegend=False
        ))

# AXIS CONFIGURATION (0-14 with 2 kPa gaps)
fig.update_layout(
    xaxis_title=x_label_input if x_label_input else "???",
    yaxis_title=y_label_input if y_label_input else "???",
    xaxis=dict(
        range=[0, 14], 
        tickvals=[0, 2, 4, 6, 8, 10, 12, 14], # Your requested 2 kPa gaps
        showgrid=True,
        gridcolor='lightgray'
    ),
    yaxis=dict(
        range=[0, 105], 
        tickvals=[0, 25, 50, 75, 100],
        showgrid=True,
        gridcolor='lightgray'
    ),
    height=750,
    template="plotly_white"
)

# REVEAL THE CURVE
reveal = st.checkbox("FINAL STEP: Reveal the Sigmoid Curve")
if reveal:
    x_curve = np.linspace(0, 14, 500)
    y_curve = [get_sao2(x) for x in x_curve]
    fig.add_trace(go.Scatter(x=x_curve, y=y_curve, name='Standard Curve', 
                             line=dict(color='black', width=3)))

st.plotly_chart(fig, use_container_width=True)
