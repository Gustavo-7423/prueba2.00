import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Configuración de la aplicación
st.title("Accidentes por Mes y Edades")
st.subheader("Visualización de accidentes de tráfico organizados por mes y las edades de los involucrados")

# Cargar los datos
file_path = "ped_crashes.csv"  # Asegúrate de colocar el archivo CSV en esta ruta
data = pd.read_csv(file_path)

# Procesar los datos
# Gráfico de accidentes por mes
accidents_per_month = (
    data['Crash Month']
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
data['Person Age'] = pd.to_numeric(data['Person Age'], errors='coerce')  # Convertir a números, ignorando los errores

# Contar las edades y graficar
age_distribution = data['Person Age'].dropna().value_counts().sort_index()  # Eliminar NaN y contar edades

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
