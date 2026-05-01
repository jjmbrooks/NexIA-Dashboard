"""
Capa de datos para NutriFlow Dashboard
Conexión a Google Sheets, parseo y limpieza de datos
"""
import json
import os
from datetime import datetime, date
from typing import Optional

SHEET_ID = "1c9upJ5hqsZsrh2q5jZswfj-ANecV_08xkaIitv2RLoA"

def get_google_creds():
    """Obtiene credenciales de Google desde st.secrets o variable de entorno"""
    try:
        import streamlit as st
        return st.secrets["google_credentials"]
    except (ImportError, KeyError):
        env_creds = os.environ.get("GOOGLE_CREDENTIALS")
        if env_creds:
            return json.loads(env_creds)
    raise ValueError("No se encontraron credenciales de Google. Configúralas en .streamlit/secrets.toml")

def get_client():
    """Retorna cliente autenticado de gspread"""
    import gspread
    from google.oauth2.service_account import Credentials
    scope = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/drive.readonly"
    ]
    creds_info = get_google_creds()
    creds = Credentials.from_service_account_info(creds_info, scopes=scope)
    return gspread.authorize(creds)

def load_food_data() -> list[dict]:
    """Carga y parsea todos los registros de alimentación"""
    gc = get_client()
    sheet = gc.open_by_key(SHEET_ID).sheet1
    rows = sheet.get_all_values()
    
    if not rows:
        return []
    
    header = rows[0]
    data = []
    for row in rows[1:]:
        if len(row) < 8 or not row[0].strip():
            continue
        record = {
            "fecha_hora": row[0].strip(),
            "comida": row[1].strip() if len(row) > 1 else "",
            "descripcion": row[2].strip() if len(row) > 2 else "",
            "calorias": _parse_float(row[3]),
            "proteina": _parse_float(row[4]),
            "carbos": _parse_float(row[5]),
            "grasas": _parse_float(row[6]),
            "fibra": _parse_float(row[7]),
            "notas": row[8].strip() if len(row) > 8 else "",
        }
        data.append(record)
    return data

def _parse_float(val) -> float:
    """Convierte string a float de forma segura"""
    if not val or not str(val).strip():
        return 0.0
    try:
        return float(str(val).strip().replace(",", ""))
    except ValueError:
        return 0.0

def parse_date(date_str: str) -> Optional[date]:
    """Parsea fecha de varios formatos a objeto date"""
    from dateutil import parser
    try:
        dt = parser.parse(date_str, dayfirst=True)
        return dt.date()
    except:
        return None
