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

if beneficio > 0:
    st.success(f"La empresa está en zona de beneficio: gana {beneficio:,.2f} €.")
elif beneficio < 0:
    st.error(f"La empresa está en zona de pérdidas: pierde {abs(beneficio):,.2f} €.")
else:
    st.info("La empresa está exactamente en el punto muerto: beneficio igual a cero.")

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

    # Guardar datos para la pantalla del informe profesional
    st.session_state["modelo"] = {
        "coste_fijo": coste_fijo,
        "coste_variable": coste_variable,
        "precio_venta": precio_venta,
        "unidades": unidades,
        "ingresos": ingresos,
        "coste_variable_total": coste_variable_total,
        "coste_total": coste_total,
        "beneficio": beneficio,
        "margen_contribucion_unitario": margen_contribucion_unitario,
        "margen_contribucion_total": margen_contribucion_total,
        "punto_muerto": punto_muerto,
        "ingresos_pm": ingresos_pm,
        "margen_seguridad_unidades": margen_seguridad_unidades,
        "margen_seguridad_euros": margen_seguridad_euros,
        "margen_seguridad_pct": margen_seguridad_pct,
        "apalancamiento_operativo": apalancamiento_operativo,
    }

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

    if beneficio >= 0:
        st.write(
            f"Con **{unidades:,.0f} unidades vendidas**, la empresa supera el punto muerto "
            f"en **{margen_seguridad_unidades:,.0f} unidades** y obtiene un beneficio de "
            f"**{beneficio:,.2f} €**."
        )
    else:
        st.write(
            f"Con **{unidades:,.0f} unidades vendidas**, la empresa está por debajo del punto muerto "
            f"en **{abs(margen_seguridad_unidades):,.0f} unidades** y registra una pérdida de "
            f"**{abs(beneficio):,.2f} €**."
        )

    st.write(
        f"El margen de seguridad equivale a **{margen_seguridad_euros:,.2f} €** "
        f"y representa un **{margen_seguridad_pct:,.2f} %** de las ventas actuales."
    )

    st.info(
        "Los datos de este escenario se han guardado automáticamente para generar "
        "el informe profesional en la segunda pantalla de la aplicación."
    )

    st.subheader("Representación gráfica del modelo")

    unidades_max = max(int(punto_muerto * 1.5), unidades * 2, 100)
    x = np.arange(0, unidades_max + 1)

    ingresos_linea = precio_venta * x
    costes_fijos_linea = np.full_like(x, coste_fijo, dtype=float)
    costes_variables_linea = coste_variable * x
    costes_totales_linea = costes_fijos_linea + costes_variables_linea
    beneficio_linea = ingresos_linea - costes_totales_linea

    fig, ax = plt.subplots(figsize=(11, 6))

    ax.plot(x, ingresos_linea, label="Ingresos")
    ax.plot(x, costes_totales_linea, label="Costes totales")
    ax.plot(x, costes_fijos_linea, linestyle="--", label="Costes fijos")
    ax.plot(x, costes_variables_linea, linestyle=":", label="Costes variables")

    ax.fill_between(
        x,
        ingresos_linea,
        costes_totales_linea,
        where=(ingresos_linea >= costes_totales_linea),
        alpha=0.20,
        label="Zona de beneficio"
    )

    ax.fill_between(
        x,
        ingresos_linea,
        costes_totales_linea,
        where=(ingresos_linea < costes_totales_linea),
        alpha=0.20,
        label="Zona de pérdida"
    )

    ax.axvline(
        punto_muerto,
        linestyle="--",
        label=f"Punto muerto: {punto_muerto:.0f} uds"
    )

    ax.axvline(
        unidades,
        linestyle="-.",
        label=f"Unidades vendidas: {unidades:.0f} uds"
    )

    ax.scatter([punto_muerto], [ingresos_pm], zorder=5)

    ax.annotate(
        f"PM: {punto_muerto:.0f} uds\n{ingresos_pm:,.2f} €",
        xy=(punto_muerto, ingresos_pm),
        xytext=(punto_muerto * 1.05, ingresos_pm * 0.85),
        arrowprops=dict(arrowstyle="->")
    )

    color_punto = "green" if beneficio >= 0 else "red"

    ax.scatter(
        [unidades],
        [ingresos],
        s=90,
        color=color_punto,
        zorder=5
    )

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

    st.subheader("Evolución del beneficio")

    fig2, ax2 = plt.subplots(figsize=(11, 4))

    ax2.plot(x, beneficio_linea, label="Beneficio")
    ax2.axhline(0, linestyle="--", label="Beneficio cero")
    ax2.axvline(punto_muerto, linestyle="--", label="Punto muerto")
    ax2.axvline(unidades, linestyle="-.", label="Unidades vendidas")

    ax2.fill_between(
        x,
        beneficio_linea,
        0,
        where=(beneficio_linea >= 0),
        alpha=0.20,
        label="Beneficio"
    )

    ax2.fill_between(
        x,
        beneficio_linea,
        0,
        where=(beneficio_linea < 0),
        alpha=0.20,
        label="Pérdida"
    )

    ax2.scatter(
        [unidades],
        [beneficio],
        s=90,
        color=color_punto,
        zorder=5
    )

    ax2.annotate(
        f"Beneficio actual:\n{beneficio:,.2f} €",
        xy=(unidades, beneficio),
        xytext=(unidades * 1.05, beneficio * 1.10 if beneficio != 0 else coste_fijo * 0.1),
        arrowprops=dict(arrowstyle="->")
    )

    ax2.set_title("Beneficio según unidades vendidas")
    ax2.set_xlabel("Unidades")
    ax2.set_ylabel("Beneficio (€)")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    st.pyplot(fig2)

else:
    st.warning(
        "No se puede calcular el punto muerto porque el precio de venta debe ser "
        "mayor que el coste variable unitario."
    )

    st.session_state["modelo"] = None
