import itertools
import pandas as pd
from app.backtester.backtester import Backtester

class ParameterOptimizer:
    def __init__(self, data: pd.DataFrame, strategy_class, param_grid: dict, metric="sharpe"):
        self.data = data
        self.strategy_class = strategy_class
        self.param_grid = param_grid
        self.metric = metric

    def optimize(self):
        best_score = float("-inf")
        best_params = None

        # combinaciones posibles de parámetros
        for params in self._param_combinations():
            strategy = self.strategy_class(**params)
            backtester = Backtester(self.data, strategy)
            backtester.run_strategy()
            result = backtester.calculate_metrics()

            score = result[self.metric]
            if score > best_score:
                best_score = score
                best_params = params

        return best_params, best_score

    def _param_combinations(self):
        keys = self.param_grid.keys()
        values = self.param_grid.values()
        for combination in itertools.product(*values):
            yield dict(zip(keys, combination))
