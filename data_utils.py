"""
Utilidades para carga, limpieza y transformación de datos.
"""

import pandas as pd
import numpy as np
import re
from typing import Dict, List, Optional, Tuple
from constants import (
    LIKERT_MAPPING, NPS_MAPPING, REQUIRED_COLUMNS,
    Q_NPS, Q_USO_IMPACTO, Q_USO, Q_MODO, Q_YO_PREFIX, Q_EQ_PREFIX,
    TIEMPO_PATTERNS
)


def clean_text(s: str) -> str:
    """
    Limpia texto: strip, reemplaza nbsp, normaliza espacios.
    """
    if pd.isna(s) or not isinstance(s, str):
        return s
    
    # Strip y reemplazar nbsp
    s = str(s).strip().replace('\xa0', ' ')
    
    # Normalizar espacios múltiples a uno solo
    s = re.sub(r'\s+', ' ', s)
    
    return s


def load_data(file_path: str) -> pd.DataFrame:
    """
    Carga el archivo Excel y selecciona automáticamente la primera hoja válida.
    """
    try:
        # Intentar leer todas las hojas
        excel_file = pd.ExcelFile(file_path, engine='openpyxl')
        
        # Buscar la primera hoja que tenga las columnas requeridas
        for sheet_name in excel_file.sheet_names:
            try:
                df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
                
                # Verificar si tiene las columnas requeridas
                if all(col in df.columns for col in REQUIRED_COLUMNS):
                    return process_dataframe(df)
                    
            except Exception as e:
                continue
        
        # Si no encuentra ninguna hoja válida, intentar la primera
        df = pd.read_excel(file_path, sheet_name=0, engine='openpyxl')
        return process_dataframe(df)
        
    except Exception as e:
        raise Exception(f"Error al cargar el archivo: {str(e)}")


def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Procesa el DataFrame: tipos, limpieza, explosión de valores múltiples.
    """
    # Verificar columnas requeridas
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Faltan columnas requeridas: {missing_cols}")
    
    # Limpiar texto en todas las columnas de texto
    text_columns = ["Correo electrónico", "Nombre", "Atributo", "Valor"]
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].apply(clean_text)
    
    # Convertir tipos
    df['Id'] = pd.to_numeric(df['Id'], errors='coerce').astype('Int64')
    
    # Convertir fechas con dayfirst=True
    for date_col in ["Hora de inicio", "Hora de finalización"]:
        if date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col], dayfirst=True, errors='coerce')
    
    # Explotar valores múltiples separados por ;
    df = explode_multivalue(df)
    
    # Agregar columnas derivadas
    df = add_derived_columns(df)
    
    return df


def explode_multivalue(df: pd.DataFrame) -> pd.DataFrame:
    """
    Explota valores múltiples en la columna Valor separados por ;
    """
    # Identificar filas con múltiples valores
    df['Valor_split'] = df['Valor'].astype(str).str.split(';')
    
    # Explotar y limpiar
    df_exploded = df.explode('Valor_split')
    df_exploded['Valor'] = df_exploded['Valor_split'].apply(clean_text)
    
    # Eliminar valores vacíos
    df_exploded = df_exploded[df_exploded['Valor'].notna() & (df_exploded['Valor'] != '')]
    
    # Eliminar columna temporal
    df_exploded = df_exploded.drop('Valor_split', axis=1)
    
    return df_exploded.reset_index(drop=True)


def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega columnas derivadas: Likert score, NPS class, etc.
    """
    # Mapear Likert cuando corresponde
    df['Likert_Score'] = df.apply(lambda row: map_likert_score(row), axis=1)
    
    # Mapear NPS class
    df['NPS_Class'] = df.apply(lambda row: map_nps_class(row), axis=1)
    
    return df


def map_likert_score(row) -> Optional[int]:
    """
    Mapea respuestas Likert a scores numéricos cuando corresponde.
    """
    atributo = str(row['Atributo'])
    valor = str(row['Valor'])
    
    # Solo aplicar a preguntas que empiecen con los prefijos correctos
    if atributo.startswith(Q_YO_PREFIX) or atributo.startswith(Q_EQ_PREFIX):
        return LIKERT_MAPPING.get(valor, np.nan)
    
    return np.nan


def map_nps_class(row) -> Optional[str]:
    """
    Clasifica respuestas NPS.
    """
    if str(row['Atributo']) == Q_NPS:
        # Normalizar el valor quitando espacios en blanco
        valor_normalizado = str(row['Valor']).strip() if pd.notna(row['Valor']) else ""
        return NPS_MAPPING.get(valor_normalizado, "Detractor")
    
    return None


def compute_kpis(df: pd.DataFrame) -> Dict:
    """
    Calcula KPIs principales.
    """
    kpis = {}
    
    # Encuestados únicos
    kpis['encuestados'] = df['Correo electrónico'].nunique()
    
    # NPS
    nps_data = df[df['NPS_Class'].notna()]
    if len(nps_data) > 0:
        nps_counts = nps_data['NPS_Class'].value_counts()
        total_nps = len(nps_data)
        
        promotores = nps_counts.get('Promotor', 0) / total_nps * 100
        detractores = nps_counts.get('Detractor', 0) / total_nps * 100
        
        kpis['nps'] = promotores - detractores
    else:
        kpis['nps'] = 0
    
    # % Percibe ahorro de tiempo
    tiempo_data = df[df['Atributo'] == Q_USO_IMPACTO]
    if len(tiempo_data) > 0:
        tiempo_responses = tiempo_data['Valor'].str.lower()
        ahorro_tiempo = any(
            any(pattern in response for pattern in TIEMPO_PATTERNS)
            for response in tiempo_responses if isinstance(response, str)
        )
        
        total_personas = tiempo_data['Correo electrónico'].nunique()
        personas_ahorro = 0
        
        for email in tiempo_data['Correo electrónico'].unique():
            person_responses = tiempo_data[tiempo_data['Correo electrónico'] == email]['Valor']
            if any(
                any(pattern in str(resp).lower() for pattern in TIEMPO_PATTERNS)
                for resp in person_responses
            ):
                personas_ahorro += 1
        
        kpis['percibe_ahorro_tiempo'] = (personas_ahorro / total_personas * 100) if total_personas > 0 else 0
    else:
        kpis['percibe_ahorro_tiempo'] = 0
    
    return kpis


