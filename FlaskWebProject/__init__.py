from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort, jsonify

from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

from clarifai.client import ClarifaiApi
import os
import tempfile
import base64
import random, string
import time
import tempfile


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///carrots.db'
app.config['DEBUG'] = True
db = SQLAlchemy(app)

class Food(db.Model):
    __tablename__ = 'food'
    id = db.Column('food_id', db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    protein = db.Column(db.Float)
    carbs = db.Column(db.Float)
    fat = db.Column(db.Float)
    calcium = db.Column(db.Float)
    vitaminA = db.Column(db.Float)
    vitaminB = db.Column(db.Float)
    vitaminC = db.Column(db.Float)
    vitaminK = db.Column(db.Float)
    healthy = db.Column(db.Boolean)
    calories=db.Column(db.Float)
    unit = db.Column(db.String(60))

    def __init__(self, name, protein, carbs, fat, calcium,
        vitaminA, vitaminB, vitaminC, vitaminK, healthy, calories, unit):
        self.name     = name
        self.protein  = protein
        self.carbs    = carbs
        self.fat      = fat
        self.calcium  = calcium
        self.vitaminA = vitaminA
        self.vitaminB = vitaminB
        self.vitaminC = vitaminC
        self.vitaminK = vitaminK
        self.healthy  = healthy
        self.calories = calories
        self.unit     = unit

class API(db.Model):
    __tablename__ = 'api'
    id = db.Column('api_id', db.Integer, primary_key=True)
    date = db.Column(db.Integer)
    food = db.Column(db.String) #ForeignKey("food.name"))
    quantity = db.Column(db.Integer)
    url = db.Column(db.String)

    def __init__(self, date, food, quantity, url):
        self.date=date
        self.food=food
        self.quantity=quantity
        self.url=url


@app.route('/')
def show_all():
    return render_template('show_all.html',
        food=Food.query.order_by(Food.id.desc()).all()
    )

@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['title']:
            flash('Title is required', 'error')
        elif not request.form['text']:
            flash('Text is required', 'error')
        else:
            todo = Todo(request.form['title'], request.form['text'])
            db.session.add(todo)
            db.session.commit()
            flash(u'Todo item was successfully created')
            return redirect(url_for('show_all'))
    return render_template('new.html')


@app.route('/update', methods=['POST'])
def update_done():
    for todo in Todo.query.all():
        todo.done = ('done.%d' % todo.id) in request.form
    flash('Updated status')
    db.session.commit()
    return redirect(url_for('show_all'))


@app.route('/get_suggestions', methods=['POST'])
def getSuggestions():

    image = request.get_json(silent=False, force=True)
    print image
    print "image"
    base_id = image['base_id']
    dest = tempfile.gettempdir() +"/" + randomword(14) + ".png"

    image_64_decode = base64.decodestring(base_id) 
    with open(dest, 'wb') as f:
        f.write(image_64_decode)
    print "decoded"
    #clarifai_api = ClarifaiApi() # aidlessumes environment variables are set.
    clarifai_api = ClarifaiApi("Sa3eWiFzsFVygnleCNQAPvJacvIVAvkBBbN5cxmY", "qIf-5HaEzO225zuUaj5FTREU7iYAJLHU5_XrpHH_")
    result = clarifai_api.tag_images(open(dest, 'rb'))

    print "api call"
    
    parsed = result['results'][0]['result']['tag']['classes']
    answer = []
    a = db.session.query(Food.name).filter(Food.name.contains(val)).first()
    
    if (a is not None):
        print 'success'
        answer.append(val)
    
    return jsonify(suggestions=answer, url=dest)

@app.route('/confirmFood', methods=['POST'])
def confirmFood():
    #initialize values
    healthy=False
    protein, carbs, fat, calcium, calories, vitaminA, vitaminB, vitaminC, vitaminK = (0 for i in range(9))

    content = request.get_json(silent=False, force=True)
    print content
    rn = time.localtime()
    day = time.strftime('%d',rn) * 10000 + time.strftime('%m',rn)*100 + time.strftime('%y', rn)

    #iterate through list in json and accumulate nutrition values
    for food,amt in content['content']:
        values = db.session.query(Food.protein, Food.carbs, Food.fat,
        Food.calcium, Food.vitaminA, Food.vitaminB,Food.vitaminB,Food.vitaminK,
        Food.calories, Food.healthy).filter_by(name = food).first()
        print values

        protein += values[0]*amt
        carbs += values[1]*amt
        fat += values[2]*amt
        calcium += values[3]
        vitaminA += values[4]
        vitaminB += values[5]
        vitaminC += values[6]
        vitaminK += values[7]
        calories += values[8]*amt
        healthy  =  values[9] or healthy

        db.session.add(API(day, food, amt, content['url']))
    #add vitamins
    vitaminList=[]

    for ind,vit,amt in [(4,"A",5),(5, "B",4),(6, "C",2),(7, "K",0.5)]:
        if (values[ind] > amt):
            vitaminList.append(vit)

    return jsonify({"food":{"protein":protein,"carbs":carbs, "fat":fat,
        "calcium":calcium, "calories":calories},"vitamins":vitaminList, "healthy":healthy,
    "url":content['url']})

@app.route('/getDay/<int:day>', methods = ['GET'])
def getDay(day):
    protein, carbs, fat, calcium, calories = (0 for i in range(5))
    foodpics = []
    vitaminList = []
    for key,amt,link in db.session.query(API.food, API.quantity, API.url).filter_by(date=day).all():
        print key, amt
        f = db.session.query(Food).filter_by(name=key).first()
        print f
        protein += f.protein*amt
        carbs += f.carbs*amt
        fat += f.fat*amt
        calcium += f.calcium
        calories += f.calories*amt
        foodpics.append(link)
        if f.vitaminA > 5   and "A" not in vitaminList: vitaminList.append("A")
        if f.vitaminB > 4   and "B" not in vitaminList: vitaminList.append("B")
        if f.vitaminC > 2   and "C" not in vitaminList: vitaminList.append("C")
        if f.vitaminK > 0.5 and "K" not in vitaminList: vitaminList.append("K")

    return jsonify({"food":{"protein":protein,"carbs":carbs, "fat":fat,
        "calcium":calcium, "calories":calories},"vitamins":vitaminList,
        "foodpics":foodpics})

#returns list of tuples containing url of picture and date
@app.route('/allPictures', methods = ['GET'])
def allPictures():
    return jsonify( urlAndDate = db.session.query(API.url, API.date).order_by(API.date.desc()).all()) #.all() #.order_by(API.date.desc())

#helper functions
def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))
