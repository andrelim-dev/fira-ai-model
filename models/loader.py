import pickle
import tensorflow as tf

from models.custom_layer import CustomDenseLayer

smart_spending_insight_model = tf.keras.models.load_model(
    'model/smart_spending_insight/smart_spending_insight_dl_model.keras',
    custom_objects={
        'CustomDenseLayer': CustomDenseLayer
    }
)

with open('model/smart_spending_insight/scaler.pkl', 'rb') as file :
    scaler = pickle.load(file)

with open('model/smart_spending_insight/target_encoder.pkl', 'rb') as file:
    target_encoder = pickle.load(file)