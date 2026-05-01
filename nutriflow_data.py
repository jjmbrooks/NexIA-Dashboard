"""
Capa de datos para NutriFlow Dashboard
Conexión directa a Google Sheets via Service Account (solo lectura)
"""
import json
import os
from datetime import date
from typing import Optional

SHEET_ID = "1c9upJ5hqsZsrh2q5jZswfj-ANecV_08xkaIitv2RLoA"
SHEET_NAME = "Registro de Alimentación"


def get_client():
    """Retorna cliente autenticado de gspread usando Service Account"""
    import gspread
    from google.oauth2.service_account import Credentials

    scope = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/drive.readonly"
    ]

    # En Streamlit Cloud: usa st.secrets
    # En local: usa variable de entorno
    creds_info = None
    try:
        import streamlit as st
        creds_info = st.secrets["google_credentials"]
    except Exception as e:
        import sys
        print(f"[get_client] st.secrets falló: {type(e).__name__}: {e}", file=sys.stderr)
        env_creds = os.environ.get("GOOGLE_CREDENTIALS")
        if env_creds:
            creds_info = json.loads(env_creds)

    if not creds_info:
        # Fallback: archivo local (desarrollo)
        sa_path = os.path.join(os.path.dirname(__file__), "service_account.json")
        if os.path.exists(sa_path):
            with open(sa_path) as f:
                creds_info = json.load(f)

    if not creds_info:
        raise ValueError("No se encontraron credenciales de Google. "
                         "Configúralas en st.secrets, GOOGLE_CREDENTIALS, o service_account.json")

    creds = Credentials.from_service_account_info(creds_info, scopes=scope)
    return gspread.authorize(creds)


def load_food_data() -> list[dict]:
    """Carga y parsea todos los registros de alimentación desde el Sheet en vivo"""
    gc = get_client()
    sheet = gc.open_by_key(SHEET_ID).worksheet(SHEET_NAME)
    rows = sheet.get_all_values()

    if not rows:
        return []

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
