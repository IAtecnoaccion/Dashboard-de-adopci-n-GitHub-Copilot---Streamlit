# DIAGRAMA VISUAL DEL PROYECTO
## Arquitectura Simplificada - Dashboard GitHub Copilot

---

## 🏗️ ARQUITECTURA GENERAL

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          📊 DASHBOARD GITHUB COPILOT                        │
│                            Tecno Acción S.A.                               │
└─────────────────────────────────────────────────────────────────────────────┘

    📥 ENTRADA                    ⚙️ PROCESAMIENTO                  📊 SALIDA
┌─────────────────┐           ┌─────────────────────┐           ┌─────────────────┐
│                 │           │                     │           │                 │
│  👥 5 Devs      │    ───►   │  🐍 Python          │    ───►   │  🖥️ Streamlit   │
│  📝 Encuesta    │           │  📊 data_utils.py   │           │  🌐 Dashboard   │
│  📋 Excel       │           │  📈 charts.py       │           │  📱 Responsive  │
│                 │           │  ⚙️ constants.py    │           │                 │
└─────────────────┘           └─────────────────────┘           └─────────────────┘
                                        │
                                        ▼
                              ┌─────────────────────┐
                              │  🎯 KPIs CLAVE      │
                              │  • NPS: 100%        │
                              │  • Ahorro: 78%      │
                              │  • Encuestados: 5   │
                              └─────────────────────┘
```

---

## 🔄 FLUJO DE DATOS

```
[📊 Excel Data] 
       │
       ▼
[🔍 Load & Clean] 
       │
       ▼
[📈 Calculate KPIs] 
       │
       ▼
[🎨 Generate Charts] 
       │
       ▼
[🖥️ Streamlit UI] 
       │
       ▼
[👥 End User]
```

---

## 📁 ESTRUCTURA DE ARCHIVOS

```
copilot-dashboard/
│
├── 📊 dashboard.py              # Main Streamlit app
├── 📈 charts.py                 # Plotly visualizations  
├── 🔧 data_utils.py             # Data processing
├── ⚙️ constants.py              # Configuration
├── 📋 requirements.txt          # Dependencies
├── 🐳 Dockerfile               # Container config
│
├── 📊 Data/
│   └── Encuesta de adopción de GitHub Copilot tabla.xlsx
│
└── 📖 Documentation/
    ├── Manual_Dashboard_GitHub_Copilot.md
    ├── Resumen_Ejecutivo_Dashboard.md
    └── Diagrama_Flujo_Proyecto.md
```

---

## 🖥️ INTERFAZ DEL DASHBOARD

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  🤖 Dashboard - Adopción GitHub Copilot                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  📊 KPIs:  [👥 5 Encuestados]    [⏱️ 78% Ahorro Tiempo]                    │
│                                                                             │
│  ┌─────────────────────┐        ┌─────────────────────┐                    │
│  │  🎭 Sentimiento     │        │  📊 NPS Score       │                    │
│  │     Circular        │        │     Circular        │                    │
│  │                     │        │                     │                    │
│  │  80% Decepcionado   │        │  100% Promotores    │                    │
│  │  20% No decp.       │        │  0% Detractores     │                    │
│  └─────────────────────┘        └─────────────────────┘                    │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🔍 Filtros:                                                                 │
│ [👥 Seleccionar Personas ▼] [📅 Desde] [📅 Hasta] [📊 Sección ▼]          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 SECCIONES DEL DASHBOARD

```
┌──────────────┬──────────────────────────────────────────────────────────────┐
│  SECCIÓN     │  CONTENIDO                                                   │
├──────────────┼──────────────────────────────────────────────────────────────┤
│  🏠 Portada  │  • KPIs principales (Encuestados, Ahorro Tiempo)            │
│              │  • Gráfico Sentimiento Circular                             │
│              │  • Gráfico NPS Circular                                     │
├──────────────┼──────────────────────────────────────────────────────────────┤
│  🚀 Uso      │  • Todas las actividades de uso (sin Top N)                │
│              │  • Modos de uso de Copilot                                  │
│              │  • Patrones de adopción                                     │
├──────────────┼──────────────────────────────────────────────────────────────┤
│  👤 Percep.  │  • Gráficos por pregunta individual                        │
│  Individual  │  • Sin promedio ni Likert                                   │
│              │  • Impacto personal por desarrollador                       │
├──────────────┼──────────────────────────────────────────────────────────────┤
│  👥 Percep.  │  • Gráficos por pregunta de equipo                         │
│  Equipo      │  • Sin promedio ni Likert                                   │
│              │  • Dinámicas grupales                                       │
├──────────────┼──────────────────────────────────────────────────────────────┤
│  💬 Coment.  │  • Impedimentos por persona                                 │
│  Usuarios    │  • Capacitaciones sugeridas                                 │
│              │  • Comentarios y recomendaciones                            │
└──────────────┴──────────────────────────────────────────────────────────────┘
```

---

## ⚙️ COMPONENTES TÉCNICOS

```
                    🖥️ FRONTEND (Streamlit)
┌─────────────────────────────────────────────────────────────────────────────┐
│  📊 Plotly Charts  │  🔍 Filters  │  📋 Tables  │  📤 Export  │  📱 Mobile   │
└─────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
                    🐍 BACKEND (Python)
