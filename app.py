import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import io
import base64
import textwrap

st.set_page_config(
    page_title="Modelo coste-ingresos",
    layout="wide"
)


def eur(valor):
    return f"{valor:,.2f} €"


def uds(valor):
    return f"{valor:,.0f} uds"


def generar_grafico_base64(
    coste_fijo,
    coste_variable,
    precio_venta,
    unidades,
    ingresos,
    beneficio,
    punto_muerto,
    ingresos_pm
):
    unidades_max = max(int(punto_muerto * 1.5), unidades * 2, 100)
    x = np.arange(0, unidades_max + 1)

    ingresos_linea = precio_venta * x
    costes_fijos_linea = np.full_like(x, coste_fijo, dtype=float)
    costes_variables_linea = coste_variable * x
    costes_totales_linea = costes_fijos_linea + costes_variables_linea

    fig, ax = plt.subplots(figsize=(11, 6))

    ax.plot(x, ingresos_linea, label="Ingresos", linewidth=2)
    ax.plot(x, costes_totales_linea, label="Costes totales", linewidth=2)
    ax.plot(x, costes_fijos_linea, linestyle="--", label="Costes fijos", linewidth=1.8)
    ax.plot(x, costes_variables_linea, linestyle=":", label="Costes variables", linewidth=1.8)

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

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=180, bbox_inches="tight")
    buffer.seek(0)
    grafico_base64 = base64.b64encode(buffer.read()).decode()
    plt.close(fig)

    return grafico_base64


