import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Configuración de la aplicación
st.title("Visualización de Datos de Accidentes de Tráfico")

# Cargar los datos
file_path = "ped_crashes.csv"  # Asegúrate de colocar el archivo CSV en esta ruta
data = pd.read_csv(file_path, thousands=',')

# Limpiar los datos eliminando filas con valores no deseados en columnas clave
data_clean = data[~data['Weather Conditions (2016+)'].isin(['uncoded', 'error', 'UNKNOWN'])]

# Sidebar para navegación principal
st.sidebar.title("Navegación")
main_option = st.sidebar.selectbox(
    "¿Qué deseas hacer?",
    ["Ver Datos", "Ver Gráficos"]
)

if main_option == "Ver Datos":
    # Mostrar los datos limpios en formato tabla
    st.subheader("Datos de Accidentes")
    st.dataframe(data_clean)

elif main_option == "Ver Gráficos":
    # Segundo selectbox para seleccionar gráficos específicos
    graph_option = st.sidebar.selectbox(
        "Selecciona el gráfico que deseas ver:",
        ["Accidentes por Mes", "Distribución de Edades", "Lesiones Más Graves", "Accidentes por Ciudad o Municipio"]
    )

    if graph_option == "Accidentes por Mes":
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
        st.write("Este gráfico muestra el número de accidentes registrados en cada mes del año. "
                 "Puedes observar las tendencias estacionales y meses con más incidentes.")

    elif graph_option == "Distribución de Edades":
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
        st.write("Este gráfico representa la distribución de edades de las personas involucradas en accidentes. "
                 "Las edades con mayor cantidad de incidentes son resaltadas.")

    elif graph_option == "Lesiones Más Graves":
        # Gráfico de torta: Lesiones más graves en los accidentes
        if 'Worst Injury in Crash' in data_clean.columns:
            injury_counts = data_clean['Worst Injury in Crash'].value_counts()
            fig3, ax3 = plt.subplots(figsize=(8, 8))
            injury_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax3, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0'])
            ax3.set_title("Distribución de Lesiones Más Graves en los Accidentes")
            ax3.set_ylabel('')
            st.subheader("Lesiones Más Graves en los Accidentes")
            st.pyplot(fig3)
            st.write("El gráfico de torta muestra las proporciones de las diferentes categorías de lesiones "
                     "registradas en los accidentes de tráfico.")
        else:
            st.warning("La columna 'Worst Injury in Crash' no se encuentra en los datos.")

    elif graph_option == "Accidentes por Ciudad o Municipio":
        # Gráfico de barras horizontales: Accidentes por Ciudad o Municipio
        if 'City or Township' in data_clean.columns:
            city_counts = data_clean['City or Township'].value_counts()
            fig4, ax4 = plt.subplots(figsize=(10, 8))
            city_counts.plot(kind='barh', color='lightcoral', ax=ax4)
            ax4.set_title("Número de Accidentes por Ciudad o Municipio")
            ax4.set_xlabel("Cantidad de Accidentes")
            ax4.set_ylabel("Ciudad o Municipio")
            st.subheader("Accidentes por Ciudad o Municipio")
            st.pyplot(fig4)
            st.write("Este gráfico de barras horizontales muestra el número de accidentes ocurridos en cada ciudad o municipio. "
                     "Es más fácil de leer cuando hay nombres largos o muchas categorías.")
        else:
            st.warning("La columna 'City or Township' no está disponible en los datos.")
