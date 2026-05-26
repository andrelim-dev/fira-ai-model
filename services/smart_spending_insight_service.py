import numpy as np

from models.loader import smart_spending_insight_model, scaler, target_encoder

USD_RATE = 17698.60

def predict_spending_category(monthly_income, monthly_expense):
    monthly_income_usd = monthly_income / USD_RATE
    monthly_expense_usd = monthly_expense /  USD_RATE
    expense_ratio = monthly_expense_usd / monthly_income_usd

    input_data = np.array([[monthly_income_usd, monthly_expense_usd, expense_ratio]])

    scaler_data = scaler.transform(input_data)

    prediction = smart_spending_insight_model.predict(scaler_data)

    predicted_index = np.argmax(prediction, axis = 1)

    predicted_label = target_encoder.inverse_transform(
        [predicted_index]
    )[0]

    return predicted_label