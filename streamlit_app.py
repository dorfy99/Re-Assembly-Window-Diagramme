import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d


#### Sidebar mit Datenaufnahme 

with st.sidebar:

       
    st.subheader('Hier einfach produktspezifische Merkamale eingeben ...')

    # Erstellen von 9 individuellen Slidern mit Titeln und ausklappbaren Abschnitten

    Anz_ReAss = st.slider('Anzahl Re-Assemblys je linearem Lebenszyklus', min_value=1, max_value=5, value=2)

    with st.expander("Ökologie spezifische Merkmale"):
            FußabdruckErste = st.slider('Fußabdruck der 1. Re-Assembly bezogen auf den Fußabdruck einer Neuproduktion [%]', min_value=0, max_value=100, value=10, format="%d %%")
            FußabdruckSteigung = st.slider('Steigung des Fußabdrucks von einer Re-Assembly zur nächsten  [%-punkte]', min_value=0, max_value=50, value=10, format="%d %%")
            FußabdruckZweite = st.slider('Fußabdruck der 1. großen Re-Assembly bezogen auf die Kosten einer Neuproduktion [%]', min_value=0, max_value=100, value=40, format="%d %%")
            FußabdruckZweiteSteigung = st.slider ('Steigung des Fußabdrucks von einer großen Re-Assembly zur nächsten [%-punkte]', min_value=0, max_value=50, value=5, format="%d %%")
            FußabdruckNutzung = st.number_input('Fußabdruck der Nutzung bezogen auf den Fußabdruck der Neuproduktion [%]', min_value=0, value=50)
            FußabdruckNutzungVerb = st.slider('Vorzeitige Effizienzsteigerung durch Re-Assembly  [0 = nicht vorhanden - 10 = sehr stark]', min_value=0, max_value=10, value=5)

    with st.expander("Kundennutzen spezifische Merkmale"):
        Innovation = st.slider('Särke des Innovationsrückgangs [0 = nicht vorhanden - 10 = sehr stark]', min_value=0, max_value=10, value=5)
        
    with st.expander("Ökonomie spezifische Merkmale"):
            KostenErste = st.slider('Kosten der 1. kleinen Re-Assembly bezogen auf die Kosten einer Neuproduktion [%]', min_value=0, max_value=100, value=10, format="%d %%")
            KostenSteigung = st.slider('Steigung der Kosten von einer kleinen Re-Assembly zur nächsten [%-punkte]', min_value=0, max_value=50, value=5, format="%d %%")
            KostenZweite = st.slider('Kosten der 1. großen Re-Assembly bezogen auf die Kosten einer Neuproduktion [%]', min_value=0, max_value=100, value=40, format="%d %%")
            KostenZweiteSteigung = st.slider ('Steigung der Kosten von einer großen Re-Assembly zur nächsten [%-punkte]', min_value=0, max_value=50, value=5, format="%d %%")
            Subskription = st.number_input('Höhe der Subskriptionserlöse in einem linearen Lebenszyklus bezogen auf den Verkaufserlös eines linearen Produkts [%]', min_value=0, value=120)
            Marge = st.slider('Marge: Anteil der Herstellungskosten am Verkaufspreis [%]', min_value=0, max_value=100, value=60, format="%d %%")

    st.divider(width="stretch")

st.sidebar.button("PDF Bericht erstellen")            

#### Hauptansicht mit Diagrammen

st.title('Simulationstool zur Re-Wind-Analyse spezifischer Produkte')
st.divider(width="stretch")
st.subheader('Einfach in der Sidebar (links) produktspezifische Merkamale eingeben ...')
st.subheader('... und Re-Wind Diagramme anzeigen lassen')

### Ökologie Diagramm

## Lineare Kurve

# Initialisierung der x- und y-Werte für die erste Kurve
okolog_x_values = []
okolog_y_values = []

# Startpunkt bei (0, 0)
okolog_x_values.append(0)
okolog_y_values.append(0)

okolog_y_temp = 100  # Der erste Sprung auf (0, 100)
okolog_x_values.append(0)
okolog_y_values.append(okolog_y_temp)

