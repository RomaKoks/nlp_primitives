import tensorflow as tf
import tensorflow_hub as hub
from featuretools.primitives import TransformPrimitive
from featuretools.variable_types import Numeric, Text


class UniversalSentenceEncoder(TransformPrimitive):
    """Transforms a sentence or short paragraph to a vector using [tfhub
    model](https://tfhub.dev/google/universal-sentence-encoder/2)

    Args:
        None

    Examples:
        >>> universal_sentence_encoder = UniversalSentenceEncoder()
        >>> sentences = ["I like to eat pizza",
        ...              "The roller coaster was built in 1885.",
        ...              ""]
        >>> output = universal_sentence_encoder(sentences)
        >>> len(output)
        512
        >>> len(output[0])
        3
        >>> values = output[:3, 0]
        >>> [round(x, 4) for x in values]
        [0.0178, 0.0616, -0.0089]
    """
    name = "universal_sentence_encoder"
    input_types = [Text]
    return_type = Numeric

    def __init__(self):
        self.handle = "https://tfhub.dev/google/universal-sentence-encoder/2"
        self.number_output_features = 512
        self.n = 512

    def install(self):
        with tf.Session():
            tf.global_variables_initializer().run()
            self.embed = hub.Module(self.handle)

    def get_function(self):
        self.install()

        def universal_sentence_encoder(col):
            with tf.Session() as session:
                session.run([tf.global_variables_initializer(),
                             tf.tables_initializer()])
                embeddings = session.run(self.embed(col.tolist()))
            return embeddings.transpose()
        return universal_sentence_encoder