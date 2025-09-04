import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import time
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import io
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF



#### Sidebar mit Datenaufnahme 

with st.sidebar:

    
    st.subheader('Hier einfach produktspezifische Merkamale eingeben ...')

    # Erstellen von 9 individuellen Slidern mit Titeln und ausklappbaren Abschnitten

    Anz_ReAss = st.slider("**Anzahl Re-Assemblys je linearem Lebenszyklus**", min_value=1, max_value=5, value=2)

    with st.expander("**Ökologie spezifische Merkmale**"):
            FußabdruckErste = st.slider('Fußabdruck der 1. kleinen Re-Assembly bezogen auf den, einer Neuproduktion [%]', min_value=0, max_value=100, value=15, format="%d %%")
            FußabdruckSteigung = st.slider('Steigung des Fußabdrucks von einer kleinen Re-Assembly zur nächsten  [%-punkte]', min_value=0, max_value=50, value=10, format="%d %%")
            FußabdruckZweite = st.slider('Fußabdruck der 1. großen Re-Assembly bezogen auf den, einer Neuproduktion [%]', min_value=0, max_value=100, value=45, format="%d %%")
            FußabdruckZweiteSteigung = st.slider ('Steigung des Fußabdrucks von einer großen Re-Assembly zur nächsten [%-punkte]', min_value=0, max_value=50, value=15, format="%d %%")
            FußabdruckNutzung = st.number_input('Fußabdruck in der Nutzung bezogen auf den Fußabdruck einer Neuproduktion [%]', min_value=0, value=80)
            FußabdruckNutzungVerb = st.slider('Grad der vorzeitigen Effizienzsteigerung durch Re-Assembly  [0 = nicht vorhanden - 10 = sehr stark]', min_value=0, max_value=10, value=5)
        
    with st.expander("**Ökonomie spezifische Merkmale**"):
            KostenErste = st.slider('Kosten der 1. kleinen Re-Assembly bezogen auf die, einer Neuproduktion [%]', min_value=0, max_value=100, value=15, format="%d %%")
            KostenSteigung = st.slider('Steigung der Kosten von einer kleinen Re-Assembly zur nächsten [%-punkte]', min_value=0, max_value=50, value=10, format="%d %%")
            KostenZweite = st.slider('Kosten der 1. großen Re-Assembly bezogen auf die, einer Neuproduktion [%]', min_value=0, max_value=100, value=45, format="%d %%")
            KostenZweiteSteigung = st.slider ('Steigung der Kosten von einer großen Re-Assembly zur nächsten [%-punkte]', min_value=0, max_value=50, value=15, format="%d %%")
            Marge = st.slider('Anteil der Herstellungskosten am Verkaufspreis [%]', min_value=0, max_value=100, value=60, format="%d %%")
            Subskription = st.number_input('Höhe der Subskriptionserlöse in einem linearen Lebenszyklus bezogen auf den linearen Verkaufserlös [%]', min_value=0, value=120)
            

    with st.expander("**Kundennutzen spezifische Merkmale**"):
        Innovation = st.slider('Grad des Innovationsrückgangs [0 = nicht vorhanden - 10 = sehr stark]', min_value=0, max_value=10, value=5)
    

    st.divider(width="stretch")

    st.button('Link zum Whitepaper')

# WZL Logo in Sidebar anzeigen
st.logo("WZL_Logo.svg", size="large", link=None, icon_image=None)



### Ökologie Diagramm Berechnung

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

for okolog_i in range(1, 21):
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
okolog_100prozent = False

# Startpunkt bei (0, 0)
okologRe_x_values.append(0)
okologRe_y_values.append(0)

# Der erste Sprung auf 101, damit de linke Fensterrand mit Vorzeichenwechsel-Kriterium sicher gefunden wird 1 Höher als lineare Kurve
okologRe_y_temp = 101  
okologRe_x_values.append(0)
okologRe_y_values.append(okologRe_y_temp)

# Weiterer Kurvenverlauf
for okologRe_i in range(1, int(20*Anz_ReAss) + 1):
    
    if (okologRe_i-1) % Anz_ReAss == 0: # Re-Assemblys, die mit einer Neuproduktion zusammenfallen sollen keine vorzeitige Verbesserung haben
        okologRe_y_temp += 100 * FußabdruckNutzung /100 /Anz_ReAss - 1 #-1 damit marker für Sweetspot an rechten rand des Bereichs rutscht, in dem der Vorteil konstant ist/wäre
    else:
        okologRe_y_temp += 100 * FußabdruckNutzung /100 /Anz_ReAss * (1-(FußabdruckNutzungVerb / 25))
    
    okologRe_x_values.append(okologRe_i/Anz_ReAss)
    okologRe_y_values.append(okologRe_y_temp)
    okologRe_y_temp2 = okologRe_y_temp

    if okologRe_i % 2 != 0 :
        okologRe_y_temp += 100 * (FußabdruckErste + FußabdruckSteigung * (okologRe_i-1)/2) / 100
        okologRe_x_values.append(okologRe_i/Anz_ReAss)
        okologRe_y_values.append(okologRe_y_temp)
        #großer Sprung durch Re-Assembly    
    
    else: 
        okologRe_y_temp +=100* (FußabdruckZweite+FußabdruckZweiteSteigung*((okologRe_i-2)/2))/100
        okologRe_x_values.append(okologRe_i/Anz_ReAss) 
        okologRe_y_values.append(okologRe_y_temp) 
        
        # Prüfen ob 100% Aufwand (Fußabdruckzuwachs) bei Re-Assembly überschritten werden
    if okologRe_y_temp - okologRe_y_temp2 >=100 and okolog_100prozent == False : 
        okolog_100prozent = okologRe_i
        

## Berechnung von Sweetspot und Fenster-Grenzen Ökologie

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
    if okologRe_x_values[i] == ((okolog_sweetspot + 1) /Anz_ReAss) :
        okolog_neustart_y_value = okologRe_y_values[i]
        break
        

# Vorzeichenwechsel finden
# Initialisierung für die Suche nach Vorzeichenwechseln
okolog_min_neg_to_pos_x = None
okolog_max_pos_to_neg_x = None


