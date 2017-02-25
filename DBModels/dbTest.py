from flask import Flask
from flask_mongoalchemy import MongoAlchemy
app = Flask(__name__)
app.config['MONGOALCHEMY_DATABASE'] = 'Athena'
db = MongoAlchemy(app)

class Tweets(db.Document):
    name = db.StringField()

class Book(db.Document):
    title = db.StringField()
    author = db.DocumentField(Author)
    year = db.IntField()


mark_pilgrim = Author(name='Mark Pilgrim')
dive = Book(title='Dive Into Python', author=mark_pilgrim, year=2004)
mark_pilgrim.save()
dive.save()