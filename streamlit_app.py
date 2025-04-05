import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Parámetros del proyecto
vida_util = 25
inversion_inicial = 349_900_000
costo_om_anual = 3_000_000
tarifa_energia_inicial = 1_000
inflacion_energetica = 0.10
deduccion_total = 0.5 * inversion_inicial
deduccion_anual = deduccion_total / 15
consumo_mensual_cliente = 12_837
consumo_anual_cliente = consumo_mensual_cliente * 12
tasa_descuento = 0.08

# Cálculos financieros
ingresos_energia = []
ahorro_tributario = []
costos = []
flujo_neto = []
flujo_descuento = []

for año in range(1, vida_util + 1):
    tarifa_energia = tarifa_energia_inicial * ((1 + inflacion_energetica) ** (año - 1))
    ingreso_anual = consumo_anual_cliente * tarifa_energia
    ahorro = deduccion_anual if año <= 15 else 0
    flujo = ingreso_anual + ahorro - costo_om_anual
    flujo_desc = flujo / ((1 + tasa_descuento) ** año)

    ingresos_energia.append(ingreso_anual)
    ahorro_tributario.append(ahorro)
    costos.append(costo_om_anual)
    flujo_neto.append(flujo)
    flujo_descuento.append(flujo_desc)

acumulado_neto = [sum(flujo_neto[:i+1]) for i in range(vida_util)]
acumulado_desc = [sum(flujo_descuento[:i+1]) for i in range(vida_util)]

# Payback
payback_simple = next((i+1 for i, v in enumerate(acumulado_neto) if v >= inversion_inicial), None)
payback_desc = next((i+1 for i, v in enumerate(acumulado_desc) if v >= inversion_inicial), None)
tir = round((sum(flujo_neto) / inversion_inicial) ** (1/vida_util) - 1, 4) * 100
vpn = round(-inversion_inicial + sum(flujo_descuento), 2)

# Streamlit UI
st.title("Análisis Financiero de Proyecto Solar Del Norte S.A.S.")
st.subheader("Resumen de Indicadores Financieros")

st.metric("Valor Presente Neto (VPN)", f"${vpn:,.0f} COP")
st.metric("Tasa Interna de Retorno (TIR)", f"{tir:.2f}%")
st.metric("Payback Simple", f"{payback_simple} años")
st.metric("Payback Descontado", f"{payback_desc} años")

# Gráficos
st.subheader("Flujos de Caja Anuales")
fig1, ax1 = plt.subplots()
ax1.plot(range(1, vida_util + 1), flujo_neto, label="Flujo Neto", marker='o')
ax1.plot(range(1, vida_util + 1), flujo_descuento, label="Flujo Descontado", marker='s')
ax1.set_xlabel("Año")
ax1.set_ylabel("COP")
ax1.legend()
ax1.grid(True)
st.pyplot(fig1)

st.subheader("Acumulado del Flujo de Caja vs Inversión")
fig2, ax2 = plt.subplots()
ax2.plot(range(1, vida_util + 1), [x / 1e6 for x in acumulado_neto], label="Acumulado Neto", marker='o')
ax2.axhline(inversion_inicial / 1e6, color='red', linestyle='--', label="Inversión Inicial")
ax2.axvline(payback_simple, color='green', linestyle='--', label=f"Payback: Año {payback_simple}")
ax2.set_xlabel("Año")
ax2.set_ylabel("Millones de COP")
ax2.legend()
ax2.grid(True)
st.pyplot(fig2)

st.subheader("Comparación de Ahorro vs Costos de Mantenimiento")
fig3, ax3 = plt.subplots()
ax3.bar(range(1, vida_util + 1), [i / 1e6 for i in ingresos_energia], label="Ahorro por Energía")
ax3.plot(range(1, vida_util + 1), [c / 1e6 for c in costos], color='red', label="Costo O&M", linestyle='--', marker='x')
ax3.set_xlabel("Año")
ax3.set_ylabel("Millones de COP")
ax3.legend()
ax3.grid(True)
st.pyplot(fig3)

st.subheader("Tabla de Flujo de Caja Anual")
df = pd.DataFrame({
    "Año": range(1, vida_util + 1),
    "Ingreso por Energía (COP)": ingresos_energia,
    "Ahorro Tributario (COP)": ahorro_tributario,
    "Costo O&M (COP)": costos,
    "Flujo Neto (COP)": flujo_neto,
    "Flujo Descontado (COP)": flujo_descuento,
    "Acumulado Neto (COP)": acumulado_neto
})
st.dataframe(df)



