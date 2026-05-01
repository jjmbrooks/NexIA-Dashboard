"""
Capa de datos para NutriFlow Dashboard
Lee datos desde un snapshot JSON local (generado periódicamente)
"""
import json
import os
from datetime import date
from typing import Optional

# Ruta al snapshot de datos
SNAPSHOT_PATH = os.path.join(os.path.dirname(__file__), "data_snapshot.json")


def load_food_data() -> list[dict]:
    """Carga los registros de alimentación desde el snapshot local"""
    if not os.path.exists(SNAPSHOT_PATH):
        raise FileNotFoundError(
            f"No se encuentra el archivo de datos ({SNAPSHOT_PATH}). "
            "Ejecuta primero el script de generación de snapshot."
        )
    with open(SNAPSHOT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_date(date_str: str) -> Optional[date]:
    """Parsea fecha de varios formatos a objeto date"""
    from dateutil import parser
    try:
        dt = parser.parse(date_str, dayfirst=True)
        return dt.date()
    except:
        return None