for i in range(1, len(df_interpolated)):
    previous_value = df_interpolated['Differenz'].iloc[i-1]
    current_value = df_interpolated['Differenz'].iloc[i]
    
    if previous_value < 0 and current_value > 0:
        # Wechsel von negativ zu positiv
        if okolog_min_neg_to_pos_x is None or df_interpolated['x'].iloc[i] < okolog_min_neg_to_pos_x:
            okolog_min_neg_to_pos_x = df_interpolated['x'].iloc[i]
    
    elif previous_value > 0 and current_value < 0:
        # Wechsel von positiv zu negativ
        if okolog_max_pos_to_neg_x is None or df_interpolated['x'].iloc[i] > okolog_max_pos_to_neg_x:
            okolog_max_pos_to_neg_x = df_interpolated['x'].iloc[i]



# Fenstergrenzen berechnen
if okolog_min_neg_to_pos_x is None:
    okolog_fenster_low = 1
    #okolog_min_neg_to_pos_x = 1/Anz_ReAss
else:
    okolog_fenster_low = int(okolog_min_neg_to_pos_x * Anz_ReAss)

if okolog_max_pos_to_neg_x is None:
    okolog_fenster_high = None
    okolog_max_pos_to_neg_x = 19
    okolog_sweetspot = False
else:
    okolog_fenster_high = int(okolog_max_pos_to_neg_x * Anz_ReAss -1)

okolog_xWindow_max_y_value = 0
for i in range(len(okolog_x_values)):
    if okolog_x_values[i] == int(okolog_max_pos_to_neg_x+1) :
        okolog_xWindow_max_y_value = okolog_y_values[i]

# Verlauf bei Neustart am Re-wind Punkt Liniendiagramm Werte
okologRe_neustart_x_values = [x + (int(okolog_sweetspot/Anz_ReAss)+(1/Anz_ReAss)) for x in okologRe_x_values]
okologRe_neustart_y_values = [y + okolog_neustart_y_value for y in okologRe_y_values]






#### Kundennutzen Diagramm Berechnung

## Kundennutzen Lineare Kurve

# Initialisierung der x- und y-Werte für den Graphen
kunde_x_values = []
kunde_y_values = []

# Startpunkt bei (0, 40)
Kunde_y_temp = 40
kunde_x_values.append(0)
kunde_y_values.append(Kunde_y_temp)

# Erstellen des Datensatzes
for kunde_i in range(1, 21):
    # Cosinusförmiger Abfall von Kunde_y_temp um 50 (Einstellwert ist die 25) zwischen kunde_i und kunde_i + 1
    kunde_x_cosine = np.linspace(kunde_i - 1, kunde_i, num=50)  # Interpolation zwischen den Punkten
    kunde_y_cosine = Kunde_y_temp - (25 * (1 - np.cos((np.pi / 2) * (kunde_x_cosine - (kunde_i - 1)))))
    
    # Hinzufügen der interpolierten Punkte zum Datensatz
    kunde_x_values.extend(kunde_x_cosine)
    kunde_y_values.extend(kunde_y_cosine)

    # Aktualisieren des aktuellen y-Wertes nach dem Abfall
    Kunde_y_temp -= 50
    
    # Sprung um ... bei Neuproduktion
    if kunde_i < 20:
        Kunde_y_temp += 60
        kunde_x_values.append(kunde_i)
        kunde_y_values.append(Kunde_y_temp)

# Erstellen des DataFrames zur Visualisierung
kunde_data = {
    "Kunde_X_Werte": kunde_x_values,
    "Kunde_Y-Werte": kunde_y_values,
}

kunde_df = pd.DataFrame(kunde_data)

# Berechnung des gleitenden Durchschnitts über ein Fenster von Größe 'window'
window_size = int(len(kunde_df) / len(np.unique(kunde_df["Kunde_X_Werte"]))) * 50 
floating_average_asymmetric = (
    pd.Series(kunde_df["Kunde_Y-Werte"])
    .rolling(window=window_size, min_periods=1)
    .mean()
)

### Kundennutzen Re-Assembly

# Initialisierung der x- und y-Werte für die ReAss Kurve
kundeRe_x_values = []
kundeRe_y_values = []

# Startpunkt bei (0, 40) für die ReAss Kurve
KundeRe_y_temp = 40
kundeRe_x_values.append(0)
kundeRe_y_values.append(KundeRe_y_temp)

# Erstellen des Datensatzes Re-Assembly
for kundeRe_i in range(1, int(20 * Anz_ReAss + 1)):
    num_points = 25  # Reduzierung der Anzahl Punkte 
    kundeRe_x_cosine = np.linspace(kundeRe_i - 1, kundeRe_i, num=num_points)
    kundeRe_y_cosine = KundeRe_y_temp - (25/(Anz_ReAss*Anz_ReAss) * (1 - np.cos((np.pi / 2) * (kundeRe_x_cosine - (kundeRe_i -1 )))))
    
    # Hinzufügen der interpolierten Punkte zum Datensatz
    kundeRe_x_values.extend(kundeRe_x_cosine)
    kundeRe_y_values.extend(kundeRe_y_cosine)

    # Aktualisieren des aktuellen y-Wertes nach dem Abfall
    KundeRe_y_temp -= 50/Anz_ReAss
    
    # Sprung um ... bei Neuproduktion - Innovationsrückgang in Klammer berücksichtigt
    if kundeRe_i < int(20 * Anz_ReAss):
        KundeRe_y_temp += (60/Anz_ReAss - 1.1*((Innovation * 25) * (((kundeRe_i)/150))))
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


# Berechnung des gleitenden Durchschnitts
window_size = int(len(kunde_re_df) / len(np.unique(kunde_re_df["KundeRe_X_Werte"]))) * 50
floating_average_Re_asymmetric = (
    pd.Series(kunde_re_df["KundeRe_Y_Werte"])
    .rolling(window=window_size, min_periods=1)
    .mean()
)


## Korridor des Kundennutzen definieren
kunde_korridor_x = np.arange(0, 21, 1)
kunde_korridor_oben = 40 + 10 * kunde_korridor_x 
kunde_korridor_unten = 5 + 10 * kunde_korridor_x 


## Kundennutzen Sweetspot berechnen

kunde_diff = floating_average_asymmetric - floating_average_Re_asymmetric
kunde_schnittpunkte = []
kunde_diff_indices = np.where(np.diff(np.sign(kunde_diff)))[0]
for idx in kunde_diff_indices:
    if idx + 1 < len(kunde_x_values):  # Sicherstellen, dass idx+1 im gültigen Bereich liegt!
        x_a, x_b = kunde_x_values[idx], kunde_x_values[idx+1]
        y_a, y_b = kunde_diff[idx], kunde_diff[idx+1]
        if y_b != y_a:
            # Lineare Interpolation für genaueren Schnittpunkt
            Kunde_schnittpunkt_x = x_a - y_a * (x_b - x_a) / (y_b - y_a)
            kunde_schnittpunkte.append(Kunde_schnittpunkt_x)


