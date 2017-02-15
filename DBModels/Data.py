import peewee
from peewee import *
import datetime

db = MySQLDatabase('Athena', user='root',passwd='')

class BaseModel(Model):
    class Meta:
        database = db

class Data(BaseModel):
    idData = peewee.PrimaryKeyField()
    filename = peewee.CharField(max_length=255,null = False)
    isClean = peewee.BooleanField(default=False,null = False)
    dateCreated = peewee.DateTimeField(default=datetime.datetime.now,null = False)
    tweetStartID = peewee.IntegerField(default=0, null=True)
    tweetEndID = peewee.IntegerField(default=0, null=True)

    class Meta:
        db_table = "Data"
        database = db

def insertNewData(filename):
    db.connect()
    Data.insert(filename=filename).execute()
    db.close()

def tweet_cleaned(filename):
    db.connect()
    Data.update(isClean=1).where(filename==filename).execute()
    db.close()


def getAllData():
    return Data.select()
