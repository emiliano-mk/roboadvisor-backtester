import pandas as pd
from .strategy import Strategy

class BreakoutStrategy(Strategy):
    """Estrategia de ruptura de rango."""

    def __init__(self, window: int = 20):
        super().__init__()
        self.window = window

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        rolling_max = data["Close"].rolling(self.window).max()
        rolling_min = data["Close"].rolling(self.window).min()

        signals = pd.Series(index=data.index, dtype=float)
        signals[data["Close"] > rolling_max.shift(1)] = 1   # Comprar
        signals[data["Close"] < rolling_min.shift(1)] = 0   # Vender
        signals = signals.ffill().fillna(0)

        return signals
