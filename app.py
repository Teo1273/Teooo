import streamlit as st
from PIL import Image

st.title("Mi Primera App!!")

st.header("En este espacio comienzo a desarrollar mis aplicaciones para interfaces multimodales.")
st.write("Facilmente puedo realizar backend y frontend.")
image = Image.open ('porsche-911-gt3-rs-purple-beast-vorsteiner-18.jpg')

st.image(image, caption='Interfaces multimodales')


texto = st.text_input('Escribe algo', 'Este es mi texto')
st.write('El texto escrito es', texto)

st.subheader("Ahora usemos 2 columnas")

col1, col2 = st.columns(2)

with col1:
  st.subheader("Esta es la primera columna")
  st.write("Las interfaces multimodales mejoran la experiencia de usuario")
  resp = st.checkbox('Estoy de acuerdo')
  if resp:
    st.write('Correcto!')
with col2:
  st.subheader("Esta es la segunda columna")
  modo = st.radio("Que Modalidad es la principal en tu interfaz",('Visual', 'Auditiva', 'Tactil'))
  if modo == 'Visual':
    st.write('La vista es fundamental para tu interfaz')
  if modo == 'Auditiva':
    st.write('La audicion es fundamental para tu interfaz')
  if modo == 'Tactil':
    st.write('El tactil es fundamental para tu interfaz')


st.subheader("Uso de botones")
if st.button('Presiona el boton'):
    st.write('Gracias por presionar')
else:
    st.write('No has presionado aun')

st.subheader("Selectbox")
in_mod = st.selectbox(
  "Selecciona la modalidad",
  ("Audio", "Visual", "Haptico"),
)
if in_mod == "Audio":
  set_mod = "Reproducir audio"
elif in_mod == "VisuaL":
  set_mod = "Reproducir video"
elif in_mod == "Haptico":
  set_mod = "Activar vibracion"
st.write(" La accion es:" , set_mod)

with st.sidebar:
  st.subheader("Configura la modalidad")
  mod_radio = st.radio(
    "Escoge la modalidad a usar",
    ("Visual", "Auditiva", "Haptica")
  )

  
    


  
