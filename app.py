import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Oxygen-Hb Masterclass", layout="wide")

st.title("🫁 Oxyhemoglobin Curve: The Discovery Canvas")
st.markdown("### Step 1: Label the Axes | Step 2: Set the Scale | Step 3: Plot")

def get_sao2(pa_o2_kpa):
    p_mmhg = pa_o2_kpa * 7.5006
    if p_mmhg <= 0: return 0
    # Standard Severinghaus Equation
    return ((((p_mmhg**3 + 150*p_mmhg)**-1)*23400) + 1)**-1 * 100

# --- SIDEBAR PHASE 1: THE AXES ---
st.sidebar.header("1. Axis Identification")
x_label = st.sidebar.text_input("Trainee Guess: X-axis Label", "")
y_label = st.sidebar.text_input("Trainee Guess: Y-axis Label", "")
show_scale = st.sidebar.checkbox("Reveal Numeric Scale (0-14 kPa)", value=False)

# --- SIDEBAR PHASE 2: THE FELLOWS' PLOTS ---
st.sidebar.header("2. Fellows' Points")
st.sidebar.info("Enter the PaO2 values provided by 6 trainees:")
names = ["Dr. 1", "Dr. 2", "Dr. 3", "Dr. 4", "Dr. 5", "Dr. 6"]
inputs = []
for name in names:
    val = st.sidebar.number_input(f"{name} PaO2 (kPa)", 0.0, 14.0, value=0.0, step=0.1)
    inputs.append(val)

fig = go.Figure()

# Plot Fellows' points as they are entered
for i, val in enumerate(inputs):
    if val > 0:
        actual_sat = round(get_sao2(val), 1)
        fig.add_trace(go.Scatter(
            x=[val], y=[actual_sat], 
            mode='markers+text',
            text=[f"{names[i]}"], 
            textposition="top center",
            marker=dict(size=18, color='crimson', symbol='diamond'),
            showlegend=False
        ))

# AXIS CONFIGURATION
fig.update_layout(
    xaxis_title=x_label if x_label else "???",
    yaxis_title=y_label if y_label else "???",
    xaxis=dict(
        range=[0, 14], 
        tickvals=[0, 2, 4, 6, 8, 10, 12, 14] if show_scale else [],
        showgrid=show_scale,
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=3
    ),
    yaxis=dict(
        range=[0, 105], 
        tickvals=[0, 25, 50, 75, 100] if show_scale else [],
        showgrid=show_scale,
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=3
    ),
    height=750,
    template="plotly_white",
    plot_bgcolor='white'
)

# --- FINAL REVEAL ---
reveal = st.checkbox("REVEAL PHYSIOLOGICAL CURVE")
if reveal:
    x_curve = np.linspace(0.1, 14, 500)
    y_curve = [get_sao2(x) for x in x_curve]
    fig.add_trace(go.Scatter(x=x_curve, y=y_curve, name='Correct Curve', 
                             line=dict(color='black', width=4)))

st.plotly_chart(fig, use_container_width=True)
