import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

st.title('Simulationstool zur Re-Wind-Analyse spezifischer Produkte')

st.divider(width="stretch")
st.subheader('Einfach produktspezifische Merkamale eingeben ...')

# Erstellen von 9 individuellen Slidern mit Titeln und ausklappbaren Abschnitten

Anz_ReAss = st.slider('Anzahl Re-Assemblys je linearem Lebenszyklus', min_value=1, max_value=5, value=2)

with st.expander("Ökologie spezifische Merkmale"):
        FußabdruckErste = st.slider('Fußabdruck der 1. Re-Assembly bezogen auf den Fußabdruck einer Neuproduktion [%]', min_value=0, max_value=100, value=10, format="%d %%")
        FußabdruckSteigung = st.slider('Steigung des Fußabdrucks von einer Re-Assembly zur nächsten  [%-punkte]', min_value=0, max_value=50, value=10, format="%d %%")
        FußabdruckNutzung = st.number_input('Fußabdruck der Nutzung bezogen auf den Fußabdruck der Neuproduktion [%]', min_value=0, value=50)
        FußabdruckNutzungVerb = st.slider('Vorzeitige Effizienzsteigerung durch Re-Assembly  [0 = nicht vorhanden - 10 = sehr stark]', min_value=0, max_value=10, value=5)

with st.expander("Kundennutzen spezifische Merkmale"):
    Innovation = st.slider('Särke des Innovationsrückgangs [0 = nicht vorhanden - 10 = sehr stark]', min_value=0, max_value=10, value=5)
    
with st.expander("Ökonomie spezifische Merkmale"):
        KostenErste = st.slider('Kosten der 1. Re-Assembly bezogen auf die Kosten einer Neuproduktion [%]', min_value=0, max_value=100, value=10, format="%d %%")
        KostenSteigung = st.slider('Steigung der Kosten von einer Re-Assembly zur nächsten [%-punkte]', min_value=0, max_value=50, value=10, format="%d %%")
        Subskription = st.number_input('Höhe der Subskriptionserlöse in einem linearen Lebenszyklus bezogen auf den Verkaufserlös eines linearen Produkts [%]', min_value=0, value=120)
        Marge = st.slider('Marge: Anteil der Herstellungskosten am Verkaufspreis [%]', min_value=0, max_value=100, value=60, format="%d %%")
       


st.divider(width="stretch")
st.subheader('... und Fenster & Sweetspot Diagramme anzeigen lassen')
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

for okonomRe_i in range(1, 11):
    current_y_curve1 += 100 * FußabdruckNutzung /100
    x_values_curve1.append(okonomRe_i)
    y_values_curve1.append(current_y_curve1)

    current_y_curve1 += 100
    x_values_curve1.append(okonomRe_i)
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

for okonomRe_i in range(1, int(10*Anz_ReAss) + 1):
    current_y_scaled += 100 * FußabdruckNutzung /100 /Anz_ReAss * (1-(FußabdruckNutzungVerb / 10))
    x_values_scaled.append(okonomRe_i/Anz_ReAss)
    y_values_scaled.append(current_y_scaled)

    current_y_scaled += 100 * (FußabdruckErste + FußabdruckSteigung * (okonomRe_i-1)) / 100
    x_values_scaled.append(okonomRe_i/Anz_ReAss)
    y_values_scaled.append(current_y_scaled)

with st.expander("Ökologie Diagramm"):

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



#### Kundennutzen Diagramm Lineares Produkt

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

# Berechnung des gleitenden Durchschnitts über ein Fenster von Größe 'window'
window_size = int(len(kunde_df) / len(np.unique(kunde_df["Kunde_X-Werte"]))) * 50 
floating_average_asymmetric = (
    pd.Series(kunde_df["Kunde_Y-Werte"])
      .rolling(window=window_size, min_periods=1)
      .mean()
)


### Kundennutzen Diagramm Re-Assembly

# Initialisierung der x- und y-Werte für die ReAss Kurve
kundeRe_x_values = []
kundeRe_y_values = []

# Startpunkt bei (0, 100) für die ReAss Kurve
KundeRe_y_temp = 100
kundeRe_x_values.append(0)
kundeRe_y_values.append(KundeRe_y_temp)

