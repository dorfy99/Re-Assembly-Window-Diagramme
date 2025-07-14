import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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
       
       



st.title('Fenster und Sweetspot Diagramme')
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
    title="Ökologie",
    xaxis=dict(title='Lineare Lebenszyklen', side='bottom', tickmode='linear', dtick=1),
    xaxis2=dict(title='Sekundäre X-Achse', side='bottom', anchor='free', position=0.2),
    yaxis=dict(title='Kumulierter ökologischer Fußabdruck', showticklabels=False),
    legend=dict(x=0, y=1, xanchor='left', yanchor='top'),
)

st.plotly_chart(fig_plotly)


## Sicherstellen, dass alle Listen die gleiche Länge haben
# min_length = min(len(x_values_scaled), len(y_values_scaled), len(y_values_curve1))

# # Kürzen der Listen auf die minimale Länge
# x_values_scaled = x_values_scaled[:min_length]
# y_values_scaled = y_values_scaled[:min_length]
# y_values_curve1 = y_values_curve1[:min_length]

# # Berechnung der Differenzen
# differenzen = [curve1 - scaled for curve1, scaled in zip(y_values_curve1, y_values_scaled)]

# # Erstellen des DataFrames mit den x-Werten der skalierten Kurve und den entsprechenden y-Werten
# data = {
#     "X-Werte (Scaled)": x_values_scaled,
#     "Y-Werte (Scaled)": y_values_scaled,
#     "Y-Werte (Curve1)": y_values_curve1,
#     "Differenz": differenzen
# }

# df = pd.DataFrame(data)

# # Anzeige als Streamlit-Tabelle
# st.table(df)

# # Ermittlung des Index mit dem höchsten Differenzwert
# max_diff_index = df['Differenz'].idxmax()

# # Ausgabe des entsprechenden X-Werts
# max_diff_x_value = df.at[max_diff_index, 'X-Werte (Scaled)']
# st.write(f"Der X-Wert mit der höchsten Differenz ist: {max_diff_x_value}")
# st.metric("Sweetspot nach ... Re-Assemblys", int(max_diff_x_value))



#### Kundennutzen Diagramm

import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Initialisierung der x- und y-Werte für den Graphen
kunde_x_values = []
kunde_y_values = []

# Startpunkt bei (0, 100)
Kunde_y_temp = 100
kunde_x_values.append(0)
kunde_y_values.append(Kunde_y_temp)

# Erstellen des Datensatzes mit dem gewünschten Muster
for kunde_i in range(1, 11):
    # Cosinusförmiger Abfall von Kunde_y_temp um 50 (Einstellwert ist die 25) zwischen kunde_i und kunde_i + 1
    kunde_x_cosine = np.linspace(kunde_i - 1, kunde_i, num=50)  # Interpolation zwischen den Punkten
    kunde_y_cosine = Kunde_y_temp - (25 * (1 - np.cos((np.pi / 2) * (kunde_x_cosine - (kunde_i - 1)))))
    
    # Hinzufügen der interpolierten Punkte zum Datensatz
    kunde_x_values.extend(kunde_x_cosine)
    kunde_y_values.extend(kunde_y_cosine)

    # Aktualisieren des aktuellen y-Wertes nach dem Abfall
    Kunde_y_temp -= 50
    
    # Sprung um ... bei Neuproduktion
    if kunde_i < 10:
        Kunde_y_temp += 60
        kunde_x_values.append(kunde_i)
        kunde_y_values.append(Kunde_y_temp)

# Erstellen des DataFrames zur Visualisierung
kunde_data = {
    "Kunde_X-Werte": kunde_x_values,
    "Kunde_Y-Werte": kunde_y_values,
}

kunde_df = pd.DataFrame(kunde_data)

# Berechnung des gleitenden Durchschnitts über ein Fenster von z.B. Größe 'window'
window_size = 50* int(len(kunde_df) / len(np.unique(kunde_df["Kunde_X-Werte"]))) 
floating_average = kunde_df["Kunde_Y-Werte"].rolling(window=window_size, min_periods=1).mean()

# Erstellen des Liniendiagramms mit Plotly ohne Punkte und mit gestrichelter Linie für Floating Average.
fig_kunde_plotly = go.Figure()

fig_kunde_plotly.add_trace(go.Scatter(
    x=kunde_df["Kunde_X-Werte"],
    y=kunde_df["Kunde_Y-Werte"],
    mode="lines",  
))

fig_kunde_plotly.add_trace(go.Scatter(
    x=kunde_df["Kunde_X-Werte"],
    y=floating_average,
    mode="lines",
    line=dict(dash='dash', color='gray'),
    name="Floating Average"
))

fig_kunde_plotly.update_layout(
     title="Concaver Abfall mit Sprüngen und Floating Average",
     xaxis=dict(title='X-Achse'),
     yaxis=dict(title='Y-Achse'),
)

st.plotly_chart(fig_kunde_plotly)