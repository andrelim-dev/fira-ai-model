from flask import Blueprint, request, jsonify

from services.smart_spending_insight_service import predict_spending_category

smart_spending_insight_bp = Blueprint('smart_spending_insight', __name__)

@smart_spending_insight_bp.route('/spending-insight', methods=['POST'])
def spending_insight():
    try:
        data = request.get_json()

        monthly_income = data.get('monthly_income')
        monthly_expense = data.get('monthly_expense')

        if (monthly_income is None or monthly_expense is None):
            return jsonify({
                'error' : 'All fields are required',    
            }), 400

        predicted_label = predict_spending_category(monthly_income, monthly_expense)

        action_recommendation = ''

        if(predicted_label == 'Wasteful'):
            action_recommendation = 'Reduce unnecessary spending and focus on building a consistent saving habit before making high-risk financial decisions.'

        elif(predicted_label == 'Moderate'):
            action_recommendation = 'Maintain a balanced financial strategy by controlling expenses while gradually increasing savings and investments.'
        
        else:
            action_recommendation = 'Your financial discipline is strong. Consider optimizing your savings through long-term investments and diversified financial planning.'
        return jsonify({
            'category' : predicted_label,
            'Action Recommendation' : action_recommendation,
        })
    
    except Exception as e:
        
        return jsonify({
            "error": str(e)
        }), 500