kunde_schnittpunkt_sweetspot = max(kunde_schnittpunkte)
kunde_sweetspot = int(kunde_schnittpunkt_sweetspot*Anz_ReAss)

## Kundennutzen Fenster Berechnen
kunde_fenster_low = 1


kunde_korridor_unten_df = 5 + (10 * (np.array(scaled_kundeRe_x_values)))

diff = np.array(kundeRe_y_values) - kunde_korridor_unten_df
kunde_ReUndKorridor_indices = np.where(np.diff(np.sign(diff)))[0]

kunde_ReUndKorridor_Schnittpunkte = []
for idx in kunde_ReUndKorridor_indices:
    if idx+1 < len(kundeRe_x_values):
        x_d, x_e = kundeRe_x_values[idx], kundeRe_x_values[idx+1]
        y_d, y_e = diff[idx], diff[idx+1]
        if y_e != y_d:
            schnitt_x = x_d - y_d * (x_e-x_d)/(y_e-y_d)
            kunde_ReUndKorridor_Schnittpunkte.append(schnitt_x)

if kunde_ReUndKorridor_Schnittpunkte:
    kunde_fenster_schnitt_high = min (kunde_ReUndKorridor_Schnittpunkte)  
    kunde_fenster_high  = int (kunde_fenster_schnitt_high)
else: 
    kunde_fenster_high= False
    kunde_fenster_schnitt_high = 20*Anz_ReAss


# Verlauf bei Neustart am Re-wind Punkt Liniendiagramm Werte
kundeRe_neustart_x_values = [x + ((kunde_sweetspot + 1)/Anz_ReAss) for x in scaled_kundeRe_x_values]
kunde_neustart_y_value =  40 + 10 *  ((kunde_sweetspot + 1)/Anz_ReAss) # Punkt von obere Korridor Grenze
kundeRe_neustart_y_values = [y + kunde_neustart_y_value - 40 for y in kundeRe_y_values] #-100 weil bei x=0 bei 100 startet


# Y-Ausdehnung ermitteln
if kunde_fenster_high == False:
    kunde_xWindow_max_y_value = 250
else:
    kunde_xWindow_max_y_value = 40 + 10 * (kunde_fenster_high/Anz_ReAss +1)  



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

for okonomRe_i in range(1, 21):
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
okonom_100prozent = False

# Startpunkt bei (0, 0)
okonomRe_x_values.append(0)
okonomRe_y_values.append(0)

okonomRe_y_temp = -100   # Der erste Sprung auf (0,-100)
okonomRe_x_values.append(0)
okonomRe_y_values.append(okonomRe_y_temp)

for okonomRe_i in range(1, int(20*Anz_ReAss) + 1):
    # lineare Steigung durch Subskription
    okonomRe_y_temp += (100+okonom_gewinn) * (Subskription/100) / Anz_ReAss
    okonomRe_x_values.append(okonomRe_i/Anz_ReAss)
    okonomRe_y_values.append(okonomRe_y_temp)

    okonomRe_y_temp2 = okonomRe_y_temp
    
    #kleiner Sprung durch Re-Assembly
    if okonomRe_i % 2 != 0:
        okonomRe_y_temp -=100* (KostenErste+KostenSteigung*((okonomRe_i-1)/2))/100
        okonomRe_x_values.append(okonomRe_i/Anz_ReAss) 
        okonomRe_y_values.append(okonomRe_y_temp) 

    #großer Sprung durch Re-Assembly    
    else: 
        okonomRe_y_temp -=100* (KostenZweite+KostenZweiteSteigung * ((okonomRe_i-2)/2))/100
        okonomRe_x_values.append(okonomRe_i/Anz_ReAss) 
        okonomRe_y_values.append(okonomRe_y_temp) 

    if okonomRe_y_temp2 - okonomRe_y_temp >= 100 and okonom_100prozent == False: 
        okonom_100prozent = okonomRe_i



## Fenster und Sweetspot Ökonomie
x_common = np.linspace(min(min(okonom_x_values), min(okonomRe_x_values)), max(max(okonom_x_values), max(okonomRe_x_values)), num=500)

okonom_interp = interp1d(okonom_x_values, okonom_y_values, kind='linear', fill_value="extrapolate")
okonomRe_interp = interp1d(okonomRe_x_values, okonomRe_y_values, kind='linear', fill_value="extrapolate")

okonom_y_values_interp = okonom_interp(x_common)
okonomRe_y_values_interp = okonomRe_interp(x_common)

okonom_diff= okonomRe_y_values_interp - okonom_y_values_interp 

# Erstelle einen DataFrame mit den x-Werten und den beiden y-Wert-Reihen und der Differenz der y-Werte
okonom_data = {
    'x': x_common,
    'Interpolated Okonom': okonom_y_values_interp,
    'Interpolated Okonom Re': okonomRe_y_values_interp,
    'Differenz' : okonom_diff
}
df_interpolated = pd.DataFrame(okonom_data)

# Sweetspot = Maximaler positiver Wert in 'Differenz' finden 
okonom_diff_max = df_interpolated[df_interpolated['Differenz'] == df_interpolated['Differenz'].max()]['x'].values[0]
okonom_sweetspot = int(okonom_diff_max*Anz_ReAss)
okonom_neustart_y_value = 0
for i in range(len(okonomRe_x_values)):
    if okonomRe_x_values[i] == ((okonom_sweetspot + 1) /Anz_ReAss) :
        okonom_neustart_y_value = okonomRe_y_values[i]
        break
        

# Vorzeichenwechsel finden für Fenstergrenzen
# Initialisierung für die Suche nach Vorzeichenwechseln
okonom_min_neg_to_pos_x = None
okonom_max_pos_to_neg_x = None

for i in range(1, len(df_interpolated)):
    previous_value = df_interpolated['Differenz'].iloc[i-1]
    current_value = df_interpolated['Differenz'].iloc[i]
    
    if previous_value < 0 and current_value > 0:
        # Wechsel von negativ zu positiv
        if okonom_min_neg_to_pos_x is None or df_interpolated['x'].iloc[i] < okonom_min_neg_to_pos_x:
            okonom_min_neg_to_pos_x = df_interpolated['x'].iloc[i]
    
    elif previous_value > 0 and current_value < 0:
        # Wechsel von positiv zu negativ
        if okonom_max_pos_to_neg_x is None or df_interpolated['x'].iloc[i] > okonom_max_pos_to_neg_x:
            okonom_max_pos_to_neg_x = df_interpolated['x'].iloc[i]


