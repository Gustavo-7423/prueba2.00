import pandas as pd
import streamlit as st
import plotly.express as px

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
        ["Accidentes por Mes", "Distribución de Edades", "Lesiones Más Graves", "Accidentes por Ciudad o Municipio", "Condiciones de Iluminación"]
    )

    if graph_option == "Accidentes por Mes":
        # Gráfico de barras: Accidentes por mes (usando Plotly)
        accidents_per_month = (
            data_clean['Crash Month']
            .value_counts()
            .reindex([
                'January', 'February', 'March', 'April', 'May', 'June', 
                'July', 'August', 'September', 'October', 'November', 'December'
            ], fill_value=0)
        )
        min_value = accidents_per_month.min()
        max_value = accidents_per_month.max()
        
        fig1 = px.bar(accidents_per_month, 
                      labels={'index': 'Mes', 'value': 'Cantidad de Accidentes'}, 
                      title=f"Número de Accidentes por Mes\
                      Min: {min_value} - Max: {max_value}")

        st.subheader("Accidentes por Mes")
        st.plotly_chart(fig1)
        st.write("Este gráfico muestra el número de accidentes registrados en cada mes del año. "
                 "Puedes observar las tendencias estacionales y meses con más incidentes.")

    elif graph_option == "Distribución de Edades":
        # Gráfico de líneas: Distribución de edades (usando Plotly)
        data_clean['Person Age'] = pd.to_numeric(data_clean['Person Age'], errors='coerce')  # Convertir edades a numérico
        age_distribution = data_clean['Person Age'].dropna().value_counts().sort_index()
        
        min_value = age_distribution.min()
        max_value = age_distribution.max()

        fig2 = px.line(age_distribution, 
                       labels={'index': 'Edad', 'value': 'Cantidad de Accidentes'}, 
                       title=f"Distribución de Edades de Involucrados en Accidentes\nMin: {min_value} - Max: {max_value}")

        st.subheader("Distribución de Edades de Involucrados en Accidentes")
        st.plotly_chart(fig2)
        st.write("Este gráfico representa la distribución de edades de las personas involucradas en accidentes. "
                 "Las edades con mayor cantidad de incidentes son resaltadas.")

    elif graph_option == "Lesiones Más Graves":
        # Gráfico de torta: Lesiones más graves en los accidentes (usando Plotly)
        if 'Worst Injury in Crash' in data_clean.columns:
            injury_counts = data_clean['Worst Injury in Crash'].value_counts()
            
            min_value = injury_counts.min()
            max_value = injury_counts.max()

            fig3 = px.pie(injury_counts, 
                          names=injury_counts.index, 
                          values=injury_counts.values, 
                          title=f"Distribución de Lesiones Más Graves en los Accidentes\nMin: {min_value} - Max: {max_value}", 
                          labels={'value': 'Cantidad de Lesiones', 'names': 'Tipo de Lesión'})
            
            st.subheader("Lesiones Más Graves en los Accidentes")
            st.plotly_chart(fig3)
            st.write("El gráfico de torta muestra las proporciones de las diferentes categorías de lesiones "
                     "registradas en los accidentes de tráfico.")
        else:
            st.warning("La columna 'Worst Injury in Crash' no se encuentra en los datos.")

    elif graph_option == "Accidentes por Ciudad o Municipio":
        # Gráfico de barras horizontales: Accidentes por Ciudad o Municipio (usando Plotly)
        if 'City or Township' in data_clean.columns:
            city_counts = data_clean['City or Township'].value_counts()
            
            min_value = city_counts.min()
            max_value = city_counts.max()

            fig4 = px.bar(city_counts, 
                          orientation='h', 
                          labels={'index': 'Ciudad o Municipio', 'value': 'Cantidad de Accidentes'}, 
                          title=f"Número de Accidentes por Ciudad o Municipio\nMin: {min_value} - Max: {max_value}")
            
            st.subheader("Accidentes por Ciudad o Municipio")
            st.plotly_chart(fig4)
            st.write("Este gráfico de barras horizontales muestra el número de accidentes ocurridos en cada ciudad o municipio. "
                     "Es más fácil de leer cuando hay nombres largos o muchas categorías.")
        else:
            st.warning("La columna 'City or Township' no está disponible en los datos.")

    elif graph_option == "Condiciones de Iluminación":
        # Gráfico de torta: Condiciones de iluminación (eliminando valores nulos, usando Plotly)
        if 'Lighting Conditions' in data_clean.columns:
            # Eliminar los valores nulos y los que no tienen información relevante
            lighting_conditions_clean = data_clean['Lighting Conditions'].dropna()
            lighting_counts = lighting_conditions_clean.value_counts()
            
            min_value = lighting_counts.min()
            max_value = lighting_counts.max()

            fig5 = px.pie(lighting_counts, 
                          names=lighting_counts.index, 
                          values=lighting_counts.values, 
                          title=f"Distribución de Accidentes por Condiciones de Iluminación\nMin: {min_value} - Max: {max_value}", 
                          labels={'value': 'Cantidad de Accidentes', 'names': 'Condiciones de Iluminación'})
            
            st.subheader("Condiciones de Iluminación en los Accidentes")
            st.plotly_chart(fig5)
            st.write("Este gráfico de torta muestra el porcentaje de accidentes ocurridos bajo diferentes condiciones de iluminación. "
                     "Los valores nulos han sido excluidos para garantizar la precisión de la visualización.")
        else:
            st.warning("La columna 'Lighting Conditions' no está disponible en los datos.")
