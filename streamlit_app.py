import streamlit as st

st.title('Daten mit Slidern einlesen')

# Erstellen von 9 individuellen Slidern mit Titeln und ausklappbaren Abschnitten
with st.expander("Abschnitt 1"):
    slider1 = st.slider('Titel für Slider 1', min_value=0, max_value=100, value=50)
    slider2 = st.slider('Titel für Slider 2', min_value=0, max_value=100, value=50)

st.subheader('Zwischenüberschrift')

with st.expander("Abschnitt 2"):
    slider3 = st.slider('Titel für Slider 3', min_value=0, max_value=100, value=50)
    slider4 = st.slider('Titel für Slider 4', min_value=0, max_value=100, value=50)

with st.expander("Abschnitt 3"):
    slider5 = st.slider('Titel für Slider 5', min_value=0, max_value=100, value=50)
    slider6 = st.slider('Titel für Slider 6', min_value=0, max_value=100, value=50)

st.subheader('Weitere Zwischenüberschrift')

with st.expander("Abschnitt 4"):
    slider7 = st.slider('Titel für Slider 7', min_value=0, max_value=100, value=50)
    slider8 = st.slider('Titel für Slider 8', min_value=0, max_value=100, value=50)
    slider9 = st.slider('Titel für Slider 9', min_value=0, max_value=100, value=50)

slider_values = [slider1, slider2, slider3, slider4,
                 slider5, slider6, slider7, slider8,
                 slider9]

st.write('Eingelesene Werte:', slider_values)