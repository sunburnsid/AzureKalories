from kalories import db
from kalories import Food, API
import csv

def initiate():
	db.create_all()

	pizza = Food('pizza', 12,36,10,7,11,6,2,0,False, 285, 'slice')
	db.session.add(pizza)
	burger = Food('burger', 20,29,17,12,0,38,0,3,False, 354, 'item')
	db.session.add(burger)
	coke = Food('cola', 0,39,0,0,0,0,12,0,False, 140, 'can')
	db.session.add(coke)
	red = Food('red bull', 1,2,3,4,5,6,7,9,True, 20, 'slice')
	db.session.add(red)
	donut = Food('donut', 1,2,3,4,5,6,7,9,True, 20, 'slice')
	db.session.add(donut)
	carrot = Food('carrot', 0.6,6,0.1,2,203,5,6,1,True, 25, 'item')
	db.session.add(carrot)
	pasta = Food('pasta', 2.9,14,0.6,0,0,1,0,0,False, 75, 'plate')
	db.session.add(pasta)
	rice = Food('rice', 4.3,45,0.4,0,5,0,0,1,True, 206, 'bowl')
	db.session.add(rice)
	sushi = Food('sushi', 5.6,8.2,3.9,5,2,6,1,2,False, 88, 'piece')
	db.session.add(sushi)
	steak = Food('steak', 62,0,48,3,1,70,0,0,False, 679, 'slice')
	db.session.add(steak)
	chicken = Food('chicken', 38,0,19,2,4,36,0,0,False, 354, 'leg')
	db.session.add(chicken)
	waffle = Food('waffle', 6,25,11,3,3,3,0,0,True, 218, 'can')
	db.session.add(waffle)
	bacon = Food('bacon', 3,0.1,3.3,0,0,1,0,0,False, 120, 'strip')
	db.session.add(bacon)
	avocado = Food('avocado', 4,17,29,2,5,25,33,0,True, 20, 'item')
	db.session.add(avocado)
	pineapple = Food('pineapple', 5,120,1,11,10,50,721,0,True, 452, 'item')
	db.session.add(pineapple)
	apple = Food('apple', 0.5,25,.3,1,1,5,14,0,True, 95, 'item')
	db.session.add(apple)
	egg = Food('egg', 6,0.6,5,2,5,15,0,11,True, 78, 'item')
	db.session.add(egg)

	pic1 = API(120616, "steak", 1, "/static/yummy1.png")
	db.session.add(pic1)
	pic2 = API(120616, "waffle", 3, "/static/yummy2.png")
	db.session.add(pic2)
	pic2 = API(170616, "pizza", 1, "/static/yummy4.png")
	db.session.add(pic2)
	
	db.session.commit()

def importCSV():
    db.create_all()
    with open('ABBREV.csv', 'rb') as csvfile:
        reader=csv.reader(csvfile)
        #x=0
        reader.next() #skip header
        for row in reader:
            #if (x<5):
                #print (row[1]+" "+ row[4]+" "+ row[7]+ row[5]+ row[10]+row[33]+row[31]+row[20]+row[43]+row[3]+row[49])
                #x+=1
            #Format: name, protein, carbs, fat, calcium, vitA, vitB, vitC, vitK, healthy, calories, unit
            #temp=Food(row[1], float(row[4]), float(row[7]), float(row[5]), float(row[10]),float(row[33]),float(row[31]),float(row[20]),float(row[43]),True,float(row[3]),row[49])
            temp=Food(row[1], row[4], row[7], row[5], row[10],row[33],row[31],row[20],row[43],True,row[3],row[49])
            db.session.add(temp)
            db.session.commit()

if __name__ == '__main__':
	initiate()
        #importCSV()