# Fenstergrenzen berechnen
if okonom_min_neg_to_pos_x == None:
    okonom_fenster_low = None
else:  
    okonom_fenster_low = int(okonom_min_neg_to_pos_x * Anz_ReAss)

if okonom_max_pos_to_neg_x == None or okonom_max_pos_to_neg_x < 2:
    okonom_fenster_high = None
    okonom_max_pos_to_neg_x = 20

else:
    okonom_fenster_high = int(okonom_max_pos_to_neg_x * Anz_ReAss -1)



# Verlauf bei Neustart am Re-wind Punkt Liniendiagramm Werte
okonomRe_neustart_x_values = [x + ((okonom_sweetspot/Anz_ReAss)+(1/Anz_ReAss)) for x in okonomRe_x_values]
okonomRe_neustart_y_values = [y + okonom_neustart_y_value for y in okonomRe_y_values]

# Y-Ausdehnung ermitteln
okonom_xWindow_max_y_value = 0
for i in range(len(okonom_x_values)):
    if okonomRe_neustart_x_values[i] == int(okonom_max_pos_to_neg_x+1) :
        okonom_xWindow_max_y_value = okonomRe_neustart_y_values[i]




### Diagramme anzeigen
st.title('Simulationstool zur Re-Wind-Analyse spezifischer Produkte')
st.text("-- Diese App wird laufend verbessert. Senden Sie uns gerne Ihre Anmerkungen --")
st.divider(width="stretch")
st.subheader('Einfach in der Sidebar (links) produktspezifische Merkamale eingeben ...')
st.subheader('... und Re-Wind Diagramme anzeigen lassen')


# Diagramm anzeigen Ökologie
with st.expander("**Ökologie Diagramm**"):

    fig_okolog_plotly = go.Figure()

    # Hinzufügen der linearen Kurve zum Diagramm auf der primären X-Achse
    fig_okolog_plotly.add_trace(go.Scatter(
        x=okolog_x_values,
        y=okolog_y_values,
        mode="lines",
        name="Produkt mit linearer Nutzung",
        line=dict(color='darkblue')
    ))

    # Hinzufügen der Re-Assembly Kurve zum Diagramm auf einer sekundären X-Achse mit Skalierung durch Anz_ReAss
    fig_okolog_plotly.add_trace(go.Scatter(
        x=okologRe_x_values,
        y=okologRe_y_values,
        mode="lines",
        name="Re-Assembly Produkt",
        line=dict(color='lightgreen')
    ))

    if okolog_min_neg_to_pos_x != None: #Abfrage ob Fenster vorhanden

        # Fenster Bereich plotten
        fig_okolog_plotly.add_shape(type="rect",
                    x0=okolog_min_neg_to_pos_x, x1=okolog_max_pos_to_neg_x,
                    y0=0, y1=okolog_xWindow_max_y_value,
                    fillcolor="orange",
                    opacity=0.1,
                    layer="below",
                    line_width=0)
        
        # Füge ein Icon zur linken Grenze hinzu
        fig_okolog_plotly.add_annotation(
            x=okolog_min_neg_to_pos_x,
            y=okolog_xWindow_max_y_value*0.5,
            text="➡️",
            showarrow=False,
            font=dict(size=15),
        )

        # Füge ein Icon zur rechten Grenze hinzu
        fig_okolog_plotly.add_annotation(
            x=okolog_max_pos_to_neg_x,
            y=okolog_xWindow_max_y_value*0.5,
            text="⬅️",
            showarrow=False,
            font=dict(size=15),
        )

        # Sweetspot Indikator und Neustartkurve plotten
        if okolog_sweetspot != False:
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

            # Hinzufügen der Re-Assembly kurve nach dem Re-Wind Punkt
            fig_okolog_plotly.add_trace(go.Scatter(
            x=okologRe_neustart_x_values,
            y=okologRe_neustart_y_values,
            mode="lines",
            name="Re-Assembly Produkt: Zweiter Kreislauf",
            line=dict(dash='dot', color='lightgreen')
            ))



    #Zweite X-Achse für Re-Assembly Zählung mit leerem Datensatz initialisieren
    okolog_x_values_Re = [x * Anz_ReAss for x in okolog_x_values]
    fig_okolog_plotly.add_trace(go.Scatter(
        x= okolog_x_values_Re,
        y=[],
        xaxis='x2',
        
    ))

    
    fig_okolog_plotly.update_layout(
        xaxis=dict(title=dict(text='Lineare Lebenszyklen',font=dict(color="darkblue")), side='bottom', tickmode='linear', dtick=1, tickfont=dict(color='darkblue'), position=0, range=[-0.01, int(okolog_max_pos_to_neg_x)+1.01]),
        xaxis2=dict(title=dict(text="Re-Assemblys",font=dict(color="lightgreen")), side='bottom', tickmode='linear', dtick=1, tickfont=dict(color='lightgreen'), overlaying='x', position=0.06, range=[-0.01, (int(okolog_max_pos_to_neg_x)+1.01)*Anz_ReAss]),
        yaxis=dict(title='Kumulierter ökologischer Fußabdruck', showticklabels=False, range=[-100, okolog_xWindow_max_y_value*1.2]),
        legend=dict(x=0, y=1, xanchor='left', yanchor='bottom', bgcolor='rgba(0,0,0,0)'),
        )




    # fig_okolog_plotly.update_layout(
    #     xaxis=dict(title='Lineare Lebenszyklen', side='bottom', tickmode='linear', dtick=1, range=[-0.01, int(okolog_max_pos_to_neg_x)+1.01]),
    #     xaxis2=dict(title='Sekundäre X-Achse', side='bottom', anchor='free', position=0.2),
    #     yaxis=dict(title='Kumulierter ökologischer Fußabdruck', showticklabels=False, range=[0, okolog_xWindow_max_y_value*1.2]),
    #     legend=dict(x=0, y=1, xanchor='left', yanchor='bottom', bgcolor='rgba(0,0,0,0)'),
    # )


    st.plotly_chart(fig_okolog_plotly)

    # Fenster und Sweetspot anzeigen Ökologie
    col1, col2, col3 = st.columns(3)
    if okolog_min_neg_to_pos_x == None: #Anzeige falls kein Fenster vorhanden
        st.markdown(f"""
                <div style="text-align: center; white-space: nowrap;">
                    <strong> Kein ReAssembly Fenster vorhanden</strong><br><br>
                    </div>
            """, unsafe_allow_html=True)
        
    else: # Anzeige wenn Fenster vorhanden
        if okolog_100prozent != False and (okolog_fenster_high == None or okolog_100prozent < okolog_fenster_high):
            st.markdown(f"""
            <div style="text-align: center; white-space: nowrap;">
            <strong> Achtung Fußabdruck übersteigt bei der {okolog_100prozent}. Re-Assembly den einer Neuproduktion</strong><br><br>
            </div>
            """, unsafe_allow_html=True)
        
        
        with col1:
            st.markdown(f"""
                <div style="text-align: center; white-space: nowrap;">
                    <strong>➡️ Untere Fenstergrenze</strong><br>
                    <span style="font-size: 24px;">≥</span> 
                    <span style="font-size: 24px;">{okolog_fenster_low}</span>
                    <span style="font-size: 14px;">Re-Assemblys</span>
                </div>
            """, unsafe_allow_html=True)

        
        with col2:
            st.markdown(f"""
                <div style="text-align: center; white-space: nowrap;">
                    <strong>🔄 Re-Wind Punkt</strong><br>
                    <span style="font-size: 14px;">nach</span>
                    <span style="font-size: 24px;">{okolog_sweetspot}</span>
                    <span style="font-size: 14px;">Re-Assemblys</span>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
                <div style="text-align: center; white-space: nowrap;">
                    <strong>⬅️ Obere Fenstergrenze</strong><br>
                    <span style="font-size: 24px;">≤</span>
                    <span style="font-size: 24px;">{okolog_fenster_high}</span>
                    <span style="font-size: 14px;">Re-Assemblys</span>
                </div>
            """, unsafe_allow_html=True)


