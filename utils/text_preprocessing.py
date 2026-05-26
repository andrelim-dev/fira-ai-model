import nltk
nltk.download('punkt')
nltk.download('punkt_tab')

import re
import string
from nltk.tokenize import word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

slang_words = {
    'bye': 'sampai jumpa', 'trims': 'terima kasih', 'dadah': 'sampai jumpa', 'gimana': 'bagaimana', 'nambah': 'tambah', 'sip': 'oke',
    'thank': 'terima kasih', 'thanks': 'terima kasih', 'makasih': 'terima kasih', 'hello': 'hai', 'helo': 'hai', 'hi': 'hai', 'halo': 'hai',
    'bot': 'fira', 'chatbot': 'fira', 'kekmana': 'bagaimana',
}

stopwords = set(StopWordRemoverFactory().get_stop_words())
stemmer = StemmerFactory().create_stemmer()

def text_preprocessing(text):
    # Case folding
    text = text.lower()

    # Cleaning
    text = re.sub(r'@\w+', '', text) # Remove mentions
    text = re.sub(r'#\w+', '', text) # Remove hashtags
    text = re.sub(r'http\S+', '', text) # Remove URLs
    text = re.sub(r'\d+', '', text) # Remove numbers
    text = text.translate(str.maketrans('', '', string.punctuation)) # Remove punctuations
    text = text.replace('\n', ' ')
    text = text.strip()

    # Tokenization
    token = word_tokenize(text)

    token = [slang_words.get(word, word) for word in token]

    # Stopword removal
    additional_stopwords = [
        'sih',
    ]
    token = [word for word in token if word not in stopwords]
    token = [word for word in token if word not in additional_stopwords]

    # Stemming
    token = [stemmer.stem(word) for word in token]

    # Convert token list back to text
    text = ' '.join(token)

    return text