import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Configuración de la aplicación
st.title("Accidentes vehuiculares ocurridos dentro del año 2010-2018")
st.subheader("en esta pagina web podremos ver los accidentes de autos que ocurrieron a lo largo de los años ")
st.markdown("<p style='font-size50px;'>Aqui veremos unos grafico con los datos sobres accidentes vehuivulares que han sucedido a lo largo de los 2010-2018 </p>", unsafe_allow_html=True)
# Barra lateral para navegación
option = st.sidebar.selectbox("Selecciona una opción", ["Ver Datos", "Ver Gráficos"])

# esto es para cargar los datos 
file_path = "ped_crashes.csv"  
data = pd.read_csv(file_path)

if option == "Ver Datos":
    # Mostrar los datos en formato tabla
    st.subheader("Datos de Accidentes")
    st.dataframe(data)  # esto es para que al usuario pueda ver los datos 

elif option == "Ver Gráficos":
    # Gráfico de accidentes por mes
    accidents_per_month = (
        data['Crash Month']
        .value_counts()
        .reindex([
            'January', 'February', 'March', 'April', 'May', 'June', 
            'July', 'August', 'September', 'October', 'November', 'December'
        ], fill_value=0)
    )

    # este es el grafico de barra con los meses y los accidentes que hay 
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
