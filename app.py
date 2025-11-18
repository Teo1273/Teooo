# app.py
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
from influxdb_client import InfluxDBClient

# --------------------------
# Configuración Streamlit
# --------------------------
st.set_page_config(
    page_title="IoT Dashboard - Monitoreo Ambiental y de Movimiento",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🌿 IoT Dashboard - Monitoreo Ambiental y de Movimiento")
st.markdown(
    "Este tablero muestra datos en tiempo real de sensores **DHT22** (temperatura y humedad) "
    "y **MPU6050** (aceleración y orientación)."
)

# --------------------------
# Sidebar - Filtros
# --------------------------
st.sidebar.header("Filtros de visualización")
tiempo_actual = datetime.now()
fecha_inicio = st.sidebar.date_input("Fecha inicio", tiempo_actual - timedelta(days=1))
fecha_fin = st.sidebar.date_input("Fecha fin", tiempo_actual)
actualizar = st.sidebar.button("Actualizar datos")

# --------------------------
# Conexión a InfluxDB
# --------------------------
INFLUX_URL = "https://tu-influxdb-url.com"
INFLUX_TOKEN = "tu-token-aqui"
INFLUX_ORG = "tu-org"
INFLUX_BUCKET = "tu-bucket"

client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
query_api = client.query_api()

# Función para obtener datos del DHT22
def obtener_dht22(fecha_inicio, fecha_fin):
    query = f'''
    from(bucket:"{INFLUX_BUCKET}")
    |> range(start: {fecha_inicio.isoformat()}T00:00:00Z, stop: {fecha_fin.isoformat()}T23:59:59Z)
    |> filter(fn: (r) => r["_measurement"] == "DHT22")
    '''
    result = query_api.query_data_frame(query)
    if not result.empty:
        df = result[["_time", "_field", "_value"]].pivot(index="_time", columns="_field", values="_value")
        df = df.reset_index()
        return df
    return pd.DataFrame()

# Función para obtener datos del MPU6050
def obtener_mpu6050(fecha_inicio, fecha_fin):
    query = f'''
    from(bucket:"{INFLUX_BUCKET}")
    |> range(start: {fecha_inicio.isoformat()}T00:00:00Z, stop: {fecha_fin.isoformat()}T23:59:59Z)
    |> filter(fn: (r) => r["_measurement"] == "MPU6050")
    '''
    result = query_api.query_data_frame(query)
    if not result.empty:
        df = result[["_time", "_field", "_value"]].pivot(index="_time", columns="_field", values="_value")
        df = df.reset_index()
        return df
    return pd.DataFrame()

# --------------------------
# Obtención de datos
# --------------------------
if actualizar:
    dht22_data = obtener_dht22(fecha_inicio, fecha_fin)
    mpu6050_data = obtener_mpu6050(fecha_inicio, fecha_fin)

    if not dht22_data.empty:
        st.subheader("🌡️ Temperatura y Humedad (DHT22)")
        fig_temp = px.line(dht22_data, x="_time", y="temperature", title="Temperatura")
        fig_hum = px.line(dht22_data, x="_time", y="humidity", title="Humedad")
        st.plotly_chart(fig_temp, use_container_width=True)
        st.plotly_chart(fig_hum, use_container_width=True)
        
        # Indicadores simples
        col1, col2 = st.columns(2)
        col1.metric("Temperatura Actual (°C)", dht22_data['temperature'].iloc[-1])
        col2.metric("Humedad Actual (%)", dht22_data['humidity'].iloc[-1])

    if not mpu6050_data.empty:
        st.subheader("🌀 Movimiento (MPU6050)")
        fig_acc = px.line(mpu6050_data, x="_time", y=["acc_x","acc_y","acc_z"], title="Aceleración")
        st.plotly_chart(fig_acc, use_container_width=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("Acc X", mpu6050_data['acc_x'].iloc[-1])
        col2.metric("Acc Y", mpu6050_data['acc_y'].iloc[-1])
        col3.metric("Acc Z", mpu6050_data['acc_z'].iloc[-1])
else:
    st.info("Seleccione la fecha y presione 'Actualizar datos' para visualizar la información.")

  
    


  
