import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from datos_etf import etfs  # Importa tu archivo de etfs

# Estilos CSS para la imagen y la interpretación
st.markdown(
    """
    <style>
    .centered-image {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 50%;  /* Ajusta el tamaño de la imagen */
    }
    .interpretacion {
        border: 1px solid blue;  /* Cambiar a borde azul */
        padding: 10px;
        margin-top: 10px;
        background-color: #F9F9F9;
        border-radius: 5px;
        text-align: center;  /* Centrar texto */
    }
    .monto-final {
        font-weight: bold;
        color: blue;
    }
    .centered-table {
        display: flex;
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True
)

# Imagen de encabezado
st.image("Allianz.png", width=300)

# Título de la aplicación
st.title("Análisis de ETFs")
st.markdown("<h2 style='color: blue;'>Simulador OptiMaxx Patrimonial</h2>", unsafe_allow_html=True)

# Sección para capturar datos del cliente
st.header("Datos del cliente:")
nombre_cliente = st.text_input("Ingrese su nombre:", "")

# Menú de selección múltiple para escoger varios ETFs
etf_nombres = [etf['nombre'] for etf in etfs]
etfs_seleccionados = st.sidebar.multiselect('Seleccione uno o más ETFs sobre el cual le gustaría calcular su Plan de Inversión:', etf_nombres)

# Selector de periodo de inversión
periodo_inversion = st.sidebar.selectbox(
    'Seleccione el periodo de inversión:',
    ['1 mes', '3 meses', '1 año', '3 años', '5 años', '10 años']
)

# Función para determinar la fecha de inicio basada en el periodo seleccionado
def obtener_fecha_inicio(periodo):
    if periodo == '1 mes':
        return pd.to_datetime('today') - pd.DateOffset(months=1)
    elif periodo == '3 meses':
        return pd.to_datetime('today') - pd.DateOffset(months=3)
    elif periodo == '1 año':
        return pd.to_datetime('today') - pd.DateOffset(years=1)
    elif periodo == '3 años':
        return pd.to_datetime('today') - pd.DateOffset(years=3)
    elif periodo == '5 años':
        return pd.to_datetime('today') - pd.DateOffset(years=5)
    elif periodo == '10 años':
        return pd.to_datetime('today') - pd.DateOffset(years=10)

fecha_inicio = obtener_fecha_inicio(periodo_inversion)
fecha_fin = pd.to_datetime('today')

# Selector para la cantidad de inversión inicial
cantidad_inversion = st.sidebar.number_input("Ingrese la cantidad con la que comenzará a invertir:", min_value=0.0, step=100.0)

# Índice de referencia (por ejemplo, S&P 500)
indice_referencia = "^GSPC"  # S&P 500

# Función para calcular métricas financieras
def calcular_metricas_financieras(simbolo, fecha_inicio, fecha_fin, indice_referencia):
    # Descargar datos históricos del ETF y del índice de referencia
    data = yf.download(simbolo, start=fecha_inicio, end=fecha_fin)
    data_indice = yf.download(indice_referencia, start=fecha_inicio, end=fecha_fin)
    
    # Calcular retornos diarios
    data['Retorno'] = data['Adj Close'].pct_change()
    data_indice['Retorno'] = data_indice['Adj Close'].pct_change()
    
    # Calcular retorno total y riesgo (desviación estándar)
    retorno_total = data['Retorno'].sum() * 100  # Retorno total en porcentaje
    riesgo = data['Retorno'].std() * (252 ** 0.5) * 100  # Desviación estándar anualizada en porcentaje
    
    # Calcular Alpha y Beta
    cov_matrix = pd.concat([data['Retorno'], data_indice['Retorno']], axis=1).cov()
    beta = cov_matrix.iloc[0, 1] / cov_matrix.iloc[1, 1]  # Beta
    alpha = retorno_total - beta * data_indice['Retorno'].sum() * 100  # Alpha en valor absoluto
    
    # Calcular pérdida máxima (max drawdown)
    data['Cumulative Return'] = (1 + data['Retorno']).cumprod()
    data['Drawdown'] = data['Cumulative Return'] / data['Cumulative Return'].cummax() - 1
    perdida_maxima = data['Drawdown'].min() * 100  # Pérdida máxima en porcentaje

    return retorno_total, riesgo, alpha, beta, perdida_maxima, data['Adj Close']

# Botón para calcular
if st.sidebar.button("Calcular"):
    if nombre_cliente and etfs_seleccionados and cantidad_inversion > 0:
        st.write(f"¡Gracias, **{nombre_cliente}**! A continuación, le presentaremos los cálculos financieros para cada uno de los ETFs seleccionados. Estos análisis le ayudarán a tomar decisiones informadas para su plan de inversión.")
        
        # Diccionario para almacenar los datos de cierre ajustado de cada ETF
        precios_df = pd.DataFrame()

        for etf_seleccionado in etfs_seleccionados:
            # Obtener la información del ETF seleccionado
            for etf in etfs:
                if etf['nombre'] == etf_seleccionado:
                    nombre_etf = etf['nombre']
                    simbolo_etf = etf['simbolo']
                    descripcion_etf = etf['descripcion']
                    break

            # Mostrar el nombre, símbolo y descripción de cada ETF seleccionado
            st.markdown(f"### **{nombre_etf} ({simbolo_etf})**")
            st.write(descripcion_etf)
       
            # Calcular las métricas financieras
            retorno_total, riesgo, alpha, beta, perdida_maxima, precios_ajustados = calcular_metricas_financieras(simbolo_etf, fecha_inicio, fecha_fin, indice_referencia)
            
            # Calcular el monto final de la inversión
            monto_final = cantidad_inversion * (1 + retorno_total / 100)

            # Crear tabla con los resultados y mostrarla
            resultados_etf = pd.DataFrame({
                "Métrica": ["Retorno total esperado (%)", "Riesgo (%)", "Alpha", "Beta", "Pérdida máxima (%)", "Monto final de la inversión ($)"],
                "Valor": [f"{retorno_total:.2f}%", f"{riesgo:.2f}%", f"{alpha:.2f}", f"{beta:.2f}", f"{perdida_maxima:.2f}%", f"<span class='monto-final'>${monto_final:.2f}</span>"]
            })

            # Centrar la tabla en HTML
            st.markdown("<div class='centered-table'>" + resultados_etf.to_html(escape=False) + "</div>", unsafe_allow_html=True)

            # Interpretación personalizada con borde
            interpretacion = f"""
                <div class="interpretacion">
                    <p><strong>{nombre_cliente}</strong>, al invertir en el ETF {nombre_etf} durante un periodo de <strong>{periodo_inversion}</strong>, podría esperar un retorno aproximado de <strong>{retorno_total:.2f}%</strong>, con un riesgo notable del <strong>{riesgo:.2f}%</strong>. 
                    La <strong>Beta de {beta:.2f}</strong> indica que este ETF es{' más' if beta > 1 else ' menos'} volátil que el mercado, y el <strong>Alpha de {alpha:.2f}</strong> sugiere que su rendimiento podría ser {'superior' if alpha > 0 else 'inferior'} al índice de referencia, el S&P 500, ajustado por riesgo.
                    Considere estas variables en su decisión, y recuerde que estos valores son estimados y se basan en la premisa de una inversión total en este ETF sin diversificación adicional.</p>
                </div>
            """
            st.markdown(interpretacion, unsafe_allow_html=True)

            # Almacenar los precios ajustados en un DataFrame para graficar
            precios_df[simbolo_etf] = precios_ajustados

        # Graficar precios ajustados de los ETFs seleccionados usando Seaborn
        if not precios_df.empty:
            precios_df.index.name = 'Fecha'  # Renombrar el índice para la gráfica
            precios_long_df = precios_df.reset_index().melt(id_vars='Fecha', var_name='ETF', value_name='Precio Ajustado')
            
            plt.figure(figsize=(10, 6))
            sns.lineplot(data=precios_long_df, x='Fecha', y='Precio Ajustado', hue='ETF', marker="o")
            plt.title('Comparación de Precios Ajustados de ETFs Seleccionados')
            plt.xlabel('Fecha')
            plt.ylabel('Precio Ajustado')
            plt.legend(title='ETFs')
            st.pyplot(plt.gcf())  # Mostrar la gráfica
            plt.clf()  # Limpiar la figura después de mostrar

    else:
        st.warning("Por favor, complete todos los campos requeridos.")


















