# Erstellen des Datensatzes mit dem gewünschten Muster
for kundeRe_i in range(1, int(10 * Anz_ReAss + 1)):
    num_points = 50  # Reduzierung der Anzahl Punkte 
    kundeRe_x_cosine = np.linspace(kundeRe_i - 1, kundeRe_i, num=num_points)
    kundeRe_y_cosine = KundeRe_y_temp - (25/(Anz_ReAss) * (1 - np.cos((np.pi / 2) * (kundeRe_x_cosine - (kundeRe_i -1 )))))
    
    # Hinzufügen der interpolierten Punkte zum Datensatz
    kundeRe_x_values.extend(kundeRe_x_cosine)
    kundeRe_y_values.extend(kundeRe_y_cosine)

    # Aktualisieren des aktuellen y-Wertes nach dem Abfall
    KundeRe_y_temp -= 50/Anz_ReAss
    
    # Sprung um ... bei Neuproduktion - Innovationsrückgang in Klammer berücksichtigt
    if kundeRe_i < int(10 * Anz_ReAss):
        KundeRe_y_temp += (60/Anz_ReAss - ((Innovation/5) * (1 + ((kundeRe_i)/50))))
        kundeRe_x_values.append(kundeRe_i)
        kundeRe_y_values.append(KundeRe_y_temp)

# Skalierung auf X - Achse des linearen Produks
scaled_kundeRe_x_values = [x / Anz_ReAss for x in kundeRe_x_values]

# Erstellen des DataFrames zur Visualisierung
kunde_re_data = {
    "KundeRe_X_Werte": scaled_kundeRe_x_values,
    "KundeRe_Y_Werte": kundeRe_y_values,
}

kunde_re_df = pd.DataFrame(kunde_re_data)

# Berechnung des gleitenden Durchschnitts über ein Fenster von Größe 'window'
window_size = int(len(kunde_re_df) / len(np.unique(kunde_re_df["KundeRe_X_Werte"]))) * 50

floating_average_Re_asymmetric = (
    pd.Series(kunde_re_df["KundeRe_Y_Werte"])
      .rolling(window=window_size, min_periods=1)
      .mean()
)

## Korridor des Kundennutzen
# X-Werte definieren: linear von 0 bis 10 in 1er Schritten
x = np.arange(0, 11, 1)

# Erste Gerade: startet bei y=100 mit einer Steigung von 10
y1 = 100 + 10 * x

# Zweite Gerade: startet bei y=75 mit einer Steigung von 10
y2 = 65 + 10 * x



## Erstellen des Liniendiagramms mit Plotly ohne Punkte und mit gestrichelter Linie für Floating Average.
with st.expander("Kundennutzen Diagramm"):
   
    fig_kunde_plotly = go.Figure()

    fig_kunde_plotly.add_trace(go.Scatter(
        x=kunde_df["Kunde_X-Werte"],
        y=kunde_df["Kunde_Y-Werte"],
        mode="lines",
        line=dict(color='darkblue'),
        name="Produkt mit linearer Nutzung"  
    ))

    fig_kunde_plotly.add_trace(go.Scatter(
        x=kunde_df["Kunde_X-Werte"],
        y=floating_average_asymmetric,
        mode="lines",
        line=dict(dash='dash', color='darkblue'),
        name="Produkt mit linearer Nutzung: langfristiges Mittel"
    ))

    fig_kunde_plotly.add_trace(go.Scatter(
        x=kunde_re_df["KundeRe_X_Werte"],
        y=kunde_re_df["KundeRe_Y_Werte"],
        mode="lines",
        line=dict(color='lightgreen'), 
        name="Re-Assembly Produkt"  
    ))

    fig_kunde_plotly.add_trace(go.Scatter(
        x=kunde_re_df["KundeRe_X_Werte"],
        y=floating_average_Re_asymmetric,
        mode="lines",
        line=dict(dash='dash', color='lightgreen'),
        name="Re-Assembly Produkt: langfristiges Mittel"  
    ))
    
    # Grauen Bereich zwischen den Linien hinzufügen (fill)
    fig_kunde_plotly.add_trace(go.Scatter(
        x=np.concatenate([x, x[::-1]]),
        y=np.concatenate([y1, y2[::-1]]),
        fill='toself',
        fillcolor='rgba(128,128,128,0.1)',
        line=dict(color='rgba(255,255,255,0)'),
        showlegend=False,
))

    fig_kunde_plotly.update_layout(
        title="Kundennutzen",
        xaxis=dict(title='Lineare Lebenszyklen', side='bottom', tickmode='linear', dtick=1),
        xaxis2=dict(title='Sekundäre X-Achse', side='bottom', anchor='free', position=0.2),
        yaxis=dict(title='Kundennutzen', showticklabels=False),
        legend=dict(x=0, y=1, xanchor='left', yanchor='top'),
    )

    st.plotly_chart(fig_kunde_plotly)

