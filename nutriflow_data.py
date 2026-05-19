"""
Capa de datos para NutriFlow Dashboard
Conexión directa a Google Sheets via Service Account (solo lectura)
"""
import json
import os
from datetime import date, datetime
from typing import Optional
from zoneinfo import ZoneInfo

SHEET_ID = "1c9upJ5hqsZsrh2q5jZswfj-ANecV_08xkaIitv2RLoA"
SHEET_NAME = "Registro de Alimentación"
SHEET_METAS = "Metas"


def get_client():
    """Retorna cliente autenticado de gspread usando Service Account"""
    import gspread
    from google.oauth2.service_account import Credentials

    scope = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/drive.readonly"
    ]

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
        # Fallback: archivo local OAuth token (desarrollo)
        token_paths = [
            "/opt/data/google_token.json",
            os.path.join(os.path.dirname(__file__), "google_token.json"),
            os.path.expanduser("~/.hermes/google_token.json"),
        ]
        for tp in token_paths:
            if os.path.exists(tp):
                with open(tp) as f:
                    tok_data = json.load(f)
                from google.oauth2.credentials import Credentials as OAuthCreds
                creds = OAuthCreds(
                    token=tok_data.get("token") or tok_data.get("access_token", ""),
                    refresh_token=tok_data.get("refresh_token"),
                    token_uri=tok_data.get("token_uri", "https://oauth2.googleapis.com/token"),
                    client_id=tok_data.get("client_id", ""),
                    client_secret=tok_data.get("client_secret", ""),
                    scopes=tok_data.get("scopes", ["https://www.googleapis.com/auth/spreadsheets"]),
                )
                return gspread.authorize(creds)

    if not creds_info:
        raise ValueError("No se encontraron credenciales de Google. "
                         "Configúralas en st.secrets, GOOGLE_CREDENTIALS, o service_account.json")

    creds = Credentials.from_service_account_info(creds_info, scopes=scope)
    return gspread.authorize(creds)


def load_goals() -> dict:
    """
    Carga las metas nutricionales desde la hoja 'Metas' del spreadsheet.
    Retorna dict: {mes: {calorias, proteina, grasas, carbos, fibra}}
    Fallback a METAS_FALLBACK si no puede leer el sheet.
    """
    from config import METAS_FALLBACK
    from datetime import datetime

    try:
        gc = get_client()
        sheet = gc.open_by_key(SHEET_ID).worksheet(SHEET_METAS)
        rows = sheet.get_all_values()

        if not rows or len(rows) < 2:
            return METAS_FALLBACK.copy()

        # Columnas esperadas: Año, Mes, Calorías, Proteína, Grasas, Carbos, Fibra, Comentario
        metas = {}
        for row in rows[1:]:
            if len(row) < 7:
                continue
            mes = row[1].strip()
            if not mes:
                continue
            metas[mes] = {
                "calorias": _parse_float(row[2]),
                "proteina": _parse_float(row[3]),
                "grasas": _parse_float(row[4]),
                "carbos": _parse_float(row[5]),
                "fibra": _parse_float(row[6]),
            }

        if metas:
            return metas
        return METAS_FALLBACK.copy()

    except Exception as e:
        import sys
        print(f"[load_goals] Error: {type(e).__name__}: {e}", file=sys.stderr)
        return METAS_FALLBACK.copy()


def get_current_goals() -> dict:
    """
    Retorna las metas del mes actual desde el sheet.
    """
    metas = load_goals()
    ahora = datetime.now(ZoneInfo("America/Mexico_City"))
    mes_nombre = ahora.strftime("%B")
    mapeo = {
        "January": "Enero", "February": "Febrero", "March": "Marzo",
        "April": "Abril", "May": "Mayo", "June": "Junio",
        "July": "Julio", "August": "Agosto", "September": "Septiembre",
        "October": "Octubre", "November": "Noviembre", "December": "Diciembre",
    }
    mes_esp = mapeo.get(mes_nombre, mes_nombre)
    return metas.get(mes_esp, {})


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
