import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Oxygen-Hb Interactive Quiz", layout="wide")

st.title("🫁 Oxyhemoglobin Curve: Fellows' Interactive Plot")
st.markdown("### Instructions: Each Fellow picks a PaO2 value to see where it lands on the curve.")

def get_sao2(pa_o2_kpa):
    p_mmhg = pa_o2_kpa * 7.5006
    if p_mmhg <= 0: return 0
    return ((((p_mmhg**3 + 150*p_mmhg)**-1)*23400) + 1)**-1 * 100

# Sidebar for the Live Quiz
st.sidebar.header("Fellows' Input")
st.sidebar.write("Enter the PaO2 (kPa) as discussed:")

names = ["Dr. 1 (P50 Target)", "Dr. 2 (75% Target)", "Dr. 3 (90% Target)", "Dr. 4 (Arterial)", "Dr. 5 (Venous)", "Dr. 6 (Critical)"]
inputs = []

for name in names:
    # We start at 0.0 so the graph starts empty
    val = st.sidebar.number_input(f"{name}", 0.0, 20.0, value=0.0, step=0.1)
    inputs.append(val)

# Generate Base Curve
x_vals = np.linspace(0, 20, 500)
y_vals = [get_sao2(x) for x in x_vals]

fig = go.Figure()

# Plot the theoretical curve in a faint gray to guide them
fig.add_trace(go.Scatter(x=x_vals, y=y_vals, name='Reference Curve', 
                         line=dict(color='lightgray', width=2, dash='dot')))

# Plot Fellows' points with specific X and Y labels
for i, val in enumerate(inputs):
    if val > 0:
        sat = round(get_sao2(val), 1)
        fig.add_trace(go.Scatter(
            x=[val], y=[sat], 
            mode='markers+text',
            text=[f"{names[i]}<br>({val} kPa, {sat}%)"], 
            textposition="top center",
            marker=dict(size=15, color='red', symbol='diamond'),
            showlegend=False
        ))

# Custom X-axis gaps as requested
fig.update_layout(
    xaxis_title="Partial Pressure of Oxygen (PaO2 in kPa)",
    yaxis_title="Oxygen Saturation (SaO2 %)",
    xaxis=dict(
        range=[0, 15], 
        tickvals=[0, 2.5, 5, 8, 10, 15], 
        gridcolor='whitesmoke'
    ),
    yaxis=dict(
        range=[0, 105], 
        tickvals=[0, 25, 50, 75, 90, 100], 
        gridcolor='whitesmoke'
    ),
    height=750,
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# Interactive Legend for the teacher
with st.expander("Show Correct Answer Key"):
    st.write("3.7 kPa = 50% | 5.6 kPa = 75% | 8.0 kPa = 90% | 13.3 kPa = 98%")