def filter_df(df: pd.DataFrame, personas: List[str] = None) -> pd.DataFrame:
    """
    Filtra el DataFrame por personas.
    """
    filtered_df = df.copy()
    
    # Filtrar por personas (solo por nombre)
    if personas and len(personas) > 0:
        # Normalizar nombres para comparación (limpiar espacios)
        nombres_normalizados = [p.strip() for p in personas]
        # Crear máscara comparando nombres normalizados
        mask = filtered_df['Nombre'].str.strip().isin(nombres_normalizados)
        filtered_df = filtered_df[mask]
    
    return filtered_df


def get_actividades_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula estadísticas de actividades de uso.
    """
    actividades = df[df['Atributo'] == Q_USO]
    if len(actividades) == 0:
        return pd.DataFrame()
    
    total_encuestados = df['Correo electrónico'].nunique()
    
    stats = actividades.groupby('Valor').agg({
        'Correo electrónico': 'nunique'
    }).rename(columns={'Correo electrónico': 'usuarios'})
    
    stats['porcentaje'] = (stats['usuarios'] / total_encuestados * 100).round(1)
    stats = stats.sort_values('porcentaje', ascending=False)
    
    return stats


def get_modos_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula estadísticas de modos de uso.
    """
    modos = df[df['Atributo'] == Q_MODO]
    if len(modos) == 0:
        return pd.DataFrame()
    
    total_encuestados = df['Correo electrónico'].nunique()
    
    stats = modos.groupby('Valor').agg({
        'Correo electrónico': 'nunique'
    }).rename(columns={'Correo electrónico': 'usuarios'})
    
    stats['porcentaje'] = (stats['usuarios'] / total_encuestados * 100).round(1)
    stats = stats.sort_values('porcentaje', ascending=False)
    
    return stats


def get_likert_stats(df: pd.DataFrame, prefix: str) -> pd.DataFrame:
    """
    Calcula estadísticas de preguntas Likert.
    """
    likert_data = df[
        df['Atributo'].str.startswith(prefix) & 
        df['Likert_Score'].notna()
    ]
    
    if len(likert_data) == 0:
        return pd.DataFrame()
    
    stats = likert_data.groupby('Atributo').agg({
        'Likert_Score': ['mean', 'count']
    }).round(2)
    
    stats.columns = ['promedio', 'total_respuestas']
    
    # Calcular % de acuerdo (scores 1 y 2)
    acuerdo_data = likert_data[likert_data['Likert_Score'].isin([1, 2])]
    acuerdo_stats = acuerdo_data.groupby('Atributo').size()
    
    stats['respuestas_acuerdo'] = stats.index.map(acuerdo_stats).fillna(0)
    stats['pct_acuerdo'] = (stats['respuestas_acuerdo'] / stats['total_respuestas'] * 100).round(1)
    
    return stats


def get_text_responses(df: pd.DataFrame, atributo: str) -> pd.DataFrame:
    """
    Obtiene respuestas de texto libre para un atributo específico.
    """
    responses = df[df['Atributo'] == atributo][
        ['Correo electrónico', 'Nombre', 'Hora de inicio', 'Valor']
    ].copy()
    
    # Filtrar respuestas vacías
    responses = responses[
        responses['Valor'].notna() & 
        (responses['Valor'].str.strip() != '')
    ]
    
    responses = responses.sort_values('Hora de inicio', ascending=False)
    
    return responses


# Test functions para validación
def test_data_quality(df: pd.DataFrame) -> Dict:
    """
    Ejecuta tests básicos de calidad de datos.
    """
    tests = {}
    
    # Test: conteo de encuestados vs correos únicos
    unique_emails = df['Correo electrónico'].nunique()
    unique_names = df['Nombre'].nunique()
    tests['emails_vs_names'] = {
        'unique_emails': unique_emails,
        'unique_names': unique_names,
        'match': unique_emails == unique_names
    }
    
    # Test: verificación de explosión por ;
    original_valores = df['Valor'].str.contains(';', na=False).sum()
    tests['multivalue_explosion'] = {
        'valores_con_semicolon': original_valores,
        'explosion_applied': original_valores == 0  # Debería ser 0 después de la explosión
    }
    
    # Test: mapeo de Likert
    likert_mapped = df['Likert_Score'].notna().sum()
    likert_questions = df['Atributo'].str.startswith((Q_YO_PREFIX, Q_EQ_PREFIX)).sum()
    tests['likert_mapping'] = {
        'likert_scores_mapped': likert_mapped,
        'potential_likert_questions': likert_questions,
        'mapping_rate': (likert_mapped / likert_questions * 100) if likert_questions > 0 else 0
    }
    
    # Test: mapeo de NPS
    nps_mapped = df['NPS_Class'].notna().sum()
    nps_questions = (df['Atributo'] == Q_NPS).sum()
    tests['nps_mapping'] = {
        'nps_classes_mapped': nps_mapped,
        'nps_questions': nps_questions,
        'mapping_rate': (nps_mapped / nps_questions * 100) if nps_questions > 0 else 0
    }
    
    return tests
