import tensorflow as tf

@tf.keras.utils.register_keras_serializable()
class CustomDenseLayer(tf.keras.layers.Layer):
    def __init__(self, units=32, activation=None, **kwargs):
        super(CustomDenseLayer, self).__init__(**kwargs)
        self.units = units
        self.activation = (
            tf.keras.activations.get(activation)
        )

    def build(self, input_shape):
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

    def call(self, inputs):
        output = tf.matmul(inputs, self.w) + self.b

        if self.activation is not None:
            output = self.activation(output)

        return output

    def compute_output_shape(self, input_shape):
        return (
            *input_shape[:-1],
            self.units
        )

    def get_config(self):
        config = super(CustomDenseLayer, self).get_config()

        config.update({
            'units': self.units,
            'activation': tf.keras.activations.serialize(
                self.activation
            ),
        })

        return config