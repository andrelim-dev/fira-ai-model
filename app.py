import os
import json
import requests
import tensorflow as tf
import pickle
import numpy as np
from data.stocks import stocks
from dotenv import load_dotenv
from flask import Flask, request, jsonify

load_dotenv()

app = Flask(__name__)

API_URL = os.getenv('HF_API_URL')

HEADERS = {
    'Authorization': f'Bearer {os.getenv("HF_TOKEN")}',
}

@tf.keras.utils.register_keras_serializable()
class CustomDenseLayer(
    tf.keras.layers.Layer
):

    def __init__(
        self,
        units=32,
        activation=None,
        **kwargs
    ):

        super(
            CustomDenseLayer,
            self
        ).__init__(**kwargs)

        self.units = units

        self.activation = (
            tf.keras.activations.get(
                activation
            )
        )

    def build(
        self,
        input_shape
    ):

        self.w = self.add_weight(
            name='kernel',
            shape=(
                input_shape[-1],
                self.units
            ),
            initializer='glorot_uniform',
            trainable=True,
        )

        self.b = self.add_weight(
            name='bias',
            shape=(self.units,),
            initializer='zeros',
            trainable=True,
        )

    def call(
        self,
        inputs
    ):

        output = (
            tf.matmul(
                inputs,
                self.w
            )
            + self.b
        )

        if self.activation is not None:

            output = self.activation(
                output
            )

        return output

    def compute_output_shape(
        self,
        input_shape
    ):

        return (
            *input_shape[:-1],
            self.units
        )

    def get_config(self):

        config = super(
            CustomDenseLayer,
            self
        ).get_config()

        config.update({

            'units': self.units,

            'activation':
            tf.keras.activations.serialize(
                self.activation
            ),
        })

        return config

model = tf.keras.models.load_model(
    'model/smart_spending_insight/smart_spending_insight_dl_model.keras',
    custom_objects={
        'CustomDenseLayer': CustomDenseLayer
    }
)

with open('model/smart_spending_insight/scaler.pkl', 'rb') as file :
    scaler = pickle.load(file)

with open('model/smart_spending_insight/target_encoder.pkl', 'rb') as file:
    target_encoder = pickle.load(file)

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

        return jsonify({
            'risk_profile': risk_profile,
            'recommendations': recommendations
        })
    
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

@app.route('/predict', methods = ['POST'])
def predict():
    try:
        data = request.get_json()

        monthly_income = data.get('monthly_income')
        monthly_expense = data.get('monthly_expense')

        required_field = [monthly_income, monthly_expense]

        if any(v is None for v in required_field):
            return jsonify({
                'error' : 'All Field are Required',    
            }), 400

        monthly_income_usd = monthly_income / 17698.60
        monthly_expense_usd = monthly_expense /  17698.60
        action_recommendation = ''
        expense_ratio = monthly_expense_usd / monthly_income_usd
        input_data = np.array([[monthly_income_usd, monthly_expense_usd, expense_ratio]])
        print(input_data)
        print(scaler)

        scaler_data = scaler.transform(input_data)
        print(scaler_data)

        prediction = model.predict(scaler_data)

        predicted_index = np.argmax(prediction, axis = 1)
        print(type(predicted_index))

        predicted_label = target_encoder.inverse_transform(
            [predicted_index]
        )[0]
        print(type(predicted_label))

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

if __name__ == '__main__':
    app.run(debug=True)