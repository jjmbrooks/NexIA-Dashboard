"""
Configuración centralizada del Dashboard NutriFlow
"""

# IDs de los Spreadsheets
SHEET_IDS = {
    "nutriflow": "1c9upJ5hqsZsrh2q5jZswfj-ANecV_08xkaIitv2RLoA",
    "bodylab": "1EUMsWu6Oxy9U9WBWE7GeqRIkQ--sLKJhTcvuFLgB7cE",
    "habitos": "1VF2N9uV0lMGI73GiHU-QO65YWEMZBcSwB_fUXE08bLA",
}

SHEET_ID = SHEET_IDS["nutriflow"]

# Nombres de hojas por proyecto
SHEET_NAMES = {
    "nutriflow": "Registro de Alimentación",
    "bodylab": "Bitácora",
    "habitos": "Registros",
    "metas": "Metas",
    "peso": "Registro de Peso",
    "datos_generales": "Datos Generales",
}

# Metas por defecto (fallback si no se puede leer del sheet)
METAS_FALLBACK = {
    "Enero":   {"calorias": 2000, "proteina": 90, "grasas": 54.7, "carbos": 287, "fibra": 25},
    "Febrero": {"calorias": 2000, "proteina": 90, "grasas": 54.7, "carbos": 287, "fibra": 25},
    "Marzo":   {"calorias": 2000, "proteina": 90, "grasas": 54.7, "carbos": 287, "fibra": 25},
    "Abril":   {"calorias": 1800, "proteina": 90, "grasas": 48.0, "carbos": 252, "fibra": 25},
    "Mayo":    {"calorias": 1800, "proteina": 90, "grasas": 48,   "carbos": 252, "fibra": 25},
    "Junio":   {"calorias": 1800, "proteina": 90, "grasas": 48,   "carbos": 252, "fibra": 25},
}

MACRO_LABELS = {
    "calorias": "Calorías",
    "proteina": "Proteína",
    "carbos": "Carbohidratos",
    "grasas": "Grasas",
    "fibra": "Fibra",
}

MACRO_COLORS = {
    "calorias": "#FF6B35",
    "proteina": "#818cf8",
    "carbos": "#22c55e",
    "grasas": "#facc15",
    "fibra": "#c084fc",
}

MACRO_UNITS = {
    "calorias": "kcal",
    "proteina": "g",
    "carbos": "g",
    "grasas": "g",
    "fibra": "g",
}

MACRO_EMOJIS = {
    "calorias": "🔥",
    "proteina": "💪",
    "carbos": "🌾",
    "grasas": "🧈",
    "fibra": "🧵",
}
