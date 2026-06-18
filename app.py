import streamlit as st

st.set_page_config(
    page_title="Modelo coste-ingresos",
    layout="wide"
)

st.title("Modelo coste-ingresos")
st.write("Aplicación desarrollada con Streamlit para trabajar modelos de costes e ingresos.")

st.info("Esta es la versión inicial convertida desde Jupyter Notebook a una aplicación Python independiente.")

st.subheader("Ejemplo básico")

coste_fijo = st.number_input("Coste fijo (€)", min_value=0.0, value=1000.0, step=100.0)
coste_variable = st.number_input("Coste variable unitario (€)", min_value=0.0, value=10.0, step=1.0)
precio_venta = st.number_input("Precio de venta unitario (€)", min_value=0.0, value=25.0, step=1.0)
unidades = st.slider("Unidades vendidas", min_value=0, max_value=1000, value=100, step=10)

coste_total = coste_fijo + coste_variable * unidades
ingresos = precio_venta * unidades
beneficio = ingresos - coste_total

c1, c2, c3 = st.columns(3)
c1.metric("Ingresos", f"{ingresos:,.2f} €")
c2.metric("Coste total", f"{coste_total:,.2f} €")
c3.metric("Beneficio", f"{beneficio:,.2f} €")

if precio_venta > coste_variable:
    punto_muerto = coste_fijo / (precio_venta - coste_variable)
    st.success(f"Punto muerto estimado: {punto_muerto:,.0f} unidades")
else:
    st.warning("El precio de venta debe ser mayor que el coste variable unitario para calcular el punto muerto.")