for okolog_i in range(1, 11):
    okolog_y_temp += 100 * FußabdruckNutzung /100
    okolog_x_values.append(okolog_i)
    okolog_y_values.append(okolog_y_temp)

    okolog_y_temp += 100
    okolog_x_values.append(okolog_i)
    okolog_y_values.append(okolog_y_temp)

## Re-Assembly Kurve

# Initialisierung der x- und y-Werte für die zweite Kurve mit Skalierung durch Anz_ReAss
okologRe_x_values = []
okologRe_y_values = []

# Startpunkt bei (0, 0)
okologRe_x_values.append(0)
okologRe_y_values.append(0)

okologRe_y_temp = 100  # Der erste Sprung auf (0, 100)
okologRe_x_values.append(0)
okologRe_y_values.append(okologRe_y_temp)

for okologRe_i in range(1, int(10*Anz_ReAss) + 1):
    okologRe_y_temp += 100 * FußabdruckNutzung /100 /Anz_ReAss * (1-(FußabdruckNutzungVerb / 10))
    okologRe_x_values.append(okologRe_i/Anz_ReAss)
    okologRe_y_values.append(okologRe_y_temp)

    if okologRe_i % 2 != 0 :
        okologRe_y_temp += 100 * (FußabdruckErste + FußabdruckSteigung * (okologRe_i-1)) / 100
        okologRe_x_values.append(okologRe_i/Anz_ReAss)
        okologRe_y_values.append(okologRe_y_temp)
        #großer Sprung durch Re-Assembly    
    
    else: 
        okologRe_y_temp +=100* (FußabdruckZweite+FußabdruckZweiteSteigung*pow(2,((okologRe_i-2)/10))*((okologRe_i-2)/2))/100
        okologRe_x_values.append(okologRe_i/Anz_ReAss) 
        okologRe_y_values.append(okologRe_y_temp) 



## Berechnung von Sweetspot und Fenster-Grenzen

x_common = np.linspace(min(min(okolog_x_values), min(okologRe_x_values)), max(max(okolog_x_values), max(okologRe_x_values)), num=500)

okolog_interp = interp1d(okolog_x_values, okolog_y_values, kind='linear', fill_value="extrapolate")
okologRe_interp = interp1d(okologRe_x_values, okologRe_y_values, kind='linear', fill_value="extrapolate")

okolog_y_values_interp = okolog_interp(x_common)
okologRe_y_values_interp = okologRe_interp(x_common)

okolog_diff= okolog_y_values_interp - okologRe_y_values_interp

# Erstelle einen DataFrame mit den x-Werten und den beiden y-Wert-Reihen und der Differenz der y-Werte
okonom_data = {
    'x': x_common,
    'Interpolated Okolog': okolog_y_values_interp,
    'Interpolated Okolog Re': okologRe_y_values_interp,
    'Differenz' : okolog_diff
}
df_interpolated = pd.DataFrame(okonom_data)

# Sweetspot = Maximaler positiver Wert in 'Differenz' finden 
okolog_diff_max = df_interpolated[df_interpolated['Differenz'] == df_interpolated['Differenz'].max()]['x'].values[0]
okolog_sweetspot = int(okolog_diff_max*Anz_ReAss)
okolog_neustart_y_value = 0
for i in range(len(okologRe_x_values)):
    if okologRe_x_values[i] == (okolog_sweetspot)/Anz_ReAss :
        okolog_neustart_y_value = okologRe_y_values[i]


# Vorzeichenwechsel finden
# Initialisierung für die Suche nach Vorzeichenwechseln
min_neg_to_pos_x = None
max_pos_to_neg_x = None

for i in range(1, len(df_interpolated)):
    previous_value = df_interpolated['Differenz'].iloc[i-1]
    current_value = df_interpolated['Differenz'].iloc[i]
    
    if previous_value < 0 and current_value > 0:
        # Wechsel von negativ zu positiv
        if min_neg_to_pos_x is None or df_interpolated['x'].iloc[i] < min_neg_to_pos_x:
            min_neg_to_pos_x = df_interpolated['x'].iloc[i]
    
    elif previous_value > 0 and current_value < 0:
        # Wechsel von positiv zu negativ
        if max_pos_to_neg_x is None or df_interpolated['x'].iloc[i] > max_pos_to_neg_x:
            max_pos_to_neg_x = df_interpolated['x'].iloc[i]

