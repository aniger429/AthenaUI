import preprocessor as p
import pandas as pd
import re
import itertools
from controllers.DataCleaning import preprocessing
from functools import reduce
from DBModels.Username import *
import os

script_path = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(script_path, "stop_words")

stopwords = pd.read_csv(file_path+"/eng-function-word.txt", header=None)
stopwords = stopwords.append(pd.read_csv(file_path+"/fil-function-words.txt", header=None))
stopwords = stopwords[0].tolist()
stopwords = [x.lower() for x in stopwords]
stopwords = [re.sub('\'|"| ', '', x) for x in stopwords]

contractions = pd.read_csv(file_path+"/contractions.csv", header=None, delimiter=',')
dictionary = dict(zip(contractions[0].tolist(), contractions[1].tolist()))

c_re = re.compile('(%s)' % '|'.join(dictionary.keys()))

nameTuple = getAllUsernames()


def read_xlsx(filename):
    return pd.read_excel(filename, encoding='utf-8')


def expand_contractions(text, c_re=c_re):
    def replace(match):
        return dictionary[match.group(0)]
    return c_re.sub(replace, text)


def data_cleaning (tweet):
    # print ("Before:"+ tweet)
    # data anonymization
    tweet = reduce(lambda a, kv: a.replace(*kv), nameTuple, tweet)
    # removes URL, hashtags, and Reserved words
    p.set_options(p.OPT.URL, p.OPT.HASHTAG, p.OPT.RESERVED, p.OPT.EMOJI)
    tweet = p.clean(tweet)
    # remove HTML characters
    tweet = re.sub("(&\S+;)",'', tweet)
    # converts the tweets to lowercase
    tweet = tweet.lower()
    # expand contradictions
    tweet = expand_contractions(tweet)
    # remove stopwords
    tweet = ' '.join([word for word in tweet.split() if word not in stopwords])
    # remove shortwords 1-2 characters
    shortword = re.compile(r'\W*\b\w{1,2}\b')
    tweet = shortword.sub('', tweet)
    # remove punctuation marks
    tweet = re.sub("(!|#|\$|%|\^|&|\*|\(|\)|\?|\.|,|\"|'|\+|=|\||\/|-|_|:|;)", '', tweet)
    # standardize words # collapse to 1
    tweet = ''.join(ch for ch, _ in itertools.groupby(tweet))
    # standardize words # collapse to 2
    # tweet = re.sub(r'(.)\1+', r'\1\1', tweet)

    print("After:"+ tweet)

    return tweet


def write_csv(filename, cleanedTweets):
    # out = csv.writer(open("/home/dudegrim/Documents/"+filename, "w"), delimiter='\r')
    # out.writerow(cleanedTweets)
    cleanedTweets.to_excel(excel_writer="/home/dudegrim/Documents/"+filename, index=False, header=None, encoding="utf-8")


def cleaning_file(file_name):
    dataSource = read_xlsx(file_name)
    # add usernames to DB
    # preprocessing.processUsernames(dataSource)
    rawTweets = dataSource['Tweet'][:20]
    cleanedTweets = []
    [cleanedTweets.append(data_cleaning(t)) for t in rawTweets]
    d = {'Tweets': cleanedTweets, 'dateCreated':dataSource['Date Created'], 'idUsername':}
    df = pd.DataFrame(data=cleanedTweets, index=None)
    # writeCSV("CleanedTweets.xlsx",df)

    for x in df:
        print(x)

file_name = "/home/dudegrim/Google Drive/Thesis/Election Data/Election-18.xlsx"
cleaning_file(file_name)