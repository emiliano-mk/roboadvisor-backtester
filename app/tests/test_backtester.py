import pandas as pd
from app.backtester.backtester import Backtester
from app.strategies.moving_average import MovingAverageCrossover
from app.strategies.breakout_strategy import BreakoutStrategy
from app.strategies.rsi_strategy import RSIStrategy
from app.strategies.bollinger_bands import BollingerBandsStrategy
from app.data.data_loader import load_data

# Cargar los datos directamente
data = load_data('MSFT', start_date='2023-01-01', end_date='2025-01-01')
print(data.head())
print(data.columns)

strategy = MovingAverageCrossover(short_window=20, long_window=50)
backtester = Backtester(data, strategy)
results = backtester.run_strategy()
metrics = backtester.calculate_metrics()

print(results.tail())
print("\n📊 Métricas de rendimiento:")
for k, v in metrics.items():
    print(f"{k}: {v:.2f}")

