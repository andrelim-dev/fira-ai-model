from flask import Blueprint, request, jsonify

from data.keyword_mapping import keyword_mapping
from data.response_mapping import response_mapping
from services.ai_financial_assistant_service import predict_intent

ai_financial_assistant_bp = Blueprint('ai_financial_assistant', __name__)

@ai_financial_assistant_bp.route('/financial-assistant', methods=['POST'])
def financial_assistant():
    try:
        data = request.get_json()

        clean_user_input, predicted_intent, confidence = predict_intent(data['user_input'])

        if confidence < 0.5:
            response = 'Maaf, saya belum memahami pertanyaan Anda.'

        keyword = None
        for key, values in keyword_mapping.items():
            for value in values:
                if value in clean_user_input:
                    keyword = key
        
        if keyword == None:
            response = response_mapping.get(predicted_intent, 'Maaf, respon tidak tersedia.')
        else:
            response = response_mapping.get(predicted_intent, 'Maaf, respon tidak tersedia.')
            
            if not isinstance(response, str):
                response = response.get(keyword, 'Maaf, respon tidak tersedia.')

        return jsonify({
            'response': response,
            'confidence': float(confidence)
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
        }), 500