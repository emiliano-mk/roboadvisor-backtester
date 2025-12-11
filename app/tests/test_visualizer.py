from app.visualizer.plotter import plot_signals, plot_equity_curve
from app.backtester.backtester import Backtester
from app.strategies.moving_average import MovingAverageCrossover
from app.data.data_loader import load_data

data = load_data("AAPL", "2024-01-01", "2024-12-31")
strategy = MovingAverageCrossover(short_window=20, long_window=50)

backtester = Backtester(data, strategy)
results = backtester.run_strategy()

plot_signals(data, results['Signals'], title="Señales de Medias Móviles (AAPL)")

plot_equity_curve(data, results['Signals'], title="Evolución del Portafolio - Medias Móviles")