def render_informe_profesional(
    coste_fijo,
    coste_variable,
    precio_venta,
    unidades,
    ingresos,
    coste_total,
    beneficio,
    margen_contribucion_total,
    punto_muerto,
    ingresos_pm,
    margen_seguridad_unidades,
    margen_seguridad_euros,
    margen_seguridad_pct,
    apalancamiento_operativo,
    grafico_base64
):
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    if beneficio > 0:
        estado = "Rentable"
        estado_clase = "badge-success"
        resumen_estado = (
            f"El escenario analizado es rentable. Con {uds(unidades)}, la empresa obtiene "
            f"un beneficio de {eur(beneficio)}."
        )
    elif beneficio < 0:
        estado = "En pérdidas"
        estado_clase = "badge-danger"
        resumen_estado = (
            f"El escenario analizado no es rentable. Con {uds(unidades)}, la empresa registra "
            f"una pérdida de {eur(abs(beneficio))}."
        )
    else:
        estado = "Punto muerto"
        estado_clase = "badge-neutral"
        resumen_estado = (
            "El escenario se encuentra exactamente en el punto muerto. Los ingresos cubren "
            "los costes totales, pero no se genera beneficio."
        )

    if np.isnan(apalancamiento_operativo):
        texto_apalancamiento = (
            "El apalancamiento operativo no está definido porque el beneficio es cero. "
            "Esto ocurre en el entorno del punto muerto, donde pequeñas variaciones en las ventas "
            "pueden provocar cambios muy intensos en el resultado."
        )
    else:
        texto_apalancamiento = (
            f"El apalancamiento operativo es {apalancamiento_operativo:,.2f}. "
            f"Esto significa que, aproximadamente, una variación del 1 % en las ventas "
            f"produciría una variación del {apalancamiento_operativo:,.2f} % en el beneficio, "
            f"manteniendo constantes el precio de venta, el coste variable unitario y los costes fijos."
        )

    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
    <meta charset="UTF-8">
    <style>
    body {{
        margin: 0;
        padding: 0;
        background: #f3f4f6;
        font-family: Arial, Helvetica, sans-serif;
        color: #111827;
    }}

    .report-wrapper {{
        background: #f3f4f6;
        padding: 32px;
    }}

    .report-container {{
        background: #ffffff;
        max-width: 1180px;
        margin: auto;
        padding: 48px;
        border-radius: 22px;
        box-shadow: 0 10px 35px rgba(15, 23, 42, 0.12);
    }}

    .report-header {{
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        border-bottom: 3px solid #e5e7eb;
        padding-bottom: 24px;
        margin-bottom: 28px;
    }}

    .report-title {{
        font-size: 38px;
        font-weight: 800;
        margin: 0;
    }}

    .report-subtitle {{
        font-size: 17px;
        color: #6b7280;
        margin-top: 8px;
    }}

    .report-date {{
        font-size: 13px;
        color: #6b7280;
        text-align: right;
    }}

    .badge-success {{
        background: #dcfce7;
        color: #166534;
        padding: 9px 16px;
        border-radius: 999px;
        font-weight: 700;
        display: inline-block;
        margin-top: 10px;
    }}

    .badge-danger {{
        background: #fee2e2;
        color: #991b1b;
        padding: 9px 16px;
        border-radius: 999px;
        font-weight: 700;
        display: inline-block;
        margin-top: 10px;
    }}

    .badge-neutral {{
        background: #e5e7eb;
        color: #374151;
        padding: 9px 16px;
        border-radius: 999px;
        font-weight: 700;
        display: inline-block;
        margin-top: 10px;
    }}

    .kpi-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin: 28px 0 34px 0;
    }}

    .kpi-card {{
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 20px;
    }}

    .kpi-label {{
        font-size: 12px;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 8px;
    }}

    .kpi-value {{
        font-size: 28px;
        font-weight: 800;
        color: #111827;
    }}

    .section-title {{
        font-size: 23px;
        font-weight: 800;
        margin-top: 34px;
        margin-bottom: 12px;
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 8px;
    }}

    .report-text {{
        font-size: 16px;
        line-height: 1.75;
        color: #374151;
        margin-bottom: 14px;
    }}

    .highlight-box {{
        background: #eff6ff;
        border-left: 5px solid #2563eb;
        padding: 18px 22px;
        border-radius: 12px;
        margin: 18px 0;
        font-size: 16px;
        line-height: 1.7;
        color: #1e3a8a;
    }}

    .chart-box {{
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 18px;
        margin-top: 16px;
    }}

    .chart-box img {{
        width: 100%;
        border-radius: 12px;
    }}

    .two-col {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 22px;
    }}

    .small-card {{
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 20px;
    }}

    .footer {{
        margin-top: 40px;
        padding-top: 18px;
        border-top: 2px solid #e5e7eb;
        font-size: 13px;
        color: #6b7280;
    }}
    </style>
    </head>

    <body>
    <div class="report-wrapper">
    <div class="report-container">

        <div class="report-header">
            <div>
                <h1 class="report-title">Informe económico del escenario</h1>
                <div class="report-subtitle">Modelo coste-volumen-beneficio · Punto muerto y sensibilidad operativa</div>
                <div class="{estado_clase}">{estado}</div>
            </div>
            <div class="report-date">
                Generado automáticamente<br>
                {fecha}
            </div>
        </div>

        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-label">Ingresos</div>
                <div class="kpi-value">{eur(ingresos)}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Coste total</div>
                <div class="kpi-value">{eur(coste_total)}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Beneficio</div>
                <div class="kpi-value">{eur(beneficio)}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Punto muerto</div>
                <div class="kpi-value">{uds(punto_muerto)}</div>
            </div>
        </div>

        <div class="section-title">1. Resumen ejecutivo</div>
        <p class="report-text">{resumen_estado}</p>

        <div class="highlight-box">
            El punto muerto se alcanza con <strong>{uds(punto_muerto)}</strong>, equivalentes a
            <strong>{eur(ingresos_pm)}</strong> de facturación. El margen de seguridad actual es de
            <strong>{uds(margen_seguridad_unidades)}</strong>, equivalente a
            <strong>{eur(margen_seguridad_euros)}</strong>.
        </div>

        <div class="section-title">2. Parámetros del modelo</div>

        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-label">Coste fijo</div>
                <div class="kpi-value">{eur(coste_fijo)}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Coste variable unitario</div>
                <div class="kpi-value">{eur(coste_variable)}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Precio venta unitario</div>
                <div class="kpi-value">{eur(precio_venta)}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Unidades vendidas</div>
                <div class="kpi-value">{uds(unidades)}</div>
            </div>
        </div>

        <div class="section-title">3. Representación gráfica</div>
        <div class="chart-box">
            <img src="data:image/png;base64,{grafico_base64}">
        </div>

        <div class="section-title">4. Interpretación económica</div>

        <div class="two-col">
            <div class="small-card">
                <h3>Punto muerto</h3>
                <p class="report-text">
                    El punto muerto representa el volumen de ventas en el que los ingresos igualan
                    a los costes totales. Por debajo de este nivel, la empresa incurre en pérdidas;
                    por encima, genera beneficios.
                </p>
            </div>

            <div class="small-card">
                <h3>Margen de seguridad</h3>
                <p class="report-text">
                    El margen de seguridad mide cuánto podrían reducirse las ventas antes de entrar
                    en pérdidas. En este escenario representa un
                    <strong>{margen_seguridad_pct:,.2f} %</strong> de las ventas actuales.
                </p>
            </div>
        </div>

        <div class="section-title">5. Apalancamiento operativo</div>
        <p class="report-text">{texto_apalancamiento}</p>

        <div class="section-title">6. Conclusión</div>
        <p class="report-text">
            El escenario muestra una relación directa entre estructura de costes, volumen de ventas
            y resultado económico. La interpretación conjunta del punto muerto, el margen de seguridad
            y el apalancamiento operativo permite valorar no solo si el escenario es rentable, sino
            también la sensibilidad del beneficio ante variaciones en la actividad.
        </p>

        <div class="footer">
            Informe generado automáticamente por la aplicación docente de análisis coste-ingresos.
        </div>

    </div>
    </div>
    </body>
    </html>
    """

    return textwrap.dedent(html)


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

tab1, tab2 = st.tabs(["Simulador", "Informe profesional"])

ingresos = precio_venta * unidades
coste_variable_total = coste_variable * unidades
coste_total = coste_fijo + coste_variable_total
beneficio = ingresos - coste_total
margen_contribucion_unitario = precio_venta - coste_variable
margen_contribucion_total = margen_contribucion_unitario * unidades

if precio_venta > coste_variable:

    punto_muerto = coste_fijo / margen_contribucion_unitario
    ingresos_pm = precio_venta * punto_muerto

    margen_seguridad_unidades = unidades - punto_muerto
    margen_seguridad_euros = ingresos - ingresos_pm
    margen_seguridad_pct = margen_seguridad_euros / ingresos * 100 if ingresos > 0 else 0.0

    apalancamiento_operativo = (
        margen_contribucion_total / beneficio
        if beneficio != 0
        else np.nan
    )

    unidades_max = max(int(punto_muerto * 1.5), unidades * 2, 100)
    x = np.arange(0, unidades_max + 1)

    ingresos_linea = precio_venta * x
    costes_fijos_linea = np.full_like(x, coste_fijo, dtype=float)
    costes_variables_linea = coste_variable * x
    costes_totales_linea = costes_fijos_linea + costes_variables_linea
    beneficio_linea = ingresos_linea - costes_totales_linea

    grafico_base64 = generar_grafico_base64(
        coste_fijo,
        coste_variable,
        precio_venta,
        unidades,
        ingresos,
        beneficio,
        punto_muerto,
        ingresos_pm
    )

    with tab1:
        st.subheader("Resultados del escenario seleccionado")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Ingresos", eur(ingresos))
        c2.metric("Coste total", eur(coste_total))
        c3.metric("Beneficio", eur(beneficio))
        c4.metric("Margen contribución total", eur(margen_contribucion_total))

        if beneficio > 0:
            st.success(f"La empresa está en zona de beneficio: gana {eur(beneficio)}.")
        elif beneficio < 0:
            st.error(f"La empresa está en zona de pérdidas: pierde {eur(abs(beneficio))}.")
        else:
            st.info("La empresa está exactamente en el punto muerto: beneficio igual a cero.")

        st.subheader("Punto muerto, margen de seguridad y apalancamiento operativo")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Punto muerto", uds(punto_muerto))
        m2.metric("Margen seguridad", uds(margen_seguridad_unidades))
        m3.metric("Margen seguridad (€)", eur(margen_seguridad_euros))
        m4.metric(
            "Apalancamiento operativo",
            "No definido" if np.isnan(apalancamiento_operativo) else f"{apalancamiento_operativo:,.2f}"
        )

        st.write(
            f"El punto muerto se alcanza con **{uds(punto_muerto)}** "
            f"y unos ingresos de **{eur(ingresos_pm)}**."
        )

        if beneficio >= 0:
            st.write(
                f"Con **{uds(unidades)}**, la empresa supera el punto muerto "
                f"en **{uds(margen_seguridad_unidades)}** y obtiene un beneficio de "
                f"**{eur(beneficio)}**."
            )
        else:
            st.write(
                f"Con **{uds(unidades)}**, la empresa está por debajo del punto muerto "
                f"en **{uds(abs(margen_seguridad_unidades))}** y registra una pérdida de "
                f"**{eur(abs(beneficio))}**."
            )

        st.write(
            f"El margen de seguridad equivale a **{eur(margen_seguridad_euros)}** "
            f"y representa un **{margen_seguridad_pct:,.2f} %** de las ventas actuales."
        )

        st.subheader("Representación gráfica del modelo")

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

    with tab2:
        informe_html = render_informe_profesional(
            coste_fijo,
            coste_variable,
            precio_venta,
            unidades,
            ingresos,
            coste_total,
            beneficio,
            margen_contribucion_total,
            punto_muerto,
            ingresos_pm,
            margen_seguridad_unidades,
            margen_seguridad_euros,
            margen_seguridad_pct,
            apalancamiento_operativo,
            grafico_base64
        )

        components.html(
            informe_html,
            height=1800,
            scrolling=True
        )

else:
    with tab1:
        st.warning(
            "No se puede calcular el punto muerto porque el precio de venta debe ser "
            "mayor que el coste variable unitario."
        )

    with tab2:
        st.warning(
            "No se puede generar el informe profesional porque el precio de venta debe ser "
            "mayor que el coste variable unitario."
        )
