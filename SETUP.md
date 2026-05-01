# Configuración de NexIA Dashboard

## Google Service Account (Lectura de Spreadsheets)

El dashboard usa una Service Account de Google Cloud para leer datos de los Spreadsheets.

### Configuración Local

1. Descarga el JSON de credenciales de la Service Account desde Google Cloud Console
2. Copia el archivo como `service_account.json` en la raíz del proyecto (está en .gitignore)
3. Crea `.streamlit/secrets.toml` con:

```toml
[google_credentials]
type = "service_account"
project_id = "nexia-dashboard"
private_key_id = "..."
private_key = """
-----BEGIN PRIVATE KEY-----
...
-----END PRIVATE KEY-----
"""
client_email = "nexia-reader@nexia-dashboard.iam.gserviceaccount.com"
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "..."
universe_domain = "googleapis.com"
```

### En Streamlit Cloud

En los Settings del dashboard, en Secrets, pega:

```toml
[google_credentials]
type = "service_account"
project_id = "nexia-dashboard"
private_key_id = "..."
private_key = """
-----BEGIN PRIVATE KEY-----
...
-----END PRIVATE KEY-----
"""
client_email = "nexia-reader@nexia-dashboard.iam.gserviceaccount.com"
...
```

## Spreadsheets Accesibles

- **NutriFlow:** Registro de Alimentación
- **Body Lab:** Registro de Actividad Física
- **Hábitos:** Registro de Hábitos
