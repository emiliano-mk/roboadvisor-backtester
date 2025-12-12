from app.models import Transaction
from app.data.market_data import get_multiple_prices


def get_portfolio_summary():
    """
    Procesa todas las transacciones y devuelve un resumen por ticker.
    Usa el cache de market_data.py para obtener precios actuales.
    """
    transactions = Transaction.query.all()

    if not transactions:
        return {}

    portfolio = {}
    tickers = set()

    # -------------------------------
    # Agrupar transacciones por ticker
    # -------------------------------
    for tx in transactions:
        t = tx.ticker.upper()
        tickers.add(t)

        if t not in portfolio:
            portfolio[t] = {
                "quantity": 0,
                "total_cost": 0,
                "avg_cost": 0,
                "current_price": None,
                "current_value": None,
                "profit_loss": None,
                "profit_loss_pct": None,
                "transactions": []
            }

        portfolio[t]["transactions"].append(tx)

        # Procesar compra
        if tx.tx_type.upper() == "BUY":
            portfolio[t]["quantity"] += tx.quantity
            portfolio[t]["total_cost"] += tx.quantity * tx.price

        # Procesar venta
        elif tx.tx_type.upper() == "SELL":
            # Restar cantidad
            portfolio[t]["quantity"] -= tx.quantity

            # Ajuste del costo utilizando el avg_cost actual
            if portfolio[t]["avg_cost"] > 0:
                portfolio[t]["total_cost"] -= tx.quantity * portfolio[t]["avg_cost"]

        # Evitar negativos
        if portfolio[t]["quantity"] < 0:
            portfolio[t]["quantity"] = 0

        # Recalcular costo promedio
        qty = portfolio[t]["quantity"]
        cost = portfolio[t]["total_cost"]
        portfolio[t]["avg_cost"] = round(cost / qty, 4) if qty > 0 else 0

    # -------------------------------
    # Obtener precios actuales usando UN solo cache
    # -------------------------------
    prices = get_multiple_prices(list(tickers))

    # -------------------------------
    # Completar métricas finales
    # -------------------------------
    for t in tickers:
        data = portfolio[t]
        qty = data["quantity"]

        if t not in prices:
            continue  # ticker inválido o sin datos

        price = prices[t]["price"]
        data["current_price"] = price
        data["current_value"] = round(qty * price, 2)

        invested = qty * data["avg_cost"]
        pl = data["current_value"] - invested

        data["profit_loss"] = round(pl, 2)
        data["profit_loss_pct"] = round((pl / invested) * 100, 2) if invested > 0 else 0

    return portfolio

