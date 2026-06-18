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
    "beneficio, punto muerto, margen de seguridad y apalancamiento operativo."
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

# Cálculos principales
ingresos = precio_venta * unidades
coste_variable_total = coste_variable * unidades
coste_total = coste_fijo + coste_variable_total
beneficio = ingresos - coste_total
margen_contribucion_unitario = precio_venta - coste_variable
margen_contribucion_total = margen_contribucion_unitario * unidades

st.subheader("Resultados del escenario seleccionado")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Ingresos", f"{ingresos:,.2f} €")
c2.metric("Coste total", f"{coste_total:,.2f} €")
c3.metric("Beneficio", f"{beneficio:,.2f} €")
c4.metric("Margen contribución total", f"{margen_contribucion_total:,.2f} €")

st.subheader("Punto muerto, margen de seguridad y apalancamiento operativo")

if precio_venta > coste_variable:

    punto_muerto = coste_fijo / margen_contribucion_unitario
    ingresos_pm = precio_venta * punto_muerto

    margen_seguridad_unidades = unidades - punto_muerto
    margen_seguridad_euros = ingresos - ingresos_pm

    if ingresos > 0:
        margen_seguridad_pct = margen_seguridad_euros / ingresos * 100
    else:
        margen_seguridad_pct = 0.0

    if beneficio != 0:
        apalancamiento_operativo = margen_contribucion_total / beneficio
    else:
        apalancamiento_operativo = np.nan

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Punto muerto", f"{punto_muerto:,.0f} uds")
    m2.metric("Margen seguridad", f"{margen_seguridad_unidades:,.0f} uds")
    m3.metric("Margen seguridad (€)", f"{margen_seguridad_euros:,.2f} €")
    m4.metric(
        "Apalancamiento operativo",
        "No definido" if np.isnan(apalancamiento_operativo) else f"{apalancamiento_operativo:,.2f}"
    )

    st.write(
        f"El punto muerto se alcanza con **{punto_muerto:,.0f} unidades** "
        f"y unos ingresos de **{ingresos_pm:,.2f} €**."
    )

    st.write(
        f"Para el nivel actual de **{unidades:,.0f} unidades**, el margen de seguridad es "
        f"de **{margen_seguridad_unidades:,.0f} unidades**, equivalente a "
        f"**{margen_seguridad_euros:,.2f} €** y a un **{margen_seguridad_pct:,.2f} %** "
        f"de las ventas actuales."
    )

    st.subheader("Representación gráfica del modelo")

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

    # Línea vertical del punto muerto
    ax.axvline(
        punto_muerto,
        linestyle="--",
        label=f"Punto muerto: {punto_muerto:.0f} uds"
    )

    # Línea vertical de las unidades vendidas
    ax.axvline(
        unidades,
        linestyle="-.",
        label=f"Unidades vendidas: {unidades:.0f} uds"
    )

    # Punto de equilibrio
    ax.scatter([punto_muerto], [ingresos_pm], zorder=5)

    ax.annotate(
        f"PM: {punto_muerto:.0f} uds\n{ingresos_pm:,.2f} €",
        xy=(punto_muerto, ingresos_pm),
        xytext=(punto_muerto * 1.05, ingresos_pm * 0.85),
        arrowprops=dict(arrowstyle="->")
    )

    # Punto del escenario actual
    ax.scatter([unidades], [ingresos], zorder=5)

    ax.annotate(
        f"Ventas actuales: {unidades:.0f} uds\nBeneficio: {beneficio:,.2f} €",
        xy=(unidades, ingresos),
        xytext=(unidades * 1.02, ingresos * 1.05 if ingresos > 0 else coste_fijo),
        arrowprops=dict(arrowstyle="->")
    )

    ax.set_title("Modelo coste-ingresos con punto muerto y margen de seguridad")
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
