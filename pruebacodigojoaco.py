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
        ["Accidentes por Mes (Barra)", "Distribución de Edades (Lineas)", "Lesiones Más Graves (Torta)"]
    )

    if graph_option == "Accidentes por Mes (Barra)":
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
        
        st.markdown("<p style='font-size50px;'>Aqui veremos un grafico de barra el cual nos muestra en concreto los meses y sus accidentes a lo largo de los años 2010-2018  </p>", unsafe_allow_html=True)

    elif graph_option == "Distribución de Edades (Lineas)":
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

    elif graph_option == "Lesiones Más Graves (Torta)":
        # Gráfico de torta: Lesiones más graves en los accidentes
        if 'Worst Injury in Crash' in data_clean.columns:
            injury_counts = data_clean['Worst Injury in Crash'].value_counts()
            fig3, ax3 = plt.subplots(figsize=(8, 8))
            injury_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax3, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0'])
            ax3.set_title("Distribución de Lesiones Más Graves en los Accidentes")
            ax3.set_ylabel('')
            st.subheader("Lesiones Más Graves en los Accidentes")
            st.pyplot(fig3)
        else:
            st.warning("La columna 'Worst Injury in Crash' no se encuentra en los datos.")
    elif graph_option == "Dispersión: Días y Meses":
        # Gráfico de dispersión: Días vs Meses
        if 'Crash Month' in data_clean.columns and 'Crash Day' in data_clean.columns:
            # Mapear los meses a valores numéricos para el eje Y
            month_map = {
                'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
            }
            data_clean['Month Numeric'] = data_clean['Crash Month'].map(month_map)
            data_clean['Crash Day'] = pd.to_numeric(data_clean['Crash Day'], errors='coerce')  # Convertir días a numérico

            # Crear gráfico de dispersión
            fig4, ax4 = plt.subplots(figsize=(10, 6))
            ax4.scatter(data_clean['Crash Day'], data_clean['Month Numeric'], alpha=0.6, color='purple')
            ax4.set_title("Dispersión de Días y Meses de Choques")
            ax4.set_xlabel("Día del Mes")
            ax4.set_ylabel("Mes (numérico)")
            ax4.set_yticks(range(1, 13))
            ax4.set_yticklabels(list(month_map.keys()), rotation=45)
            st.subheader("Dispersión de Días y Meses de Choques")
            st.pyplot(fig4)
            st.write("Este gráfico de dispersión muestra la relación entre los días del mes y los meses en los que ocurrieron los accidentes. "
                     "Ayuda a visualizar en qué días y meses se registraron más choques.")
        else:
            st.warning("Las columnas 'Crash Month' o 'Crash Day' no están disponibles en los datos.")
