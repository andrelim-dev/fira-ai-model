from flask import Blueprint, request, jsonify

from services.smart_investment_advisor_service import generate_investment_recommendation

smart_investment_advisor_bp = Blueprint('smart_investment_advisor', __name__)

@smart_investment_advisor_bp.route('/investment-recommendation', methods=['POST'])
def investment_recommendation():
    try:
        data = request.get_json()

        result = generate_investment_recommendation(data)

        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': str(e),
        }), 500