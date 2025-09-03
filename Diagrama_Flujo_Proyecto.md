# DIAGRAMA DE FLUJO DEL PROYECTO
## Dashboard de Adopción GitHub Copilot - Tecno Acción S.A.

---

## 🏗️ ARQUITECTURA GENERAL DEL PROYECTO

```mermaid
graph TD
    A[📊 Encuesta GitHub Copilot] --> B[📋 Excel: Encuesta de adopción de GitHub Copilot tabla.xlsx]
    B --> C[🐍 Python: data_utils.py]
    C --> D[📈 Procesamiento de Datos]
    D --> E[📊 charts.py - Visualizaciones]
    D --> F[⚙️ constants.py - Configuración]
    E --> G[🖥️ dashboard.py - Streamlit App]
    F --> G
    G --> H[🌐 Streamlit Cloud]
    H --> I[👥 Usuario Final]
    
    J[📝 Documentación] --> K[📖 Manual Completo]
    J --> L[📄 Resumen Ejecutivo]
    J --> M[📋 Informes Detallados]
    
    style A fill:#e1f5fe
    style H fill:#c8e6c9
    style I fill:#fff3e0
    style J fill:#f3e5f5
```

---

## 🔄 FLUJO DE DATOS DETALLADO

```mermaid
flowchart TD
    subgraph "📥 ENTRADA DE DATOS"
        A1[👥 5 Desarrolladores]
        A2[📝 Encuesta Online]
        A3[📊 Respuestas Recolectadas]
        A1 --> A2 --> A3
    end
    
    subgraph "🗂️ ALMACENAMIENTO"
        B1[📋 Excel File]
        B2[Columnas: Id, Nombre, Atributo, Valor]
        B3[Datos de Agosto 2025]
        A3 --> B1
        B1 --> B2 --> B3
    end
    
    subgraph "⚙️ PROCESAMIENTO"
        C1[📊 data_utils.py]
        C2[Limpieza de Datos]
        C3[Cálculo de KPIs]
        C4[Filtrado Dinámico]
        B3 --> C1 --> C2 --> C3 --> C4
    end
    
    subgraph "📈 VISUALIZACIÓN"
        D1[📊 charts.py]
        D2[Gráficos Plotly]
        D3[Métricas KPI]
        D4[Tablas Dinámicas]
        C4 --> D1 --> D2
        C4 --> D3
        C4 --> D4
    end
    
    subgraph "🖥️ DASHBOARD"
        E1[🏠 Portada]
        E2[🚀 Uso]
        E3[👤 Percepción Individual]
        E4[👥 Percepción Equipo]
        E5[💬 Comentarios]
        E6[📤 Exportar]
        D2 --> E1
        D2 --> E2
        D2 --> E3
        D2 --> E4
        D3 --> E1
        D4 --> E5
        C4 --> E6
    end
    
    subgraph "🌐 DESPLIEGUE"
        F1[🚀 Streamlit Cloud]
        F2[🔗 URL Pública]
        F3[📱 Acceso Multi-dispositivo]
        E1 --> F1
        E2 --> F1
        E3 --> F1
        E4 --> F1
        E5 --> F1
        E6 --> F1
        F1 --> F2 --> F3
    end
    
    style A1 fill:#e3f2fd
    style F1 fill:#e8f5e8
    style F3 fill:#fff8e1
```

---

## 📁 ESTRUCTURA DE ARCHIVOS

```mermaid
graph LR
    subgraph "📂 copilot-dashboard/"
        A[🐍 dashboard.py<br/>• Main Streamlit App<br/>• 5 Secciones<br/>• Filtros Dinámicos]
        B[📊 charts.py<br/>• Gráficos Plotly<br/>• Visualizaciones<br/>• Timeline]
        C[🔧 data_utils.py<br/>• Procesamiento<br/>• KPIs<br/>• Filtrado]
        D[⚙️ constants.py<br/>• Configuración<br/>• Variables<br/>• Constantes]
        E[📋 Excel Data<br/>• Encuesta Original<br/>• 5 Desarrolladores<br/>• Agosto 2025]
        F[📝 requirements.txt<br/>• Dependencias<br/>• Streamlit<br/>• Plotly, Pandas]
        G[🐳 Dockerfile<br/>• Containerización<br/>• Deploy Config]
        H[📖 Documentación<br/>• Manual Completo<br/>• Resumen Ejecutivo<br/>• Informes]
    end
    
    style A fill:#bbdefb
    style B fill:#c8e6c9
    style C fill:#dcedc8
    style D fill:#f8bbd9
```

---

## 🔧 FLUJO DE FUNCIONALIDADES