## Diagramm anzeigen Ökonomie
with st.expander("**Ökonomie Diagramm**"):

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

    #Zweite X-Achse für Re-Assembly Zählung mit leerem Datensatz initialisieren
    okonom_x_values_Re = [x * Anz_ReAss for x in okonom_x_values]
    fig_okonom_plotly.add_trace(go.Scatter(
        x= okonom_x_values_Re,
        y=[],
        xaxis='x2',
        
    ))

    
    fig_okonom_plotly.update_layout(
        xaxis=dict(title=dict(text='Lineare Lebenszyklen',font=dict(color="darkblue")), side='bottom', tickmode='linear', dtick=1, tickfont=dict(color='darkblue'), position=0, range=[-0.01, int(okonom_max_pos_to_neg_x)+1.01]),
        xaxis2=dict(title=dict(text="Re-Assemblys",font=dict(color="lightgreen")), side='bottom', tickmode='linear', dtick=1, tickfont=dict(color='lightgreen'), overlaying='x', position=0.06, range=[-0.01, (int(okonom_max_pos_to_neg_x)+1.01)*Anz_ReAss]),
        yaxis=dict(title='Kumulierter ökologischer Fußabdruck', showticklabels=False, range=[-100-okonom_xWindow_max_y_value*0.1, okonom_xWindow_max_y_value*1.2]),
        legend=dict(x=0, y=1, xanchor='left', yanchor='bottom', bgcolor='rgba(0,0,0,0)'),
        )

    if okonom_min_neg_to_pos_x != None: #Abfrage ob Fenster vorhanden
        # Hinzufügen der Re-Assembly kurve nach dem Re-Wind Punkt
        fig_okonom_plotly.add_trace(go.Scatter(
            x=okonomRe_neustart_x_values,
            y=okonomRe_neustart_y_values,
            mode="lines",
            name="Re-Assembly Produkt: Zweiter Kreislauf",
            line=dict(dash='dot', color='lightgreen')
        ))

        # Fenster Bereich plotten
        fig_okonom_plotly.add_shape(type="rect",
            x0=okonom_min_neg_to_pos_x, x1=okonom_max_pos_to_neg_x,
            y0=-100,
            y1=okonom_xWindow_max_y_value,
            fillcolor="orange",
            opacity=0.1,
            layer="below",
            line_width=0)
    
        # Füge ein Icon zur linken Grenze hinzu
        fig_okonom_plotly.add_annotation(
            x=okonom_min_neg_to_pos_x,
            y=okonom_xWindow_max_y_value*0.5,
            text="➡️",
            showarrow=False,
            font=dict(size=15),
        )

        # Füge ein Icon zur rechten Grenze hinzu
        fig_okonom_plotly.add_annotation(
            x=okonom_max_pos_to_neg_x,
            y=okonom_xWindow_max_y_value*0.5,
            text="⬅️",
            showarrow=False,
            font=dict(size=15),
        )

        # Sweetspot Indikator plotten
        okonom_sweetspot_marker_x_values = [okonom_sweetspot/Anz_ReAss, okonom_diff_max, okonom_diff_max]
        okonom_sweetspot_marker_y_values = [-100, (okonom_xWindow_max_y_value)*0.1-100, okonom_xWindow_max_y_value]
        fig_okonom_plotly.add_trace(go.Scatter(
            x=okonom_sweetspot_marker_x_values,
            y=okonom_sweetspot_marker_y_values,
            mode='lines',
            line=dict(color="red", width=2),
            showlegend=False))
        
        # Füge ein Icon hinzu zum Neustartzeitpunkt
        fig_okonom_plotly.add_annotation(
            x=okonom_diff_max,
            y=okonom_xWindow_max_y_value,
            text="🔄",
            showarrow=False,
            font=dict(size=20),
        )
    
    st.plotly_chart(fig_okonom_plotly)