# Fenstergrenzen berechnen
if min_neg_to_pos_x is None:
    okonom_fenster_low = 1
    min_neg_to_pos_x = 1/Anz_ReAss
else:
    okonom_fenster_low = int(min_neg_to_pos_x * Anz_ReAss)

if max_pos_to_neg_x is None:
    okonom_fenster_high = "unendlich"
    max_pos_to_neg_x = 10
else:
    okonom_fenster_high = int(max_pos_to_neg_x * Anz_ReAss -1)

okolog_xWindow_max_y_value = 0
for i in range(len(okolog_x_values)):
    if okolog_x_values[i] == int(max_pos_to_neg_x+1) :
        okolog_xWindow_max_y_value = okolog_y_values[i]

# Verlauf bei Neustart am optimalen Zeitpunkt zeigen
okologRe_neustart_x_values = [x + (int(okolog_sweetspot/Anz_ReAss)+(1/Anz_ReAss)) for x in okologRe_x_values]
okologRe_neustart_y_values = [y + okolog_neustart_y_value for y in okologRe_y_values]


# Diagramm anzeigen
with st.expander("Ökologie Diagramm"):

    fig_okolog_plotly = go.Figure()

    # Hinzufügen der ersten Kurve zum Diagramm auf der primären X-Achse
    fig_okolog_plotly.add_trace(go.Scatter(
        x=okolog_x_values,
        y=okolog_y_values,
        mode="lines",
        name="Produkt mit linearer Nutzung",
        line=dict(color='darkblue')
    ))

    # Hinzufügen der zweiten Kurve zum Diagramm auf einer sekundären X-Achse mit Skalierung durch Anz_ReAss
    fig_okolog_plotly.add_trace(go.Scatter(
        x=okologRe_x_values,
        y=okologRe_y_values,
        mode="lines",
        name="Re-Assembly Produkt",
        line=dict(color='lightgreen')
    ))

    # Hinzufügen der Re-Assembly kurve nach dem optimalen Abbruch
    fig_okolog_plotly.add_trace(go.Scatter(
        x=okologRe_neustart_x_values,
        y=okologRe_neustart_y_values,
        mode="lines",
        name="Re-Assembly Produkt: Zweiter Kreislauf",
        line=dict(dash='dot', color='lightgreen')
    ))


    # Fenster Bereich plotten
    fig_okolog_plotly.add_shape(type="rect",
                x0=min_neg_to_pos_x, x1=max_pos_to_neg_x,
                y0=0,
                y1=okolog_xWindow_max_y_value,
                fillcolor="orange",
                opacity=0.1,
                layer="below",
                line_width=0)
    
    # Füge ein Icon zur linken Grenze hinzu
    fig_okolog_plotly.add_annotation(
        x=min_neg_to_pos_x,
        y=okolog_xWindow_max_y_value*0.5,
        text="➡️",
        showarrow=False,
        font=dict(size=15),
    )

        # Füge ein Icon zur rechten Grenze hinzu
    fig_okolog_plotly.add_annotation(
        x=max_pos_to_neg_x,
        y=okolog_xWindow_max_y_value*0.5,
        text="⬅️",
        showarrow=False,
        font=dict(size=15),
    )

    # Sweetspot Indikator plotten
        # Werte für Sweetspot indikator linie
    okolog_sweetspot_marker_x_values = [okolog_sweetspot/Anz_ReAss, okolog_diff_max, okolog_diff_max]
    okolog_sweetspot_marker_y_values = [0, 100, okolog_xWindow_max_y_value]
    fig_okolog_plotly.add_trace(go.Scatter(
        x=okolog_sweetspot_marker_x_values,
        y=okolog_sweetspot_marker_y_values,
        mode='lines',
        line=dict(color="red", width=2),
        showlegend=False))
    
    # Füge ein Icon hinzu zum Neustartzeitpunkt
    fig_okolog_plotly.add_annotation(
        x=okolog_diff_max,
        y=okolog_xWindow_max_y_value,
        text="🔄",
        showarrow=False,
        font=dict(size=20),
    )

    fig_okolog_plotly.update_layout(
        title="Ökologie",
        xaxis=dict(title='Lineare Lebenszyklen', side='bottom', tickmode='linear', dtick=1, range=[0, int(max_pos_to_neg_x)+1.01]),
        xaxis2=dict(title='Sekundäre X-Achse', side='bottom', anchor='free', position=0.2),
        yaxis=dict(title='Kumulierter ökologischer Fußabdruck', showticklabels=False, range=[0, okolog_xWindow_max_y_value*1.2]),
        legend=dict(x=0, y=1, xanchor='left', yanchor='top', bgcolor='rgba(0,0,0,0)'),
    )



    st.plotly_chart(fig_okolog_plotly)

    # Fenster und Sweetspot anzeigen
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
            <div style="text-align: center; white-space: nowrap;">
                <strong>➡️ Untere Fenstergrenze</strong><br>
                <span style="font-size: 24px;">{okonom_fenster_low}</span>
                <span style="font-size: 14px;">Re-Assemblys</span>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div style="text-align: center; white-space: nowrap;">
                <strong>🔄 Optimaler Neustartpunkt</strong><br>
                <span style="font-size: 14px;">nach</span>
                <span style="font-size: 24px;">{okolog_sweetspot}</span>
                <span style="font-size: 14px;">Re-Assemblys</span>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div style="text-align: center; white-space: nowrap;">
                <strong>⬅️ Obere Fenstergrenze</strong><br>
                <span style="font-size: 24px;">{okonom_fenster_high}</span>
                <span style="font-size: 14px;">Re-Assemblys</span>
            </div>
        """, unsafe_allow_html=True)

# Digramm als Bild speichern
fig_okolog_plotly.write_image("Oekologie_Diagramm.png")

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
        legend=dict(x=0, y=1, xanchor='left', yanchor='top', bgcolor='rgba(0,0,0,0)'),
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

okonomRe_y_temp = -100   # Der erste Sprung auf (0,-100)
okonomRe_x_values.append(0)
okonomRe_y_values.append(okonomRe_y_temp)

for okonomRe_i in range(1, int(10*Anz_ReAss) + 1):
    # lineare Steigung durch Subskription
    okonomRe_y_temp += (100+okonom_gewinn) * (Subskription/100) / Anz_ReAss
    okonomRe_x_values.append(okonomRe_i/Anz_ReAss)
    okonomRe_y_values.append(okonomRe_y_temp)

    #kleiner Sprung durch Re-Assembly
    if okonomRe_i % 2 != 0:
        okonomRe_y_temp -=100* (KostenErste+KostenSteigung*((okonomRe_i-1)/2))/100
        okonomRe_x_values.append(okonomRe_i/Anz_ReAss) 
        okonomRe_y_values.append(okonomRe_y_temp) 

    #großer Sprung durch Re-Assembly    
    else: 
        okonomRe_y_temp -=100* (KostenZweite+KostenZweiteSteigung*pow(2,((okonomRe_i-2)/8))*((okonomRe_i-2)/2))/100
        okonomRe_x_values.append(okonomRe_i/Anz_ReAss) 
        okonomRe_y_values.append(okonomRe_y_temp) 

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
        title="Ökonomie",
        xaxis=dict(title='Lineare Lebenszyklen', side='bottom', tickmode='linear', dtick=1),
        xaxis2=dict(title='Sekundäre X-Achse', side='bottom', anchor='free', position=.2),
        yaxis=dict(title='Kumulierter Gewinn des Herstellers', showticklabels=False),
        legend=dict(x=0, y=1, xanchor='left', yanchor='top', bgcolor='rgba(0,0,0,0)'),
    )

    st.plotly_chart(fig_okonom_plotly)