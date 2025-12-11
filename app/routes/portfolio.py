from flask import Blueprint, render_template
from app.data.portfolio import get_portfolio_summary

portfolio_bp = Blueprint("portfolio", __name__)

@portfolio_bp.route("/portfolio")
def portfolio_view():
    summary = get_portfolio_summary()
    return render_template("portfolio.html", summary=summary)


