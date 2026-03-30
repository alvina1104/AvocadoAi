import streamlit as st
import requests

from main import avocado_app

api_url = 'http://127.0.0.1:8000/predict/'


st.title(' Predidict  the Avacado Ripeness ')

firmness = st. number_input('Firmness:', format='%.1f')
hue = st.number_input('Hue:', value=0)
saturation = st.number_input('Saturation:', value=0)
brightness = st.number_input('Brightness:', value=0)
sound_db = st.number_input('Sound DB:', value=0)
weight_g = st.number_input('Weight G:', value=0)
size_cm3 = st.number_input('Size CM3:', value=0)
color_category = st.selectbox('Color Category:', ('black', 'green', 'dark green', 'purple'))



avocado_data = {
    'firmness': firmness,
    'hue': hue,
    'saturation': saturation,
    'brightness': brightness,
    'sound_db': sound_db,
    'weight_g': weight_g,
    'size_cm3': size_cm3,
    'color_category': color_category
}

if st.button('Predict'):

    try:
        answer = requests.post(api_url, json=avocado_data, timeout=10)
        if answer.status_code == 200:
            result = answer.json()
            st.success(f'Predict: {result.get('predicted_ripeness')}')
            #st.json
        else:
            st.error(f'Error: {answer.status_code}')
    except requests.exceptions.RequestException:
        st.error(f'Failed to connect to Avacado Ripeness API')
