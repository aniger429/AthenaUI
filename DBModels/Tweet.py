import peewee
from peewee import *


db = MySQLDatabase('Athena', user='root',passwd='')

class BaseModel(Model):
    class Meta:
        database = db

class Tweet (BaseModel):
    idTweets = peewee.PrimaryKeyField()
    tweet = peewee.CharField()
    dateCreated = peewee.DateField()
    idUsername = peewee.IntegerField()

    class Meta:
        db_table = "Tweeets"
        database = db

def insertNewUsername(tweets):
    db.connect()

    row_dicts = ({'username': key, 'numTweets': value.numTweets, 'numMentions': value.numMentions} for key, value in usernameDict.items())
    Username.insert_many(row_dicts).execute()
    db.close()


def getAllUsernames():
    return Tweet.select()
