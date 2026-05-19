"""
Capa de datos para Body Lab Dashboard
Conexión directa a Google Sheets via Service Account
"""
import json
import os
from datetime import date, datetime
from typing import Optional

SHEET_ID = "1EUMsWu6Oxy9U9WBWE7GeqRIkQ--sLKJhTcvuFLgB7cE"
SHEET_BITACORA = "Bitácora"

SHEET_ID_NUTRI = "1c9upJ5hqsZsrh2q5jZswfj-ANecV_08xkaIitv2RLoA"
SHEET_PESO = "Registro de Peso"


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


def _parse_float(val) -> float:
    """Convierte string a float de forma segura"""
    if not val or not str(val).strip():
        return 0.0
    try:
        return float(str(val).strip().replace(",", ""))
    except ValueError:
        return 0.0


def parse_date(date_str: str) -> Optional[date]:
    """Parsea fecha desde formato DD/MM/YYYY o YYYY-MM-DD"""
    if not date_str:
        return None
    s = str(date_str).strip()
    try:
        if "-" in s and s.index("-") == 4:  # YYYY-MM-DD
            return datetime.strptime(s, "%Y-%m-%d").date()
        elif "/" in s:  # DD/MM/YYYY o DD/MM/YY
            parts = s.split("/")
            if len(parts) == 3:
                day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
                if year < 100:
                    year += 2000
                return date(year, month, day)
        return None
    except (ValueError, IndexError):
        return None


def load_activity_data() -> list[dict]:
    """Carga todos los registros de actividad desde la Bitácora"""
    gc = get_client()
    sheet = gc.open_by_key(SHEET_ID).worksheet(SHEET_BITACORA)
    rows = sheet.get_all_values()

    if not rows:
        return []

    data = []
    headers = rows[0]
    for row in rows[1:]:
        if len(row) < 1 or not row[0].strip():
            continue
        record = {
            "fecha_raw": row[0].strip() if len(row) > 0 else "",
            "hora": row[1].strip() if len(row) > 1 else "",
            "categoria": row[2].strip() if len(row) > 2 else "",
            "ejercicio": row[3].strip() if len(row) > 3 else "",
            "metrica1": _parse_float(row[4]) if len(row) > 4 else 0,
            "unidad1": row[5].strip() if len(row) > 5 else "",
            "metrica2": _parse_float(row[6]) if len(row) > 6 else 0,
            "unidad2": row[7].strip() if len(row) > 7 else "",
            "calorias": _parse_float(row[8]) if len(row) > 8 else 0,
            "notas": row[9].strip() if len(row) > 9 else "",
        }
        record["fecha"] = parse_date(record["fecha_raw"])
        data.append(record)

    return data


def load_weight_data() -> list[dict]:
    """Carga el historial de peso desde NutriFlow"""
    gc = get_client()
    sheet = gc.open_by_key(SHEET_ID_NUTRI).worksheet(SHEET_PESO)
    rows = sheet.get_all_values()

    if not rows:
        return []

    data = []
    for row in rows[1:]:
        if len(row) < 2 or not row[0].strip():
            continue
        record = {
            "fecha_raw": row[0].strip(),
            "peso_kg": _parse_float(row[1]),
            "notas": row[2].strip() if len(row) > 2 else "",
            "imc": _parse_float(row[3]) if len(row) > 3 else 0,
        }
        record["fecha"] = parse_date(record["fecha_raw"])
        if record["peso_kg"] > 0:
            data.append(record)

    return data