```mermaid
flowchart TD
    subgraph "🎯 USUARIO INTERACTÚA"
        U1[👤 Usuario accede al Dashboard]
        U2[🔍 Aplica Filtros]
        U3[📊 Navega entre Secciones]
        U4[📤 Exporta Datos]
        U1 --> U2 --> U3 --> U4
    end
    
    subgraph "⚙️ BACKEND PROCESA"
        B1[📊 Carga Datos Excel]
        B2[🔧 Aplica Filtros]
        B3[📈 Calcula KPIs]
        B4[📊 Genera Gráficos]
        B5[📋 Prepara Exportación]
        B1 --> B2 --> B3 --> B4
        B4 --> B5
    end
    
    subgraph "🖥️ FRONTEND MUESTRA"
        F1[🏠 KPIs en Portada]
        F2[📊 Gráficos Interactivos]
        F3[📋 Tablas Dinámicas]
        F4[💬 Comentarios de Usuarios]
        F5[📤 Descarga CSV]
    end
    
    U2 --> B2
    U3 --> B3
    U4 --> B5
    
    B3 --> F1
    B4 --> F2
    B4 --> F3
    B1 --> F4
    B5 --> F5
    
    style U1 fill:#e1f5fe
    style B1 fill:#f3e5f5
    style F1 fill:#e8f5e8
```

---

## 📊 FLUJO DE DATOS POR SECCIÓN

```mermaid
graph TD
    subgraph "📋 DATOS FUENTE"
        D1[Excel: 5 Desarrolladores]
        D2[Atributos: Sentimiento, NPS, Uso, etc.]
        D3[Valores: Respuestas específicas]
        D1 --> D2 --> D3
    end
    
    subgraph "🏠 PORTADA"
        P1[👥 KPI: Encuestados = 5]
        P2[⏱️ KPI: Ahorro Tiempo = 78%]
        P3[🎭 Gráfico: Sentimiento Circular]
        P4[📊 Gráfico: NPS Circular]
        D3 --> P1
        D3 --> P2
        D3 --> P3
        D3 --> P4
    end
    
    subgraph "🚀 USO"
        U1[📊 Actividades: Todas sin Top N]
        U2[🔧 Modos de Uso]
        U3[📈 Patrones Temporales]
        D3 --> U1
        D3 --> U2
        D3 --> U3
    end
    
    subgraph "👤 PERCEPCIÓN INDIVIDUAL"
        I1[📊 Gráficos por Pregunta]
        I2[🚫 Sin Promedio]
        I3[🚫 Sin Likert]
        D3 --> I1
    end
    
    subgraph "👥 PERCEPCIÓN EQUIPO"
        T1[📊 Gráficos por Pregunta]
        T2[🚫 Sin Promedio]
        T3[🚫 Sin Likert]
        D3 --> T1
    end
    
    subgraph "💬 COMENTARIOS"
        C1[🚧 Impedimentos Individuales]
        C2[🎓 Capacitaciones Individuales]
        C3[💭 Comentarios Individuales]
        D3 --> C1
        D3 --> C2
        D3 --> C3
    end
    
    style D1 fill:#e3f2fd
    style P1 fill:#e8f5e8
    style U1 fill:#fff3e0
    style I1 fill:#fce4ec
    style T1 fill:#f3e5f5
    style C1 fill:#e0f2f1
```

---

## 🔄 CICLO DE DESARROLLO Y DEPLOYMENT

```mermaid
graph TD
    subgraph "💻 DESARROLLO LOCAL"
        DEV1[👨‍💻 Código Python]
        DEV2[🧪 Testing Local]
        DEV3[📊 Validación Datos]
        DEV1 --> DEV2 --> DEV3
    end
    
    subgraph "📚 CONTROL DE VERSIONES"
        GIT1[📁 GitHub Repository]
        GIT2[🔄 Commits]
        GIT3[🚀 Push to Main]
        DEV3 --> GIT1 --> GIT2 --> GIT3
    end
    
    subgraph "🌐 DEPLOYMENT"
        DEPLOY1[☁️ Streamlit Cloud]
        DEPLOY2[🔗 Auto-Deploy]
        DEPLOY3[🌍 URL Pública]
        GIT3 --> DEPLOY1 --> DEPLOY2 --> DEPLOY3
    end
    
    subgraph "👥 USUARIO FINAL"
        USER1[📱 Acceso Multi-dispositivo]
        USER2[🔍 Filtros e Interacción]
        USER3[📊 Análisis de Datos]
        USER4[📤 Exportación]
        DEPLOY3 --> USER1 --> USER2 --> USER3 --> USER4
    end
    
    subgraph "🔄 FEEDBACK LOOP"
        FB1[📝 Recolección Feedback]
        FB2[🔧 Mejoras del Código]
        FB3[🚀 Nueva Versión]
        USER4 --> FB1 --> FB2 --> FB3
        FB3 --> DEV1
    end
    
    style DEV1 fill:#e1f5fe
    style DEPLOY1 fill:#e8f5e8
    style USER1 fill:#fff8e1
    style FB1 fill:#f3e5f5
```

