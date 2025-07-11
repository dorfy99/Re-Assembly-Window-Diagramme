import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt

st.title('Daten mit Slidern einlesen')

# Erstellen von 9 individuellen Slidern mit Titeln und ausklappbaren Abschnitten
st.subheader('Einflussgrößen auf die Diagramme')

Anz_ReAss = st.slider('Anzahl Re-Assemblys je linearem Lebenszyklus', min_value=1, max_value=5, value=2)

with st.expander("Ökologie spezifisch"):
        FußabdruckErste = st.slider('Fußabdruck der 1. Re-Assembly bezogen auf den Fußabdruck einer Neuproduktion [%]', min_value=0, max_value=100, value=10, format="%d %%")
        FußabdruckSteigung = st.slider('Steigung des Fußabdrucks von einer Re-Assembly zur nächsten  [%-punkte]', min_value=0, max_value=50, value=10, format="%d %%")
        FußabdruckNutzung = st.number_input('Fußabdruck der Nutzung bezogen auf den Fußabdruck der Neuproduktion [%]', min_value=0, value=0)
        FußabdruckNutzungVerb = st.slider('Vorzeitige Effizienzsteigerung durch Re-Assembly  [0 = nicht vorhanden - 10 = sehr stark]', min_value=0, max_value=10, value=5)

with st.expander("Kundennutzen spezifisch"):
    Innovation = st.slider('Särke des Innovationsrückgangs [0 = nicht vorhanden - 10 = sehr stark]', min_value=0, max_value=10, value=5)
    
with st.expander("Ökonomie spezifisch"):
        KostenErste = st.slider('Kosten der 1. Re-Assembly bezogen auf die Kosten einer Neuproduktion [%]', min_value=0, max_value=100, value=10, format="%d %%")
        KostenSteigung = st.slider('Steigung der Kosten von einer Re-Assembly zur nächsten [%-punkte]', min_value=0, max_value=50, value=10, format="%d %%")
        Subskription = st.number_input('Höhe der Subskriptionserlöse in einem linearen Lebenszyklus bezogen auf den Verkaufserlös eine linearen Produkts [%]', min_value=0, value=50)
       
       



st.title('Datenvisualisierung mit Plotly')
## Lineare Kurve

# Initialisierung der x- und y-Werte für die erste Kurve
x_values_curve1 = []
y_values_curve1 = []

# Startpunkt bei (0, 0)
x_values_curve1.append(0)
y_values_curve1.append(0)

current_y_curve1 = 100  # Der erste Sprung auf (0, 100)
x_values_curve1.append(0)
y_values_curve1.append(current_y_curve1)

for i in range(1, 11):
    current_y_curve1 += 100 * FußabdruckNutzung /100
    x_values_curve1.append(i)
    y_values_curve1.append(current_y_curve1)

    current_y_curve1 += 100
    x_values_curve1.append(i)
    y_values_curve1.append(current_y_curve1)

## Re-Assembly Kurve

# Initialisierung der x- und y-Werte für die zweite Kurve mit Skalierung durch Anz_ReAss
x_values_scaled = []
y_values_scaled = []

# Startpunkt bei (0, 0)
x_values_scaled.append(0)
y_values_scaled.append(0)

current_y_scaled = 100  # Der erste Sprung auf (0, 100)
x_values_scaled.append(0)
y_values_scaled.append(current_y_scaled)

for i in range(1, int(10*Anz_ReAss) + 1):
    current_y_scaled += 100 * FußabdruckNutzung /100 /Anz_ReAss * (1-(FußabdruckNutzungVerb / 10))
    x_values_scaled.append(i/Anz_ReAss)
    y_values_scaled.append(current_y_scaled)

    current_y_scaled += 100 * (FußabdruckErste + FußabdruckSteigung * (i-1)) / 100
    x_values_scaled.append(i/Anz_ReAss)
    y_values_scaled.append(current_y_scaled)

fig_plotly = go.Figure()

# Hinzufügen der ersten Kurve zum Diagramm auf der primären X-Achse
fig_plotly.add_trace(go.Scatter(
    x=x_values_curve1,
    y=y_values_curve1,
    mode="lines",
    name="Produkt mit linearer Nutzung",
     line=dict(color='darkblue')
))

# Hinzufügen der zweiten Kurve zum Diagramm auf einer sekundären X-Achse mit Skalierung durch Anz_ReAss
fig_plotly.add_trace(go.Scatter(
    x=x_values_scaled,
    y=y_values_scaled,
    mode="lines",
    name="Re-Assembly Produkt",
     line=dict(color='lightgreen')
))

fig_plotly.update_layout(
    title="Diagramm mit zwei skalierten Zyklen",
    xaxis=dict(title='Lineare Lebenszyklen', side='bottom', tickmode='linear', dtick=1),
    xaxis2=dict(title='Sekundäre X-Achse', side='bottom', anchor='free', position=0.2),
    yaxis=dict(title='Kumulierter ökologischer Fußabdruck', showticklabels=False),
    legend=dict(x=0, y=1, xanchor='left', yanchor='top'),
)

st.plotly_chart(fig_plotly)