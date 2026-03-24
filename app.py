import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Oxygen-Hb Curve Training", layout="wide")

st.title("🫁 Interactive Oxyhemoglobin Curve: The Steep Zone")
st.markdown("### Focus: $PaO_2$ 3.6 to 8.8 kPa")

def get_sao2(pa_o2_kpa):
    p_mmhg = pa_o2_kpa * 7.5006
    if p_mmhg <= 0: return 0
    return ((((p_mmhg**3 + 150*p_mmhg)**-1)*23400) + 1)**-1 * 100

# Sidebar with 6 Doctor Slots
st.sidebar.header("Fellows' Data Entry")
names = ["Dr. 1 (P50)", "Dr. 2 (75%)", "Dr. 3 (90%)", "Dr. 4 (Arterial)", "Dr. 5", "Dr. 6"]
inputs = []

for name in names:
    val = st.sidebar.number_input(f"{name} (kPa)", 0.0, 20.0, value=0.0, step=0.1)
    inputs.append(val)

# Generate Curve
x_vals = np.linspace(0, 20, 500)
y_vals = [get_sao2(x) for x in x_vals]

fig = go.Figure()

# Background Curve
fig.add_trace(go.Scatter(x=x_vals, y=y_vals, name='Physiological Curve', 
                         line=dict(color='royalblue', width=5)))

# Plotting Fellows' points
for i, val in enumerate(inputs):
    if val > 0:
        fig.add_trace(go.Scatter(x=[val], y=[get_sao2(val)], mode='markers+text',
                                 text=[names[i]], textposition="top left",
                                 marker=dict(size=15, color='red', line=dict(width=2, color='white')),
                                 showlegend=False))

# VISUAL SETTINGS FOR STEEPNESS
fig.update_layout(
    xaxis_title="PaO2 (kPa)",
    yaxis_title="SaO2 (%)",
    # Zooming in on 0-12 kPa makes the 3.6-8.8 range look very steep
    xaxis=dict(range=[0, 12], dtick=1, gridcolor='LightPink'), 
    yaxis=dict(range=[0, 105], tickvals=[0, 25, 50, 75, 90, 100], gridcolor='LightPink'),
    height=800, # Tall height + narrow X-axis = extreme steepness
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# Comparison Table
st.info(f"Critical Zone: 3.7 kPa (P50) → 5.6 kPa (75%) → 8.0 kPa (90%)")
