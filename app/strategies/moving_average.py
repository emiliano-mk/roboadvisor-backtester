from .strategy import Strategy
import pandas as pd


class MovingAverageCrossover(Strategy):
    
    def __init__(self, short_window: int = 20, long_window: int = 50):
        super().__init__()
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        short_ma = data["Close"].rolling(window=self.short_window).mean()
        long_ma = data["Close"].rolling(window=self.long_window).mean()

        # Señal: 1 cuando la media corta > media larga, 0 en caso contrario
        signals = (short_ma > long_ma).astype(int)
        return signals
