import os
import json
import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify

load_dotenv()

app = Flask(__name__)

API_URL = os.getenv('HF_API_URL')

HEADERS = {
    'Authorization': f'Bearer {os.getenv("HF_TOKEN")}',
}

stocks = [
    {
        'stock_code': 'BBCA',
        'sector': 'Banking',
        'risk_level': 'Low',
        'potential': 'Stable Growth'
    },
    {
        'stock_code': 'BBRI',
        'sector': 'Banking',
        'risk_level': 'Medium',
        'potential': 'Dividend Growth'
    },
    {
        'stock_code': 'BMRI',
        'sector': 'Banking',
        'risk_level': 'Medium',
        'potential': 'Stable Growth'
    },
    {
        'stock_code': 'BBNI',
        'sector': 'Banking',
        'risk_level': 'Medium',
        'potential': 'Turnaround Growth'
    },
    {
        'stock_code': 'BNGA',
        'sector': 'Banking',
        'risk_level': 'Medium',
        'potential': 'Dividend Stability'
    },

    {
        'stock_code': 'GOTO',
        'sector': 'Technology',
        'risk_level': 'High',
        'potential': 'High Growth'
    },
    {
        'stock_code': 'BUKA',
        'sector': 'Technology',
        'risk_level': 'High',
        'potential': 'Speculative Growth'
    },
    {
        'stock_code': 'DCII',
        'sector': 'Technology',
        'risk_level': 'High',
        'potential': 'Explosive Growth'
    },
    {
        'stock_code': 'MCAS',
        'sector': 'Technology',
        'risk_level': 'Medium',
        'potential': 'Digital Expansion'
    },
    {
        'stock_code': 'MLPT',
        'sector': 'Technology',
        'risk_level': 'Medium',
        'potential': 'Enterprise Growth'
    },

    {
        'stock_code': 'KLBF',
        'sector': 'Healthcare',
        'risk_level': 'Low',
        'potential': 'Long-Term Growth'
    },
    {
        'stock_code': 'SIDO',
        'sector': 'Healthcare',
        'risk_level': 'Low',
        'potential': 'Stable Dividend'
    },
    {
        'stock_code': 'HEAL',
        'sector': 'Healthcare',
        'risk_level': 'Medium',
        'potential': 'Healthcare Expansion'
    },
    {
        'stock_code': 'SILO',
        'sector': 'Healthcare',
        'risk_level': 'Medium',
        'potential': 'Premium Healthcare Growth'
    },
    {
        'stock_code': 'MIKA',
        'sector': 'Healthcare',
        'risk_level': 'Medium',
        'potential': 'Stable Expansion'
    },

    {
        'stock_code': 'ADRO',
        'sector': 'Energy',
        'risk_level': 'Medium',
        'potential': 'Dividend Growth'
    },
    {
        'stock_code': 'PTBA',
        'sector': 'Energy',
        'risk_level': 'Medium',
        'potential': 'Commodity Stability'
    },
    {
        'stock_code': 'ITMG',
        'sector': 'Energy',
        'risk_level': 'Medium',
        'potential': 'Dividend Stability'
    },
    {
        'stock_code': 'MEDC',
        'sector': 'Energy',
        'risk_level': 'High',
        'potential': 'Commodity Upside'
    },
    {
        'stock_code': 'PGAS',
        'sector': 'Energy',
        'risk_level': 'Medium',
        'potential': 'Energy Recovery'
    },

    {
        'stock_code': 'UNVR',
        'sector': 'Consumer Goods',
        'risk_level': 'Low',
        'potential': 'Stable Dividend'
    },
    {
        'stock_code': 'ICBP',
        'sector': 'Consumer Goods',
        'risk_level': 'Low',
        'potential': 'Defensive Growth'
    },
    {
        'stock_code': 'INDF',
        'sector': 'Consumer Goods',
        'risk_level': 'Low',
        'potential': 'Stable Growth'
    },
    {
        'stock_code': 'MYOR',
        'sector': 'Consumer Goods',
        'risk_level': 'Medium',
        'potential': 'Export Growth'
    },
    {
        'stock_code': 'ROTI',
        'sector': 'Consumer Goods',
        'risk_level': 'Medium',
        'potential': 'Consumption Growth'
    },

    {
        'stock_code': 'BSDE',
        'sector': 'Property',
        'risk_level': 'Medium',
        'potential': 'Property Recovery'
    },
    {
        'stock_code': 'PWON',
        'sector': 'Property',
        'risk_level': 'Medium',
        'potential': 'Mall Recovery'
    },
    {
        'stock_code': 'CTRA',
        'sector': 'Property',
        'risk_level': 'Medium',
        'potential': 'Residential Growth'
    },
    {
        'stock_code': 'SMRA',
        'sector': 'Property',
        'risk_level': 'Medium',
        'potential': 'Urban Expansion'
    },
    {
        'stock_code': 'DMAS',
        'sector': 'Property',
        'risk_level': 'Low',
        'potential': 'Industrial Estate Growth'
    },

    {
        'stock_code': 'TLKM',
        'sector': 'Telecommunication',
        'risk_level': 'Low',
        'potential': 'Stable Growth'
    },
    {
        'stock_code': 'ISAT',
        'sector': 'Telecommunication',
        'risk_level': 'Medium',
        'potential': 'High Growth'
    },
    {
        'stock_code': 'EXCL',
        'sector': 'Telecommunication',
        'risk_level': 'Medium',
        'potential': 'Subscriber Growth'
    },
    {
        'stock_code': 'MTEL',
        'sector': 'Telecommunication',
        'risk_level': 'Low',
        'potential': 'Infrastructure Expansion'
    },
    {
        'stock_code': 'TOWR',
        'sector': 'Telecommunication',
        'risk_level': 'Low',
        'potential': 'Recurring Revenue Growth'
    },

    {
        'stock_code': 'ASII',
        'sector': 'Industrial',
        'risk_level': 'Low',
        'potential': 'Diversified Stability'
    },
    {
        'stock_code': 'UNTR',
        'sector': 'Industrial',
        'risk_level': 'Medium',
        'potential': 'Heavy Equipment Growth'
    },
    {
        'stock_code': 'AUTO',
        'sector': 'Industrial',
        'risk_level': 'Medium',
        'potential': 'EV Component Growth'
    },
    {
        'stock_code': 'SMSM',
        'sector': 'Industrial',
        'risk_level': 'Medium',
        'potential': 'Automotive Export Growth'
    },
    {
        'stock_code': 'IMPC',
        'sector': 'Industrial',
        'risk_level': 'Medium',
        'potential': 'Infrastructure Demand Growth'
    }
]

