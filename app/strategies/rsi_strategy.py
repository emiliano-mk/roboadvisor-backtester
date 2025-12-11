import pandas as pd
from .strategy import Strategy

class RSIStrategy(Strategy):
    """Estrategia basada en el indicador RSI."""

    def __init__(self, period: int = 14):
        super().__init__()
        self.period = period

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        delta = data["Close"].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(self.period).mean()
        avg_loss = loss.rolling(self.period).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        signals = pd.Series(index=data.index, dtype=float)
        signals[rsi < 30] = 1   # Comprar
        signals[rsi > 70] = 0   # Vender
        signals = signals.ffill().fillna(0)

        return signals
