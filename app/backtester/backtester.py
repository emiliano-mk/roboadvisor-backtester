import pandas as pd
import numpy as np
import plotly.graph_objs as go

class Backtester:
    def __init__(self, data: pd.DataFrame, strategy, initial_capital: float = 10000):
        """
        data: DataFrame con columna 'Close' como precios
        strategy: objeto que hereda de Strategy
        """
        self.data = data.copy()
        self.strategy = strategy
        self.initial_capital = initial_capital
        self.results = None

    def run_strategy(self) -> pd.Series:
        # Generar señales usando la estrategia
        signals = self.strategy.generate_signals(self.data).shift(1).fillna(0)

        returns = self.data["Close"].pct_change().fillna(0)

        portfolio = (1 + returns * signals).cumprod() * self.initial_capital
        
        self.results = pd.DataFrame({
            "Capital": portfolio,
            "Signals": signals,
            "Returns": returns
        })
        return self.results
    
    def calculate_metrics(self):
        if self.results is None:
            raise ValueError("Primero debes ejecutar run_strategy().")

        capital = self.results["Capital"]
        returns = self.results["Returns"]
        signals = self.results["Signals"]

        total_return = (capital.iloc[-1] / capital.iloc[0]) - 1
        n_days = len(returns)
        annualized_return = (1 + total_return) ** (252 / n_days) - 1

        sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(252) if returns.std() != 0 else 0

        rolling_max = capital.cummax()
        drawdown = (capital - rolling_max) / rolling_max
        max_drawdown = drawdown.min()

        # Win rate (solo días donde hubo posición activa)
        trade_returns = returns[signals == 1]
        win_rate = (trade_returns > 0).sum() / len(trade_returns) if len(trade_returns) > 0 else np.nan

        metrics = {
            "Total Return (%)": total_return * 100,
            "Annualized Return (%)": annualized_return * 100,
            "Sharpe Ratio": sharpe_ratio,
            "Max Drawdown (%)": max_drawdown * 100,
            "Win Rate (%)": win_rate * 100
        }

        return metrics

    def generate_plots(self):
        if self.results is None:
            raise ValueError("Primero debes ejecutar run_strategy().")

        df = self.results

        # -----------------------------
        # Función auxiliar para limpiar el fondo
        # -----------------------------
        def clean_bg(fig):
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',  
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color="white")
            )

            fig.update_xaxes(
                showgrid=True,
                gridcolor="rgba(255,255,255,0.15)",
                zerolinecolor="rgba(255,255,255,0.25)",
                color="white"
            )

            fig.update_yaxes(
                showgrid=True,
                gridcolor="rgba(255,255,255,0.15)",
                zerolinecolor="rgba(255,255,255,0.25)",
                color="white"
            )
            return fig

        # --- 1. Gráfica de capital ---
        fig_capital = go.Figure()
        fig_capital.add_trace(go.Scatter(
            x=df.index,
            y=df["Capital"],
            mode="lines",
            name="Capital"
        ))
        fig_capital.update_layout(title="Evolución del Capital")
        fig_capital = clean_bg(fig_capital)

        # --- 2. Gráfica de retornos ---
        fig_returns = go.Figure()
        fig_returns.add_trace(go.Scatter(
            x=df.index,
            y=df["Returns"],
            mode="lines",
            name="Returns"
        ))
        fig_returns.update_layout(title="Retornos Diarios")
        fig_returns = clean_bg(fig_returns)

        # --- 3. Señales ---
        fig_signals = go.Figure()
        fig_signals.add_trace(go.Scatter(
            x=self.data.index,
            y=self.data["Close"],
            mode="lines",
            name="Precio"
        ))

        buy_points = df[df["Signals"] == 1]
        sell_points = df[df["Signals"] == 0]

        fig_signals.add_trace(go.Scatter(
            x=buy_points.index,
            y=self.data.loc[buy_points.index]["Close"],
            mode="markers",
            marker=dict(color="lime", size=8),
            name="Compra"
        ))

        fig_signals.add_trace(go.Scatter(
            x=sell_points.index,
            y=self.data.loc[sell_points.index]["Close"],
            mode="markers",
            marker=dict(color="red", size=8),
            name="Venta"
        ))

        fig_signals.update_layout(title="Señales de Trading")
        fig_signals = clean_bg(fig_signals)

        return {
            "capital": fig_capital,
            "returns": fig_returns,
            "signals": fig_signals
        }