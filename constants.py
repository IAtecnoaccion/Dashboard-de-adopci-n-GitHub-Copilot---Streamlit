"""
Constantes y textos de preguntas para el dashboard de adopción de GitHub Copilot.
"""

# Textos exactos de preguntas para detectar
Q_SENTIMIENTO = "¿Cómo te sentirías si ya no pudieras usar GitHub Copilot?"
Q_USO = "En las últimas 2 semanas, use Copilot para..."
Q_USO_IMPACTO = "En las 2 últimas semanas usando Copilot..."
Q_YO_PREFIX = "Al usar Copilot, yo"
Q_EQ_PREFIX = "Al usar Copilot, mi equipo"
Q_MODO = "¿Qué tipo de modo preferís al usar Copilot?"
Q_NPS = "¿Qué tan probable es que recomiendes Copilot a un/a colega?"
Q_IMPEDIMENTOS = "¿Existe algún impedimento para utilizar más Copilot?"
Q_CAPACITACIONES = "¿Que capacitaciones te ayudarían a sacarle más provecho?"
Q_COMENTARIOS = "Comentarios y recomendaciones que quieras hacer:"

# Mapeo de valores Likert (incluyendo variantes con tildes/espacios)
LIKERT_MAPPING = {
    "Estoy muy de acuerdo": 2,
    "Estoy muy de acuerdo.": 2,
    "Muy de acuerdo": 2,
    "Estoy de acuerdo": 1,
    "Estoy de acuerdo.": 1,
    "De acuerdo": 1,
    "Neutro": 0,
    "Neutral": 0,
    "No estoy de acuerdo": -1,
    "No estoy de acuerdo.": -1,
    "En desacuerdo": -1,
    "Estoy muy en desacuerdo": -2,
    "Estoy muy en desacuerdo.": -2,
    "Muy en desacuerdo": -2
}

# Mapeo de NPS
NPS_MAPPING = {
    "Muy recomendable": "Promotor",
    "Recomendable": "Promotor",
    "Poco recomendable": "Pasivo",
    "No recomendable": "Detractor",
    "Nada recomendable": "Detractor"
}

# Columnas esperadas en el dataset
REQUIRED_COLUMNS = ["Id", "Hora de inicio", "Hora de finalización", 
                   "Correo electrónico", "Nombre", "Atributo", "Valor"]

# Bloques de preguntas para el filtro
BLOQUES = [
    "Portada",
    "Uso",
    "Percepción Individual", 
    "Percepción Equipo",
    "Texto Libre",
    "Exportar"
]

# Patrones de tiempo para detección
TIEMPO_PATTERNS = [
    "ahorre tiempo",
    "ahorro tiempo", 
    "ahorré tiempo",
    "ahorrar tiempo",
    "save time",
    "tiempo ahorrado"
]
