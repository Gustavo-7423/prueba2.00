import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Configuración de la aplicación
st.title("Accidentes por Mes y Edades")
st.subheader("Visualización de accidentes de tráfico organizados por mes, las edades de los involucrados y las condiciones climáticas")

# Barra lateral para navegación
option = st.sidebar.selectbox("Selecciona una opción", ["Ver Datos", "Ver Gráficos"])

# Cargar los datos
file_path = "ped_crashes.csv"  # Asegúrate de colocar el archivo CSV en esta ruta

# Leer el archivo y eliminar comas como separadores de miles
data = pd.read_csv(file_path, thousands=',')

# Limpiar los datos eliminando filas con "uncoded" o "error" en las columnas relevantes
data_clean = data[~data['Weather Conditions (2016+)'].isin(['Uncoded & errors
', 'error', 'Unknown'])]  # Puedes agregar más valores si es necesario

if option == "Ver Datos":
    # Mostrar los datos en formato tabla
    st.subheader("Datos de Accidentes")
    st.dataframe(data_clean)  # Mostrar los primeros 20 registros por defecto

elif option == "Ver Gráficos":
    # Gráfico de accidentes por mes
    accidents_per_month = (
        data_clean['Crash Month']
        .value_counts()
        .reindex([
            'January', 'February', 'March', 'April', 'May', 'June', 
            'July', 'August', 'September', 'October', 'November', 'December'
        ], fill_value=0)
    )

    # Crear el gráfico de barras de accidentes por mes
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    accidents_per_month.plot(kind='bar', color='skyblue', ax=ax1)
    ax1.set_title("Número de Accidentes por Mes")
    ax1.set_xlabel("Mes")
    ax1.set_ylabel("Cantidad de Accidentes")
    ax1.tick_params(axis='x', rotation=45)

    # Mostrar gráfico de accidentes por mes
    st.subheader("Accidentes por Mes")
    st.pyplot(fig1)

    # Procesar el gráfico de distribución de edades
    data_clean['Person Age'] = pd.to_numeric(data_clean['Person Age'], errors='coerce')  # Convertir a números, ignorando los errores

    # Contar las edades y graficar
    age_distribution = data_clean['Person Age'].dropna().value_counts().sort_index()  # Eliminar NaN y contar edades

    # Crear el gráfico de líneas de distribución de edades
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    age_distribution.plot(kind='line', color='green', marker='o', ax=ax2)
    ax2.set_title("Distribución de Edades de Involucrados en Accidentes")
    ax2.set_xlabel("Edad")
    ax2.set_ylabel("Cantidad de Accidentes")
    ax2.tick_params(axis='x', rotation=45)

    # Mostrar gráfico de distribución de edades
    st.subheader("Distribución de Edades de Involucrados en Accidentes")
    st.pyplot(fig2)

    # Gráfico de torta para las condiciones climáticas
    if 'Weather Conditions (2016+)' in data_clean.columns:
        weather_counts = data_clean['Weather Conditions (2016+)'].value_counts()  # Contar las condiciones climáticas
        fig3, ax3 = plt.subplots(figsize=(8, 8))
        weather_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax3, colors=['#66b3ff','#99ff99','#ffcc99','#ff6666'])
        ax3.set_title("Distribución de Accidentes según Condiciones Climáticas")
        ax3.set_ylabel('')  # Eliminar etiqueta de y en el gráfico de torta
        st.subheader("Condiciones Climáticas en los Accidentes")
        st.pyplot(fig3)
    else:
        st.warning("La columna 'Weather Conditions (2016+)' no se encuentra en los datos.")