# Fenster und Sweetspot anzeigen Ökonomie
    col1, col2, col3 = st.columns(3)
    if okonom_min_neg_to_pos_x == None: #Anzeige falls kein Fenster vorhanden
        st.markdown(f"""
            <div style="text-align: center; white-space: nowrap;">
            <strong> Kein ReAssembly Fenster vorhanden</strong><br><br>
            </div>
            """, unsafe_allow_html=True)
    
    else: #Anzeige falls Fenster vorhanden

        if okonom_100prozent != False and (okonom_fenster_high == None or okonom_100prozent < okonom_fenster_high):
            st.markdown(f"""
            <div style="text-align: center; white-space: nowrap;">
            <strong> Achtung Kosten übersteigen bei der {okonom_100prozent}. Re-Assembly die einer Neuproduktion</strong><br><br>
            </div>
            """, unsafe_allow_html=True)

        with col1:
            st.markdown(f"""
                <div style="text-align: center; white-space: nowrap;">
                    <strong>➡️ Untere Fenstergrenze</strong><br>
                    <span style="font-size: 24px;">≥</span> 
                    <span style="font-size: 24px;">{(okonom_fenster_low)}</span>
                    <span style="font-size: 14px;">Re-Assemblys</span>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div style="text-align: center; white-space: nowrap;">
                    <strong>🔄 Re-Wind Punkt</strong><br>
                    <span style="font-size: 14px;">nach</span>
                    <span style="font-size: 24px;">{okonom_sweetspot}</span>
                    <span style="font-size: 14px;">Re-Assemblys</span>
                </div>
            """, unsafe_allow_html=True)

        if okonom_fenster_high == None: okonom_fenster_high = "Out of Scope"
        with col3:
            st.markdown(f"""
                <div style="text-align: center; white-space: nowrap;">
                    <strong>⬅️ Obere Fenstergrenze</strong><br>
                    <span style="font-size: 24px;">≤</span>
                    <span style="font-size: 24px;">{okonom_fenster_high}</span>
                    <span style="font-size: 14px;">Re-Assemblys</span>
                </div>
            """, unsafe_allow_html=True)


## Diagramm anzeigen Kundennutzen
with st.expander("**Kundennutzen Diagramm**"):

    fig_kunde_plotly = go.Figure()

    # Lineares Produkt
    fig_kunde_plotly.add_trace(go.Scatter(
        x=kunde_df["Kunde_X_Werte"],
        y=kunde_df["Kunde_Y-Werte"],
        mode="lines",
        line=dict(color='darkblue'),
        name="Produkt mit linearer Nutzung"  
    ))

    # Lineares Podukt Mittelwert
    fig_kunde_plotly.add_trace(go.Scatter(
        x=kunde_df["Kunde_X_Werte"],
        y=floating_average_asymmetric,
        mode="lines",
        line=dict(dash='dash', color='darkblue'),
        name="Produkt mit linearer Nutzung: langfristiges Mittel"
    ))

    # ReAssembly Produkt 
    fig_kunde_plotly.add_trace(go.Scatter(
        x=kunde_re_df["KundeRe_X_Werte"],
        y=kunde_re_df["KundeRe_Y_Werte"],
        mode="lines",
        line=dict(color='lightgreen'), 
        name="Re-Assembly Produkt"  
    ))

    # ReAssembly Produkt Mittelwert
    fig_kunde_plotly.add_trace(go.Scatter(
        x=kunde_re_df["KundeRe_X_Werte"],
        y=floating_average_Re_asymmetric,
        mode="lines",
        line=dict(dash='dash', color='lightgreen'),
        name="Re-Assembly Produkt: langfristiges Mittel"  
    ))
    
    # Korridor des Kundennutzen
    fig_kunde_plotly.add_trace(go.Scatter(
        x=np.concatenate([kunde_korridor_x, kunde_korridor_x[::-1]]),
        y=np.concatenate([kunde_korridor_unten, kunde_korridor_oben[::-1]]),
        fill='toself',
        fillcolor='rgba(128,128,128,0.1)',
        line=dict(color='rgba(255,255,255,0)'),
        showlegend=False,
    ))

    if Anz_ReAss != 1 and Innovation != 0: #Abfrage ob Kundennutzen Vorteilhaft sein kann
        

        # Hinzufügen der Re-Assembly kurve nach dem Re-Wind Punkt
        fig_kunde_plotly.add_trace(go.Scatter(
            x=kundeRe_neustart_x_values,
            y=kundeRe_neustart_y_values,
            mode="lines",
            name="Re-Assembly Produkt: Zweiter Kreislauf",
            line=dict(dash='dot', color='lightgreen')
        ))

        # Fenster Bereich plotten
        fig_kunde_plotly.add_shape(type="rect",
                    x0=0.5, x1= (kunde_fenster_schnitt_high/Anz_ReAss),
                    y0=0, y1=kunde_xWindow_max_y_value,
                    fillcolor="orange",
                    opacity=0.1,
                    layer="below",
                    line_width=0)
        
        # Füge ein Icon zur linken Grenze hinzu
        fig_kunde_plotly.add_annotation(
            x=0.5,
            y=kunde_xWindow_max_y_value*0.4,
            text="➡️",
            showarrow=False,
            font=dict(size=15),
        )

        # Füge ein Icon zur rechten Grenze hinzu
        fig_kunde_plotly.add_annotation(
            x=(kunde_fenster_schnitt_high/Anz_ReAss),
            y=kunde_xWindow_max_y_value*0.4,
            text="⬅️",
            showarrow=False,
            font=dict(size=15),
        )

        # Sweetspot Indikator plotten
            # Werte für Sweetspot indikator linie
        kunde_sweetspot_marker_x_values = [kunde_sweetspot/Anz_ReAss, kunde_schnittpunkt_sweetspot, kunde_schnittpunkt_sweetspot]
        kunde_sweetspot_marker_y_values = [0, 20, kunde_xWindow_max_y_value]
        fig_kunde_plotly.add_trace(go.Scatter(
            x=kunde_sweetspot_marker_x_values,
            y=kunde_sweetspot_marker_y_values,
            mode='lines',
            line=dict(color="red", width=2),
            showlegend=False))
        
        # Füge ein Icon hinzu zum Neustartzeitpunkt
        fig_kunde_plotly.add_annotation(
            x=kunde_schnittpunkt_sweetspot,
            y=kunde_xWindow_max_y_value,
            text="🔄",
            showarrow=False,
            font=dict(size=20),
        )

    
    #Zweite X-Achse für Re-Assembly Zählung mit leerem Datensatz initialisieren
    kunde_x_values_Re = [x * Anz_ReAss for x in kunde_x_values]
    fig_kunde_plotly.add_trace(go.Scatter(
        x= kunde_x_values_Re,
        y=[],
        xaxis='x2',
        
    ))

    
    fig_kunde_plotly.update_layout(
        xaxis=dict(title=dict(text='Lineare Lebenszyklen',font=dict(color="darkblue")), side='bottom', tickmode='linear', dtick=1, range=[-0.01, int(kunde_fenster_schnitt_high)/Anz_ReAss +2.1], tickfont=dict(color='darkblue'), position=0),
        xaxis2=dict(title=dict(text="Re-Assemblys",font=dict(color="lightgreen")), overlaying='x', side='bottom', layer="above traces", tickmode='linear', dtick=1, range=[-0.01, int(kunde_fenster_schnitt_high) +2.1*Anz_ReAss], tickfont=dict(color='lightgreen'), position=0.06),
        yaxis=dict(title='Kundennutzen', showticklabels=False, range=[-kunde_xWindow_max_y_value*0.1, kunde_xWindow_max_y_value*1.2]),
        legend=dict(x=0, y=1, xanchor='left', yanchor='bottom', bgcolor='rgba(0,0,0,0)'),
    )


    st.plotly_chart(fig_kunde_plotly)

