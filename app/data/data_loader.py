import os
import pandas as pd
import yfinance as yf
import time

# ============================
# CACHE GLOBAL DE DATA HISTÓRICA
# ============================
DATA_CACHE = {}
CACHE_TTL = 60 * 30   # 30 minutos


def _is_fresh(ts):
    return (time.time() - ts) < CACHE_TTL


def load_data(symbol: str, start_date=None, end_date=None):
    """
    Descarga datos históricos desde yfinance.
    Ahora incluye un cache por (symbol, start_date, end_date).
    """

    # ----------------------------
    # Crear clave única de caché
    # ----------------------------
    key = (symbol.upper(), str(start_date), str(end_date))

    # ----------------------------
    # Si está en caché y NO expiró
    # ----------------------------
    if key in DATA_CACHE and _is_fresh(DATA_CACHE[key]["timestamp"]):
        print(f"♻️ Usando datos cacheados para {symbol} ({start_date} → {end_date})")
        return DATA_CACHE[key]["data"].copy()

    # ----------------------------
    # Si no está en cache → descargar
    # ----------------------------
    print(f"🔍 Descargando datos para {symbol}...")
    data = yf.download(symbol, start=start_date, end=end_date, group_by='ticker')

    # Aplanar columnas en caso necesario
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(1)

    if "Close" not in data.columns:
        raise KeyError(f"❌ No se encontró la columna 'Close' en los datos descargados: {data.columns}")

    data.dropna(inplace=True)

    # Guardar en cache
    DATA_CACHE[key] = {
        "timestamp": time.time(),
        "data": data.copy()
    }

    print(f"✅ Datos cargados para {symbol}. Cache actualizado.")
    return data

