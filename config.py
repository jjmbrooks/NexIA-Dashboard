"""
Configuración centralizada del Dashboard NutriFlow
"""

# IDs de los Spreadsheets
SHEET_IDS = {
    "nutriflow": "1c9upJ5hqsZsrh2q5jZswfj-ANecV_08xkaIitv2RLoA",
    "bodylab": "1EUMsWu6Oxy9U9WBWE7GeqRIkQ--sLKJhTcvuFLgB7cE",
    "habitos": "1VF2N9uV0lMGI73GiHU-QO65YWEMZBcSwB_fUXE08bLA",
}

SHEET_ID = SHEET_IDS["nutriflow"]  # Default para compatibilidad

# Nombres de hojas por proyecto
SHEET_NAMES = {
    "nutriflow": "Registro de Alimentación",
    "bodylab": "Bitácora",
    "habitos": "Registros",
}

# Metas mensuales (calorías, proteína, grasa, carbos, fibra)
METAS_MENSUALES = {
    "Febrero": {"calorias": 2000, "proteina": 90, "grasas": 54.7, "carbos": 287, "fibra": 25},
    "Marzo":   {"calorias": 2000, "proteina": 90, "grasas": 54.7, "carbos": 287, "fibra": 25},
    "Abril":   {"calorias": 1800, "proteina": 90, "grasas": 48.0, "carbos": 252, "fibra": 25},
    "Mayo":    {"calorias": 1700, "proteina": 90, "grasas": 44.7, "carbos": 234.5, "fibra": 25},
    "Junio":   {"calorias": 1600, "proteina": 90, "grasas": 41.3, "carbos": 217, "fibra": 25},
    "Julio":   {"calorias": 1500, "proteina": 90, "grasas": 38.0, "carbos": 199.5, "fibra": 25},
    "Agosto":  {"calorias": 1400, "proteina": 90, "grasas": 34.7, "carbos": 182, "fibra": 25},
    "Septiembre": {"calorias": 1300, "proteina": 90, "grasas": 31.3, "carbos": 164.5, "fibra": 25},
    "Octubre": {"calorias": 1300, "proteina": 90, "grasas": 31.3, "carbos": 164.5, "fibra": 25},
}

# Mapeo de nombres de macros
MACRO_LABELS = {
    "calorias": "Calorías",
    "proteina": "Proteína",
    "carbos": "Carbohidratos",
    "grasas": "Grasas",
    "fibra": "Fibra",
}

MACRO_COLORS = {
    "calorias": "#FF6B35",
    "proteina": "#1E88E5",
    "carbos": "#43A047",
    "grasas": "#FDD835",
    "fibra": "#8E24AA",
}

MACRO_UNITS = {
    "calorias": "kcal",
    "proteina": "g",
    "carbos": "g",
    "grasas": "g",
    "fibra": "g",
}