def determine_risk_profile(monthly_income, monthly_expense, investment_goal, investment_budget, investment_experience):
    # Count savings ratio
    savings = monthly_income - monthly_expense
    savings_ratio = savings / monthly_income

    score = 0

    # Savings ratio
    if savings_ratio < 0.2:
        score += 1
    elif savings_ratio < 0.5:
        score += 2
    else:
        score += 3
    
    # Investment goal
    if investment_goal == 'Capital Preservation':
        score += 1
    elif investment_goal == 'Long-Term Growth':
        score += 2
    elif investment_goal == 'Aggressive Growth':
        score += 3
    
    # Investment budget
    if investment_budget < 1000000:
        score += 1
    elif investment_budget < 5000000:
        score += 2
    else:
        score += 3
    
    # Investment experience
    if investment_experience == 'Beginner':
        score += 1
    elif investment_experience == 'Intermediate':
        score += 2
    elif investment_experience == 'Expert':
        score += 3

    # Determine risk profile
    if score <= 5:
        return 'Conservative'
    elif score <= 8:
        return 'Moderate'
    else:
        return 'Aggressive'

@app.route('/investment-recommendation', methods=['POST'])
def investment_recommendation():
    try:
        data = request.get_json()

        monthly_income = data.get('monthly_income')
        monthly_expense = data.get('monthly_expense')
        investment_goal = data.get('investment_goal')
        investment_budget = data.get('investment_budget')
        preferred_sectors = data.get('preferred_sectors')
        investment_experience = data.get('investment_experience')

        risk_profile = determine_risk_profile(monthly_income, monthly_expense, investment_goal, investment_budget, investment_experience)

        filtered_stocks = [stock for stock in stocks if stock['sector'] in data['preferred_sectors']]

        prompt = f"""
            You are a professional financial advisor. Based on the following user profile, recommend exactly 4 investment recommendations for the user.

            User Profile:
            - Monthly Income: {monthly_income}
            - Monthly Expense: {monthly_expense}
            - Investment Goal: {investment_goal}
            - Investment Budget: Rp{investment_budget}
            - Preferred Sectors: {', '.join(preferred_sectors)}
            - Investment Experience: {investment_experience}
            - Risk Profile: {risk_profile}

            Candidate Stocks: {json.dumps(filtered_stocks)}

            Return ONLY valid JSON.

            Rules:
            - Do not include markdown
            - Do not include explanation outside JSON
            - Use double quotes only
            - Return valid JSON array
            - Do not write ```json

            Response Format:
            [
                {{
                    "stock_code": "",
                    "sector": "",
                    "risk_level": "",
                    "potential": "",
                    "reason": "",
                }}
            ]
        """

        payload = {
            'messages': [
                {
                    'role': 'user',
                    'content': prompt,
                }
            ],
            'model': 'Qwen/Qwen2.5-3B-Instruct:featherless-ai',
            'max_tokens': 300,
            'temperature': 0.3,
        }

        print(API_URL)

        response = requests.post(API_URL, headers=HEADERS, json=payload)

        # Check status code
        if response.status_code != 200:
            return jsonify({
                'error': 'Failed to get response from AI model',
                'status_code': response.status_code,
                'details': response.text,
            }), response.status_code

        result = response.json()

        # Handle Hugging Face error
        if isinstance(result, dict) and result.get('error'):
            return jsonify({
                'error': 'Model API error',
                'details': result.get('error'),
            }), 500
        
        generated_text = result['choices'][0]['message']['content']

        # Find JSON array
        json_start = generated_text.find('[')
        json_end = generated_text.rfind(']') + 1

        clean_json = generated_text[json_start:json_end]

        recommendations = json.loads(clean_json)

        return jsonify(recommendations)
    
    except requests.exceptions.Timeout:
        return jsonify({
            'error': 'Request to AI model timed out',
        }), 504
    
    except requests.exceptions.RequestException as e:
        return jsonify({
            'error': 'Failed to connect to AI model',
            'details': str(e),
        }), 500
    
    except Exception as e:
        return jsonify({
            'error': 'An unexpected error occurred',
            'details': str(e),
        }), 500

if __name__ == '__main__':
    app.run(debug=True)