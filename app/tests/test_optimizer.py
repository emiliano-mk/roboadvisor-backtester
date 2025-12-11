from app.data.data_loader import load_data
from app.strategies.moving_average import MovingAverageCrossover
from app.optimizer.parameter_optimizer import ParameterOptimizer

df = load_data("AAPL")  # tus datos
param_grid = {
    "short_window": [10, 20, 30],
    "long_window": [50, 100, 150]
}

optimizer = ParameterOptimizer(df, MovingAverageCrossover, param_grid, metric="Sharpe Ratio")
best_params, best_score = optimizer.optimize()

print(f"Mejores parámetros: {best_params}")
print(f"Mejor Sharpe ratio: {best_score:.2f}")
