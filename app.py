from flask import Flask

from routes.smart_spending_insight_routes import smart_spending_insight_bp
from routes.ai_financial_assistant_routes import ai_financial_assistant_bp
from routes.smart_investment_advisor_routes import smart_investment_advisor_bp

app = Flask(__name__)

app.register_blueprint(smart_spending_insight_bp)
app.register_blueprint(ai_financial_assistant_bp)
app.register_blueprint(smart_investment_advisor_bp)

if __name__ == '__main__':
    app.run(debug=True)