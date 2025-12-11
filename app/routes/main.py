from flask import Blueprint, render_template, request
from app.backtester.backtester import Backtester
from app.strategies.moving_average import MovingAverageCrossover
from app.strategies.rsi_strategy import RSIStrategy
from app.strategies.breakout_strategy import BreakoutStrategy
from app.strategies.bollinger_bands import BollingerBandsStrategy
from app.data.data_loader import load_data
from app.data.market_data import get_multiple_prices, get_fx_rates

main = Blueprint('main', __name__)

# Diccionario para mapear nombres de estrategia a clases
STRATEGIES = {
    "moving_average": MovingAverageCrossover,
    "rsi": RSIStrategy,
    "breakout": BreakoutStrategy,
    "bollinger": BollingerBandsStrategy
}


@main.route("/")
def dashboard():
    stocks = ["AAPL", "MSFT", "TSLA"]
    stock_data = get_multiple_prices(stocks)

    cryptos = ["BTC-USD", "ETH-USD"]
    crypto_data = get_multiple_prices(cryptos)

    fx_pairs = [("USD", "MXN"), ("EUR", "MXN"), ("CNY", "MXN")]
    fx_data = get_fx_rates(fx_pairs)

    return render_template(
        "dashboard.html",
        stocks=stock_data,
        cryptos=crypto_data,
        fx=fx_data
    )


@main.route('/backtest', methods=['GET', 'POST'])
def backtest():
    results = None
    plots = None
    
    if request.method == 'POST':
        strategy_name = request.form.get('strategy')
        ticker = request.form.get('ticker', 'AAPL')  # por defecto AAPL
        strategy_class = STRATEGIES[strategy_name]

        # Cargamos los datos
        data = load_data(ticker, start_date='2023-01-01', end_date='2025-01-01')

        # Inicializamos la estrategia
        strategy = strategy_class()

        # Ejecutamos el backtest
        backtester = Backtester(data, strategy)
        backtester.run_strategy()
        metrics = backtester.calculate_metrics()
        plots_raw = backtester.generate_plots()
        plots = {
            name: fig.to_html(include_plotlyjs='cdn', full_html=False)
            for name, fig in plots_raw.items()
        }

        results = {
            "ticker": ticker,
            "strategy": strategy_name,
            "metrics": metrics
        }

    return render_template('backtest.html', results=results, strategies=STRATEGIES.keys(), plots=plots)
