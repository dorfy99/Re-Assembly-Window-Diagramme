import streamlit as st
import matplotlib.pyplot as plt

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
    
with st.expander("Ökonomie spezifisch"):
        KostenErste = st.slider('Kosten der 1. Re-Assembly bezogen auf die Kosten einer Neuproduktion', min_value=0, max_value=100, value=10)
        KostenSteigung = st.slider('Steigung der Kosten von einer Re-Assembly zur nächsten', min_value=0, max_value=50, value=10)
        Subskription = st.number_input('Höhe der Subskriptionserlöse in einem linearen Lebenszyklus bezogen auf den Verkaufserlös eine linearen Produkts', min_value=0, value=50)
       
       

import matplotlib.pyplot as plt
print(matplotlib.__version__)