### Ökonomie Diagramm

## Lineare Kurve Ökonomie
# Berechnung Gewinn pro Verkauf
okonom_gewinn=100/(Marge/100) - 100

# Initialisierung der x- und y-Werte für die erste Kurve
okonom_x_values = []
okonom_y_values = []

# Startpunkt bei (0, 0)
okonom_x_values.append(0)
okonom_y_values.append(0)

okonom_current_y = okonom_gewinn  # Der erste Sprung bei x=0
okonom_x_values.append(0)
okonom_y_values.append(okonom_current_y)

for okonomRe_i in range(1, 11):
    #Steigung in Nutzung
    okonom_current_y += 0
    okonom_x_values.append(okonomRe_i)
    okonom_y_values.append(okonom_current_y)

    #Sprung bei Neukauf
    okonom_current_y += okonom_gewinn
    okonom_x_values.append(okonomRe_i)
    okonom_y_values.append(okonom_current_y)

## Re-Assembly Kurve Ökonomie

# Initialisierung der x- und y-Werte für die zweite Kurve mit Skalierung durch Anz_ReAss
okonomRe_x_values = []
okonomRe_y_values = []

# Startpunkt bei (0, 0)
okonomRe_x_values.append(0)
okonomRe_y_values.append(0)

okonomRe_current_y_scaled = -100   # Der erste Sprung auf (0,-100)
okonomRe_x_values.append(0)
okonomRe_y_values.append(okonomRe_current_y_scaled)

# lineare Steigung durch Subskription
for okonomRe_i in range(1, int(10*Anz_ReAss) + 1):
    okonomRe_current_y_scaled += (100+okonom_gewinn) * (Subskription/100) / Anz_ReAss
    okonomRe_x_values.append(okonomRe_i/Anz_ReAss)
    okonomRe_y_values.append(okonomRe_current_y_scaled)

    #Sprung durch Re-Assembly
    okonomRe_current_y_scaled -=100* (KostenErste+KostenSteigung*(okonomRe_i-1))/100
    okonomRe_x_values.append(okonomRe_i/Anz_ReAss) 
    okonomRe_y_values.append(okonomRe_current_y_scaled) 

with st.expander("Ökonomie Diagramm"):

    fig_okonom_plotly= go.Figure()

    fig_okonom_plotly.add_trace(go.Scatter(
        x=okonom_x_values,
        y=okonom_y_values,
        mode="lines",
        name="Produkt mit linearer Nutzung",
        line=dict(color='darkblue')
    ))

    fig_okonom_plotly.add_trace(go.Scatter(
        x=okonomRe_x_values,
        y=okonomRe_y_values,
        mode="lines",
        name="Produkt mit linearer Nutzung",
        line=dict(color='lightgreen')
    ))


    fig_okonom_plotly.update_layout(
        title="Ökologie",
        xaxis=dict(title='Lineare Lebenszyklen', side='bottom', tickmode='linear', dtick=1),
        xaxis2=dict(title='Sekundäre X-Achse', side='bottom', anchor='free', position=.2),
        yaxis=dict(title='Kumulierter Gewinn des Herstellers', showticklabels=True),
        legend=dict(x=0, y=1, xanchor='left', yanchor='top'),
    )

    st.plotly_chart(fig_okonom_plotly)