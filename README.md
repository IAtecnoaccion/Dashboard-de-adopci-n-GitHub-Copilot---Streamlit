# 🤖 Dashboard de Adopción GitHub Copilot

Dashboard interactivo desarrollado con Streamlit para analizar la adopción y percepción de GitHub Copilot en equipos de desarrollo.

## 📊 Características

- **KPIs Principales**: Número de encuestados, NPS Score, percepción de ahorro de tiempo
- **Análisis de Sentimiento**: Visualización de actitudes hacia GitHub Copilot
- **Uso y Percepción**: Análisis detallado del uso individual y en equipo
- **Recomendaciones**: Gráficos de torta mostrando nivel de recomendación
- **Filtros Dinámicos**: Filtrado por persona para análisis específicos
- **Exportación**: Funcionalidad para exportar datos filtrados

## 🚀 Funcionalidades

### Secciones del Dashboard
1. **Portada**: KPIs principales y gráficos de sentimiento/recomendación
2. **Uso**: Análisis de patrones de uso de Copilot
3. **Percepción Individual**: Impacto personal en productividad
4. **Percepción de Equipo**: Impacto en dinámicas de equipo
5. **Texto Libre**: Comentarios y sugerencias de los usuarios
6. **Exportar**: Descarga de datos en formato Excel

## 📈 Métricas Calculadas

- **NPS (Net Promoter Score)**: Basado en recomendación a colegas
- **Categorización NPS**:
  - Promotores: "Muy recomendable", "Recomendable"
  - Pasivos: "Poco recomendable"
  - Detractores: "No recomendable", "Nada recomendable"

## 🛠️ Tecnologías

- **Streamlit**: Framework de aplicación web
- **Pandas**: Procesamiento de datos
- **Plotly**: Visualizaciones interactivas
- **OpenPyXL**: Lectura de archivos Excel

## 📁 Estructura del Proyecto

```
copilot-dashboard/
├── dashboard.py          # Aplicación principal Streamlit
├── data_utils.py         # Funciones de procesamiento de datos
├── charts.py            # Funciones de visualización
├── constants.py         # Constantes y mapeos
├── requirements.txt     # Dependencias
├── .streamlit/
│   └── config.toml     # Configuración de Streamlit
└── Encuesta de adopción de GitHub Copilot tabla.xlsx
```

## 🚀 Ejecución Local

```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

## 📊 Formato de Datos

El dashboard espera un archivo Excel con las siguientes columnas:
- `Id`: Identificador único
- `Hora de inicio`: Timestamp de inicio
- `Hora de finalización`: Timestamp de finalización  
- `Correo electrónico`: Email del encuestado
- `Nombre`: Nombre del encuestado
- `Atributo`: Pregunta/categoría
- `Valor`: Respuesta del encuestado

## 👥 Desarrollado por

Dashboard desarrollado para análisis de adopción de GitHub Copilot en **Tecno Accion S.A**

---

🔗 **Demo**: [Link al dashboard en vivo](https://encuesta-ghcopilot-tasa.streamlit.app/)
