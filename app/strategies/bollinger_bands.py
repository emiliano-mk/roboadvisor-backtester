import pandas as pd
from .strategy import Strategy

class BollingerBandsStrategy(Strategy):
    def __init__(self, window: int = 20, num_std: float = 2.0):
        super().__init__()
        self.window = window
        self.num_std = num_std

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        close = data["Close"]

        # Calcular la media móvil y la desviación estándar
        rolling_mean = close.rolling(window=self.window).mean()
        rolling_std = close.rolling(window=self.window).std()

        upper_band = rolling_mean + (self.num_std * rolling_std)
        lower_band = rolling_mean - (self.num_std * rolling_std)

        # Generar señales: 1 = compra, 0 = venta
        signals = pd.Series(index=data.index, dtype=float)
        signals[close < lower_band] = 1   # Compra
        signals[close > upper_band] = 0   # Venta
        signals = signals.ffill().fillna(0)

        return signals
