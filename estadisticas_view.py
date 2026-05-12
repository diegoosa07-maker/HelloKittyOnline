import streamlit as st

try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_OK = True
except ImportError:
    PLOTLY_OK = False

COLOR_NIVEL = {
    "Crítico": "#e74c3c",
    "Alto":    "#e67e22",
    "Medio":   "#f1c40f",
    "Bajo":    "#2ecc71",
}


def render_estadisticas(ctrl):
    st.subheader("Estadísticas de incidencias")

    if not PLOTLY_OK:
        st.warning("Instala plotly para ver las gráficas: `pip install plotly`")
        return

    df = ctrl.obtener_df()
    if df.empty:
        st.info("Registra al menos una incidencia para ver las estadísticas.")
        return

    # KPIs
    total    = ctrl.total_incidencias()
    criticos = int((df["Nivel de Riesgo"] == "Crítico").sum())
    nivel_fq = ctrl.nivel_mas_frecuente()
    tipo_fq  = ctrl.tipo_mas_frecuente()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total incidencias",    total)
    col2.metric("Incidencias críticas", criticos)
    col3.metric("Nivel más frecuente",  nivel_fq)
    col4.metric("Tipo más frecuente",   tipo_fq)

    st.divider()

    # Gráficas
    col_izq, col_der = st.columns(2)

    with col_izq:
        serie = ctrl.conteo_por_clasificacion()
        if not serie.empty:
            df_plot = serie.reset_index()
            df_plot.columns = ["Tipo", "Cantidad"]
            fig = px.bar(
                df_plot, x="Tipo", y="Cantidad", color="Tipo",
                title="Incidencias por tipo de amenaza", text="Cantidad",
            )
            fig.update_traces(textposition="outside")
            fig.update_layout(showlegend=False, xaxis_tickangle=-20)
            st.plotly_chart(fig, use_container_width=True)

    with col_der:
        serie = ctrl.conteo_por_nivel()
        if not serie.empty:
            df_plot = serie.reset_index()
            df_plot.columns = ["Nivel", "Cantidad"]
            colores = [COLOR_NIVEL.get(n, "#95a5a6") for n in df_plot["Nivel"]]
            fig = go.Figure(go.Pie(
                labels=df_plot["Nivel"],
                values=df_plot["Cantidad"],
                hole=0.45,
                marker_colors=colores,
                textinfo="label+percent",
            ))
            fig.update_layout(title="Distribución por nivel de riesgo")
            st.plotly_chart(fig, use_container_width=True)

    # Evolución temporal
    df_temp = ctrl.evolucion_temporal()
    if not df_temp.empty and len(df_temp) >= 2:
        st.divider()
        fig = px.area(
            df_temp, x="Fecha", y="Total",
            title="Evolución temporal de incidencias", markers=True,
        )
        st.plotly_chart(fig, use_container_width=True)
