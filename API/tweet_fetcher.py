import twint
import pandas as pd
import re
from nltk.corpus import words
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer

stop_words = set(stopwords.words('english'))
setofwords = set(words.words())

file = "D:\\Project\\HMRS_3.0\\API\\data\\twitter.csv"


def sentiment_ana(senti_text):
    sc = SentimentIntensityAnalyzer().polarity_scores(senti_text)
    nega = sc['neg']
    post = sc['pos']
    return post, nega


def removemeaningless(text6):
    temo = []
    for i in text6.split(' '):
        if i in setofwords:
            temo.append(i)
    return " ".join(temo)


def remove_stopwords(text5):
    no_stopword_text = [w for w in text5.split() if not w in stop_words]
    return ' '.join(no_stopword_text)


def whitespacehandler(text4):
    text = ' '.join(text4.split())
    return text


def nonalphanumer(text3):
    text = re.sub('[^0-9a-zA-Z\s]+', '', text3)
    return text


def deLinker(text2):
    text = re.sub('http://\S+|https://\S+', '', text2)
    return text


def deEmojify(text1):
    regrex_pattern = re.compile(pattern="["
                                u"\U0001F600-\U0001F64F"  # emoticons
                                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                "]+", flags=re.UNICODE)
    return regrex_pattern.sub(r'', text1)


def fetch_tweet(userName):
    open(file, 'w').close()
    cleanedtweets = []
    c = twint.Config()
    c.Username = userName
    c.Limit = 300
    c.Store_csv = True
    c.Custom_csv = ["id", "user_id", "username", "tweet"]
    c.Output = file
    twint.run.Search(c)
    dataset = pd.read_csv(file)
    ftCol = dataset.iloc[:, 10].values

    for str in ftCol:
        cleanedtweets.append(remove_stopwords(
            whitespacehandler(nonalphanumer(deLinker(deEmojify(str))))))

    uncleaned_tweets = "".join(cleanedtweets)
    tweets = removemeaningless(uncleaned_tweets)
    emotion = sentiment_ana(tweets)

    result_dict = dict()
    result_dict["cleaned_tweet"] = tweets
    result_dict["emotion_range"] = list(emotion)

    return result_dict
