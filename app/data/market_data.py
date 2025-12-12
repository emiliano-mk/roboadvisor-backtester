import yfinance as yf
import requests
import time

# Cache de 10 minutos por ticker
PRICE_CACHE = {}
CACHE_TTL = 600   # 10 minutos


def _is_fresh(timestamp):
    return (time.time() - timestamp) < CACHE_TTL


def get_price(ticker):
    """
    Devuelve el precio actual y cambio porcentual del ticker.
    Usa caché individual por símbolo.
    Formato:
    {
        "price": float,
        "change": float
    }
    """

    ticker = ticker.upper()

    # 1. Revisar cache
    if ticker in PRICE_CACHE and _is_fresh(PRICE_CACHE[ticker]["timestamp"]):
        return PRICE_CACHE[ticker]["data"]

    # 2. Si no está en cache o expiró → llamar a yfinance
    tk = yf.Ticker(ticker)
    info = tk.history(period="5d", interval="1d").dropna()

    if info.empty:
        return None

    price = info["Close"].iloc[-1]
    prev = info["Close"].iloc[-2] if len(info) > 1 else price
    change = ((price - prev) / prev) * 100 if prev != 0 else 0

    result = {
        "price": round(price, 2),
        "change": round(change, 2)
    }

    # 3. Guardar en cache
    PRICE_CACHE[ticker] = {
        "timestamp": time.time(),
        "data": result
    }

    return result


def get_multiple_prices(tickers):
    """
    Recibe una lista de tickers y regresa diccionario:
    {
        "AAPL": { "price": 123.4, "change": 0.45 }
        "TSLA": ...
    }
    """
    data = {}
    for t in tickers:
        info = get_price(t)
        if info:
            data[t] = info
    
    return data

FX_CACHE = {
    "timestamp": 0,
    "data": {}
}

def get_fx_rates(pairs):
    import time
    import requests

    # --- CACHE GLOBAL ---
    global FX_CACHE

    # Si hay datos cacheados y no han pasado 10min → devolver cache
    if time.time() - FX_CACHE["timestamp"] < 600:
        return FX_CACHE["data"]

    # Si no, llamar a la API
    rates = {}
    for base, quote in pairs:
        url = f"https://open.er-api.com/v6/latest/{base}"
        res = requests.get(url).json()

        if res.get("result") == "success":
            value = res["rates"].get(quote)
            rates[f"{base}/{quote}"] = round(value, 4) if value else "N/A"
        else:
            rates[f"{base}/{quote}"] = "N/A"

    # Guardar en cache
    FX_CACHE["timestamp"] = time.time()
    FX_CACHE["data"] = rates

    return rates
