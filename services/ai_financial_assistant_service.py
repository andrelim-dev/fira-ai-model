import numpy as np
import tensorflow as tf

from utils.text_preprocessing import text_preprocessing
from models.loader import ai_financial_assistant_model, label_encoder, tokenizer

def predict_intent(user_input):
    clean_user_input = text_preprocessing(user_input)

    sequence = tokenizer.texts_to_sequences([clean_user_input])

    padded_sequence = tf.keras.preprocessing.sequence.pad_sequences(sequence, maxlen=16, padding='post', truncating='post')

    prediction = ai_financial_assistant_model.predict(padded_sequence)

    predicted_index = np.argmax(prediction)

    confidence = prediction[0][predicted_index]

    predicted_intent = label_encoder.inverse_transform(
        [predicted_index]
    )[0]

    return clean_user_input, predicted_intent, confidence