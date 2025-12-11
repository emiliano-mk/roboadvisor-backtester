import matplotlib.pyplot as plt
import pandas as pd

def plot_signals(data: pd.DataFrame, signals: pd.Series, title: str = "Trading Signals"):
    """
    Muestra el precio del activo junto con las señales de compra y venta.
    """

    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['Close'], label='Precio de cierre', color='blue', linewidth=1.5)

    # Señales de compra y venta
    buy_signals = data.loc[signals == 1]
    sell_signals = data.loc[signals == 0]

    plt.scatter(buy_signals.index, buy_signals['Close'], label='Compra', marker='^', color='green', s=100)
    plt.scatter(sell_signals.index, sell_signals['Close'], label='Venta', marker='v', color='red', s=100)

    plt.title(title)
    plt.xlabel('Fecha')
    plt.ylabel('Precio')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_equity_curve(data: pd.DataFrame, signals: pd.Series, title: str = "Evolución del Portafolio", initial_capital: float = 10000):
    """
    Muestra cómo evoluciona el valor del portafolio a lo largo del tiempo.
    """
    
    close = data['Close']
    
    # Calculamos los retornos diarios
    returns = close.pct_change().fillna(0)
    
    # Retorno de la estrategia = retorno diario * posición
    strategy_returns = signals * returns
    
    # Valor acumulado del portafolio
    equity = (1 + strategy_returns).cumprod() * initial_capital

    # --- Gráfica ---
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, close / close.iloc[0] * initial_capital, label='Activo subyacente', color='blue', alpha=0.6)
    plt.plot(data.index, equity, label='Estrategia', color='green', linewidth=2)

    plt.title(title)
    plt.xlabel('Fecha')
    plt.ylabel('Valor del portafolio ($)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
