import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Oxygen-Hb Curve Training", layout="wide")

st.title("🫁 Interactive Oxyhemoglobin Curve (Steep View)")
st.markdown("### Focus: The critical 0-10 kPa range")

# Severinghaus function for SaO2 calculation
def get_sao2(pa_o2_kpa):
    p_mmhg = pa_o2_kpa * 7.5006
    if p_mmhg <= 0: return 0
    # Standard equation for the curve
    return ((((p_mmhg**3 + 150*p_mmhg)**-1)*23400) + 1)**-1 * 100

st.sidebar.header("Plotting Session")
st.sidebar.info("Assign each doctor a kPa value to see where it lands.")

names = ["Dr. 1 (P50)", "Dr. 2 (Venous)", "Dr. 3 (Shoulder)", "Dr. 4 (Arterial)", "Dr. 5", "Dr. 6"]
inputs = []
# Default values provided to help guide the steep curve shape
defaults = [3.7, 5.6, 8.0, 13.3, 2.5, 1.0] 

for i, name in enumerate(names):
    val = st.sidebar.number_input(f"{name} PaO2", 0.0, 15.0, value=0.0, step=2.5)
    inputs.append(val)

# Generate the true curve line
x_vals = np.linspace(0, 20, 300)
y_vals = [get_sao2(x) for x in x_vals]

fig = go.Figure()

# The physiological curve
fig.add_trace(go.Scatter(x=x_vals, y=y_vals, name='Physiological Curve', 
                         line=dict(color='royalblue', width=4)))

# The fellows' points
x_points = [i for i in inputs if i > 0]
y_points = [get_sao2(i) for i in x_points]
fig.add_trace(go.Scatter(x=x_points, y=y_points, mode='markers+text', 
                         text=[names[i] for i, v in enumerate(inputs) if v > 0],
                         textposition="top left",
                         marker=dict(size=14, color='red', symbol='circle'), 
                         name="Fellows' Points"))

# STEEP VIEW: We limit the visible range to 0-15 kPa to make the 0-10 section look larger
fig.update_layout(
    xaxis_title="Partial Pressure (PaO2 in kPa)",
    yaxis_title="Saturation (SaO2 %)",
    xaxis=dict(range=[0, 15], dtick=1), # Zoomed in for a steeper look
    yaxis=dict(range=[0, 105], tickvals=[0, 25, 50, 75, 90, 100]),
    height=700,
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

st.success("💡 Discussion Point: Notice how the curve is almost vertical between 2 and 7 kPa!")
