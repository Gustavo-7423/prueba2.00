import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Configuración de la aplicación
st.title("Accidentes por Mes, Edades y Condiciones Climáticas")
st.subheader("Visualización de datos de accidentes de tráfico")

# Barra lateral para navegación
option = st.sidebar.selectbox(
    "Selecciona una opción", 
    ["Ver Datos", "Ver Gráficos"]
)

# Cargar los datos
file_path = "ped_crashes.csv"  # Asegúrate de colocar el archivo CSV en esta ruta
data = pd.read_csv(file_path, thousands=',')

# Limpiar los datos eliminando filas con valores no deseados en columnas clave
data_clean = data[~data['Weather Conditions (2016+)'].isin(['uncoded', 'error', 'UNKNOWN'])]

if option == "Ver Datos":
    # Mostrar los datos limpios en formato tabla
    st.subheader("Datos de Accidentes")
    st.dataframe(data_clean)

elif option == "Ver Gráficos":
    # Gráfico de barras: Accidentes por mes
    accidents_per_month = (
        data_clean['Crash Month']
        .value_counts()
        .reindex([
            'January', 'February', 'March', 'April', 'May', 'June', 
            'July', 'August', 'September', 'October', 'November', 'December'
        ], fill_value=0)
    )
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    accidents_per_month.plot(kind='bar', color='skyblue', ax=ax1)
    ax1.set_title("Número de Accidentes por Mes")
    ax1.set_xlabel("Mes")
    ax1.set_ylabel("Cantidad de Accidentes")
    ax1.tick_params(axis='x', rotation=45)
    st.subheader("Accidentes por Mes")
    st.pyplot(fig1)

    # Gráfico de líneas: Distribución de edades
    data_clean['Person Age'] = pd.to_numeric(data_clean['Person Age'], errors='coerce')  # Convertir edades a numérico
    age_distribution = data_clean['Person Age'].dropna().value_counts().sort_index()
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    age_distribution.plot(kind='line', color='green', marker='o', ax=ax2)
    ax2.set_title("Distribución de Edades de Involucrados en Accidentes")
    ax2.set_xlabel("Edad")
    ax2.set_ylabel("Cantidad de Accidentes")
    ax2.tick_params(axis='x', rotation=45)
    st.subheader("Distribución de Edades de Involucrados en Accidentes")
    st.pyplot(fig2)

    # Gráfico de torta: Condiciones climáticas
    if 'Weather Conditions (2016+)' in data_clean.columns:
        weather_counts = data_clean['Weather Conditions (2016+)'].value_counts()
        fig3, ax3 = plt.subplots(figsize=(8, 8))
        weather_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax3, colors=['#66b3ff','#99ff99','#ffcc99','#ff6666'])
        ax3.set_title("Distribución de Accidentes según Condiciones Climáticas")
        ax3.set_ylabel('')
        st.subheader("Condiciones Climáticas en los Accidentes")
        st.pyplot(fig3)
    else:
        st.warning("La columna 'Weather Conditions (2016+)' no se encuentra en los datos.")

    # Gráfico de dispersión: Edades
    if 'Person Age' in data_clean.columns:
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        scatter_data = data_clean['Person Age'].dropna()  # Eliminar valores nulos en edades
        ax4.scatter(scatter_data, [1] * len(scatter_data), alpha=0.5, c='orange', edgecolors='w')
        ax4.set_title("Dispersión de Edades en los Accidentes")
        ax4.set_xlabel("Edad")
        ax4.set_yticks([])  # Quitar el eje Y ya que no es relevante
        ax4.set_ylabel("")
        st.subheader("Dispersión de Edades en los Accidentes")
        st.pyplot(fig4)
    else:
        st.warning("La columna 'Person Age' no se encuentra en los datos.")
