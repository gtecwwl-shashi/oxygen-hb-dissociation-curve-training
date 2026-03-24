import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Oxygen-Hb Masterclass", layout="wide")

st.title("🫁 Oxyhemoglobin Curve: The Blank Canvas")
st.markdown("### Step 1: Define the Axes | Step 2: Plot the Points | Step 3: Reveal")

def get_sao2(pa_o2_kpa):
    p_mmhg = pa_o2_kpa * 7.5006
    if p_mmhg <= 0: return 0
    return ((((p_mmhg**3 + 150*p_mmhg)**-1)*23400) + 1)**-1 * 100

# --- STEP 1: DEFINE LABELS ---
st.sidebar.header("1. Define the Graph")
x_axis_title = st.sidebar.text_input("Label for X-axis", "")
y_axis_title = st.sidebar.text_input("Label for Y-axis", "")
show_numbers = st.sidebar.checkbox("Show Scale/Numbers", value=False)

# --- STEP 2: INPUT FELLOWS' DATA ---
st.sidebar.header("2. Fellows' Data")
names = ["Doctor 1", "Doctor 2", "Doctor 3", "Doctor 4", "Doctor 5", "Doctor 6"]
inputs = []
for name in names:
    val = st.sidebar.number_input(f"{name} Value", 0.0, 20.0, value=0.0, step=0.1)
    inputs.append(val)

fig = go.Figure()

# Plot points only if values are entered
for i, val in enumerate(inputs):
    if val > 0:
        sat = round(get_sao2(val), 1)
        fig.add_trace(go.Scatter(
            x=[val], y=[sat], 
            mode='markers+text',
            text=[f"{names[i]}"], 
            textposition="top center",
            marker=dict(size=15, color='crimson'),
            showlegend=False
        ))

# BLANK AXIS CONFIGURATION
fig.update_layout(
    xaxis_title=x_axis_title if x_axis_title else "",
    yaxis_title=y_axis_title if y_axis_title else "",
    xaxis=dict(
        range=[0, 14], 
        showticklabels=show_numbers, # Hidden until checkbox is clicked
        tickvals=[0, 2, 4, 6, 8, 10, 12, 14],
        showgrid=show_numbers,
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=2
    ),
    yaxis=dict(
        range=[0, 105], 
        showticklabels=show_numbers, # Hidden until checkbox is clicked
        tickvals=[0, 25, 50, 75, 100],
        showgrid=show_numbers,
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=2
    ),
    height=700,
    template="plotly_white",
    plot_bgcolor='white'
)

# --- STEP 3: REVEAL ---
reveal = st.checkbox("3. REVEAL PHYSIOLOGICAL CURVE")
if reveal:
    x_curve = np.linspace(0, 14, 500)
    y_curve = [get_sao2(x) for x in x_curve]
    fig.add_trace(go.Scatter(x=x_curve, y=y_curve, name='Standard Curve', 
                             line=dict(color='black', width=3)))

st.plotly_chart(fig, use_container_width=True)
