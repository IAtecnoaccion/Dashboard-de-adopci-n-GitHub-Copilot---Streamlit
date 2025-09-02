"""
Dashboard principal de Streamlit para análisis de adopción de GitHub Copilot.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
from typing import List, Optional

# Importar módulos del proyecto
import data_utils
import charts
from constants import (
    BLOQUES, Q_SENTIMIENTO, Q_USO, Q_MODO, Q_YO_PREFIX, Q_EQ_PREFIX,
    Q_IMPEDIMENTOS, Q_CAPACITACIONES, Q_COMENTARIOS, Q_NPS
)

# Configuración de la página
st.set_page_config(
    page_title="Encuesta Adopción GitHub Copilot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
.metric-card {
    background: linear-gradient(45deg, #1f77b4, #aec7e8);
    padding: 1rem;
    border-radius: 0.5rem;
    color: white;
    text-align: center;
    margin: 0.5rem;
}
.stSelectbox > div > div > select {
    background-color: #f0f2f6;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_survey_data(file_path: str = "Encuesta de adopción de GitHub Copilot tabla.xlsx"):
    """
    Carga los datos de la encuesta con caching.
    """
    try:
        return data_utils.load_data(file_path)
    except Exception as e:
        st.error(f"Error al cargar los datos: {str(e)}")
        return pd.DataFrame()


def create_sidebar_filters(df: pd.DataFrame):
    """
    Crea los filtros en el sidebar.
    """
    st.sidebar.header("🔍 Filtros")
    
    # Filtro de personas
    if not df.empty:
        # Solo mostrar nombres únicos (sin emails) y limpiar espacios extra
        nombres_raw = df['Nombre'].dropna().unique().tolist()
        nombres_disponibles = sorted([nombre.strip() for nombre in nombres_raw if nombre.strip()])
        
        # Agregar opción "Todos" al principio
        opciones_personas = ["Todos"] + nombres_disponibles
        
        personas_seleccionadas = st.sidebar.multiselect(
            "Seleccionar personas:",
            options=opciones_personas,
            default=["Todos"],
            help="Selecciona 'Todos' para ver todos los encuestados o elige personas específicas"
        )
        
        # Si "Todos" está seleccionado, no filtrar por personas
        if "Todos" in personas_seleccionadas:
            personas_seleccionadas = []
        
        # Eliminar filtro de fechas ya que no es necesario
        fecha_desde = None
        fecha_hasta = None
    else:
        personas_seleccionadas = []
        fecha_desde = None
        fecha_hasta = None
    
    # Selector de bloque
    st.sidebar.header("📊 Navegación")
    bloque_seleccionado = st.sidebar.selectbox(
        "Seleccionar sección:",
        options=BLOQUES,
        index=0
    )
    
    return personas_seleccionadas, fecha_desde, fecha_hasta, bloque_seleccionado


def show_portada(df: pd.DataFrame):
    """
    Muestra la página de portada con KPIs y gráfico de sentimiento.
    """
    st.header("🤖 Dashboard - Adopción GitHub Copilot")
    st.markdown("---")
    
    # DEBUG: Mostrar todas las respuestas
    with st.expander("🔍 DEBUG: Todas las respuestas de la encuesta"):
        st.write("**Datos completos de la encuesta:**")
        st.dataframe(df[['Nombre', 'Atributo', 'Valor']].sort_values(['Nombre', 'Atributo']))
        
        st.write("**Valores únicos y frecuencias:**")
        valores_unicos = df['Valor'].value_counts()
        st.dataframe(valores_unicos)
        
        st.write("**Respuestas por atributo:**")
        for atributo in df['Atributo'].unique():
            if pd.notna(atributo):
                st.write(f"**{atributo}:**")
                respuestas_attr = df[df['Atributo'] == atributo][['Nombre', 'Valor']]
                st.dataframe(respuestas_attr)
    
    if df.empty:
        st.warning("No hay datos disponibles para mostrar.")
        return    # Calcular KPIs
    kpis = data_utils.compute_kpis(df)
    
    # Mostrar KPIs
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="👥 Encuestados",
            value=kpis.get('encuestados', 0)
        )
    
    with col2:
        nps_value = kpis.get('nps', 0)
        st.metric(
            label="📊 NPS Score",
            value=f"{nps_value:.0f}%",
            delta=None
        )
    
    with col3:
        tiempo_value = kpis.get('percibe_ahorro_tiempo', 0)
        st.metric(
            label="⏱️ Percibe Ahorro de Tiempo",
            value=f"{tiempo_value:.0f}%"
        )
    
    st.markdown("---")
    
    # Gráficos
    col1, col2 = st.columns([1, 1])
    
    # Gráfico de sentimiento
    with col1:
        st.subheader("🎭 Sentimiento hacia GitHub Copilot")
        sentiment_data = df[df['Atributo'] == Q_SENTIMIENTO]
        if not sentiment_data.empty:
            fig_pie = charts.create_sentiment_chart(df, Q_SENTIMIENTO, "pie")
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No hay datos de sentimiento disponibles.")
    
    # Gráfico de NPS
    with col2:
        st.subheader("📊 Recomendación a un Colega")
        nps_data = df[df['Atributo'] == Q_NPS]
        if not nps_data.empty:
            fig_nps = charts.create_nps_pie_chart(df)
            st.plotly_chart(fig_nps, use_container_width=True)
        else:
            st.info("No hay datos de recomendación disponibles.")


def show_uso(df: pd.DataFrame):
    """
    Muestra análisis de uso de Copilot.
    """
    st.header("🚀 Uso de GitHub Copilot")
    st.markdown("---")
    
    if df.empty:
        st.warning("No hay datos disponibles para mostrar.")
        return
    
    # Actividades
    st.subheader("📋 Actividades de Uso")
    actividades_stats = data_utils.get_actividades_stats(df)
    
    if not actividades_stats.empty:
        # Mostrar todas las actividades sin selector Top N
        fig_actividades = charts.create_horizontal_bar_chart(
            actividades_stats,
            "Todas las actividades utilizadas",
            top_n=None  # Mostrar todas
        )
        st.plotly_chart(fig_actividades, use_container_width=True)
        
        # Tabla de datos
        with st.expander("Ver datos detallados de actividades"):
            st.dataframe(actividades_stats)
    else:
        st.info("No hay datos de actividades disponibles.")
    
    st.markdown("---")
    
    # Modos
    st.subheader("🎯 Modos de Uso Preferidos")
    modos_stats = data_utils.get_modos_stats(df)
    
    if not modos_stats.empty:
        fig_modos = charts.create_horizontal_bar_chart(
            modos_stats,
            "Modos de uso preferidos"
        )
        st.plotly_chart(fig_modos, use_container_width=True)
        
        with st.expander("Ver datos detallados de modos"):
            st.dataframe(modos_stats)
    else:
        st.info("No hay datos de modos disponibles.")


def show_percepcion_individual(df: pd.DataFrame):
    """
    Muestra análisis de percepción individual.
    """
    st.header("👤 Percepción Individual")
    st.markdown("---")
    
    if df.empty:
        st.warning("No hay datos disponibles para mostrar.")
        return
    
    # Stats de Likert individual
    likert_stats = data_utils.get_likert_stats(df, Q_YO_PREFIX)
    
    if not likert_stats.empty:
        # Solo mostrar gráfico apilado
        st.subheader("📊 Distribución de Respuestas")
        fig_stacked = charts.create_likert_stacked_bar(
            df, Q_YO_PREFIX, "Percepción Individual - Distribución"
        )
        st.plotly_chart(fig_stacked, use_container_width=True)
        
        # Tabla detallada
        with st.expander("Ver datos detallados"):
            st.dataframe(likert_stats)
    else:
        st.info("No hay datos de percepción individual disponibles.")


def show_percepcion_equipo(df: pd.DataFrame):
    """
    Muestra análisis de percepción del equipo.
    """
    st.header("👥 Percepción del Equipo")
    st.markdown("---")
    
    if df.empty:
        st.warning("No hay datos disponibles para mostrar.")
        return
    
    # Stats de Likert equipo
    likert_stats = data_utils.get_likert_stats(df, Q_EQ_PREFIX)
    
    if not likert_stats.empty:
        # Solo mostrar gráfico apilado
        st.subheader("📊 Distribución de Respuestas")
        fig_stacked = charts.create_likert_stacked_bar(
            df, Q_EQ_PREFIX, "Percepción del Equipo - Distribución"
        )
        st.plotly_chart(fig_stacked, use_container_width=True)
        
        # Tabla detallada
        with st.expander("Ver datos detallados"):
            st.dataframe(likert_stats)
    else:
        st.info("No hay datos de percepción del equipo disponibles.")


def show_texto_libre(df: pd.DataFrame):
    """
    Muestra comentarios individuales de los usuarios.
    """
    st.header("💬 Comentarios de Usuarios")
    st.markdown("---")
    
    if df.empty:
        st.warning("No hay datos disponibles para mostrar.")
        return

    # Impedimentos
    st.subheader("🚧 Impedimentos")
    impedimentos = data_utils.get_text_responses(df, Q_IMPEDIMENTOS)
    
    if not impedimentos.empty:
        for _, respuesta in impedimentos.iterrows():
            st.markdown(f"**{respuesta['Nombre']}** _{respuesta['Hora de inicio']}_")
            st.markdown(f"_{respuesta['Valor']}_")
            st.markdown("---")
    else:
        st.info("No hay respuestas sobre impedimentos.")
    
    st.markdown("---")

    # Capacitaciones
    st.subheader("🎓 Capacitaciones Sugeridas")
    capacitaciones = data_utils.get_text_responses(df, Q_CAPACITACIONES)
    
    if not capacitaciones.empty:
        for _, respuesta in capacitaciones.iterrows():
            st.markdown(f"**{respuesta['Nombre']}** _{respuesta['Hora de inicio']}_")
            st.markdown(f"_{respuesta['Valor']}_")
            st.markdown("---")
    else:
        st.info("No hay respuestas sobre capacitaciones.")
    
    st.markdown("---")

    # Comentarios
    st.subheader("💭 Comentarios y Recomendaciones")
    comentarios = data_utils.get_text_responses(df, Q_COMENTARIOS)
    
    if not comentarios.empty:
        for _, comentario in comentarios.iterrows():
            st.markdown(f"**{comentario['Nombre']}** _{comentario['Hora de inicio']}_")
            st.markdown(f"_{comentario['Valor']}_")
            st.markdown("---")
    else:
        st.info("No hay comentarios disponibles.")


def show_exportar(df: pd.DataFrame):
    """
    Muestra opciones de exportación.
    """
    st.header("📤 Exportar Datos")
    st.markdown("---")
    
    if df.empty:
        st.warning("No hay datos disponibles para exportar.")
        return
    
    st.subheader("🔽 Descargar Reportes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Dataset filtrado
        if st.button("📊 Exportar Dataset Filtrado", use_container_width=True):
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Descargar CSV",
                data=csv_data,
                file_name=f"encuesta_copilot_filtrado_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )
        
        # Actividades
        actividades_stats = data_utils.get_actividades_stats(df)
        if not actividades_stats.empty:
            if st.button("📋 Exportar Actividades", use_container_width=True):
                csv_data = actividades_stats.to_csv().encode('utf-8')
                st.download_button(
                    label="Descargar CSV",
                    data=csv_data,
                    file_name=f"actividades_copilot_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv"
                )
    
    with col2:
        # Modos
        modos_stats = data_utils.get_modos_stats(df)
        if not modos_stats.empty:
            if st.button("🎯 Exportar Modos", use_container_width=True):
                csv_data = modos_stats.to_csv().encode('utf-8')
                st.download_button(
                    label="Descargar CSV",
                    data=csv_data,
                    file_name=f"modos_copilot_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv"
                )
        
        # Respuestas de texto libre
        impedimentos = data_utils.get_text_responses(df, Q_IMPEDIMENTOS)
        capacitaciones = data_utils.get_text_responses(df, Q_CAPACITACIONES)
        comentarios = data_utils.get_text_responses(df, Q_COMENTARIOS)
        
        if not impedimentos.empty or not capacitaciones.empty or not comentarios.empty:
            if st.button("💬 Exportar Comentarios", use_container_width=True):
                # Combinar todas las respuestas de texto
                texto_libre = pd.concat([
                    impedimentos.assign(Tipo='Impedimentos'),
                    capacitaciones.assign(Tipo='Capacitaciones'),
                    comentarios.assign(Tipo='Comentarios')
                ], ignore_index=True)
                
                csv_data = texto_libre.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Descargar CSV",
                    data=csv_data,
                    file_name=f"texto_libre_copilot_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv"
                )
    
    st.markdown("---")
    
    # Likert stats
    st.subheader("📈 Estadísticas Likert")
    
    col1, col2 = st.columns(2)
    
    with col1:
        likert_individual = data_utils.get_likert_stats(df, Q_YO_PREFIX)
        if not likert_individual.empty:
            if st.button("👤 Exportar Percepción Individual", use_container_width=True):
                csv_data = likert_individual.to_csv().encode('utf-8')
                st.download_button(
                    label="Descargar CSV",
                    data=csv_data,
                    file_name=f"likert_individual_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv"
                )
    
    with col2:
        likert_equipo = data_utils.get_likert_stats(df, Q_EQ_PREFIX)
        if not likert_equipo.empty:
            if st.button("👥 Exportar Percepción Equipo", use_container_width=True):
                csv_data = likert_equipo.to_csv().encode('utf-8')
                st.download_button(
                    label="Descargar CSV",
                    data=csv_data,
                    file_name=f"likert_equipo_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv"
                )


def main():
    """
    Función principal de la aplicación.
    """
    # Cargar datos
    df = load_survey_data()
    
    # Crear filtros en sidebar
    personas_seleccionadas, fecha_desde, fecha_hasta, bloque_seleccionado = create_sidebar_filters(df)
    
    # Aplicar filtros
    if not df.empty:
        df_filtered = data_utils.filter_df(
            df, 
            personas_seleccionadas
        )
        
        # Mostrar información de filtros aplicados
        # Solo mostrar si hay filtros específicos aplicados (no "Todos")
        filtros_especificos = len(personas_seleccionadas) > 0
        if filtros_especificos:
            st.sidebar.markdown("---")
            st.sidebar.markdown("**Filtros aplicados:**")
            st.sidebar.markdown(f"👥 Personas: {len(personas_seleccionadas)}")
            st.sidebar.markdown(f"📊 Registros: {len(df_filtered)}/{len(df)}")
        else:
            st.sidebar.markdown("---")
            st.sidebar.markdown("**Vista:** Todos los datos")
            st.sidebar.markdown(f"📊 Total registros: {len(df_filtered)}")
    else:
        df_filtered = df
    
    # Mostrar contenido según bloque seleccionado
    if bloque_seleccionado == "Portada":
        show_portada(df_filtered)
    elif bloque_seleccionado == "Uso":
        show_uso(df_filtered)
    elif bloque_seleccionado == "Percepción Individual":
        show_percepcion_individual(df_filtered)
    elif bloque_seleccionado == "Percepción Equipo":
        show_percepcion_equipo(df_filtered)
    elif bloque_seleccionado == "Comentarios de Usuarios":
        show_texto_libre(df_filtered)
    elif bloque_seleccionado == "Exportar":
        show_exportar(df_filtered)
    
    # Mostrar información de debug en sidebar si no hay datos
    if df.empty:
        with st.sidebar.expander("🔧 Información de Debug"):
            st.write("**Archivo esperado:** `Encuesta de adopción de GitHub Copilot tabla.xlsx`")
            st.write("**Ubicación:** Raíz del proyecto")
            st.write("**Columnas requeridas:**")
            for col in ["Id", "Hora de inicio", "Hora de finalización", 
                       "Correo electrónico", "Nombre", "Atributo", "Valor"]:
                st.write(f"- {col}")
    else:
        # Debug para verificar nombres disponibles
        with st.sidebar.expander("🔧 Debug - Nombres en datos"):
            nombres_unicos = sorted(df['Nombre'].dropna().unique().tolist())
            st.write(f"**Total nombres únicos:** {len(nombres_unicos)}")
            
            # Buscar "Alexis" específicamente
            alexis_matches = [n for n in nombres_unicos if 'alexis' in n.lower()]
            if alexis_matches:
                st.write("**Nombres con 'Alexis':**")
                for nombre in alexis_matches:
                    st.write(f"- '{nombre}' (len: {len(nombre)})")
                    # Mostrar caracteres especiales
                    st.write(f"  Repr: {repr(nombre)}")
            else:
                st.write("❌ No se encontró ningún nombre con 'Alexis'")
            
            st.write("**Primeros 15 nombres:**")
            for i, nombre in enumerate(nombres_unicos[:15]):
                st.write(f"{i+1}. '{nombre}'")
            if len(nombres_unicos) > 15:
                st.write(f"... y {len(nombres_unicos) - 15} más")
        
        # Debug adicional para filtrado
        with st.sidebar.expander("🔧 Debug - Filtrado"):
            if personas_seleccionadas:
                st.write(f"**Personas seleccionadas:** {personas_seleccionadas}")
                for persona in personas_seleccionadas:
                    matches = df[df['Nombre'] == persona]
                    st.write(f"- '{persona}': {len(matches)} registros")
                    if len(matches) > 0:
                        st.write(f"  Primeros emails: {matches['Correo electrónico'].unique()[:3].tolist()}")
            else:
                st.write("No hay filtros específicos aplicados")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "**Dashboard de Adopción GitHub Copilot** - "
        "Generado con Streamlit 🚀"
    )


if __name__ == "__main__":
    main()
