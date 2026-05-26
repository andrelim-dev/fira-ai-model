import json

from data.stocks import stocks
from services.hf_service import call_hf_api
from utils.risk_profile import determine_risk_profile

def generate_investment_recommendation(data):
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

        Rules for Reasoning:
        - Each stock MUST have a completely different reasoning approach
        - Do NOT reuse sentence patterns
        - Do NOT repeat phrases like "high-risk high-growth"
        - Each reason must focus on different financial logic
        - Do NOT mention about user's profile (like investment goal, preferred sectors, investment experience, and risk profile) in the reasoning, focus on financial logic instead

        Return ONLY valid JSON.

        Rules for Response Format:
        - Do not include markdown
        - Do not include explanation outside JSON
        - Use double quotes only
        - Return valid JSON array
        - Do not write ```json

        Response Format (Must Follow This Format Exactly):
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
        'max_tokens': 400,
        'temperature': 0.3,
    }

    result = call_hf_api(payload)

    generated_text = result['choices'][0]['message']['content']

    # Find JSON array
    json_start = generated_text.find('[')
    json_end = generated_text.rfind(']') + 1

    clean_json = generated_text[json_start:json_end]

    recommendations = json.loads(clean_json)

    return {
        'risk_profile': risk_profile,
        'recommendations': recommendations
    }