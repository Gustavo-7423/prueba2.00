import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar y limpiar datos
@st.cache_data
def load_data():
    file_path = "ped_crashes.csv"  # Ruta fija del archivo subido
    df = pd.read_csv(file_path)
    df = df.dropna()  # Eliminar datos NaN
    return df

# Cargar datos
data = load_data()

# Configuración de la barra lateral
st.sidebar.title("Opciones de visualización")

# Seleccionar tipo de gráfico
chart_type = st.sidebar.selectbox(
    "Selecciona el tipo de gráfico",
    ["Gráfico de barras", "Gráfico de dispersión", "Gráfico de torta"]
)

# Seleccionar columnas para los gráficos
columns = data.columns
x_axis = st.sidebar.selectbox("Selecciona el eje X", columns)
y_axis = st.sidebar.selectbox("Selecciona el eje Y", columns)

if chart_type == "Gráfico de barras":
    st.header("Gráfico de barras")
    bar_chart = px.bar(data, x=x_axis, y=y_axis, title="Gráfico de barras")
    st.plotly_chart(bar_chart)

elif chart_type == "Gráfico de dispersión":
    st.header("Gráfico de dispersión")
    scatter_plot = px.scatter(data, x=x_axis, y=y_axis, title="Gráfico de dispersión")
    st.plotly_chart(scatter_plot)

elif chart_type == "Gráfico de torta":
    st.header("Gráfico de torta")
    category = st.sidebar.selectbox("Selecciona la columna para categorizar", columns)
    pie_chart = px.pie(data, names=category, title="Gráfico de torta")
    st.plotly_chart(pie_chart)

# Mostrar tabla de datos limpios
if st.sidebar.checkbox("Mostrar datos limpios"):
    st.write("Datos después de eliminar valores NaN:")
    st.dataframe(data)
