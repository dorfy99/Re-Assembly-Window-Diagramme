import streamlit as st
import plotly.graph_objects as go

st.title('Daten mit Slidern einlesen')

# Erstellen von 9 individuellen Slidern mit Titeln und ausklappbaren Abschnitten
st.subheader('Einflussgrößen auf die Diagramme')

Anz_ReAss = st.slider('Anzahl Re-Assemblys je linearem Lebenszyklus', min_value=1, max_value=5, value=2)

with st.expander("Ökologie spezifisch"):
        FußabdruckErste = st.slider('Fußabdruck der 1. Re-Assembly bezogen auf den Fußabdruck einer Neuproduktion', min_value=0, max_value=100, value=10)
        FußabdruckSteigung = st.slider('Steigung des Fußabdrucks von einer Re-Assembly zur nächsten', min_value=0, max_value=50, value=10)
        FußabdruckNutzung = st.number_input('Fußabdruck der Nutzung bezogen auf den Fußabdruck der Neuproduktion', min_value=0, value=0)

with st.expander("Kundennutzen spezifisch"):
    Innovation = st.slider('Särke des Innovationsrückgangs', min_value=0, max_value=10, value=5)
    
with st.expander("Ökonomie spezifisch 3"):
        KostenErste = st.slider('Kosten der 1. Re-Assembly bezogen auf die Kosten einer Neuproduktion', min_value=0, max_value=100, value=10)
        KostenSteigung = st.slider('Steigung der Kosten von einer Re-Assembly zur nächsten', min_value=0, max_value=50, value=10)
        Subskription = st.number_input('Höhe der Subskriptionserlöse in einem linearen Lebenszyklus bezogen auf den Verkaufserlös eine linearen Produkts', min_value=0, value=50)
       

# Beispiel-Daten
x_values = [0, 1, 2 ,3 ,4 ,5]
y_values_curve1 = [0 ,1 ,2 ,3 ,None ,6] # Hier wird der Sprung dargestellt bei x=5 
y_values_curve2 = [0.5 ,1.5 ,2.5,None,None,None]

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=x_values,
    y=y_values_curve1,
    mode="lines+markers",
    name="Kurve 1"
))

fig.add_trace(go.Scatter(
    x=x_values,
    y=y_values_curve2,
    mode="lines+markers",
    name="Kurve 2"
))

fig.update_layout(
    xaxis_title="X-Achse",
    yaxis_title="Y-Achse"
)

st.plotly_chart(fig)