# Fenster und Sweetspot anzeigen Kundennutzen
    if Anz_ReAss == 1: #Anzeige Kundennutzen nicht vorteilhaft
        st.markdown(f"""
            <div style="text-align: center; white-space: nowrap;">
            <strong> Dieser Re-Assembly Zyklus führt nicht zu einer Verbesserung des Kundennutzens</strong><br><br>
            </div>
            """, unsafe_allow_html=True)
        
    elif Innovation == 0:
        st.markdown(f"""
            <div style="text-align: center; white-space: nowrap;">
            <strong> Dies wäre ein optimales (utopisches) Produkt, welches den Kundennutzen enorm steigert</strong><br><br>
            </div>
            """, unsafe_allow_html=True)
    
    else: #Anzeige falls Fenster vorhanden
    
        col1, col2, col3 = st.columns(3)
        if 1 == None: #Anzeige falls kein Fenster vorhanden
            st.markdown(f"""
                    <div style="text-align: center; white-space: nowrap;">
                        <strong> Kein ReAssembly Fenster vorhanden</strong><br><br>
                        </div>
                """, unsafe_allow_html=True)
        else:
            with col1:
                st.markdown(f"""
                    <div style="text-align: center; white-space: nowrap;">
                        <strong>➡️ Untere Fenstergrenze</strong><br>
                        <span style="font-size: 24px;">≥</span> 
                        <span style="font-size: 24px;">{kunde_fenster_low}</span>
                        <span style="font-size: 14px;">Re-Assemblys</span>
                    </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                    <div style="text-align: center; white-space: nowrap;">
                        <strong>🔄 Re-Wind Punkt</strong><br>
                        <span style="font-size: 14px;">nach</span>
                        <span style="font-size: 24px;">{kunde_sweetspot}</span>
                        <span style="font-size: 14px;">Re-Assemblys</span>
                    </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                    <div style="text-align: center; white-space: nowrap;">
                        <strong>⬅️ Obere Fenstergrenze</strong><br>
                        <span style="font-size: 24px;">≤</span>
                        <span style="font-size: 24px;">{kunde_fenster_high}</span>
                        <span style="font-size: 14px;">Re-Assemblys</span>
                    </div>
                """, unsafe_allow_html=True)






### PDF Export

