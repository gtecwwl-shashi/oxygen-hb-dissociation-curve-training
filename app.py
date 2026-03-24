import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Set up the wide layout for the best visual presentation
st.set_page_config(page_title="Oxygen-Hb Curve Training", layout="wide")

# The requested main title at the top
st.title("🩸 Oxygen-Haemoglobin Dissociation Curve")
st.markdown("---")
st.subheader("Interactive Clinical Simulation")

# Hill Equation: Perfectly models the human sigmoid shape
# P50 = 3.6 kPa, Hill Coefficient (n) = 2.8 for adult Hb
def calculate_hill_sao2(po2_kpa):
    if po2_kpa <= 0: return 0
    p50_target = 3.6  
    n_hill = 2.8      
    sao2 = (po2_kpa**n_hill) / ((po2_kpa**n_hill) + (p50_target**n_hill))
    return sao2 * 100

# --- PHASE 1: THE DISCOVERY SIDEBAR ---
st.sidebar.header("1. Identify and Scale")
x_label_guess = st.sidebar.text_input("Trainee Guess: X-axis label", "")
y_label_guess = st.sidebar.text_input("Trainee Guess: Y-axis label", "")
show_scale_numbers = st.sidebar.checkbox("Reveal Numeric Scale & Grid", value=False)

# --- PHASE 2: THE DATA EXTRACTION ---
st.sidebar.header("2. Extract Trainee Points")
st.sidebar.info("Ask 6 trainees for a PaO2 (kPa) to plot.")
names = ["Doctor 1", "Doctor 2", "Doctor 3", "Doctor 4", "Doctor 5", "Doctor 6"]
inputs = []
for name in names:
    # Scale limited to 14.0 with 0.1 increments
    val = st.sidebar.number_input(f"{name} Input (kPa)", 0.0, 14.0, value=0.0, step=0.1)
    inputs.append(val)

fig = go.Figure()

# Plot the diamonds representing the trainees' points
for i, val in enumerate(inputs):
    if val > 0:
        actual_sat = round(calculate_hill_sao2(val), 1)
        fig.add_trace(go.Scatter(
            x=[val], y=[actual_sat], 
            mode='markers+text',
            text=[f"{names[i]}<br>({val} kPa)"], 
            textposition="top center",
            marker=dict(size=18, color='crimson', symbol='diamond', line=dict(width=2, color='black')),
            showlegend=False
        ))

# BLANK AXIS CONFIGURATION
# Numbers and grids are hidden until 'show_scale_numbers' is checked
fig.update_layout(
    xaxis_title=x_label_guess if x_label_guess else "--- ??? ---",
    yaxis_title=y_label_guess if y_label_guess else "--- ??? ---",
    xaxis=dict(
        range=[0, 14.5], 
        tickvals=[0, 2, 4, 6, 8, 10, 12, 14], 
        showticklabels=show_scale_numbers, 
        showgrid=show_scale_numbers,       
        gridcolor='LightGray',
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=3
    ),
    yaxis=dict(
        range=[0, 105], 
        tickvals=[0, 20, 40, 60, 80, 100],
        showticklabels=show_scale_numbers, 
        showgrid=show_scale_numbers,       
        gridcolor='LightGray',
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=3
    ),
    height=800, 
    template="plotly_white",
    plot_bgcolor='white'
)

# --- PHASE 3: THE REVEAL ---
st.markdown("### Physiological Validation")
reveal_curve = st.checkbox("FINAL STEP: Reveal standard physiological curve")
if reveal_curve:
    x_curve = np.linspace(0.1, 14, 500)
    y_curve = [calculate_hill_sao2(x) for x in x_curve]
    fig.add_trace(go.Scatter(x=x_curve, y=y_curve, name='Standard Curve', 
                             line=dict(color='royalblue', width=5)))
    st.info("💡 Analysis: Note the P50 at 3.6 kPa and the distinct plateau above 10 kPa.")

st.plotly_chart(fig, use_container_width=True)
