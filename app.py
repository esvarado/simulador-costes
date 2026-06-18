import numpy as np
import matplotlib.pyplot as plt

st.subheader("Representación gráfica del punto muerto")

if precio_venta > coste_variable:
    punto_muerto = coste_fijo / (precio_venta - coste_variable)

    unidades_max = max(int(punto_muerto * 1.5), unidades * 2, 100)
    x = np.arange(0, unidades_max + 1)

    ingresos_linea = precio_venta * x
    costes_linea = coste_fijo + coste_variable * x

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.plot(x, ingresos_linea, label="Ingresos")
    ax.plot(x, costes_linea, label="Costes totales")

    ax.axvline(
        punto_muerto,
        linestyle="--",
        label=f"Punto muerto: {punto_muerto:.0f} unidades"
    )

    ax.scatter(
        [punto_muerto],
        [precio_venta * punto_muerto],
        zorder=5
    )

    ax.set_title("Modelo coste-ingresos y punto muerto")
    ax.set_xlabel("Unidades")
    ax.set_ylabel("Euros")
    ax.legend()
    ax.grid(True, alpha=0.3)

    st.pyplot(fig)

else:
    st.warning(
        "No se puede representar el punto muerto porque el precio de venta "
        "debe ser mayor que el coste variable unitario."
    )
