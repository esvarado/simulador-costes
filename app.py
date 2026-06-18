import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Modelo coste-ingresos",
    layout="wide"
)

st.title("Modelo coste-ingresos")
st.write(
    "Aplicación docente para analizar costes fijos, costes variables, ingresos, "
    "beneficio y punto muerto."
)

st.sidebar.header("Parámetros del modelo")

coste_fijo = st.sidebar.number_input(
    "Coste fijo (€)",
    min_value=0.0,
    value=1000.0,
    step=100.0
)

coste_variable = st.sidebar.number_input(
    "Coste variable unitario (€)",
    min_value=0.0,
    value=10.0,
    step=1.0
)

precio_venta = st.sidebar.number_input(
    "Precio de venta unitario (€)",
    min_value=0.0,
    value=25.0,
    step=1.0
)

unidades = st.sidebar.slider(
    "Unidades vendidas",
    min_value=0,
    max_value=1000,
    value=100,
    step=10
)

coste_total = coste_fijo + coste_variable * unidades
ingresos = precio_venta * unidades
beneficio = ingresos - coste_total

st.subheader("Resultados del escenario seleccionado")

c1, c2, c3 = st.columns(3)
c1.metric("Ingresos", f"{ingresos:,.2f} €")
c2.metric("Coste total", f"{coste_total:,.2f} €")
c3.metric("Beneficio", f"{beneficio:,.2f} €")

st.subheader("Punto muerto")

if precio_venta > coste_variable:
    punto_muerto = coste_fijo / (precio_venta - coste_variable)
    ingresos_pm = precio_venta * punto_muerto

    st.success(f"Punto muerto: {punto_muerto:,.0f} unidades")

    st.write(
        "El punto muerto representa el nivel de producción o ventas en el que "
        "los ingresos igualan a los costes totales. A partir de ese punto, "
        "el modelo empieza a generar beneficio."
    )

    st.subheader("Representación gráfica del modelo")

if precio_venta > coste_variable:
    punto_muerto = coste_fijo / (precio_venta - coste_variable)
    ingresos_pm = precio_venta * punto_muerto

    unidades_max = max(int(punto_muerto * 1.5), unidades * 2, 100)
    x = np.arange(0, unidades_max + 1)

    ingresos_linea = precio_venta * x
    costes_fijos_linea = np.full_like(x, coste_fijo, dtype=float)
    costes_variables_linea = coste_variable * x
    costes_totales_linea = costes_fijos_linea + costes_variables_linea

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(x, ingresos_linea, label="Ingresos")
    ax.plot(x, costes_totales_linea, label="Costes totales")
    ax.plot(x, costes_fijos_linea, linestyle="--", label="Costes fijos")
    ax.plot(x, costes_variables_linea, linestyle=":", label="Costes variables")

    ax.axvline(
        punto_muerto,
        linestyle="--",
        label=f"Punto muerto: {punto_muerto:.0f} unidades"
    )

    ax.scatter([punto_muerto], [ingresos_pm], zorder=5)

    ax.annotate(
        f"PM: {punto_muerto:.0f} uds\\n{ingresos_pm:,.2f} €",
        xy=(punto_muerto, ingresos_pm),
        xytext=(punto_muerto * 1.05, ingresos_pm * 0.85),
        arrowprops=dict(arrowstyle="->")
    )

    ax.set_title("Modelo coste-ingresos con CF, CV, CT e ingresos")
    ax.set_xlabel("Unidades")
    ax.set_ylabel("Euros")
    ax.legend()
    ax.grid(True, alpha=0.3)

    st.pyplot(fig)

else:
    st.warning(
        "No se puede calcular el punto muerto porque el precio de venta debe ser "
        "mayor que el coste variable unitario."
    )