# Funktion zum Erstellen des PDFs
def create_pdf(product_name):
    timestamp = int(time.time())  # Aktuellen Zeitstempel erhalten
    pdf_file_path = f"output_{timestamp}.pdf"
    c = canvas.Canvas(pdf_file_path, pagesize=A4)  # A4-Größe in cm
    width, height = A4
    
    ## Kopfzeile vorberiten für alle Seiten
    def kopfzeile():
        # WZL Logo oben links    
        c.drawImage("WZL_Logo2.png", 0.5 * cm, height - 1.6 * cm, width=5 * cm, height=1.33 * cm)

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


    ## Kopfzeile einfügen
    kopfzeile()

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
    oekolog_Eigenschaften_Benennung = ["Fußabdruck der 1. kleinen Re-Assembly bezogen auf den, einer Neuproduktion", 
            "Steigung des Fußabdrucks von einer kleinen Re-Assembly zur nächsten",
            "Fußabdruck der 1. großen Re-Assembly bezogen auf den, einer Neuproduktion",
            "Steigung des Fußabdrucks von einer großen Re-Assembly zur nächsten",
            "Fußabdruck der Nutzung bezogen auf den Fußabdruck einer Neuproduktion",  
            "Grad der vorzeitigen Effizienzsteigerung durch Re-Assembly"]  
    
    oekolog_Eigenschaften_Werte = [f"{FußabdruckErste} %", f"{FußabdruckSteigung} %-punkte", f"{FußabdruckZweite} %", f"{FußabdruckZweiteSteigung} %-punkte", 
            f"{FußabdruckNutzung} %", f"{FußabdruckNutzungVerb} (0-10)"]  
    
    oekolog_Eigenschaften_Tabelle = height - 7.5 * cm
    for term, value in zip(oekolog_Eigenschaften_Benennung, oekolog_Eigenschaften_Werte):
        c.drawString(2 * cm, oekolog_Eigenschaften_Tabelle, term)
        c.drawString(16 * cm, oekolog_Eigenschaften_Tabelle, value) 
        oekolog_Eigenschaften_Tabelle -= 0.5 * cm


    # Ökonomische Eigenschaften in Tabelle
    c.setFont("Helvetica-Bold", 10)
    c.drawString(2 * cm, height - 11 * cm, "Ökologie spezifisch")

    c.setFont("Helvetica", 10)
    oekonom_Eigenschaften_Benennung = ["Kosten der 1. kleinen Re-Assembly bezogen auf die, einer Neuproduktion", 
            "Steigung der Kosten von einer kleinen Re-Assembly zur nächsten",
            "Kosten der 1. großen Re-Assembly bezogen auf die, einer Neuproduktion",
            "Steigung der Kosten von einer großen Re-Assembly zur nächsten",
            "Anteil der Herstellungskosten am Verkaufspreis",
            "Höhe der Subskriptionserlöse in einem linearen Lebenszyklus",
            "bezogen auf einen linearen Verkaufserlös"]  
    
    oekonom_Eigenschaften_Werte = [f"{KostenErste} %", f"{KostenSteigung} %-punkte", f"{KostenZweite} %", f"{KostenZweiteSteigung} %-punkte", 
            f"{Marge} (0-10)", f"{Subskription} %",""]  
    
    oekonom_Eigenschaften_Tabelle = height - 11.5 * cm
    for term, value in zip(oekonom_Eigenschaften_Benennung, oekonom_Eigenschaften_Werte):
        c.drawString(2 * cm, oekonom_Eigenschaften_Tabelle, term)
        c.drawString(16 * cm, oekonom_Eigenschaften_Tabelle, value) 
        oekonom_Eigenschaften_Tabelle -= 0.5 * cm


    # Kundennutzen Eigenschaften in Tabelle
    c.setFont("Helvetica-Bold", 10)
    c.drawString(2 * cm, height - 15.5 * cm, "Kundennutzen spezifisch")

    c.setFont("Helvetica", 10)
    kunde_Eigenschaften_Benennung = ["Grad des Innovationsrückgangs"]

    kunde_Eigenschaften_Werte = [f"{Innovation} (0-10)"]  
    
    kunde_Eigenschaften_Tabelle = height -16 * cm
    for term, value in zip(kunde_Eigenschaften_Benennung, kunde_Eigenschaften_Werte):
        c.drawString(2 * cm, kunde_Eigenschaften_Tabelle, term)
        c.drawString(16 * cm, kunde_Eigenschaften_Tabelle, value) 
        kunde_Eigenschaften_Tabelle -= 0.5 * cm
    

    ## Untertitel: Gesamtergebnis
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, height - 18 * cm, "Gesamtergebnis in den drei Dimensionen")

    if okolog_fenster_high == None: okolog_fenster_high_ = 100
    else: okolog_fenster_high_ = okolog_fenster_high
    if kunde_fenster_high == None: kunde_fenster_high_ = 100
    else: kunde_fenster_high_ = kunde_fenster_high
    if okonom_fenster_high == None: okonom_fenster_high_ =100
    else: okonom_fenster_high_ = okonom_fenster_high

    ges_fenster_low = max(okolog_fenster_low,kunde_fenster_low, okonom_fenster_low)
    ges_fenster_high = min(okolog_fenster_high_, kunde_fenster_high_, okonom_fenster_high_)
    min_sweetspot = min(okolog_sweetspot, kunde_sweetspot, okonom_sweetspot)
    max_sweetspot = max(okolog_sweetspot, kunde_sweetspot, okonom_sweetspot)


    values = [["", "Unterer Grenze", "ReWind Punkt", "Obere Grenze"],
                ["Ökologie", str(okolog_fenster_low), str(okolog_sweetspot), str(okolog_fenster_high)], 
                ["Ökonomie", str(okonom_fenster_low), str(okonom_sweetspot), str(okonom_fenster_high)], 
                ["Kundennutzen", str(kunde_fenster_low), str(kunde_sweetspot), str(kunde_fenster_high)],
                ["Gesamt", str(ges_fenster_low), f"zwischen {min_sweetspot} & {max_sweetspot}", str(ges_fenster_high)]]
    
    table_ergebnisse=Table(values, colWidths=[100,100,100,100], rowHeights=[25,25,25,25,25], style=None, splitByRow=1, repeatRows=0, 
            repeatCols=0, rowSplitRange=None, spaceBefore=None, spaceAfter=None, cornerRadii=None)

    table_ergebnisse.setStyle(TableStyle([
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),   # horizontal zentriert
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),  # vertikal zentriert
    ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), #erste Zeile fett
    ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Oblique"), #letzte Zeile fett
    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"), #erste Spalte fett
    ]))

    # Tabelle vorbereiten
    table_width, table_height = table_ergebnisse.wrapOn(c, 0, 0)

    # X- und Y- Position setzen
    table_ergebnisse.drawOn(c, 2*cm, height - 23* cm)

    
    # Seitenumbruch
    c.showPage()

    kopfzeile()

    # Diagramme zu Bild konvertirern
    def plotly_zu_image (fig, width=2000, heigt=800):
        buf = io.BytesIO()
        fig.write_image(buf, format="png", width=width, height=height)
        buf.seek(0)
        return buf
    
    # Diagramme (als Bild) anzeigen
    plots = [
    ("Ökologie Diagramm", fig_okolog_plotly),
    ("Ökonomie Diagramm", fig_okonom_plotly),
    ("Kundennutzen Diagramm", fig_kunde_plotly)]

    y_cursor = height - 3*cm

    for title, fig in plots:
        # Überschrift linksbündig
        c.setFont("Helvetica-Bold", 16)
        c.drawString(2*cm, y_cursor, title)

        # Plot in BytesIO PNG
        img_buf = plotly_zu_image(fig)
        img = ImageReader(img_buf)

        # Seitenverhältnis & Größe
        img_height = 7*cm
        img_width = img_height * 2000/800 # siehe Verhältnis Breite/Höhe in bild Erstellung oben
        
        # Position auf der Seite
        x_pos = (width - img_width)/2
        y_cursor -= img_height + 1*cm  # Platz für Bild + Abstand

        c.drawImage(img, x_pos, y_cursor, width=img_width, height=img_height)

        # Abstand zwischen Plot und nächster Überschrift
        y_cursor -= 1*cm

    c.save()  # PDF speichern
    
    return pdf_file_path



### Dialog Fenster zur Eingabe des Produktnamens und PDF-Erstellung
@st.dialog("PDF Bericht erstellen")
def product_dialog():
    product_name_input = st.text_input("Bitte geben Sie den Namen des Produkts oder Berichts ein:")
    
    if st.button("PDF generieren"):
        if product_name_input:
            with st.spinner("Einen Moment bitte...", show_time=True): # Ladebalken wird angezeigt
                pdf_file_path = create_pdf(product_name_input)

            if pdf_file_path:
                download_filename = f"ReWind_Analyse_{product_name_input}.pdf"
                with open(pdf_file_path, "rb") as pdf_file:
                    st.download_button("Download PDF", pdf_file, file_name=download_filename, mime='application/pdf')

    
        else:
            st.warning("Bitte geben Sie einen Namen ein.")

    # Hinzufügen eines Buttons zum Senden einer E-Mail ans WZL
    email_address = "lukas.weirowitz@rwth-aachen.de"
    subject = f"ReWind Analyse Bericht: {product_name_input}"
    body = (
    f"Sehr geehrter Herr Weirowitz,%0A%0A"
    f"im Anhang finden Sie eine mit Ihrem Online-Tool erstellte Re-Wind analyse zu unserem Produkt {product_name_input}. %0A"
    f"Wir würden uns über einen Austausch zum Thema Re-Assembly und Kreislaufwirtschaft freuen %0A%0A"
    f"------- bitte Bericht manuell als pdf anhängen ------- %0A%0A")
    
    mailto_link = f"mailto:{email_address}?subject={subject}&body={body}"
    
    # Verwende HTML für den Link
    st.markdown(f'Wir würden uns freuen, wenn Sie ihre Ergebnisse mit dem WZL teilen würden: <a href="{mailto_link}" target="_blank">Email öffnen</a>', unsafe_allow_html=True)

# Button nicht im Dialog sondern in App
if "vote" not in st.session_state:
    if st.sidebar.button('PDF Bericht erstellen'):
        product_dialog()