┌─────────────────────────────────────────────────────────────────────────────┐
│  📊 data_utils.py  │  📈 charts.py  │  ⚙️ constants.py  │  🔧 dashboard.py │
└─────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
                    📊 DATA LAYER
┌─────────────────────────────────────────────────────────────────────────────┐
│           📋 Excel: Encuesta de adopción de GitHub Copilot tabla.xlsx        │
│           👥 5 Desarrolladores │ 📅 Agosto 2025 │ 📊 Multiple Attributes     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 CICLO DE VIDA

```
    📝 Encuesta                 🖥️ Dashboard               📊 Análisis
    ┌─────────┐                ┌─────────────┐             ┌─────────┐
    │ Online  │───────────────►│ Streamlit   │────────────►│ KPIs &  │
    │ 5 Devs  │                │ Interactive │             │ Insights│
    └─────────┘                └─────────────┘             └─────────┘
         │                           ▲                          │
         ▼                           │                          ▼
    ┌─────────┐                ┌─────────────┐             ┌─────────┐
    │ Excel   │───────────────►│ Python      │◄────────────│ Feedback│
    │ Data    │                │ Processing  │             │ & Update│
    └─────────┘                └─────────────┘             └─────────┘
```

---

## 🎯 INDICADORES CLAVE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              🎯 KPIs DASHBOARD                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  👥 ENCUESTADOS: 5          📊 NPS SCORE: 100%         ⏱️ AHORRO: 78%      │
│  ├─ Andrea Minin            ├─ 5 Promotores            ├─ Percepción        │
│  ├─ Rodolfo Ferreyra       ├─ 0 Pasivos               ├─ Positiva          │
│  ├─ Dante Casalla          ├─ 0 Detractores           ├─ Alto impacto      │
│  ├─ Rodrigo Cuellar        └─ Resultado Excepcional   └─ Mejora tangible   │
│  └─ Alexis Gutierrez                                                       │
│                                                                             │
│  🎭 SENTIMIENTO: 80% "Algo Decepcionado" sin Copilot                       │
│  └─ Indica dependencia positiva y valoración alta                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 DEPLOYMENT FLOW

```
👨‍💻 Developer         📚 GitHub              ☁️ Streamlit Cloud      👥 Users
┌─────────┐         ┌─────────────┐         ┌─────────────────┐      ┌─────────┐
│ Local   │   git   │ Repository  │  auto   │ Cloud Platform  │ URL  │ Browser │
│ Changes │ ──────► │ Main Branch │ ──────► │ Auto-Deploy     │ ───► │ Access  │
│         │  push   │             │ deploy  │                 │      │         │
└─────────┘         └─────────────┘         └─────────────────┘      └─────────┘
```

---

## 📈 RESULTADOS VISUALES

```
📊 GRÁFICO NPS (100%)
┌─────────────────────────────────────────┐
│ 🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢 Promotores (100%) │
│ 🟡                     Pasivos (0%)     │
│ 🔴                     Detractores (0%) │
└─────────────────────────────────────────┘

🎭 GRÁFICO SENTIMIENTO
┌─────────────────────────────────────────┐
│ 😔 Algo Decepcionado      █████████ 80% │
│ 😐 No Decepcionado        ██ 20%        │
└─────────────────────────────────────────┘

⏱️ AHORRO DE TIEMPO
┌─────────────────────────────────────────┐
│ ✅ Percibe Ahorro        ████████ 78%   │
│ ❌ No Percibe Ahorro     ██ 22%         │
└─────────────────────────────────────────┘
```

---

## 🔧 FUNCIONALIDADES INTERACTIVAS

```
🔍 FILTROS DINÁMICOS
├─ 👥 Por Persona: [Todos ▼] [Andrea] [Rodolfo] [Dante] [Rodrigo] [Alexis]
├─ 📅 Por Fecha: [Desde: 01/08/2025] [Hasta: 31/08/2025]
└─ 📊 Actualización: Tiempo real en todos los gráficos

📤 EXPORTACIÓN
├─ 📊 Datos Completos (CSV)
├─ 🚀 Respuestas de Uso (CSV)
├─ 💬 Comentarios (CSV)
└─ 📋 Con timestamp automático

📱 RESPONSIVE DESIGN
├─ 💻 Desktop: Columnas múltiples
├─ 📱 Mobile: Columna única
├─ 🖱️ Interactividad: Hover, click, zoom
└─ ⚡ Performance: Carga rápida
```

---

## 🎯 CONCLUSIÓN DEL FLUJO

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ✅ PROYECTO EXITOSO                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  📊 DATOS: 5 desarrolladores, 100% participación                           │
│  ⚙️ PROCESAMIENTO: Python automatizado, KPIs precisos                      │
│  🖥️ VISUALIZACIÓN: Dashboard interactivo, fácil de usar                    │
│  🌐 DEPLOY: Streamlit Cloud, acceso público                                │
│  📈 RESULTADOS: NPS 100%, 78% ahorro tiempo                                │
│                                                                             │
│  🎯 IMPACTO: Justifica inversión, guía decisiones futuras                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

**💡 Nota**: Este diagrama muestra todo el flujo del proyecto desde la encuesta hasta el dashboard final, incluyendo todos los componentes técnicos y funcionales.

**📅 Fecha**: 3 de Septiembre de 2025  
**🏢 Proyecto**: Tecno Acción S.A.  
**🤖 Desarrollado**: Con GitHub Copilot
