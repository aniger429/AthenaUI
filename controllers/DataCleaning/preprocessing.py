import re
from collections import Counter
from Model.UsernameModel import *
from DBModels.Username import *
import pandas as pd


def findUsername(tweet):
    pattern = '@'

#this function returns a dictionary where the key is the username and the value is the username model class
def createInitUsernameList(usernameList):
    #All usernames from the column
    usernameDict = {}

    for u, value in dict(Counter(usernameList)).items():
        user = UsernameModel(username='@'+u, numTweets=value)
        usernameDict['@'+u] = user
    return usernameDict

def usernameMentions(usernameDict, newUsernameList):
    # All usernames from the tweets

    for nu, value in dict(Counter(newUsernameList)).items():
        if nu not in usernameDict:
            user = UsernameModel(username=nu, numMentions=value)
            usernameDict[nu] = user
        else:
            usernameDict[nu].numMentions = value
    return usernameDict


def addToDB(usernameList):
    insertNewUsername(usernameList)
    print("done inserting to table: username")

def filterOutUsernames(usernameList):
    return [username for username in usernameList if len(username) < 17]


def processUsernames(dataSource):
    # 1. Get all usernames from the username columns
    usernameDict = createInitUsernameList(dataSource['Username'])

    Tweets = dataSource['Tweet']
    # 3. Iterate over all Tweet column
    pattern = re.compile("@[a-zA-Z0-9_]+")
    foundUsernameList = []
    [foundUsernameList.extend(m) for l in Tweets for m in [pattern.findall(l)] if m]
    foundUsernameList = filterOutUsernames(foundUsernameList)
    usernameDict = usernameMentions(usernameDict, foundUsernameList)

    # addToDB(usernameDict)
    print("Done processing the username")


# def read_xlsx(filename):
#     return pd.read_excel(filename, encoding='utf-8')
#
#
# file_name = "/home/dudegrim/Google Drive/Thesis/Election Data/Election-18.xlsx"
# processUsernames(read_xlsx(file_name))
# usernameIDs = getAllUsernames()
# print (usernameIDs)

