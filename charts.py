"""
Funciones para generar gráficos con Plotly Express.
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Optional


def create_sentiment_chart(df: pd.DataFrame, atributo: str, 
                          chart_type: str = "pie") -> go.Figure:
    """
    Crea gráfico de dona o barras para sentimientos.
    """
    data = df[df['Atributo'] == atributo]['Valor'].value_counts()
    
    if len(data) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No hay datos disponibles",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    if chart_type == "pie":
        fig = px.pie(
            values=data.values,
            names=data.index,
            title="Sentimiento hacia GitHub Copilot",
            hole=0.4  # Hacer dona
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
    else:  # barras
        fig = px.bar(
            x=data.values,
            y=data.index,
            orientation='h',
            title="Sentimiento hacia GitHub Copilot",
            labels={'x': 'Cantidad', 'y': 'Respuesta'}
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    
    fig.update_layout(
        showlegend=True,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig


def create_horizontal_bar_chart(stats_df: pd.DataFrame, 
                               title: str, 
                               x_col: str = 'porcentaje',
                               y_col: str = None,
                               top_n: Optional[int] = None) -> go.Figure:
    """
    Crea gráfico de barras horizontales.
    """
    if len(stats_df) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No hay datos disponibles",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    data = stats_df.copy()
    
    if top_n:
        data = data.head(top_n)
    
    if y_col is None:
        y_values = data.index
    else:
        y_values = data[y_col]
    
    fig = px.bar(
        data,
        x=x_col,
        y=y_values,
        orientation='h',
        title=title,
        labels={'x': 'Porcentaje (%)', 'y': ''},
        text=x_col
    )
    
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        margin=dict(t=50, b=50, l=50, r=150),
        height=max(400, len(data) * 25)
    )
    
    return fig


def create_likert_heatmap(stats_df: pd.DataFrame, title: str) -> go.Figure:
    """
    Crea heatmap para respuestas Likert.
    """
    if len(stats_df) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No hay datos disponibles",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    # Simplificar nombres de preguntas para mejor visualización
    stats_df_display = stats_df.copy()
    stats_df_display.index = [
        item.replace("Al usar Copilot, yo ", "").replace("Al usar Copilot, mi equipo ", "")
        for item in stats_df_display.index
    ]
    
    fig = go.Figure(data=go.Heatmap(
        z=stats_df_display[['promedio']].values.flatten(),
        y=stats_df_display.index,
        x=['Promedio Likert'],
        colorscale='RdYlGn',
        zmid=0,
        zmin=-2,
        zmax=2,
        text=stats_df_display['promedio'].round(2).astype(str),
        texttemplate='%{text}',
        textfont={"size": 12},
        colorbar=dict(
            title="Escala Likert",
            tickvals=[-2, -1, 0, 1, 2],
            ticktext=['Muy en desacuerdo', 'En desacuerdo', 'Neutro', 'De acuerdo', 'Muy de acuerdo']
        )
    ))
    
    fig.update_layout(
        title=title,
        height=max(400, len(stats_df_display) * 30),
        margin=dict(t=50, b=50, l=300, r=50)
    )
    
    return fig


def create_likert_stacked_bar(df: pd.DataFrame, prefix: str, title: str) -> go.Figure:
    """
    Crea gráfico de barras apiladas para respuestas Likert.
    """
    likert_data = df[
        df['Atributo'].str.startswith(prefix) & 
        df['Likert_Score'].notna()
    ]
    
    if len(likert_data) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No hay datos disponibles",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    # Mapear scores a etiquetas
    score_labels = {
        -2: 'Muy en desacuerdo',
        -1: 'En desacuerdo', 
        0: 'Neutro',
        1: 'De acuerdo',
        2: 'Muy de acuerdo'
    }
    
    # Crear tabla de contingencia
    likert_data = likert_data.copy()  # Evitar SettingWithCopyWarning
    likert_data.loc[:, 'Score_Label'] = likert_data['Likert_Score'].map(score_labels)
    
    # Simplificar nombres de preguntas
    likert_data.loc[:, 'Pregunta_Short'] = likert_data['Atributo'].str.replace(prefix, "").str.strip()
    
    # Calcular porcentajes por pregunta
    contingency = pd.crosstab(
        likert_data['Pregunta_Short'], 
        likert_data['Score_Label'], 
        normalize='index'
    ) * 100
    
    # Reordenar columnas
    score_order = ['Muy en desacuerdo', 'En desacuerdo', 'Neutro', 'De acuerdo', 'Muy de acuerdo']
    contingency = contingency.reindex(columns=[col for col in score_order if col in contingency.columns])
    
    # Crear gráfico apilado
    fig = go.Figure()
    
    colors = ['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4', '#9467bd']
    
    for i, (score, color) in enumerate(zip(score_order, colors)):
        if score in contingency.columns:
            fig.add_trace(go.Bar(
                name=score,
                x=contingency[score],
                y=contingency.index,
                orientation='h',
                marker_color=color,
                text=[f'{val:.1f}%' if val > 5 else '' for val in contingency[score]],
                textposition='inside'
            ))
    
    fig.update_layout(
        barmode='stack',
        title=title,
        xaxis_title='Porcentaje (%)',
        yaxis_title='',
        height=max(400, len(contingency) * 40),
        margin=dict(t=50, b=50, l=300, r=50),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig


def create_kpi_cards(kpis: dict) -> str:
    """
    Crea HTML para mostrar KPIs como tarjetas.
    """
    html = """
    <div style="display: flex; justify-content: space-around; margin: 20px 0;">
    """
    
    # Encuestados
    html += f"""
        <div style="background: linear-gradient(45deg, #1f77b4, #aec7e8); 
                   padding: 20px; border-radius: 10px; text-align: center; 
                   color: white; min-width: 150px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h3 style="margin: 0; font-size: 2em;">{kpis.get('encuestados', 0)}</h3>
            <p style="margin: 5px 0 0 0;">Encuestados</p>
        </div>
    """
    
    # NPS
    nps_value = kpis.get('nps', 0)
    nps_color = "#2ca02c" if nps_value > 0 else "#d62728" if nps_value < 0 else "#ff7f0e"
    html += f"""
        <div style="background: linear-gradient(45deg, {nps_color}, {nps_color}88); 
                   padding: 20px; border-radius: 10px; text-align: center; 
                   color: white; min-width: 150px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h3 style="margin: 0; font-size: 2em;">{nps_value:.1f}</h3>
            <p style="margin: 5px 0 0 0;">NPS Score</p>
        </div>
    """
    
    # Ahorro de tiempo
    tiempo_value = kpis.get('percibe_ahorro_tiempo', 0)
    html += f"""
        <div style="background: linear-gradient(45deg, #ff7f0e, #ffbb78); 
                   padding: 20px; border-radius: 10px; text-align: center; 
                   color: white; min-width: 150px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h3 style="margin: 0; font-size: 2em;">{tiempo_value:.1f}%</h3>
            <p style="margin: 5px 0 0 0;">Percibe Ahorro de Tiempo</p>
        </div>
    """
    
    html += "</div>"
    return html


def create_timeline_comments(responses_df: pd.DataFrame) -> str:
    """
    Crea una visualización tipo timeline para comentarios.
    """
    if len(responses_df) == 0:
        return "<p>No hay comentarios disponibles.</p>"
    
    html = """
    <div style="max-height: 400px; overflow-y: auto; padding: 10px;">
    """
    
    for _, row in responses_df.iterrows():
        fecha = row['Hora de inicio'].strftime('%d/%m/%Y %H:%M') if pd.notna(row['Hora de inicio']) else 'Sin fecha'
        nombre = row['Nombre'] if pd.notna(row['Nombre']) else 'Anónimo'
        comentario = row['Valor'] if pd.notna(row['Valor']) else ''
        
        html += f"""
        <div style="border-left: 3px solid #1f77b4; padding-left: 15px; margin-bottom: 20px;">
            <div style="color: #666; font-size: 0.9em; margin-bottom: 5px;">
                <strong>{nombre}</strong> - {fecha}
            </div>
            <div style="background: #f8f9fa; padding: 10px; border-radius: 5px; 
                       border: 1px solid #e9ecef;">
                {comentario}
            </div>
        </div>
        """
    
    html += "</div>"
    return html


def create_nps_pie_chart(df: pd.DataFrame) -> go.Figure:
    """
    Crea gráfico de torta para recomendación a un colega (NPS).
    """
    from constants import Q_NPS
    
    # Filtrar datos NPS
    nps_data = df[df['Atributo'] == Q_NPS]['Valor'].value_counts()
    
    if len(nps_data) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No hay datos disponibles",
            x=0.5, y=0.5,
            font=dict(size=16, color="gray"),
            showarrow=False
        )
        return fig
    
    # Colores para las categorías NPS
    colors = {
        'Muy recomendable': '#2E8B57',      # Verde oscuro
        'Recomendable': '#90EE90',          # Verde claro
        'Poco recomendable': '#FFD700',     # Amarillo
        'No recomendable': '#FF6347',       # Rojo claro
        'Nada recomendable': '#DC143C'      # Rojo oscuro
    }
    
    # Crear lista de colores en el orden de los datos
    chart_colors = [colors.get(label, '#CCCCCC') for label in nps_data.index]
    
    fig = px.pie(
        values=nps_data.values,
        names=nps_data.index,
        title="Recomendación a un Colega",
        color_discrete_sequence=chart_colors
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Respuestas: %{value}<br>Porcentaje: %{percent}<extra></extra>'
    )
    
    fig.update_layout(
        font=dict(size=12),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05
        ),
        margin=dict(t=40, b=40, l=40, r=120)
    )
    
    return fig
