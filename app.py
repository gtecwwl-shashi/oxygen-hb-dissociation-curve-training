import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Oxygen-Hb Curve Training", layout="wide")

st.title("Oxyhemoglobin Dissociation Curve Interactive")
st.markdown("### Fellows: Enter your PaO2 (kPa) to plot your point")

# Function for the standard curve (Severinghaus)
def get_sao2(pa_o2_kpa):
    p_mmhg = pa_o2_kpa * 7.5006
    if p_mmhg <= 0: return 0
    return ((((p_mmhg**3 + 150*p_mmhg)**-1)*23400) + 1)**-1 * 100

# Create inputs for 6 doctors in the sidebar
st.sidebar.header("Data Entry")
names = ["Dr. 1", "Dr. 2", "Dr. 3", "Dr. 4", "Dr. 5", "Dr. 6"]
inputs = []
for name in names:
    inputs.append(st.sidebar.number_input(f"{name} (kPa)", 0.0, 20.0, 0.0, step=0.1))

# Generate the true curve line
x_vals = np.linspace(0, 20, 200)
y_vals = [get_sao2(x) for x in x_vals]

fig = go.Figure()

# Add the correct physiological curve
fig.add_trace(go.Scatter(x=x_vals, y=y_vals, name='Standard Curve', line=dict(color='gray', dash='dash')))

# Add the doctors' points
y_points = [get_sao2(i) for i in inputs if i > 0]
x_points = [i for i in inputs if i > 0]
fig.add_trace(go.Scatter(x=x_points, y=y_points, mode='markers+text', 
                         text=names[:len(x_points)], textposition="top center",
                         marker=dict(size=12, color='red'), name="Fellows' Points"))

fig.update_layout(xaxis_title="PaO2 (kPa)", yaxis_title="SaO2 (%)",
                  xaxis=dict(range=[0, 20], dtick=2), yaxis=dict(range=[0, 105]))

st.plotly_chart(fig, use_container_width=True)

# Landmarks Table
st.markdown("---")
st.markdown("### Reference Landmarks")
st.table({"Point": ["P50", "Venous (75%)", "Arterial (98%)"], "PaO2 (kPa)": [3.7, 5.6, 13.3]})
