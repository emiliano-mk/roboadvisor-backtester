import pandas as pd
import matplotlib.pyplot as plt


def plot_price_history(ticker: str):
    """
    Carga los datos de un activo desde datasets/ y grafica su precio de cierre.
    """
    path = f"app/data/datasets/{ticker}.csv"
    
    try:
        df = pd.read_csv(path, index_col=0, skiprows=[1], parse_dates=True)
    except FileNotFoundError:
        print(f"❌ No se encontró el archivo {path}. Descarga primero los datos con data_loader.py.")
        return
    print(df.columns)
    print(df.head())
    print(df.index.name)
    # Graficamos la columna de cierre
    plt.figure(figsize=(10, 5))
    plt.plot(df["Close"], label=f"{ticker} - Precio de cierre")
    plt.title(f"Histórico de precios: {ticker}")
    plt.xlabel("Fecha")
    plt.ylabel("Precio ($)")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    ticker = input("Introduce el ticker (ej. AAPL, BTC-USD): ").upper()
    plot_price_history(ticker)
