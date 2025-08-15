import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import time


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
            FußabdruckNutzungVerb = st.slider('Stärke der vorzeitigen Effizienzsteigerung durch Re-Assembly  [0 = nicht vorhanden - 10 = sehr stark]', min_value=0, max_value=10, value=5)

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

    st.button('Link zum Whitepaper')

# WZL Logo in Sidebar anzeigen
st.logo("https://upload.wikimedia.org/wikipedia/commons/5/58/WZL_Logo2.png", size="large", link=None, icon_image=None)

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



### PDF Export

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

# Funktion zum Erstellen des PDFs
def create_pdf(product_name):
    timestamp = int(time.time())  # Aktuellen Zeitstempel erhalten
    pdf_file_path = f"output_{timestamp}.pdf"
    c = canvas.Canvas(pdf_file_path, pagesize=A4)  # A4-Größe in cm
    width, height = A4
    
    ## WZL Logo
    logo_path = "https://upload.wikimedia.org/wikipedia/commons/5/58/WZL_Logo2.png"
    c.drawImage(logo_path, 0.5 * cm, height - 1.6 * cm, width=5 * cm, height= 1.33 * cm)

    ## Disclaimer
    c.setFont("Helvetica", 10)
    disclaimer1 = "Erstellt mit einem Online-Tool des WZL der RWTH-Aachen"
    disclaimer2 = "Verfügbar unter https://re-wind.streamlit.app/"
    c.drawString((width - (c.stringWidth(disclaimer1)))/2, height - 0.7 * cm, disclaimer1)
    c.drawString((width - (c.stringWidth(disclaimer2)))/2, height - 1.2 * cm, disclaimer2)

    ## Datum
    from datetime import datetime
    current_date = datetime.now().strftime("%d.%m.%Y")
    c.setFont("Helvetica", 10)
    c.drawString(width - (1 * cm + c.stringWidth(current_date)), height - 1.2 * cm, current_date)

    # Zeichne eine Linie unter dem Logo (Kopfzeile)
    c.line(0.5 * cm, height - 1.5 * cm, width - 0.5 * cm, height - 1.5 * cm)  # Horizontale Linie


    ## Titel
    c.setFont("Helvetica-Bold", 18)
    c.drawString(2 * cm, height - 3.25 * cm, f"Re-Wind Analyse zum Produkt: {product_name}")
    
    # Untertitel: Annahmen zu den Produkteigenschaften
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, height - 5 * cm, "Annahmen zu den Produkteigenschaften")

   
    ## Re-Assembly Zyklus Eigenschaft
    c.setFont("Helvetica-Bold", 10)
    oekolog_Eigenschaften_Benennung = ["Anzahl Re-Assemblys je linearem Lebenszyklus"]  
    
    oekolog_Eigenschaften_Werte = [f"{Anz_ReAss}"]  
    
    oekolog_Eigenschaften_Tabelle = height - 6 * cm
    for term, value in zip(oekolog_Eigenschaften_Benennung, oekolog_Eigenschaften_Werte):
        c.drawString(2 * cm, oekolog_Eigenschaften_Tabelle, term)
        c.drawString(16 * cm, oekolog_Eigenschaften_Tabelle, value) 
        oekolog_Eigenschaften_Tabelle -= 0.5 * cm 
        
    # Ökologische Eigenschaften in Tabelle
    c.setFont("Helvetica-Bold", 10)
    c.drawString(2 * cm, height - 7 * cm, "Ökonomie spezifisch")

    c.setFont("Helvetica", 10)
    oekolog_Eigenschaften_Benennung = ["Fußabdruck der 1. Re-Assembly bezogen auf den Fußabdruck einer Neuproduktion", 
             "Steigung des Fußabdrucks von einer Re-Assembly zur nächsten",
             "Fußabdruck der 1. großen Re-Assembly bezogen auf die Kosten einer Neuproduktion",
             "Steigung des Fußabdrucks von einer großen Re-Assembly zur nächsten",
             "Fußabdruck der Nutzung bezogen auf den Fußabdruck der Neuproduktion",  
             "Stärke der vorzeitigen Effizienzsteigerung durch Re-Assembly"]  
    
    oekolog_Eigenschaften_Werte = [f"{FußabdruckErste} %", f"{FußabdruckSteigung} %-punkte", f"{FußabdruckZweite} %", f"{FußabdruckZweiteSteigung} %-punkte", 
              f"{FußabdruckNutzung} %", f"{FußabdruckNutzungVerb} (0-10)"]  
    
    oekolog_Eigenschaften_Tabelle = height - 7.5 * cm
    for term, value in zip(oekolog_Eigenschaften_Benennung, oekolog_Eigenschaften_Werte):
        c.drawString(2 * cm, oekolog_Eigenschaften_Tabelle, term)
        c.drawString(16 * cm, oekolog_Eigenschaften_Tabelle, value) 
        oekolog_Eigenschaften_Tabelle -= 0.5 * cm

    # Kundennutzen Eigenschaften in Tabelle
    c.setFont("Helvetica-Bold", 10)
    c.drawString(2 * cm, height - 11 * cm, "Kundennutzen spezifisch")
   
    c.setFont("Helvetica", 10)
    kunde_Eigenschaften_Benennung = ["Särke des Innovationsrückgangs"]

    kunde_Eigenschaften_Werte = [f"{Innovation} (0-10)"]  
    
    kunde_Eigenschaften_Tabelle = height -11.5 * cm
    for term, value in zip(kunde_Eigenschaften_Benennung, kunde_Eigenschaften_Werte):
        c.drawString(2 * cm, kunde_Eigenschaften_Tabelle, term)
        c.drawString(16 * cm, kunde_Eigenschaften_Tabelle, value) 
        kunde_Eigenschaften_Tabelle -= 0.5 * cm

    # Ökonomische Eigenschaften in Tabelle
    c.setFont("Helvetica-Bold", 10)
    c.drawString(2 * cm, height - 12.5 * cm, "Ökologie spezifisch")

    c.setFont("Helvetica", 10)
    oekonom_Eigenschaften_Benennung = ["Kosten der 1. kleinen Re-Assembly bezogen auf die Kosten einer Neuproduktion", 
             "Steigung der Kosten von einer kleinen Re-Assembly zur nächsten",
             "Kosten der 1. großen Re-Assembly bezogen auf die Kosten einer Neuproduktion",
             "Steigung der Kosten von einer großen Re-Assembly zur nächsten",
             "Höhe der Subskriptionserlöse in einem linearen Lebenszyklus bezogen auf den Verkaufserlös eines linearen Produkts",  
             "Marge: Anteil der Herstellungskosten am Verkaufspreis"]  
    
    oekonom_Eigenschaften_Werte = [f"{KostenErste} %", f"{KostenSteigung} %-punkte", f"{KostenZweite} %", f"{KostenZweiteSteigung} %-punkte", 
              f"{Subskription} %", f"{Marge} (0-10)"]  
    
    oekonom_Eigenschaften_Tabelle = height - 13 * cm
    for term, value in zip(oekonom_Eigenschaften_Benennung, oekonom_Eigenschaften_Werte):
        c.drawString(2 * cm, oekonom_Eigenschaften_Tabelle, term)
        c.drawString(16 * cm, oekonom_Eigenschaften_Tabelle, value) 
        oekonom_Eigenschaften_Tabelle -= 0.5 * cm
    

    ## Untertitel: Gesamtergebnis
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, height - 17.5 * cm, "Gesamtergebnis in den drei Dimensionen")

    # Setze die Startposition für die Tabelle
    table_start_x = 2 * cm  # x-Position der Tabelle
    table_start_y = height - 18 * cm  # y-Position der Tabelle (anpassbar)

    # Tabellenparameter
    num_rows = 4
    num_cols = 4
    cell_width = (width - 4 * cm) / num_cols  # Breite jeder Zelle
    cell_height = 1 * cm  # Höhe jeder Zelle

    # Zeichne Gitterlinien und fülle die Kopfzeile und erste Spalte aus
    c.setFont("Helvetica-Bold", 10)

    # Kopfzeile 
    headers = ["", "Unterer Grenze", "Optimaler \n Abbruchzeitpunkt", "Obere Grenze"]
    
    for col in range(num_cols):
        c.drawString(table_start_x + col * cell_width + (cell_width / 2) - (c.stringWidth(headers[col]) / 2), 
                     table_start_y, headers[col])
        c.line(table_start_x + col * cell_width, table_start_y + cell_height,
               table_start_x + col * cell_width, table_start_y - (num_rows) * cell_height)  # Vertikale Linie

        if col == num_cols - 1:  
            c.line(table_start_x + col * cell_width, table_start_y + cell_height,
                   table_start_x + col * cell_width, table_start_y - (num_rows) * cell_height)  

    
    c.setFont("Helvetica-Bold", 10)

    # Erste Spalte mit fettem Text 
    first_column_labels = ["", "Ökologie", "Kundennutzen", "Ökonomie"]
    
    for row in range(1, num_rows):  
        c.drawString(table_start_x + (cell_width / 2) - (c.stringWidth(first_column_labels[row]) / 2),
                     table_start_y - row * cell_height - (cell_height / 2), first_column_labels[row])
        
        c.line(table_start_x, 
               table_start_y - row * cell_height,
               table_start_x + width - (3*cm), 
               table_start_y - row * cell_height)  

        if row == num_rows-1:
            c.line(table_start_x ,table_start_y-(row)*cell_height,
                   width-(3*cm),table_start_y-(row)*cell_height)
    
   
    # Füge Platzhalterwerte hinzu und zeichne Gitterlinien 
    values_placeholder = [["Var1", "Var2", "Var3"], ["Var4", "Var5", "Var6"], ["Var7","Var8","Var9"]]

    for row in range(1,num_rows):
       for col in range(1,num_cols):  
           value_text=values_placeholder[row-1][col-1]  
           x_pos=table_start_x+col*cell_width+(cell_width/2)-(c.stringWidth(value_text)/2)
           y_pos=table_start_y-row*cell_height-(cell_height/2)
           c.drawString(x_pos,y_pos,value_text)

   # Ziehe horizontale und vertikale Linien für die gesamte Tabelle 
    for i in range(num_rows+1):  
       c.line(table_start_x ,table_start_y-i*cell_height,
               width-(3*cm),table_start_y-i*cell_height)

    for j in range(num_cols+1):  
       c.line(table_start_x+j*cell_width ,table_start_y,
               table_start_x+j*cell_width ,table_start_y-(num_rows)*cell_height)





    c.save()  # PDF speichern
      
    return pdf_file_path



### Dialog Fenster zur Eingabe des Produktnamens und PDF-Erstellung
@st.dialog("Produktname eingeben")
def product_dialog():
    product_name_input = st.text_input("Bitte geben Sie den Namen des Produkts oder Berichts ein:")
    
    if st.button("PDF generieren"):
        if product_name_input:
            pdf_file_path = create_pdf(product_name_input)

            if pdf_file_path:
                download_filename = f"ReWind_Analyse_{product_name_input}.pdf"
                with open(pdf_file_path, "rb") as pdf_file:
                    st.download_button("Download PDF", pdf_file, file_name=download_filename, mime='application/pdf')
        else:
            st.warning("Bitte geben Sie einen Namen ein.")

# Button nicht im Dialog sondern in App
if "vote" not in st.session_state:
    if st.sidebar.button('PDF Bericht erstellen'):
        product_dialog()
else:

    f"You voted for {st.session_state.vote['item']} because {st.session_state.vote['reason']}"
