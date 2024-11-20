import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Configuración de la aplicación
st.title("Accidentes por Mes del Año")
st.subheader("Visualización de accidentes de tráfico organizados por mes")

# Cargar los datos
file_path = "ped_crashes.csv"  # Asegúrate de colocar el archivo CSV en esta ruta
data = pd.read_csv(file_path)

# Procesar los datos
# Contar los accidentes por cada mes y asegurarse de que estén en orden cronológico
accidents_per_month = (
    data['Crash Month']
    .value_counts()
    .reindex([
        'January', 'February', 'March', 'April', 'May', 'June', 
        'July', 'August', 'September', 'October', 'November', 'December'
    ], fill_value=0)
)

# Crear el gráfico de barras
fig, ax = plt.subplots()
accidents_per_month.plot(kind='bar', color='skyblue', ax=ax)
ax.set_title("Número de Accidentes por Mes")
ax.set_xlabel("Mes")
ax.set_ylabel("Cantidad de Accidentes")
plt.xticks(rotation=45)

# Mostrar el gráfico en Streamlit
st.pyplot(fig)
