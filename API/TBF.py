import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
import re
from nltk.corpus import stopwords


clf = pickle.load(
    open('D:\\Project\\HMRS_3.0\\API\\data\\final_model.pickle', 'rb'))

multilabel_binarizer = pickle.load(
    open('D:\\Project\\HMRS_3.0\\API\\data\\multilabel.pickle', 'rb'))

tfidf_vectorizer = pickle.load(
    open('D:\\Project\\HMRS_3.0\\API\\data\\vectorizer.pickle', 'rb'))

# nltk.download('stopwords')

stop_words = set(stopwords.words('english'))


def clean_text(text):
    # remove backslash-apostrophe
    text = re.sub("\'", "", text)
    # remove everything except alphabets
    text = re.sub("[^a-zA-Z]", " ", text)
    # remove whitespaces
    text = ' '.join(text.split())
    # convert text to lowercase
    text = text.lower()

    return text


def remove_stopwords(text):
    no_stopword_text = [w for w in text.split() if not w in stop_words]
    return ' '.join(no_stopword_text)


def infer_tags(q):
    q = clean_text(q)
    print(q)
    q = remove_stopwords(q)
    q_vec = tfidf_vectorizer.transform([q])
    q_pred = clf.predict(q_vec)
    return multilabel_binarizer.inverse_transform(q_pred)


def fetch_genre(text):
    return infer_tags(text)