---

## 🧩 COMPONENTES TÉCNICOS

```mermaid
mindmap
  root)Dashboard GitHub Copilot(
    (Frontend)
      Streamlit UI
      Plotly Charts
      Interactive Filters
      Responsive Design
    (Backend)
      Python Data Processing
      Pandas DataFrames
      Excel File Reading
      KPI Calculations
    (Data)
      Excel Source
      5 Developers
      Multiple Attributes
      August 2025 Data
    (Infrastructure)
      GitHub Repository
      Streamlit Cloud
      Auto-deployment
      Public URL
    (Documentation)
      Technical Manual
      Executive Summary
      User Guide
      API Reference
```

---

## 📈 FLUJO DE MÉTRICAS Y KPIs

```mermaid
flowchart LR
    subgraph "📊 DATOS RAW"
        R1[Respuesta 1: NPS]
        R2[Respuesta 2: Sentimiento]
        R3[Respuesta 3: Uso]
        R4[Respuesta 4: Tiempo]
        R5[Respuesta 5: Comentarios]
    end
    
    subgraph "⚙️ PROCESAMIENTO"
        P1[Cálculo NPS<br/>% Promotores - % Detractores]
        P2[Análisis Sentimiento<br/>Distribución porcentual]
        P3[Conteo Encuestados<br/>Total únicos]
        P4[Percepción Tiempo<br/>% que reporta ahorro]
    end
    
    subgraph "📈 KPIs FINALES"
        K1[👥 Encuestados: 5]
        K2[📊 NPS: 100%]
        K3[🎭 Sentimiento: 80% Decepcionado]
        K4[⏱️ Ahorro Tiempo: 78%]
    end
    
    R1 --> P1 --> K2
    R2 --> P2 --> K3
    R3 --> P3 --> K1
    R4 --> P4 --> K4
    
    style R1 fill:#e3f2fd
    style P1 fill:#f3e5f5
    style K1 fill:#e8f5e8
```

---

## 🎯 PUNTOS CLAVE DEL FLUJO

### 📥 **INPUT (Entrada)**
- **Fuente**: Encuesta online a 5 desarrolladores
- **Formato**: Excel con estructura específica
- **Período**: Datos de Agosto 2025
- **Contenido**: Respuestas sobre uso, percepción y recomendación

### ⚙️ **PROCESSING (Procesamiento)**
- **Lenguaje**: Python con Pandas
- **Limpieza**: Normalización y validación de datos
- **Cálculos**: KPIs automáticos (NPS, porcentajes, conteos)
- **Filtrado**: Dinámico por persona y fecha

### 📊 **OUTPUT (Salida)**
- **Visualización**: Dashboard interactivo en Streamlit
- **Gráficos**: Plotly para interactividad
- **Exportación**: CSV descargables
- **Acceso**: URL pública responsive

### 🔄 **DEPLOYMENT (Despliegue)**
- **Repositorio**: GitHub con auto-deploy
- **Hosting**: Streamlit Cloud gratuito
- **Actualizaciones**: Automáticas desde commits
- **Accesibilidad**: Multi-dispositivo y navegador

### 👥 **USER EXPERIENCE (Experiencia)**
- **Navegación**: 5 secciones principales
- **Interacción**: Filtros dinámicos y exportación
- **Insights**: KPIs claros y visualizaciones intuitivas
- **Documentación**: Manual completo y guía ejecutiva

---

## 🚀 BENEFICIOS DE LA ARQUITECTURA

### ✅ **Escalabilidad**
- Fácil agregar nuevos desarrolladores o encuestas
- Estructura modular para nuevas funcionalidades
- Separación clara de responsabilidades

### 🔧 **Mantenibilidad**
- Código bien documentado y organizado
- Constantes centralizadas en `constants.py`
- Funciones reutilizables en módulos separados

### 📊 **Usabilidad**
- Interfaz intuitiva sin curva de aprendizaje
- Filtros dinámicos para análisis personalizado
- Exportación para análisis externos

### 🌐 **Accesibilidad**
- Deploy automático y gratuito
- Acceso desde cualquier dispositivo
- No requiere instalaciones locales

---

**📅 Versión**: 1.0 - Septiembre 2025  
**🏢 Proyecto**: Dashboard GitHub Copilot - Tecno Acción S.A.  
**👨‍💻 Desarrollado**: Con GitHub Copilot

---

*Este diagrama muestra el flujo completo desde la recolección de datos hasta la visualización final, incluyendo todos los componentes técnicos y funcionales del proyecto.*
