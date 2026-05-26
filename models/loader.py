import pickle
import tensorflow as tf

from models.custom_layer import CustomDenseLayer
from models.custom_loss import CustomSparseCategoricalCrossentropy

smart_spending_insight_model = tf.keras.models.load_model(
    'model/smart_spending_insight/smart_spending_insight_dl_model.keras',
    custom_objects={
        'CustomDenseLayer': CustomDenseLayer,
        'CustomSparseCategoricalCrossentropy': CustomSparseCategoricalCrossentropy
    }
)

with open('model/smart_spending_insight/scaler.pkl', 'rb') as file :
    scaler = pickle.load(file)

with open('model/smart_spending_insight/target_encoder.pkl', 'rb') as file:
    target_encoder = pickle.load(file)

ai_financial_assistant_model = tf.keras.models.load_model(
    'model/ai_financial_assistant/ai_financial_assistant_model.keras',
    custom_objects={
        'CustomDenseLayer': CustomDenseLayer,
        'CustomSparseCategoricalCrossentropy': CustomSparseCategoricalCrossentropy
    }
)

with open('model/ai_financial_assistant/label_encoder.pkl', 'rb') as file:
    label_encoder = pickle.load(file)

with open('model/ai_financial_assistant/tokenizer.pkl', 'rb') as file:
    tokenizer = pickle.load(file)