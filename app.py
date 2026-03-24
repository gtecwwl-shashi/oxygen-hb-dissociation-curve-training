import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Oxygen-Hb Exam Simulation", layout="wide")

st.title("🫁 Oxyhemoglobin Curve: Exam Mode")
st.markdown("### Challenge: Plot the key points of the curve from memory.")

def get_sao2(pa_o2_kpa):
    p_mmhg = pa_o2_kpa * 7.5006
    if p_mmhg <= 0: return 0
    return ((((p_mmhg**3 + 150*p_mmhg)**-1)*23400) + 1)**-1 * 100

# Sidebar for Fellows' Inputs
st.sidebar.header("Exam Data Entry")
names = ["Doctor A", "Doctor B", "Doctor C", "Doctor D", "Doctor E", "Doctor F"]
inputs = []

for name in names:
    val = st.sidebar.number_input(f"{name} - Pick a PaO2 (kPa)", 0.0, 20.0, value=0.0, step=0.1)
    inputs.append(val)

# Generate Data for the "Reveal" (hidden until you check the box)
x_vals = np.linspace(0, 20, 500)
y_vals = [get_sao2(x) for x in x_vals]

fig = go.Figure()

# Plot Fellows' points ONLY
for i, val in enumerate(inputs):
    if val > 0:
        sat = round(get_sao2(val), 1)
        fig.add_trace(go.Scatter(
            x=[val], y=[sat], 
            mode='markers+text',
            text=[f"{names[i]}<br>({val} kPa)"], 
            textposition="top center",
            marker=dict(size=18, color='crimson', symbol='circle'),
            showlegend=False
        ))

# EXAM FORMATTING: No background lines, no reference curve
fig.update_layout(
    xaxis_title="PaO2 (kPa)",
    yaxis_title="SaO2 (%)",
    xaxis=dict(
        range=[0, 15], 
        showgrid=False, # Removed grid for exam mode
        tickvals=[0, 2.5, 5, 8, 10, 15] # The requested gaps
    ),
    yaxis=dict(
        range=[0, 105], 
        showgrid=False, # Removed grid for exam mode
        tickvals=[0, 25, 50, 75, 100]
    ),
    height=750,
    template="plotly_white",
    plot_bgcolor='white'
)

# REVEAL TOGGLE: Only shows the curve when you are ready to mark them
reveal = st.checkbox("REVEAL CORRECT SIGMOID CURVE")
if reveal:
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, name='Correct Curve', 
                             line=dict(color='black', width=3)))

st.plotly_chart(fig, use_container_width=True)
