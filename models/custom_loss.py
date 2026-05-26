import tensorflow as tf

@tf.keras.utils.register_keras_serializable()
class CustomSparseCategoricalCrossentropy(tf.keras.losses.Loss):
  def __init__(
      self,
      from_logits=False,
      ignore_class=None,
      reduction='sum_over_batch_size',
      name='custom_sparse_categorical_crossentropy'
  ):
    super().__init__(
        reduction=reduction,
        name=name,
    )
    self.from_logits = from_logits
    self.ignore_class = ignore_class

  def call(self, y_true, y_pred):
    # Hitung sparse categorical crossentropy per sample
    loss = tf.keras.losses.sparse_categorical_crossentropy(
        y_true,
        y_pred,
        from_logits=self.from_logits,
    )

    if self.ignore_class is not None:
      mask = tf.not_equal(y_true, self.ignore_class)
      mask = tf.cast(mask, loss.dtype)

      loss = loss * mask

      return tf.reduce_sum(loss) / tf.reduce_sum(mask)

    return tf.reduce_mean(loss)

  def get_config(self):
    config = super().get_config()

    config.update({
        'from_logits': self.from_logits,
        'ignore_class': self.ignore_class,
    })

    return config