from flask import Blueprint, request, jsonify

from services.smart_investment_advisor_service import generate_investment_recommendation

smart_investment_advisor_bp = Blueprint('smart_investment_advisor', __name__)

@smart_investment_advisor_bp.route('/investment-recommendation', methods=['POST'])
def investment_recommendation():
    try:
        data = request.get_json()

        risk_profile, recommendations = generate_investment_recommendation(data)

        return jsonify({
            'risk_profile': risk_profile,
            'recommendations': recommendations
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
        }), 500